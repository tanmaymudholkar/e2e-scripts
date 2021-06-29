#!/bin/bash

set -e
cd ${_CONDOR_SCRATCH_DIR}

CFGPATH=Configuration/GenProduction/python/Guns
CFG=pi0_back_to_back_cfg.py
# for crab submission: NEVTS will be automatically overwritten by totalUnits in crab cfg
NEVTS=${1}
EVTCONT=AODSIM
PU=noPU
GT=102X_upgrade2018_realistic_v15
ERA=Run2_2018
BEAM=Realistic25ns13TeVEarly2018Collision
IDENTIFIER=${2}
CFGFORMATTED=`echo ${CFG} | sed "s|\.|_|"`
OUTPUT_PREFIX="${CFGFORMATTED}_GEN_SIM_DIGI_L1_DIGI2RAW_HLT_RAW2DIGI_L1Reco_RECO_${IDENTIFIER}"
OUTPUT_EOS_DIR=${3}
FIXED_MASS=${4}
GENERATOR_SEED=${5}

source setup_environment_remote.sh

## NoPileup ##
set -x
cmsDriver.py ${CFGPATH}/${CFG} --conditions ${GT} -n ${NEVTS} --mc --era ${ERA} --eventcontent ${EVTCONT} --runUnscheduled --step GEN,SIM,DIGI,L1,DIGI2RAW,HLT:@fake,RAW2DIGI,L1Reco,RECO --geometry DB:Extended --datatier GEN-SIM-DIGI-RAW-RECO --beamspot ${BEAM} --customise_commands "process.source.numberEventsInLuminosityBlock=cms.untracked.uint32(2000)\nprocess.generator.PGunParameters.FixedMass=${FIXED_MASS}\nprocess.RandomNumberGeneratorService.generator.initialSeed=${GENERATOR_SEED}" --fileout file:${OUTPUT_PREFIX}.root --python_filename ${OUTPUT_PREFIX}.py

xrdmv_with_check ${OUTPUT_PREFIX}.root ${OUTPUT_EOS_DIR}/${OUTPUT_PREFIX}.root

# cleanup
rm ${OUTPUT_PREFIX}.py
cleanup

echo "All done!"

set +x

## For full MC campaign cfgs, follow test or setup commands in Actions column on McM for desired campaign. For example, for: https://cms-pdmv.cern.ch/mcm/requests?dataset_name=HAHMHToAA_AToGG_MA-0p1GeV_TuneCP5_PSweights_13TeV-madgraph_pythia8&page=0&shown=127

# LHE->GEN->SIM (LHEGS): https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_setup/HIG-RunIIFall18wmLHEGS-03374
# DIGI->RECO + pre-mixed PU: https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_setup/HIG-RunIIAutumn18DRPremix-02702
# AOD->MINIAOD: https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_setup/HIG-RunIIAutumn18MiniAOD-02720
# MINIAOD->NANOAOD: https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_setup/HIG-RunIIAutumn18NanoAODv7-02726

# Some tweaking of the arguments might be needed to get them to work...
