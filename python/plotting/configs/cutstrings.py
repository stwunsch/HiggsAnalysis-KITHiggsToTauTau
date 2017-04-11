
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import sys

class CutStringsDict:
	
	@staticmethod
	def baseline(channel, cut_type):
		cuts = {}
		cuts["blind"] = "{blind}"
		cuts["os"] = "((q_1*q_2)<0.0)"
		
		if channel == "mm":
			cuts["extra_lepton_veto"] = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)"
			cuts["iso_1"] = "(iso_1 < 0.15)"
			cuts["iso_2"] = "(iso_2 < 0.15)"
			cuts["m_vis"] = "(m_vis > 60.0)*(m_vis < 120.0)"
		elif channel == "ee":
			pass
		elif channel == "em":
			cuts["trigger_threshold"] = "(pt_1 > 24.0 || pt_2 > 24.0)" if "2016" in cut_type else "(1.0)"
			cuts["pzeta"] = "(pZetaMissVis > -35.0)" if "2016" in cut_type and not "mssm" in cut_type else "(pZetaMissVis > -20.0)"
			cuts["extra_lepton_veto"] = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)"
			cuts["iso_1"] = "(iso_1 < 0.15)"
			cuts["iso_2"] = "(iso_2 < 0.2)" if "2016" in cut_type else "(iso_2 < 0.15)"
			#if not "mssm" in cut_type: cuts["bveto"] = "(nbtag == 0)"
		elif channel == "mt":
                        # Change the mt cut here -------------------------------------------------------------------------->
			cuts["mt"] = "(mt_1<40.0)" if cut_type == "mssm2016" else "(mt_1<30.0)" if cut_type == "mssm" else "(mt_1<50.0)" if "2016" in cut_type else "(mt_1<40.0)"
			cuts["anti_e_tau_discriminators"] = "(againstElectronVLooseMVA6_2 > 0.5)"
			cuts["anti_mu_tau_discriminators"] = "(againstMuonTight3_2 > 0.5)"
			cuts["extra_lepton_veto"] = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)"
			cuts["dilepton_veto"] = "(dilepton_veto < 0.5)"
			cuts["iso_1"] = "(iso_1 < 0.15)" if "2016" in cut_type else "(iso_1 < 0.1)"
                        # Change the Tau isolation here ---------------------------------------------------------------->
			cuts["iso_2"] = "(byMediumIsolationMVArun2v1DBoldDMwLT_2 > 0.5)" if cut_type == "mssm2016" else "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
			#if not "mssm" in cut_type: cuts["bveto"] = "(nbtag == 0)"
		elif channel == "et":
			cuts["mt"] = "(mt_1<50.0)" if "2016" in cut_type else "(mt_1<40.0)"
			cuts["anti_e_tau_discriminators"] = "(againstElectronTightMVA6_2 > 0.5)"
			cuts["anti_mu_tau_discriminators"] = "(againstMuonLoose3_2 > 0.5)"
			cuts["extra_lepton_veto"] = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)"
			cuts["dilepton_veto"] = "(dilepton_veto < 0.5)"
			cuts["iso_1"] = "(iso_1 < 0.1)"
			cuts["iso_2"] = "(byMediumIsolationMVArun2v1DBoldDMwLT_2 > 0.5)" if cut_type == "mssm2016" else "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
			#if not "mssm" in cut_type: cuts["bveto"] = "(nbtag == 0)"
		elif channel == "tt":
			cuts["pt_1"] = "(pt_1 > 50.0)" if "2016" in cut_type and not "mssm" in cut_type else "(1.0)"
			cuts["extra_lepton_veto"] = "(extraelec_veto < 0.5)*(extramuon_veto < 0.5)"
			cuts["anti_e_tau_discriminators"] = "(againstElectronVLooseMVA6_1 > 0.5)*(againstElectronVLooseMVA6_2 > 0.5)"
			cuts["anti_mu_tau_discriminators"] = "(againstMuonLoose3_1 > 0.5)*(againstMuonLoose3_2 > 0.5)"
			cuts["iso_1"] = "(byTightIsolationMVArun2v1DBoldDMwLT_1 > 0.5)" if "2016" in cut_type else "(byVTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
			cuts["iso_2"] = "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)" if "2016" in cut_type else "(byVTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antievloosepass(channel, cut_type):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["mt"] = "(mt_1 < 30.0)"
			cuts["iso_2"] = "(byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
			cuts["discriminator"] = "(againstElectronVLooseMVA6_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antievloosefail(channel, cut_type):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["mt"] = "(mt_1 < 30.0)"
			cuts["iso_2"] = "(byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
			cuts["discriminator"] = "(againstElectronVLooseMVA6_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antieloosepass(channel, cut_type):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["mt"] = "(mt_1 < 30.0)"
			cuts["iso_2"] = "(byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
			cuts["discriminator"] = "(againstElectronLooseMVA6_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antieloosefail(channel, cut_type):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["mt"] = "(mt_1 < 30.0)"
			cuts["iso_2"] = "(byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
			cuts["discriminator"] = "(againstElectronLooseMVA6_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antiemediumpass(channel, cut_type):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["mt"] = "(mt_1 < 30.0)"
			cuts["iso_2"] = "(byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
			cuts["discriminator"] = "(againstElectronMediumMVA6_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antiemediumfail(channel, cut_type):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["mt"] = "(mt_1 < 30.0)"
			cuts["iso_2"] = "(byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
			cuts["discriminator"] = "(againstElectronMediumMVA6_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antietightpass(channel, cut_type):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["mt"] = "(mt_1 < 30.0)"
			cuts["iso_2"] = "(byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
			cuts["discriminator"] = "(againstElectronTightMVA6_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antietightfail(channel, cut_type):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["mt"] = "(mt_1 < 30.0)"
			cuts["iso_2"] = "(byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
			cuts["discriminator"] = "(againstElectronTightMVA6_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antievtightpass(channel, cut_type):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["mt"] = "(mt_1 < 30.0)"
			cuts["iso_2"] = "(byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
			cuts["discriminator"] = "(againstElectronVTightMVA6_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antievtightfail(channel, cut_type):
		if channel == "et":
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["mt"] = "(mt_1 < 30.0)"
			cuts["iso_2"] = "(byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
			cuts["discriminator"] = "(againstElectronVTightMVA6_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antimuloosepass(channel, cut_type):
		if channel == "mt":
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["pzeta"] = "(pZetaMissVis > -20.0)"
			cuts["discriminator"] = "(againstMuonLoose3_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antimuloosefail(channel, cut_type):
		if channel == "mt":
			cuts = CutStringsDict.baseline(channel, cut_type)
			#cuts["pzeta"] = "(pZetaMissVis > -20.0)"
			cuts["discriminator"] = "(againstMuonLoose3_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antimutightpass(channel, cut_type):
		if channel == "mt":
			cuts = CutStringsDict.baseline(channel, cut_type)
			#cuts["pzeta"] = "(pZetaMissVis > -20.0)"
			cuts["discriminator"] = "(againstMuonTight3_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def antimutightfail(channel, cut_type):
		if channel == "mt":
			cuts = CutStringsDict.baseline(channel, cut_type)
			#cuts["pzeta"] = "(pZetaMissVis > -20.0)"
			cuts["discriminator"] = "(againstMuonTight3_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def tauidloosepass(channel, cut_type):
		if channel in ["mt", "et"]:
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["pzeta"] = "(pZetaMissVis > -25.0)"
			cuts["bveto"] = "(nbtag == 0)"
			cuts["discriminator"] = "(byLooseIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def tauidloosefail(channel, cut_type):
		if channel in ["mt", "et"]:
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["pzeta"] = "(pZetaMissVis > -25.0)"
			cuts["bveto"] = "(nbtag == 0)"
			cuts["discriminator"] = "(byLooseIsolationMVArun2v1DBoldDMwLT_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def tauidmediumpass(channel, cut_type):
		if channel in ["mt", "et"]:
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["pzeta"] = "(pZetaMissVis > -25.0)"
			cuts["bveto"] = "(nbtag == 0)"
			cuts["discriminator"] = "(byMediumIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def tauidmediumfail(channel, cut_type):
		if channel in ["mt", "et"]:
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["pzeta"] = "(pZetaMissVis > -25.0)"
			cuts["bveto"] = "(nbtag == 0)"
			cuts["discriminator"] = "(byMediumIsolationMVArun2v1DBoldDMwLT_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def tauidtightpass(channel, cut_type):
		if channel in ["mt", "et"]:
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["pzeta"] = "(pZetaMissVis > -25.0)"
			cuts["bveto"] = "(nbtag == 0)"
			cuts["discriminator"] = "(byTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def tauidtightfail(channel, cut_type):
		if channel in ["mt", "et"]:
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["pzeta"] = "(pZetaMissVis > -25.0)"
			cuts["bveto"] = "(nbtag == 0)"
			cuts["discriminator"] = "(byTightIsolationMVArun2v1DBoldDMwLT_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def tauidvtightpass(channel, cut_type):
		if channel in ["mt", "et"]:
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["pzeta"] = "(pZetaMissVis > -25.0)"
			cuts["bveto"] = "(nbtag == 0)"
			cuts["discriminator"] = "(byVTightIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def tauidvtightfail(channel, cut_type):
		if channel in ["mt", "et"]:
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["pzeta"] = "(pZetaMissVis > -25.0)"
			cuts["bveto"] = "(nbtag == 0)"
			cuts["discriminator"] = "(byVTightIsolationMVArun2v1DBoldDMwLT_2 < 0.5)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts
	
	@staticmethod
	def tauescuts(channel, cut_type):
		if channel == "mt":
			cuts = CutStringsDict.baseline(channel, cut_type)
			if not "2016" in cut_type:
				# the cuts below lead to W+jets being estimated to zero
				# with new background estimation technique
				cuts["pzeta"] = "(pZetaMissVis > -25.0)"
				cuts["bveto"] = "(nbtag == 0)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	@staticmethod
	def relaxedETauMuTauWJ(channel, cut_type):
		if channel in ["mt", "et"]:
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["iso_1"] = "(iso_1 < 0.3)"
			cuts["iso_2"] = "(byMediumIsolationMVArun2v1DBoldDMwLT_2 > 0.5)"
		elif channel in ["em"]:
			cuts = CutStringsDict.baseline(channel, cut_type)
			cuts["iso_1"] = "(iso_1 < 0.3)"
			cuts["iso_2"] = "(iso_1 < 0.3)"
		else:
			log.fatal("No cut values implemented for channel \"%s\" in \"%s\"" % (channel, cut_type))
			sys.exit(1)
		return cuts

	@staticmethod
	def baseline_low_mvis(channel, cut_type):
		cuts = CutStringsDict.baseline(channel, cut_type)
		cuts["m_vis"] = "((m_vis > 40.0) * (m_vis < 80.0))"
		return cuts

	@staticmethod
	def _get_cutdict(channel, cut_type):
		cuts = {}
		if cut_type=="baseline":
			cuts = CutStringsDict.baseline(channel, cut_type)
		elif cut_type=="baseline2016":
			cuts = CutStringsDict.baseline(channel, cut_type)
		elif cut_type=="mssm":
			cuts = CutStringsDict.baseline(channel, cut_type)
		elif cut_type=="mssm2016":
			cuts = CutStringsDict.baseline(channel, cut_type)
		elif cut_type=="antievloosepass":
			cuts = CutStringsDict.antievloosepass(channel, cut_type)
		elif cut_type=="antievloosefail":
			cuts = CutStringsDict.antievloosefail(channel, cut_type)
		elif cut_type=="antieloosepass":
			cuts = CutStringsDict.antieloosepass(channel, cut_type)
		elif cut_type=="antieloosefail":
			cuts = CutStringsDict.antieloosefail(channel, cut_type)
		elif cut_type=="antiemediumpass":
			cuts = CutStringsDict.antiemediumpass(channel, cut_type)
		elif cut_type=="antiemediumfail":
			cuts = CutStringsDict.antiemediumfail(channel, cut_type)
		elif cut_type=="antietightpass":
			cuts = CutStringsDict.antietightpass(channel, cut_type)
		elif cut_type=="antietightfail":
			cuts = CutStringsDict.antietightfail(channel, cut_type)
		elif cut_type=="antievtightpass":
			cuts = CutStringsDict.antievtightpass(channel, cut_type)
		elif cut_type=="antievtightfail":
			cuts = CutStringsDict.antievtightfail(channel, cut_type)
		
		elif cut_type=="antimuloosepass":
			cuts = CutStringsDict.antimuloosepass(channel, cut_type)
		elif cut_type=="antimuloosefail":
			cuts = CutStringsDict.antimuloosefail(channel, cut_type)
		elif cut_type=="antimutightpass":
			cuts = CutStringsDict.antimutightpass(channel, cut_type)
		elif cut_type=="antimutightfail":
			cuts = CutStringsDict.antimutightfail(channel, cut_type)
		
		elif cut_type=="tauidloosepass":
			cuts = CutStringsDict.tauidloosepass(channel, cut_type)
		elif cut_type=="tauidloosefail":
			cuts = CutStringsDict.tauidloosefail(channel, cut_type)
		elif cut_type=="tauidmediumpass":
			cuts = CutStringsDict.tauidmediumpass(channel, cut_type)
		elif cut_type=="tauidmediumfail":
			cuts = CutStringsDict.tauidmediumfail(channel, cut_type)
		elif cut_type=="tauidtightpass":
			cuts = CutStringsDict.tauidtightpass(channel, cut_type)
		elif cut_type=="tauidtightfail":
			cuts = CutStringsDict.tauidtightfail(channel, cut_type)
		elif cut_type=="tauidvtightpass":
			cuts = CutStringsDict.tauidvtightpass(channel, cut_type)
		elif cut_type=="tauidvtightfail":
			cuts = CutStringsDict.tauidvtightfail(channel, cut_type)
		
		elif cut_type=="tauescuts":
			cuts = CutStringsDict.tauescuts(channel, cut_type)
		elif cut_type=="tauescuts2016":
			cuts = CutStringsDict.tauescuts(channel, cut_type)
		elif cut_type=="relaxedETauMuTauWJ":
			cuts = CutStringsDict.relaxedETauMuTauWJ(channel, cut_type)
		
		elif cut_type=="baseline_low_mvis":
			cuts = CutStringsDict.baseline_low_mvis(channel, cut_type)
		
		else:
			log.fatal("No cut dictionary implemented for \"%s\"!" % cut_type)
			sys.exit(1)
		return cuts

