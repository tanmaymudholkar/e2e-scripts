#!/bin/bash

set -e
cd ${_CONDOR_SCRATCH_DIR}
INPUT_PATH=${1}
OUTPUT_EOS_DIR_WITH_XRD_PREFIX=${2}
OUTPUT_ID=${3}

source setup_environment_remote.sh

set -x
cmsRun ${CMSSW_BASE}/src/MLAnalyzer/RecHitAnalyzer/python/SCRegressor_cfg.py inputFiles=${INPUT_PATH} outputFile=ntuples.root
xrdmv_with_check ntuples.root ${OUTPUT_EOS_DIR_WITH_XRD_PREFIX}/ntuples_${OUTPUT_ID}.root
set +x

# cd ${_CONDOR_SCRATCH_DIR}
# echo "Removing everything else..."
# cleanup

echo "====================================================================================="
echo "All done!"
