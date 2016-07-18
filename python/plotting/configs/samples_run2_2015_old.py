
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import copy

import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.samples_run2_2016 as samples
from Kappa.Skimming.registerDatasetHelper import get_nick_list

# constants for all plots
energy = 13
class Samples(samples.Samples):

	data_format = "MINIAOD"
	mc_campaign = "RunIIFall15MiniAOD.*"
	default_lumi = 2.301*1000.0

	@staticmethod
	def ztt_genmatch(channel):
		if channel in ["mt", "et"]:
			return "(gen_match_2 == 5)*"
		elif channel == "em":
			return "(gen_match_1 > 2 && gen_match_2 > 3)*"
		elif channel == "mm":
			return "(gen_match_1 > 3 && gen_match_2 > 3)*"
		elif channel == "tt":
			return "(gen_match_1 == 5 && gen_match_2 == 5)*"
		else:
			log.fatal("No ZTT selection implemented for channel \"%s\"!" % channel)
			sys.exit(1)
	@staticmethod
	def zll_genmatch(channel):
		if channel in ["mt", "et"]:
			return "(gen_match_2 < 5 || gen_match_2 == 6)*"
		elif channel == "em":
			return "(gen_match_1 < 3 || gen_match_2 < 4)*"
		elif channel == "mm":
			return "(gen_match_1 < 4 || gen_match_2 < 4)*"
		elif channel == "tt":
			return "((gen_match_1 < 6 && gen_match_2 < 6 && !(gen_match_1 == 5 && gen_match_2 == 5)) || gen_match_2 == 6 || gen_match_1 == 6)*"
		else:
			log.fatal("No ZLL selection implemented for channel \"%s\"!" % channel)
			sys.exit(1)
	# needs to be overwritten since extentions have not been available in Fall15 nicks
	@staticmethod
	def artus_file_names( query, expect_n_results = 1):
		query["energy"] = energy
		found_file_names = []
		for nick in get_nick_list ( query, expect_n_results = expect_n_results):
			if("ext") in nick:
				nick = nick[0:nick.rfind("_")]
			found_file_names.append(nick  + "/*.root")
		return " ".join(found_file_names) # convert it to a HP-readable format

	def files_data(self, channel):
		query = {}
		expect_n_results = 1 # adjust in if-statements if different depending on channel
		if channel == "mt":
			query = { "process" : "SingleMuon" }
		elif channel == "et":
			query = { "process" : "SingleElectron" }
		elif channel == "em":
			query = { "process" : "MuonEG" }
		elif channel == "mm":
			query = { "process" : "DoubleMuon" }
		elif channel == "tt":
			query = { "process" : "Tau" }
		else:
			log.error("Sample config (Data) currently not implemented for channel \"%s\"!" % channel)
		query["scenario"] = "16Dec2015v1"
		query["data"] = True
		query["campaign"] = "Run2015D.*"
		return self.artus_file_names(query, expect_n_results)


	def files_ztt(self, channel):
		query = { "data" : False,
				"campaign" : self.mc_campaign,
				"generator" :  "madgraph\-pythia8",
				"process" : "(DYJetsToLLM150|DYJetsToLLM50|DY1JetsToLLM50|DY2JetsToLLM50|DY3JetsToLLM50|DY4JetsToLLM50)" }
		artus_files = self.artus_file_names(query , 6)

		query = { "data" : False,
				"campaign" : self.mc_campaign,
				"generator" :  "amcatnlo-pythia8",
				"process" : "DYJetsToLLM10to50"}
		artus_files = artus_files + " " + self.artus_file_names(query , 1)
		return artus_files


	def files_zll(self, channel):
		query = { "data" : False,
				"campaign" : self.mc_campaign,
				"generator" :  "madgraph\-pythia8",
				"process" : "(DYJetsToLLM50|DY1JetsToLLM50|DY2JetsToLLM50|DY3JetsToLLM50|DY4JetsToLLM50)" }
		artus_files = self.artus_file_names(query , 5)

		query = { "data" : False,
				"campaign" : self.mc_campaign,
				"generator" :  "amcatnlo-pythia8",
				"process" : "DYJetsToLLM10to50"}
		artus_files = artus_files + " " + self.artus_file_names(query , 1)
		return artus_files


	def files_ttj(self, channel):
		return self.artus_file_names({"process" : "TT", "data": False, "campaign" : self.mc_campaign}, 1)


	def files_vv(self, config):
		return self.artus_file_names({ "process" : "(STt-channelantitop4fleptonDecays|STt-channeltop4fleptonDecays|STtWantitop5finclusiveDecays|STtWtop5finclusiveDecays|"
		                                    + "WWTo1L1Nu2Q|"
		                                    + "WZJets|WZTo1L1Nu2Q|WZTo1L3Nu|WZTo2L2Q|"
		                                    + "ZZTo2L2Q|ZZTo4L|VVTo2L2Nu)",
		                      "data" : False, "campaign" : self.mc_campaign}, 12)


	def files_wj(self, channel):
		return self.artus_file_names({"process" : "(W1JetsToLNu|W2JetsToLNu|W3JetsToLNu|W4JetsToLNu|WJetsToLNu)", "data": False, "campaign" : self.mc_campaign, "generator" : "madgraph-pythia8"}, 5)

	def files_ggh(self, channel, mass=125):
		return self.artus_file_names({"process" : "GluGluHToTauTauM"+str(mass), "data": False, "campaign" : self.mc_campaign}, 1)

	def files_susy_ggh(self, channel, mass=125):
		return super(Samples, self).files_susy_ggh(channel)

	def files_qqh(self, channel, mass=125):
		return self.artus_file_names({"process" : "VBFHToTauTauM"+str(mass), "data": False, "campaign" : self.mc_campaign}, 1)

	def files_wh_minus(self, channel, mass=125):
		return self.artus_file_names({"process" : "WminusHToTauTauM"+str(mass), "data": False, "campaign" : self.mc_campaign}, 1)

	def files_wh_plus(self, channel, mass=125):
		return self.artus_file_names({"process" : "WminusHToTauTauM"+str(mass), "data": False, "campaign" : self.mc_campaign}, 1)

	def files_zh(self, channel, mass=125):
		return self.artus_file_names({"process" : "ZHToTauTauM"+str(mass), "data": False, "campaign" : self.mc_campaign}, 1)

	def htt(self, config, channel, category, weight, nick_suffix, higgs_masses, normalise_signal_to_one_pb=False,
	        lumi=default_lumi, exclude_cuts=None, additional_higgs_masses_for_shape=[], mssm=False, normalise_to_sm_xsec=False, **kwargs):

		if exclude_cuts is None:
			exclude_cuts = []

		# gluon fusion (SM/MSSM)
		config = self.ggh(config, channel, category, weight, nick_suffix+"_noplot", higgs_masses+additional_higgs_masses_for_shape,
		                  normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, no_plot=True, mssm=mssm, **kwargs)
		if mssm and  normalise_to_sm_xsec:
			config = self.ggh(config, channel, category, weight, nick_suffix+"_sm_noplot", higgs_masses,
			                  normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, no_plot=True, mssm=False, **kwargs)

		# vector boson fusion (SM)
		if (not mssm) or normalise_to_sm_xsec:
			config = self.qqh(config, channel, category, weight, nick_suffix+("_sm" if mssm else "")+"_noplot", higgs_masses+([] if mssm else additional_higgs_masses_for_shape),
			                  normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, no_plot=True, **kwargs)

		# Higgs strahlung (SM)
		if (not mssm) or normalise_to_sm_xsec:
			config = self.vh(config, channel, category, weight, nick_suffix+("_sm" if mssm else "")+"_noplot", higgs_masses+([] if mssm else additional_higgs_masses_for_shape),
			                 normalise_signal_to_one_pb, lumi=0, exclude_cuts=exclude_cuts, no_plot=True, **kwargs)

		# production in association with b-quarks (MSSM)
		if mssm:
			config = self.bbh(config, channel, category, weight, nick_suffix+"_noplot", higgs_masses+additional_higgs_masses_for_shape,
			                  normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, no_plot=True, **kwargs)

		def final_nick(tmp_sample, tmp_mass, add_nick_suffix=True):
			return tmp_sample+str(tmp_mass)+("_"+str(int(kwargs["scale_signal"])) if kwargs.get("scale_signal", 1.0) != 1.0 else "")+(nick_suffix if add_nick_suffix else "")

		for index, mass in enumerate(additional_higgs_masses_for_shape+higgs_masses):
			is_additional_mass = (index < len(additional_higgs_masses_for_shape))

			if not "AddHistograms" in config.get("analysis_modules", []):
				config.setdefault("analysis_modules", []).append("AddHistograms")
			config.setdefault("add_nicks", []).append(" ".join([final_nick(sample, mass)+"_noplot" for sample in ["ggh"]+(["bbh"] if mssm else ["qqh", "vh"])]))
			config.setdefault("add_result_nicks", []).append(final_nick("htt", mass)+"_noplot")

			if not is_additional_mass:
				config.setdefault("add_nicks", []).append(" ".join([final_nick("htt", m)+"_noplot" for m in [mass]+additional_higgs_masses_for_shape]))
				config.setdefault("add_result_nicks", []).append(final_nick("htt", mass)+"_noplot_shape")

				if mssm and normalise_to_sm_xsec:
					config.setdefault("add_nicks", []).append(" ".join([final_nick(sample, mass)+"_sm_noplot" for sample in ["ggh", "qqh", "vh"]]))
					config.setdefault("add_result_nicks", []).append(final_nick("htt", mass)+"_sm_noplot")

				if not "ShapeYieldMerge" in config.get("analysis_modules", []):
					config.setdefault("analysis_modules", []).append("ShapeYieldMerge")
				config.setdefault("shape_nicks", []).append(final_nick("htt", mass)+"_noplot_shape")
				config.setdefault("yield_nicks", []).append(final_nick("htt", mass)+("_sm" if mssm and normalise_to_sm_xsec else "")+"_noplot")
				config.setdefault("shape_yield_nicks", []).append(final_nick("htt", mass))

			if (not kwargs.get("no_plot", False)) and (not is_additional_mass):
				if not mssm:
					Samples._add_bin_corrections(
							config,
							final_nick("htt", mass),
							nick_suffix
					)
				Samples._add_plot(
						config,
						"bkg" if kwargs.get("stack_signal", False) else "htt",
						"LINE",
						"L",
						final_nick("htt", mass, False),
						nick_suffix
				)
		return config
	def wj(self, config, channel, category, weight, nick_suffix, lumi=default_lumi, exclude_cuts=None, cut_type="baseline", fakefactor_method=None, estimationMethod="classic", controlregions=False,**kwargs):
		if exclude_cuts is None:
			exclude_cuts = []

		scale_factor = lumi
		if not self.postfit_scales is None:
			scale_factor *= self.postfit_scales.get("WJets", 1.0)

		data_weight, mc_weight = self.projection(kwargs)

		if channel in ["mt", "et"]:
			if estimationMethod == "new":
				Samples._add_input(
						config,
						self.files_ztt(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*" + Samples.ztt_genmatch(channel) + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						("noplot_" if not controlregions else "") + "ztt_os_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_zll(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*" + Samples.zll_genmatch(channel) + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						("noplot_" if not controlregions else "") + "zll_os_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_ztt(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*" + Samples.zl_genmatch(channel) + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						("noplot_" if not controlregions else "") + "zl_os_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_ztt(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*" + Samples.zj_genmatch(channel) + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						("noplot_" if not controlregions else "") + "zj_os_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_ttj(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						("noplot_" if not controlregions else "") + "ttj_os_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_vv(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						("noplot_" if not controlregions else "") + "vv_os_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_data(channel),
						self.root_file_folder(channel),
						1.0,
						data_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						("noplot_" if not controlregions else "") + "data_os_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_wj(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*stitchWeightWJ*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						("noplot_" if not controlregions else "") + "wj_os_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_ztt(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*" + Samples.ztt_genmatch(channel) + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt", "os"], cut_type=cut_type) + "*(mt_1>70.0)*((q_1*q_2)>0.0)",
						("noplot_" if not controlregions else "") + "ztt_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_zll(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*" + Samples.zll_genmatch(channel) + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt", "os"], cut_type=cut_type) + "*(mt_1>70.0)*((q_1*q_2)>0.0)",
						("noplot_" if not controlregions else "") + "zll_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_zll(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*" + Samples.zl_genmatch(channel) + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt", "os"], cut_type=cut_type) + "*(mt_1>70.0)*((q_1*q_2)>0.0)",
						("noplot_" if not controlregions else "") + "zl_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_zll(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*" + Samples.zj_genmatch(channel) + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt", "os"], cut_type=cut_type) + "*(mt_1>70.0)*((q_1*q_2)>0.0)",
						("noplot_" if not controlregions else "") + "zj_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_ttj(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt", "os"], cut_type=cut_type) + "*(mt_1>70.0)*((q_1*q_2)>0.0)",
						("noplot_" if not controlregions else "") + "ttj_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_vv(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt", "os"], cut_type=cut_type) + "*(mt_1>70.0)*((q_1*q_2)>0.0)",
						("noplot_" if not controlregions else "") + "vv_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_data(channel),
						self.root_file_folder(channel),
						1.0,
						data_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt", "os"], cut_type=cut_type) + "*(mt_1>70.0)*((q_1*q_2)>0.0)",
						("noplot_" if not controlregions else "") + "data_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_wj(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)*(mt_1>70.0)",
						("noplot_" if not controlregions else "") + "wj_ss_highmt",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_wj(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*stitchWeightWJ*" + self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
						"wj",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_wj(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*stitchWeightWJ*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt"], cut_type=cut_type),
						"noplot_wj_mc_os_inclusive",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_wj(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*stitchWeightWJ*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt", "os"], cut_type=cut_type) + "*((q_1*q_2)>0.0)",
						"noplot_wj_mc_ss_inclusive",
						nick_suffix=nick_suffix
				)
				if not "EstimateWjetsAndQCD" in config.get("analysis_modules", []):
					config.setdefault("analysis_modules", []).append("EstimateWjetsAndQCD")
				if controlregions:
					config.setdefault("wjets_ss_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "ztt_ss_highmt zll_ss_highmt ttj_ss_highmt vv_ss_highmt".split()]))
					config.setdefault("wjets_ss_data_nicks", []).append("data_ss_highmt"+nick_suffix)
					config.setdefault("wjets_os_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "ztt_os_highmt zll_os_highmt ttj_os_highmt vv_os_highmt".split()]))
					config.setdefault("wjets_os_data_nicks", []).append("data_os_highmt"+nick_suffix)
					config.setdefault("wjets_shape_nicks", []).append("wj"+nick_suffix)
					config.setdefault("wjets_ss_mc_nicks", []).append("noplot_wj_mc_ss_inclusive"+nick_suffix)
					config.setdefault("wjets_ss_highmt_mc_nicks", []).append("wj_ss_highmt"+nick_suffix)
					config.setdefault("wjets_os_mc_nicks", []).append("noplot_wj_mc_os_inclusive"+nick_suffix)
					config.setdefault("wjets_os_highmt_mc_nicks", []).append("wj_os_highmt"+nick_suffix)
					config.setdefault("wjets_os_lowmt_mc_nicks", []).append("wj"+nick_suffix)
					for nick in ["ztt_os_highmt", "zll_os_highmt", "zl_os_highmt", "zj_os_highmt", "ttj_os_highmt", "vv_os_highmt", "data_os_highmt", "wj_os_highmt", "ztt_ss_highmt", "zll_ss_highmt", "zl_ss_highmt", "zj_ss_highmt", "ttj_ss_highmt", "vv_ss_highmt", "data_ss_highmt", "wj_ss_highmt"]:
						if not kwargs.get("mssm", False):
							Samples._add_bin_corrections(config, nick, nick_suffix)
						Samples._add_plot(config, "bkg", "HIST", "F", nick, nick_suffix)
				else:
					config.setdefault("wjets_ss_substract_nicks", []).append(" ".join(["noplot_"+nick+nick_suffix for nick in "ztt_ss_highmt zll_ss_highmt ttj_ss_highmt vv_ss_highmt".split()]))
					config.setdefault("wjets_ss_data_nicks", []).append("noplot_data_ss_highmt"+nick_suffix)
					config.setdefault("wjets_os_substract_nicks", []).append(" ".join(["noplot_"+nick+nick_suffix for nick in "ztt_os_highmt zll_os_highmt ttj_os_highmt vv_os_highmt".split()]))
					config.setdefault("wjets_os_data_nicks", []).append("noplot_data_os_highmt"+nick_suffix)
					config.setdefault("wjets_shape_nicks", []).append("wj"+nick_suffix)
					config.setdefault("wjets_ss_mc_nicks", []).append("noplot_wj_mc_ss_inclusive"+nick_suffix)
					config.setdefault("wjets_ss_highmt_mc_nicks", []).append("noplot_wj_ss_highmt"+nick_suffix)
					config.setdefault("wjets_os_mc_nicks", []).append("noplot_wj_mc_os_inclusive"+nick_suffix)
					config.setdefault("wjets_os_highmt_mc_nicks", []).append("noplot_wj_os_highmt"+nick_suffix)
					config.setdefault("wjets_os_lowmt_mc_nicks", []).append("wj"+nick_suffix)

			if estimationMethod == "classic":
				shape_weight = mc_weight+weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type)
				#if (not category is None) and (category != ""):
					## relaxed isolation
					#shape_weight = weight+"*eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["blind", "iso_2"], cut_type=cut_type) + "*(byCombinedIsolationDeltaBetaCorrRaw3Hits_2<10.0)"

				Samples._add_input(
						config,
						self.files_wj(channel),
						self.root_file_folder(channel),
						lumi,
						shape_weight,
						"wj",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_data(channel),
						self.root_file_folder(channel),
						1.0,
						data_weight+"eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						"noplot_wj_data_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_ztt(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"eventWeight*" + Samples.ztt_genmatch(channel) + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						"noplot_ztt_mc_wj_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_zll(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"eventWeight*" + Samples.zll_genmatch(channel) + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						"noplot_zll_wj_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_ttj(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						"noplot_ttj_wj_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_vv(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"eventWeight*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						"noplot_vv_wj_control",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_wj(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+weight+"*eventWeight*stitchWeightWJ*" + self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
						"noplot_wj_mc_signal",
						nick_suffix=nick_suffix
				)
				Samples._add_input(
						config,
						self.files_wj(channel),
						self.root_file_folder(channel),
						lumi,
						mc_weight+"eventWeight*stitchWeightWJ*" + self._cut_string(channel, exclude_cuts=exclude_cuts+["mt"], cut_type=cut_type) + "*(mt_1>70.0)",
						"noplot_wj_mc_control",
						nick_suffix=nick_suffix
				)

				if not "EstimateWjets" in config.get("analysis_modules", []):
					config.setdefault("analysis_modules", []).append("EstimateWjets")
				if channel in ["mt", "et"] and fakefactor_method == "standard":
					config["weights"][config["nicks"].index("wj")] = config["weights"][config["nicks"].index("wj")]  + "*(gen_match_2 != 6)"
					config.setdefault("wjets_from_mc", []).append(True)
				if channel in ["mt", "et"] and fakefactor_method == "comparison":
					config["weights"][config["nicks"].index("wj")] = config["weights"][config["nicks"].index("wj")]  + "*(gen_match_2 == 6)"
					config.setdefault("wjets_from_mc", []).append(False)
				if fakefactor_method is None:
					config.setdefault("wjets_from_mc", []).append(False)
				config.setdefault("wjets_shape_nicks", []).append("wj"+nick_suffix)
				config.setdefault("wjets_data_control_nicks", []).append("noplot_wj_data_control"+nick_suffix)
				config.setdefault("wjets_data_substract_nicks", []).append(" ".join([nick+nick_suffix for nick in "noplot_ztt_mc_wj_control noplot_zll_wj_control noplot_ttj_wj_control noplot_vv_wj_control".split()]))
				config.setdefault("wjets_mc_signal_nicks", []).append("noplot_wj_mc_signal"+nick_suffix)
				config.setdefault("wjets_mc_control_nicks", []).append("noplot_wj_mc_control"+nick_suffix)

		elif channel in ["em", "tt", "mm"]:
			Samples._add_input(
					config,
					self.files_wj(channel),
					self.root_file_folder(channel),
					lumi,
					weight+"*eventWeight*stitchWeightWJ*" + self._cut_string(channel, exclude_cuts=exclude_cuts, cut_type=cut_type),
					"wj",
					nick_suffix=nick_suffix
			)
		else:
			log.error("Sample config (WJets) currently not implemented for channel \"%s\"!" % channel)

		if not kwargs.get("no_plot", False):
			if not kwargs.get("mssm", False):
				Samples._add_bin_corrections(config, "wj", nick_suffix)
			Samples._add_plot(config, "bkg", "HIST", "F", "wj", nick_suffix)
		return config