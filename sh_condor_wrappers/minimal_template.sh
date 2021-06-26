#!/bin/bash

set -e

cd ${_CONDOR_SCRATCH_DIR}

EXAMPLE_ARG=${1}
source setup_environment_remote.sh

set -x
echo "Starting to run example..."
echo "====================================================================================="
echo "EXAMPLE_ARG: ${EXAMPLE_ARG}"
echo "====================================================================================="
echo "Output of ls:"
ls
echo "====================================================================================="
echo "Some subfolders:"
echo "CMSSW:"
ls CMSSW_10_2_20_UL/src
echo "====================================================================================="
echo "e2e-scripts:"
ls e2e-scripts
echo "====================================================================================="
echo "e2e-scripts/bin:"
ls e2e-scripts/bin
echo "====================================================================================="
echo "tmPyUtils:"
ls tmPyUtils
echo "====================================================================================="
echo "tmCPPUtils:"
ls tmCPPUtils
echo "====================================================================================="

cd ${_CONDOR_SCRATCH_DIR}
echo "Removing everything else..."
cleanup

echo "====================================================================================="
echo "All done!"

set +x
