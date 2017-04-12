#!/bin/bash

# source Artus ini script
source $CMSSW_BASE/src/Artus/Configuration/scripts/ini_ArtusAnalysis.sh

# source Harry ini script
source $CMSSW_BASE/src/Artus/HarryPlotter/scripts/ini_harry_cmssw.sh

# set the environment
export KITHIGGSTOTAUTAUPATH=$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau
