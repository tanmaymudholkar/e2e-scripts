from __future__ import print_function, division

import os, sys

# print("Importing environment variables...")
e2e_root = os.getenv("E2E_ROOT")
e2e_eos_root = os.getenv("E2E_EOS_ROOT")
e2e_archives = os.getenv("E2E_ARCHIVES")
e2e_cmssw_base = os.getenv("E2E_CMSSW_BASE")
eos_prefix = os.getenv("EOSPREFIX")
tmUtils_parent = os.getenv("TM_UTILS_PARENT")
hostname = os.getenv("HOSTNAME")
x509Proxy = os.getenv("X509_USER_PROXY")
condor_work_area_root = os.getenv("CONDORWORKAREAROOT")
e2e_analysis_root = os.getenv("E2E_ANALYSISROOT")
scratch_area = os.getenv("SCRATCHAREA")
habitat = ""
if ("lxplus" in hostname):
    habitat = "lxplus"
elif ("fnal" in hostname):
    habitat = "fnal"
else:
    sys.exit("ERROR: Unrecognized hostname: {h}, seems to be neither lxplus nor fnal.".format(h=hostname))

# print("e2e_root: {e2eR}".format(e2eR=e2e_root))
# print("e2e_eos_root: {E2EER}".format(E2EER=e2e_eos_root))
# print("e2e_archives: {sA}".format(sA=e2e_archives))
# print("e2e_cmssw_base: {E2ECB}".format(E2ECB=e2e_cmssw_base))
# print("eos_prefix: {eP}".format(eP=eos_prefix))
# print("tmUtils_parent: {tUP}".format(tUP=tmUtils_parent))
# print("hostname: {hN}".format(hN=hostname))
# print("x509Proxy: {xP}".format(xP=x509Proxy))
# print("condor_work_area_root: {cWAR}".format(cWAR=condor_work_area_root))
# print("e2e_analysis_root: {aR}".format(aR=e2e_analysis_root))
# print("scratch_area: {sA}".format(sA=scratch_area))
# print("Setting habitat = {h}".format(h=habitat))

def get_execution_command(commandToRun):
    env_setup_command = "bash -c \"cd {e2eR}/sh_snippets && source setup_env.sh && cd ..".format(e2eR=e2e_root)
    return "{e_s_c} && set -x && {c} && set +x\"".format(e_s_c=env_setup_command, c=commandToRun)

def execute_in_env(commandToRun, isDryRun=False, functionToCallIfCommandExitsWithError=None):
    executionCommand = get_execution_command(commandToRun)
    if (isDryRun):
        print("Dry-run, not executing:")
        print("{c}".format(c=executionCommand))
    else:
        print("Executing:")
        print("{c}".format(c=executionCommand))
        returnCode = os.system(executionCommand)
        if (returnCode != 0):
            if not(functionToCallIfCommandExitsWithError is None):
                if not(callable(functionToCallIfCommandExitsWithError)): sys.exit("ERROR in execute_in_env: command exited with error and unable to call functionToCallIfCommandExitsWithError")
                else: functionToCallIfCommandExitsWithError()
            sys.exit("ERROR in execute_in_env: command \"{c}\" returned status {rC}".format(c=executionCommand, rC=returnCode))
