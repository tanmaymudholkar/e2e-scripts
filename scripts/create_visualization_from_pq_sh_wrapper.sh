#!/bin/bash

INPUT_PATH=${1}
OUTPUT_FOLDER=${2}
OUTPUT_FILE_NAME=${3}

cd ${E2E_ROOT}
source /cvmfs/sft.cern.ch/lcg/views/LCG_97/x86_64-centos7-gcc8-opt/setup.sh

cd ${E2E_ROOT}
set -x
./scripts/create_visualization_from_pq.py --inputPQFile=${INPUT_PATH} --outputFolder=${OUTPUT_FOLDER} --outputFileName=${OUTPUT_FILE_NAME}
set +x
