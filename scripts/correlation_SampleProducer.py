#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import copy
import os
import re

import Artus.Utility.jsonTools as jsonTools
import sys
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2015_old as samples
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.binnings as import_binnings
import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot
import Artus.Utility.tools as aTools
import ROOT
import glob
import array
import itertools
import ROOT
from scipy import stats
ROOT.PyConfig.IgnoreCommandLineOptions = True

def get_upper_limit(chi2_val, number):
	nums = number*1.0
	last_nums = number*0.9
	stat = 0
	last_stat = 0
	if number < 1:
		return 3.7
	while True:
		stat = stats.chi2.cdf(nums, 2 * (number+1))
		if abs(stat - chi2_val) < 0.01:
			break
		if stat > chi2_val and last_stat < chi2_val:
			keep = nums
			nums = last_nums + 0.5*(nums-last_nums)
			last_nums = keep
			last_stat = stat
		elif stat < chi2_val and last_stat > chi2_val:
			keep = nums
			nums = nums + 0.5*(last_nums-nums)
			last_nums = keep
			last_stat = stat
		elif stat > chi2_val and last_stat > chi2_val:
			keep = nums
			nums = nums * 0.5
			last_nums = keep
			last_stat = stat
		elif stat < chi2_val and last_stat < chi2_val:
			keep = nums
			nums = nums * 2.
			last_nums = keep
			last_stat = stat
	return nums/2.

def calc_from_hist(args, NBins=50):
	binnings_dict = import_binnings.BinningsDict()
	sample_settings = samples.Samples()
	if "qcd" in args["request_nick"] or "wj" in args["request_nick"]:
		args["request_nick"] = ["qcd", "wj"]
	if not isinstance(args["request_nick"], list):
		args["request_nick"] = [args["request_nick"]]

	list_of_samples = [getattr(samples.Samples,nick) for nick in args["request_nick"]]
	base_config = sample_settings.get_config(
					samples=list_of_samples,
					channel=args["channel"],
					category=args["category"],
					higgs_masses=args["user_masses"],
					normalise_signal_to_one_pb=False,
					ztt_from_mc=False,
					weight="(%s)"%args["user_weights"],
					exclude_cuts=args["user_exclude"],
					stack_signal=False,
					lumi = args["lumi"],
					scale_signal=1.0,
					estimationMethod="new" if args["channel"] in ["et", "mt"] else "classic"
					)
	base_config["qcd_subtract_shape"] = [True]
	for key in ["labels", "legend", "legend_cols", "leged_markers", "markers", "colors", "y_label", "y_lims", "y_rel_lims"]:
		try:
			del base_config[key]
		except KeyError:
			continue
	plot_configs = []
	for variables in [it for it in itertools.combinations(args["parameters_list"], 2)] + zip (args["parameters_list"], args["parameters_list"]):
		config = copy.deepcopy(base_config)
		[xbins, ybins] = get_bins([binnings_dict.get_binning("%s_"%args["channel"]+variables[0]).strip(),
					binnings_dict.get_binning("%s_"%args["channel"]+variables[1]).strip()], NBins, reduce_range=0.75)
		config["x_expressions"] = [variables[0]]
		config["x_bins"] = [",".join(map(str, xbins))]
		config["y_expressions"] = [variables[1]]
		config["y_bins"] = [",".join(map(str, ybins))]
		config["directories"] = [args["root_input_dir"]]
		config["output_dir"] = args["storage_name_extension"]
		config["filename"] = "__".join(variables)
		config["plot_modules"] = ["ExportRoot"]
		if os.path.exists(os.path.join(args["storage_name_extension"], config["filename"]+".root")) and not args["overwrite_samples"]:
			continue
		plot_configs.append(config)
	#for variable in config["parameters_list"]:
		#bins = binnings_dict.get_binning("%s_"%config["channel"]+variable).strip()
		#bins = get_bins(bins)
		#config["x_expressions"] = [variable]
		#config["x_bins"] = ",".join(bins)
		#config["y_expressions"] = [variable]
		#config["y_bins"] = ",".join(bins)
		#config["directories"] = [config["root_input_dir"]]
		#config["output_dir"] = config["storage_name_extension"]
		#config["filename"] = "__".join(variables)
		#config["plot_modules"] = ["ExportRoot"]
		#plot_configs.append(config)
	higgsplot.HiggsPlotter(list_of_config_dicts=plot_configs, list_of_args_strings=[""], n_processes=args["n_processes"])
	event_list = [{str(args["weight_variable"]):1./args["lumi"]} for i in range(NBins**2)]
	for variables in [it for it in itertools.combinations(args["parameters_list"], 2)] + zip (args["parameters_list"], args["parameters_list"]):
		file_name = os.path.join(args["storage_name_extension"], "__".join(variables)+".root")
		tfile = ROOT.TFile(file_name)
		hists = [tfile.Get(nick) for nick in args["request_nick"]]
		hist = hists.pop(0)
		for haddit in hists:
			try:
				hist.Add(haddit)
			except TypeError:
				print args["channel"], args["category"], variables, hists
		x_var, y_var = variables
		x_str = "%s_%s_%s"%(x_var, x_var, y_var)
		y_str = "%s_%s_%s"%(y_var, x_var, y_var)
		count = 0
		for x in range(1, NBins+1):
			for y in range(1, NBins+1):
				event_list[count][x_str] = hist.GetXaxis().GetBinCenter(x)
				event_list[count][y_str] = hist.GetYaxis().GetBinCenter(y)
				event_list[count]["ew_"+"__".join(variables)] = hist.GetBinContent(x, y)
				count += 1
	jsonTools.JsonDict({"event_list": event_list}).save(os.path.join(args["storage_name_extension"], "JsonNtuple.json"), indent=4)
	args["storage_file"] = os.path.join(args["storage_name_extension"], "JsonNtuple.json")
	return args
