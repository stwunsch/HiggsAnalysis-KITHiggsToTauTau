#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)
import sys
import os
import ROOT
import array
import itertools
import matplotlib.pyplot as plt
from matplotlib import cm
import Artus.Utility.jsonTools as jsonTools
import Artus.Utility.tools as aTools
import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.binnings as import_binnings
ROOT.PyConfig.IgnoreCommandLineOptions = True

def visualize_bdt(run_config):
	#Setup of all the readers/methods etc. for value calculation

	training_dict = jsonTools.JsonDict(run_config["log_file"])
	weight_file = run_config["weight_file"]
	channel = training_dict["channels"][0]
	plot_path = run_config["plot_path"]
	#plot_name = run_config["plot_name"]
	#root_file = ROOT.TFile(run_config["rootfile"],"READ")
	#tree = root_file.Get("TestTree")

	#find variable ranges
	binnings_dict = import_binnings.BinningsDict()
	ranges_dict = {}
	variables_list = [x.split(";")[0] for x in training_dict["quantities"]]
	for variable in variables_list:
		bins = binnings_dict.get_binning("%s_"%channel+variable).strip()
		bins_raw = []
		if " " in bins:
			tmp_bins = bins.split(" ")
			bins_raw = [float(tmp_bins[0]),float(tmp_bins[-1])]
		elif "," in bins:
			tmp_bins = bins.split(",")
			bins_raw = [float(tmp_bins[1]),float(tmp_bins[-1])]
		else:
			bins_raw = [0.,250.]
		ranges_dict[variable] = [bins_raw[0], bins_raw[1], [bins_raw[0]+x*(bins_raw[1]-bins_raw[0])/50.0 for x in range(50)]]

	#Booking Reader and initialize variable pointers
	ROOT.TMVA.Tools.Instance()
	all_variables = {}
	for var in variables_list:
		if not var in all_variables:
			all_variables[var] = array.array('f', [0])
	reader = ROOT.TMVA.Reader()
	for var_name in variables_list:
		reader.AddVariable(ROOT.TString(var_name), all_variables[var_name])
	reader.BookMVA("BDT", weight_file)

	title_str = ["Minimum", "Maximum", "Mean"]
	for (var1, var2) in itertools.combinations(variables_list, 2):
		log.info("Calculate Variables: {var1} and {var2}".format(var1=var1, var2=var2))
		x_points = [ranges_dict[var1][0]+x*(ranges_dict[var1][1]-ranges_dict[var1][0])/10.0 for x in range(50)]
		y_points = [ranges_dict[var2][0]+x*(ranges_dict[var2][1]-ranges_dict[var2][0])/10.0 for x in range(50)]
		iterator = itertools.product(x_points, y_points)
		plot_name = run_config["plot_name"]+"{var1}+-+{var2}".format(var1=var1, var2=var2)
		plot_x = []
		plot_y = []
		mins = []
		maxs = []
		means = []
		for x, y in iterator:
			all_variables[var1][0] = x
			all_variables[var2][0] = y
			values = []
			for i in range(10):
				for variable in variables_list:
					if variable not in [var1, var2]:
						all_variables[variable][0] = ranges_dict[variable][2][i]
				values.append(reader.EvaluateMVA("BDT"))
			mins.append(min(values))
			maxs.append(max(values))
			means.append(sum(values)/10.)
			plot_x.append(x)
			plot_y.append(y)
		w_values = [mins, maxs, means]
		for i in range(3):
			fig = plt.figure()
			ax = fig.add_subplot(111)
			counts, xedges, yedges, cax = ax.hist2d(plot_x, plot_y, weights=w_values[i], bins=[10, 10], range=[(ranges_dict[var1][0],ranges_dict[var1][1]),(ranges_dict[var2][0],ranges_dict[var2][1])], cmap=cm.coolwarm, vmin=-1, vmax=1.0)
			title_string = "{range_str} Evaluation: {title}".format(range_str=title_str[i], title=run_config["title"])
			plot_title = ax.set_title(title_string)
			cbar = fig.colorbar(cax, ticks=[-1.0, 0, 1.0])
			cbar.ax.set_yticklabels([str(-1.0), '0', str(1.0)])
			plt.savefig(os.path.join(plot_path, plot_name.format(range_str=title_str[i])+".png"), bbox_extra_artists=(plot_title,), bbox_inches='tight')

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description="Plot overlapping signal events.",
									 parents=[logger.loggingParser])
	parser.add_argument("-L", "--log-file", required=True,
						help="Path to TrainingLog")
	parser.add_argument("-W", "--weight-file", required=True,
						help="Pathon to Weightfile")

	args = parser.parse_args()
	logger.initLogger(args)
	config_list = []
	config = {}
	config["plot_path"] = "./"
	config["plot_name"] = "{range_str}/TestVisualization_"
	config["log_file"] = os.path.expandvars(args.log_file)
	config["weight_file"] = os.path.expandvars(args.weight_file)
	config["title"] = "TestBDT"
	config_list.append(config)
	aTools.parallelize(visualize_bdt, config_list, n_processes=1)
