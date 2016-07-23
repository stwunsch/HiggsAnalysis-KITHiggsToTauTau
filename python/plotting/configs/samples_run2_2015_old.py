
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
		return self.artus_file_names({"process" : "WplusHToTauTauM"+str(mass), "data": False, "campaign" : self.mc_campaign}, 1)

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
			                 normalise_signal_to_one_pb, lumi=lumi, exclude_cuts=exclude_cuts, no_plot=True, **kwargs)

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