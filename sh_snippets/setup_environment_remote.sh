set -e

function xrdcp_with_check {
    if [ "${#}" != 2  ]; then
        echo "ERROR: number of arguments passed to \"${FUNCNAME}\": ${#}"
        exit 1
    fi
    xrdcp --nopbar --verbose --force --path --streams 15 ${1} ${2} 2>&1
    XRDEXIT=${?}
    if [[ ${XRDEXIT} -ne 0 ]]; then
        echo "exit code ${XRDEXIT}, failure in xrdcp"
        exit ${XRDEXIT}
    fi
}

function xrdmv_with_check {
    if [ "${#}" != 2  ]; then
        echo "ERROR: number of arguments passed to \"${FUNCNAME}\": ${#}"
        exit 1
    fi
    xrdcp_with_check "${1}" "${2}"
    rm ${1}
}

function cleanup {
    cd ${_CONDOR_SCRATCH_DIR}
    rm -r -f proxy
    rm -r -f tmPyUtils
    rm -r -f tmCPPUtils
    rm -r -f e2e-scripts
    rm -r -f CMSSW_10_2_20_UL
}

cd ${_CONDOR_SCRATCH_DIR}

# Make sure there's exactly one file beginning with "x509"
x509Matches=`find . -maxdepth 2 -type f -name x509*`
NMatchesMinusOne=`echo ${x509Matches} | tr -cd " \t" | wc -c`
if [ "${NMatchesMinusOne}" != "0" ]; then
    echo "ERROR: More than one file found beginning with x509"
    exit 1
fi

# Move file to proxy
mkdir proxy
mv -v x509* proxy/
x509Matches=`find proxy/ -maxdepth 2 -type f -name x509*`
export X509_USER_PROXY=${_CONDOR_SCRATCH_DIR}/${x509Matches}
echo "Set X509_USER_PROXY=${X509_USER_PROXY}"
echo "voms output:"
voms-proxy-info --all

cd ${_CONDOR_SCRATCH_DIR}

echo "Starting job on: `date`" #Date/time of start of job
echo "Running on: `uname -a`" #Condor job is running on this node
echo "System software: `cat /etc/redhat-release`" #Operating System on that node

# Source CMSSW environment
echo "Sourcing CMSSW environment..."
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc700
xrdcp --nopbar --verbose --force --path --streams 15 root://cmseos.fnal.gov//store/user/tmudholk/e2e_tarballs/CMSSW10220UL.tar.gz .
tar -xzf CMSSW10220UL.tar.gz && rm CMSSW10220UL.tar.gz
cd CMSSW_10_2_20_UL/src/ && scramv1 b ProjectRename && eval `scramv1 runtime -sh`
echo "CMSSW version: ${CMSSW_BASE}"
cd ${_CONDOR_SCRATCH_DIR}

xrdcp --nopbar --verbose --force --path --streams 15 root://cmseos.fnal.gov//store/user/tmudholk/e2e_tarballs/tmUtils.tar.gz .
echo "Extracting tmUtils tarball..."
tar -xzf tmUtils.tar.gz && rm tmUtils.tar.gz
export TMPYUTILS=${_CONDOR_SCRATCH_DIR}/tmPyUtils/
export TMCPPUTILS=${_CONDOR_SCRATCH_DIR}/tmCPPUtils/
export PYTHONPATH=${_CONDOR_SCRATCH_DIR}/tmPyUtils:${PYTHONPATH}
cd tmCPPUtils/generalUtils && mkdir lib && mkdir obj && make clean && make
cd ${_CONDOR_SCRATCH_DIR}
cd tmCPPUtils/ROOTUtils && mkdir lib && mkdir obj && make clean && make
cd ${_CONDOR_SCRATCH_DIR}

xrdcp --nopbar --verbose --force --path --streams 15 root://cmseos.fnal.gov//store/user/tmudholk/e2e_tarballs/e2e-scripts.tar.gz .
echo "Extracting main work area tarball..."
tar -xzf e2e-scripts.tar.gz && rm e2e-scripts.tar.gz
export PYTHONPATH=${_CONDOR_SCRATCH_DIR}/e2e-scripts/py_modules:${PYTHONPATH}
cd e2e-scripts && make clean && make
cd ${_CONDOR_SCRATCH_DIR}
