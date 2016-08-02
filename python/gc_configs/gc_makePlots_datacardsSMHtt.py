#from gcSettings import Settings
#   this import is only needed to execute the script standalone
#   (<GCDIR>/packages needs to be in your PYTHONPATH - or grid-control was properly installed)

import time
import os
print(time.time())
active = ["0jet", "1jet", "2jet"]

active = active[1]
project_name = "FirstScan"
print "doing stuff for " + active

cfg = Settings()
channels= ["et", "mt", "tt", "em"]
cfg.workflow.task = 'UserTask'
cfg.workflow.backend = 'local'
cfg.workflow.proxy = "VomsProxy"

cfg.jobs.wall_time = '12:00:00'
cfg.jobs.set("memory", "14000")

cfg.usertask.executable = 'HiggsAnalysis/KITHiggsToTauTau/scripts/userjob_epilog.sh'
cmssw_base = os.getenv("CMSSW_BASE") + "/src/"
cfg.usertask.set("input files", [cmssw_base + "HiggsAnalysis/KITHiggsToTauTau/scripts/userjob_epilog.sh", cmssw_base + "HiggsAnalysis/KITHiggsToTauTau/scripts/makePlots_datacardsMVATest.py"] )

executable = 'makePlots_datacardsMVATest.py'
input_dataset = "-i /nfs/dust/cms/user/mschmitt/htautau/artus/2016-07-28_14-35_FinalBDTCached/merged/"

if active == "2jet":
	variable = "-x TwoJets_FinalBDT"
elif active == "1jet":
	variable = "-x OneJets_FinalBDT"
else:
	variable = "-x ZeroJets_FinalBDT"
mass = "-m 125"
output_dir = "-o ."
extra=" --n-plots 1000 0 --auto-rebin --qcd-subtract-shape -n 1 --remote --use-asimov-dataset"


cfg.parameters.set("parameters", ["P1", "P2"])
cfg.parameters.set("repeat", 1)
cfg.parameters.set("P1", [str(x/100.-1.) for x in range(50,200,50)])
cfg.parameters.set("P2", [str(x/100.-1.) for x in range(50,200,50)])
#if active == "2jet":
	#cfg.parameters.set("P1", [str(x/100.-1.) for x in range(0,200,10)])
	#cfg.parameters.set("P2", [str(x/100.-1.) for x in range(0,200,10)])
#elif active == "1jet":
	#cfg.parameters.set("P1", [str(x/100.-1.) for x in range(0,200,10)])
	#cfg.parameters.set("P2", [str(x/100.-1.) for x in range(0,200,10)])
#else:
	#cfg.parameters.set("P1", [str(x/100.-1.) for x in range(0,200,10)])
	#cfg.parameters.set("P2", [str(x/100.-1.) for x in range(0,200,10)])

arguments = executable + " " + variable +" "+ mass +" "+ output_dir+ " " + extra + " " + input_dataset
#for channel in channels:
arguments = arguments +" --channel " + " ".join(channels) + " --categories"
if active == "0jet":
	arguments = arguments +" 0jet_@P1@_@P2@ i0jet_@P1@_@P2@ "
#else:
	#arguments = arguments +" ZeroJet30 "
	#arguments = arguments +" 0jet_10_50 i0jet_10_50 "

if active == "1jet":
	arguments = arguments +" 1jet_@P1@_@P2@ i1jet_@P1@_@P2@ "
#else:
	#arguments = arguments +" OneJet30 "
	#arguments = arguments +" 1jet_120_40 i1jet_120_40 "

if active == "2jet":
	arguments = arguments +" vbf_@P1@_@P2@ ivbf_@P1@_@P2@ "
	#else:
		#arguments = arguments +" TwoJet30 "
		#arguments = arguments +" vbf_400_3.0 ivbf_400_3.0 "

cfg.usertask.set('arguments', "%s"%arguments)
cfg.storage.set('se path', "/nfs/dust/cms/user/mschmitt/htautau/artus/" + project_name + "/" + active + "_scan")
cfg.storage.set('se output files', "jobresult.tar")
cfg.storage.set('se output pattern', "@P1@_@P2@/@X@")
getattr(cfg, 'global').set('workdir', "/nfs/dust/cms/user/mschmitt/htautau/artus/" + project_name + "/" + active + "_workdir")
print(cfg)
print('=' * 20)