def get_bins(bin_strings, N=10, reduce_range=1.0):
	if isinstance(bin_strings, str):
		bin_strings = [bin_strings]

	for i, bins in enumerate(bin_strings):
		if " " in bins:
			tmp_bins = bins.split(" ")
			bin_strings[i] = [N,float(tmp_bins[0]),reduce_range*float(tmp_bins[-1])]
		elif "," in bins:
			tmp_bins = bins.split(",")
			bin_strings[i] = [N,float(tmp_bins[1]),reduce_range*float(tmp_bins[-1])]
		else:
			bin_strings[i] = [N,0.,250]
	return bin_strings

def calculate_partial_correlation(config):
	channel = config["channel"]
	category = config["category"]
	requested_sample = config["request_nick"]

	if not config["calc_from_hist"]:
	#construct list of rootfiles, if prepare samples is enabled, files are produced
		c_tree = ""
		c_tree_list = ROOT.TList()
		root_file_name_list = []
		root_storage_file = "%s/%s.root"%(config["storage_name_extension"], "NTuples")
		config["storage_file"] = root_storage_file
		config["storage_ntuple"]=config["folders"][0].replace("/ntuple", "")

		cuts = ""
		#find all physical files and store them in root_filename_list
		for i,nick in enumerate(config["nicks"]):
			if not bool(sum([x in nick for x in ["wmh", "wph", "zh"]])) and "noplot" in nick:
				continue
			log.debug("search files:\n" + str(config["files"][i]))
			#next line splits file_string into filenames, those could contain * -> use glob.glob to map * to real names, add the list to root_file_name_list
			map(root_file_name_list.__iadd__, map(glob.glob, map(config["root_input_dir"].__add__, config["files"][i].split(" "))))
			if (not cuts == "") and (not cuts == config["weights"][i]):
				log.error("can not decide which weight to use for sample %s nick %s" %(config["request_nick"],nick))
				log.error(config)
				#sys.exit()
			cuts = config["weights"][i]
			config["lumi"] = config["scale_factors"][i]

		if config["prepare_samples"] and not (os.path.exists(root_storage_file) and not config["overwrite_samples"]):
			log.info("Recreate Sample %s"%root_storage_file)
			for root_file_name in root_file_name_list:
				log.debug("Prepare Rootfile %s as Sample %s" %(root_file_name, config["request_nick"]))
				c_tree_list.append(ROOT.TChain())
				root_file_name = root_file_name + '/' + config["folders"][0]
				c_tree_list[-1].Add(root_file_name)
				c_tree_list[-1].SetName("list_tree")

			store_file = ROOT.TFile(root_storage_file, "RECREATE")
			selection_string = cuts.replace("eventWeight*", "")
			if config["request_nick"] in ["ztt", "zll"]:
				selection_string = cuts.replace("eventWeight*", "")
			for index in range(len(c_tree_list)):
				log.debug("Cut Tree %s for Sample %s "%(root_file_name_list[index], root_storage_file))
				c_tree_list[index]=c_tree_list[index].CopyTree(selection_string)
			log.debug("Merge Trees for Sample %s "%root_storage_file)
			if len(c_tree_list) > 1:
				c_tree = ROOT.TTree.MergeTrees(c_tree_list)
			elif len(c_tree_list) == 1:
				c_tree = c_tree_list[0]
			else:
				c_tree =ROOT.TChain()
			log.debug("Prepare Sample %s from %i files"%(root_storage_file,len(c_tree_list)))
			c_tree.SetName(config["folders"][0].replace("/ntuple", ""))
			c_tree.Write()
			for i in range(len(c_tree_list)):
				del c_tree_list[0]
			del c_tree_list
			#store_file.Write()
			store_file.Close()
	else:
		config = calc_from_hist(config)
	#log.error("Reached Breakpoint, would start calculations next!")
	#sys.exit()
	root_histograms = {}
	corr_vars = {}
	binnings_dict = import_binnings.BinningsDict()
	nick_path = os.path.join(config["output_dir_path"], channel, category, requested_sample)
	log.debug("save output to folder %s"%nick_path)
	if not os.path.exists(nick_path):
		os.makedirs(nick_path)

	root_inf = False
	root_inst = []
	if config["calc_from_hist"]:
		root_inst = jsonTools.JsonDict(config["storage_file"])["event_list"]
	else:
		root_inf = ROOT.TFile(config["storage_file"], "read")
		root_inst = root_inf.Get(config["storage_ntuple"])

	log.debug("===============================X-Y Correlations==============================")
	for variables in [it for it in itertools.combinations(config["parameters_list"], 2)] + zip(config["parameters_list"], config["parameters_list"]):
		[xbins, ybins] = get_bins([binnings_dict.get_binning("%s_"%config["channel"]+variables[0]).strip(),
					binnings_dict.get_binning("%s_"%config["channel"]+variables[1]).strip()])
		root_histograms["__".join(variables)] = ROOT.TProfile("__".join(variables),
													"correlation: %s vs %s"%variables, *(xbins+ybins[1:]+[ 's']))
		log.debug("Generate RootHistogram TH2F: %s"%("__".join(variables)))
		log.debug("options: " + str(xbins+ybins[1:]+[ 's']))
		root_histograms["__".join(variables[-1::-1])] = ROOT.TProfile("__".join(variables[-1::-1]),
													"correlation: %s vs %s"%(variables[-1::-1]), *(ybins+xbins[1:]+[ 's']))
		log.debug("Generate RootHistogram TH2F: %s"%("__".join(variables[-1::-1])))
		log.debug("options: " + str(ybins+xbins[1:]+[ 's']))
		corr_vars["__".join(variables)] = 0.
		corr_vars["single_%s_%s_%s"%(variables[0],variables[0],variables[1])] = 0.
		corr_vars["square_%s_%s_%s"%(variables[0],variables[0],variables[1])] = 0.
		corr_vars["single_%s_%s_%s"%(variables[1],variables[0],variables[1])] = 0.
		corr_vars["square_%s_%s_%s"%(variables[1],variables[0],variables[1])] = 0.
		corr_vars["weight_"+"__".join(variables)] = 0.
		corr_vars["weight2_"+"__".join(variables)] = 0.
		root_histograms["__".join(variables)].SetDirectory(0)
		ROOT.SetOwnership (root_histograms["__".join(variables)], False)
		root_histograms["__".join(variables[-1::-1])].SetDirectory(0)
		ROOT.SetOwnership (root_histograms["__".join(variables[-1::-1])], False)

	#log.debug("===============================X-X Correlations==============================")
	#for variable in config["parameters_list"]:
		#bins = binnings_dict.get_binning("%s_"%config["channel"]+variable).strip()
		#bins_raw = get_bins(bins)

		#log.debug("Generate RootHistogram TH2F: %s"%("__".join([variable,variable])))
		#log.debug(bins_raw*2)
		#root_histograms["__".join([variable,variable])] = ROOT.TProfile("__".join([variable,variable]),
													#"correlation: %s vs %s"%(variable,variable), *(bins_raw+bins_raw[1:]+[ 's']))
		#corr_vars["__".join([variable,variable])] = 0
		#corr_vars[variable] = 0
		#corr_vars["var_%s"%variable] = 0
		#corr_vars["weight_"+"__".join(variables)] = 0
		#corr_vars["weight2_"+"__".join(variables)] = 0
		#root_histograms["__".join([variable,variable])].SetDirectory(0)
		#ROOT.SetOwnership (root_histograms["__".join([variable,variable])], False)
	log.info( "=================================================================================")
	log.info( "Calculate correlations in sample %s and make scatter plots for %i variable pairs."%(config["request_nick"],len(root_histograms)))
	log.info( "=================================================================================")
	#sys.exit()
	i = 0.
	n = 0
	w2 = 0
	zero_vals = {}
	lumi_val = config["lumi"]
	extractor = 0
	get_weight = 1.0
	if isinstance(root_inst, list):
		extractor = lambda event, varl: event.__getitem__("_".join(varl))
		#get_weight = lambda event, string: get_upper_limit(0.95, event.__getitem__("ew_"+"__".join(string)))
		get_weight = lambda event, string: event.__getitem__("ew_"+"__".join(string))
	else:
		extractor = lambda event, var1, var2, var3: event.__getattr__(var1)
		get_weight = lambda event, string: 1.0

	for event in root_inst:
		calced_means = []
		base_weight = extractor(event, [config["weight_variable"]]) * lumi_val
		#if config["request_nick"] in ["ztt", "zll", "wj"]:
			#w *= event.__getattr__("stitchWeight%s"%(config["request_nick"].upper()))
		for varxy in corr_vars.iterkeys():
			if "single" in varxy or "weight" in varxy or "ew_" in varxy or "square" in varxy:
				continue
			varx, vary = map(str, varxy.split("__"))
			x = extractor(event, [varx,varx,vary])
			y = extractor(event, [vary,varx,vary])
			#x, y = [extractor(event, string) for string in map(str, varxy.split("__"))]
			w = get_weight(event, [varx,vary]) * base_weight
			#print w, base_weight
			root_histograms["__".join([varx, vary])].Fill(x, y, w)
			root_histograms["__".join([vary, varx])].Fill(y, x, w)


			#if varx not in zero_vals:
				#zero_vals[varx] = 0
			#if vary not in zero_vals:
				#zero_vals[vary] = 0
			x_string = "%s_%s_%s"%(varx,varx,vary)
			y_string = "%s_%s_%s"%(vary,varx,vary)
			if x_string not in calced_means:
				#log.info( "calculate mean for %s" %varx)
				corr_vars["single_"+x_string] += w*(x)
				corr_vars["square_"+x_string] += w*(x)**2
				calced_means.append(x_string)
			if y_string not in calced_means:
				#log.info( "calculate mean for %s" %vary)
				corr_vars["single_"+y_string] += w*(y)
				corr_vars["square_"+y_string] += w*(y)**2
				calced_means.append(y_string)
			corr_vars[varxy] += w*(x) * (y)
			corr_vars["weight_"+varxy] += w
			corr_vars["weight2_"+varxy] += w*w

		n += 1
		if n%250 == 0:
			log.info( "processed: %i events"%n)

	hist_file = ROOT.TFile(os.path.join(nick_path, "Histograms.root"),"RECREATE")
	for varxy in root_histograms.iterkeys():
		root_histograms[varxy].Write()
	#corr_vars["weight_sum"] = i
	#corr_vars["weight_square"] = w2
	corr_vars["n"] = n
	hist_file.Close()
	if root_inf:
		root_inf.Close()
	config["correlations"] = corr_vars
	jsonTools.JsonDict(config).save(os.path.join(nick_path,"Correlations.json"),indent=4)

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Produce reduced samples and calculate correlations",
									 parents=[logger.loggingParser])
	parser.add_argument("-A", "--artus-input", default=None, help="merged folder of ArtusOutput please have a look at --reduced-input [Default=%(default)s]")
	parser.add_argument("-R", "--reduced-input", default=None, help="reduced input from Artus, already processed by this script[Default=%(default)s] --- If artus-input and reduced-input is given, reproduce missing reduceded samplesin artus-input directory")
	parser.add_argument("-B", "--bdt_files", nargs="*", default=[], help="tmva output root files[Default=%(default)s]")
	parser.add_argument("-O", "--overwrite-samples", action="store_true", default=False,
						help="specify if you already produced reduced files and want to overwrite them. [Default: %(default)s]")
	parser.add_argument("-s", "--samples", nargs="+",
						default=["ggh", "qqh", "vh", "ztt", "zll", "ttj", "vv", "wj", "data", "qcd"],
						choices=["ggh", "qqh", "vh", "ztt", "zll", "ttj", "vv", "wj", "data", "qcd"],
						help="Samples for correlation calculation and scatter plots. [Default: %(default)s]")
	#parser.add_argument("-M", "--Mvas", nargs="+",
						#default=[],
						#help="Calculate correlation within each bin of every MVA. [Default: %(default)s]")
	parser.add_argument("-n", "--n-processes", type=int, default=1,
						help="Number of (parallel) processes. [Default: %(default)s]")
	parser.add_argument("-o", "--output-dir",
						default="$CMSSW_BASE/src/plots/correlations",
						help="Output directory - Create Subfolder with date and time to store everything[Default: %(default)s]")
	parser.add_argument("--force-this-output",
						default=None,
						help="Force to write output exactly to this folder - you might override precious samples![Default: %(default)s]")
	parser.add_argument("-f", "--filename",
						default="Correlation",
						help="Output filename. [Default: %(default)s]")
	parser.add_argument("-e", "--exclude-cuts", nargs="+",
						default=[],
						choices=["pZetaMiss", "pZetaVis", "iso_1", "iso_2", "mt_1", "mt_2", "mt", "pzeta"],
						help="""Exclude (default) selection cuts.
						[Default: %(default)s]""")
	parser.add_argument("-c", "--channels", nargs="*",
						default=["tt", "mt", "et", "em", "mm", "ee"],
						help="Channels. [Default: %(default)s]")
	parser.add_argument("--mssm", default=False, action="store_true",
	                    help="Produce the plots for the MSSM. [Default: %(default)s]")
	parser.add_argument("--mva", default=False, action="store_true",
	                    help="Produce plots for the mva studies. [Default: %(default)s]")
	parser.add_argument("--categories", nargs="+", default=["inclusive"],
	                    help="Categories. [Default: %(default)s]")
	parser.add_argument("--higgs-masses", nargs="+", default=["125"],
						help="Higgs masses. [Default: %(default)s]")
	parser.add_argument("--add-vars", nargs="+", default=[],
						help="add variables which were not used for training MVAs to correlation calculatioin. [Default: %(default)s]")
	parser.add_argument("-w", "--weight", default="1.0",
						help="""Additional weight (cut) expression.
						[Default: %(default)s]""")
	parser.add_argument("--lumi", type=float, default=samples.default_lumi/1000,
	                    help="Luminosity for the given data in fb^(-1). [Default: %(default)s]")
	parser.add_argument("--splits", type=int, default=10,
	                    help="Number of SubSamples [Default: %(default)s]")
	parser.add_argument("--dry-run", action="store_true", default=False,
	                    help="Dry Run - Abort before real work is done [Default: %(default)s]")
	parser.add_argument("--calc-from-hist", action="store_true", default=False,
						help="use the variables defined in MVATestMethods settings of artus run. [Default: %(default)s]")
	parser.add_argument("-m", "--mva-variables", action="store_true", default=False,
						help="use the variables defined in MVATestMethods settings of artus run. [Default: %(default)s]")
	args = parser.parse_args()
	logger.initLogger(args)
	plot_configs = []
	hist_plot_configs = []
	from datetime import datetime as dt

	output_dir_path = os.path.join(os.path.expandvars(args.output_dir), str(dt.utcnow().strftime("%Y_%m_%d_%H-%M"))+"_%s"%args.filename)
	root_input_dir = ""
	skip_classic_input = False
	storage_name_extension = ""
	if args.force_this_output:
		output_dir_path = args.force_this_output
	if args.artus_input is None and args.reduced_input is None:
		storage_name_extension = os.path.join(output_dir_path, "storage")
		skip_classic_input = True
	if args.artus_input is None and args.reduced_input is None and args.bdt_files == []:
		log.error("Need Input!")
		sys.exit()
	elif not args.artus_input is None and not args.reduced_input is None:
		root_input_dir = os.path.expandvars(args.artus_input)
		storage_name_extension = os.path.join(args.reduced_input, "storage")
		prepare_samples = True
		overwrite_samples = args.overwrite_samples
	elif args.artus_input is not None:
		root_input_dir = os.path.expandvars(args.artus_input)
		storage_name_extension = os.path.join(output_dir_path, "storage")
		prepare_samples = True
		overwrite_samples = args.overwrite_samples
	elif args.reduced_input is not None:
		root_input_dir = os.path.expandvars(args.reduced_input)
		storage_name_extension = os.path.join(args.reduced_input, "storage")
		prepare_samples = False
		overwrite_samples = args.overwrite_samples

	if output_dir_path is None:
		pass
	elif not os.path.exists(output_dir_path):
		os.makedirs(output_dir_path)
		os.makedirs(output_dir_path+"/storage")
	elif not os.path.exists(output_dir_path+"/storage"):
		os.makedirs(output_dir_path+"/storage")

	sample_settings = samples.Samples()
	if "wj" in args.samples and "qcd" in args.samples:
		args.samples = [s for s in args.samples if "wj" != s]
 	#get all configs
	if not skip_classic_input:
		for channel in args.channels:
			for category in args.categories:
				if category != None:
					if(args.mssm):
						category_string = "catHttMSSM13TeV"
					if args.mva:
						category_string = "catMVAStudies"
					else:
						category_string = "catHtt13TeV"
					category_string = (category_string + "_{channel}_{category}").format(channel=channel, category=category)
				for requested_sample in args.samples:
					list_of_samples = [getattr(samples.Samples, requested_sample)]
					#for splits in range(args.splits):
					#diff = 100./args.splits
					#weight = "*(TrainingSelectionValue <= %i && %i < TrainingSelectionValue)"%(int(splits*diff), int((splits+1)*diff))
					config = sample_settings.get_config(
							samples=list_of_samples,
							channel=channel,
							category=category_string,
							higgs_masses=args.higgs_masses,
							normalise_signal_to_one_pb=False,
							ztt_from_mc=False,
							weight="(%s)"%args.weight,
							exclude_cuts=args.exclude_cuts,
							stack_signal=False,
							lumi = args.lumi*1000,
							scale_signal=1.0,
							mssm=args.mssm
							)
					config["category"] = category_string
					config["request_nick"] = requested_sample
					config["calc_from_hist"] = args.calc_from_hist if requested_sample != "qcd" else True
					config["channel"] = channel
					config["prepare_samples"] = prepare_samples
					config["overwrite_samples"] = overwrite_samples
					#config["storage_name_extension"] = os.path.join(storage_name_extension, channel, category_string, requested_sample+"%i"%splits)
					config["storage_name_extension"] = os.path.join(storage_name_extension, channel, category_string, requested_sample)
					if not os.path.exists(config["storage_name_extension"]):
						os.makedirs(config["storage_name_extension"])
					config["output_filename"] = args.filename
					config["output_dir_path"] = output_dir_path
					config["root_input_dir"] = root_input_dir+"/"
					config["weight_variable"] = "eventWeight"
					config["user_weights"] = args.weight
					config["user_exclude"] = args.exclude_cuts
					config["user_masses"] = args.higgs_masses
					config["lumi"] = args.lumi * 1000.
					config["n_processes"] = args.n_processes
					if config["calc_from_hist"]:
						hist_plot_configs.append(config)
					else:
						plot_configs.append(config)

		#artus =jsonTools.JsonDict(glob.glob(os.path.join(config["input_dir"], "artus_*.json")))
		#find all correlations to be calculated and plottet
		for config in plot_configs+hist_plot_configs:
			parsed_parameters = []
			for additional_var in args.add_vars:
				if not additional_var in parsed_parameters:
					parsed_parameters.append(additional_var)
			config["parameters_list"] = parsed_parameters

	bdt_file_dict = {}
	for bdt_file in args.bdt_files:
		folder, full_name = os.path.split(bdt_file)
		name = full_name.replace(".root", "")
		count = 0
		for letter in name[-1::-1]:
			count -= 1
			if letter == "T":
				break
		name = name[:count]
		folder_and_name = os.path.join(folder, name)
		if folder_and_name in bdt_file_dict.keys():
			bdt_file_dict[folder_and_name].append(full_name)
		else:
			bdt_file_dict[folder_and_name] = [full_name]

	for key, file_list in bdt_file_dict.iteritems():
		config = {}
		folder, name = os.path.split(key)
		container = name.split("__")
		config["root_input_dir"] = folder+"/"
		config["channel"] = container[0]

		config["category"] = container[1].replace("1", "One").replace("2", "Two").replace("0", "Zero").replace("Jets", "Jet30")
		category_string = "catMVAStudies"
		config["category"] = (category_string + "_{channel}_{category}").format(channel=channel, category=config["category"])

		config["scale_factors"] = [1]
		config["folders"] = ["TestTree"]
		config["weight_variable"] = "weight"
		config["files"] = ["/"+" /".join(file_list)]
		config["output_filename"] = args.filename
		config["output_dir_path"] = output_dir_path
		config["prepare_samples"] = True
		config["overwrite_samples"] = True

		config["parameters_list"] = []
		#print "Open RootFile\t", os.path.join(folder, file_list[0])
		infile = ROOT.TFile(os.path.join(folder, file_list[0]), "READ")
		intree = infile.Get("TestTree")
		for branch in intree.GetListOfBranches():
			branch_name = branch.GetName()
			if not "class" in branch_name and not "weight" in branch_name:
				config["parameters_list"].append(branch.GetName())
		infile.Close()

		config["request_nick"] = container[2]+"_signal"
		config["nicks"] = [container[2]+"_signal"]
		config["weights"]= ["(classID==1)"]
		channel, category_string, requested_sample = config["channel"], config["category"], config["request_nick"]
		config["storage_name_extension"] = os.path.join(storage_name_extension, channel, category_string, requested_sample)
		plot_configs.append(copy.deepcopy(config))
		if not os.path.exists(config["storage_name_extension"]):
			os.makedirs(config["storage_name_extension"])

		config["request_nick"] = container[2]+"_bkg"
		config["nicks"] = [container[2]+"_bkg"]
		config["weights"]= ["(classID==0)"]
		channel, category_string, requested_sample = config["channel"], config["category"], config["request_nick"]
		config["storage_name_extension"] = os.path.join(storage_name_extension, channel, category_string, requested_sample)
		plot_configs.append(copy.deepcopy(config))
		if not os.path.exists(config["storage_name_extension"]):
			os.makedirs(config["storage_name_extension"])

	if args.dry_run:
		print plot_configs[0]
		print "Dry-Run aborting!", len(plot_configs)
		sys.exit()
	for hist_plot in hist_plot_configs:
		try:
			calculate_partial_correlation(hist_plot)
		except KeyboardInterrupt:
			log.critical("KeyboardInterrupt - exiting program")
			sys.exit()
		except:
			continue
	aTools.parallelize(calculate_partial_correlation, plot_configs, n_processes=args.n_processes)
