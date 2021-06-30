#!/bin/bash

set -e
cd ${_CONDOR_SCRATCH_DIR}
INPUT_PATH=${1}
OUTPUT_EOS_DIR=${2}
OUTPUT_ID=${3}

source setup_environment_remote.sh
source /cvmfs/sft.cern.ch/lcg/views/LCG_97/x86_64-centos7-gcc8-opt/setup.sh

set -x
python ${CMSSW_BASE}/src/MLAnalyzer/convert_root2pq_ESshower.py --infile=${INPUT_PATH} --decay=converted_${OUTPUT_ID}
xrdmv_with_check converted_${OUTPUT_ID}.parquet.0 ${OUTPUT_EOS_DIR}/converted_${OUTPUT_ID}.parquet.0
set +x

# cd ${_CONDOR_SCRATCH_DIR}
# echo "Removing everything else..."
# cleanup

echo "====================================================================================="
echo "All done!"
