export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
source ${VO_CMS_SW_DIR}/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc700
cd ${E2E_CMSSW_BASE}/src && eval `scramv1 runtime -sh`
cd ${E2E_ROOT}
export PYTHONPATH=${E2E_ROOT}/py_modules:${PYTHONPATH}
