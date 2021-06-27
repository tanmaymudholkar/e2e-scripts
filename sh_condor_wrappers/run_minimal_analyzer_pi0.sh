#!/bin/bash

set -e
cd ${_CONDOR_SCRATCH_DIR}
INPUT_PATH=${1}
OUTPUT_EOS_DIR=${2}
OUTPUT_ID=${3}

source setup_environment_remote.sh

set -x
cmsRun e2e-scripts/cmssw_interface/make_pi0_deltaR_histograms_cfg.py inputPath=${INPUT_PATH}
xrdmv_with_check histograms.root ${OUTPUT_EOS_DIR}/histograms_${OUTPUT_ID}.root
set +x
cd ${_CONDOR_SCRATCH_DIR}
echo "Removing everything else..."
cleanup

echo "====================================================================================="
echo "All done!"
