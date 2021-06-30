#!/usr/bin/env python

from __future__ import print_function, division

import os, sys, subprocess, argparse
import tmJDLInterface
import e2e_env, e2e_common, e2e_settings

inputArgumentsParser = argparse.ArgumentParser(description='Submit ntuplization jobs for generated AODs.')
inputArgumentsParser.add_argument('--isProductionRun', action='store_true', help="By default, this script does not submit the actual jobs and instead only prints the shell command that would have been called. Passing this switch will execute the commands.")
inputArguments = inputArgumentsParser.parse_args()

condor_directory = "{cA}/e2e_ntuplization".format(cA=e2e_env.condor_work_area_root)
script_directory = "sh_condor_wrappers"
script_name = "run_genAOD_ntuplization.sh"
filesToTransfer = [e2e_env.x509Proxy, "{er}/sh_snippets/setup_environment_remote.sh".format(er=e2e_env.e2e_root)]

# Make condor folder if it doesn't exist
subprocess.check_call("mkdir -p {cd}".format(cd=condor_directory), executable="/bin/bash", shell=True)

# Copy script over to condor folder
subprocess.check_call("cp -u {sd}/{sn} {cd}/.".format(sd=script_directory, sn=script_name, cd=condor_directory), executable="/bin/bash", shell=True)

# Make sure all tarballs are up to date
e2e_common.update_and_upload_e2e_tarballs()

settings = e2e_settings.Settings("settings.json")

# First gamma
for copy_index in range(settings.values_["generate_gamma"]["nCopies"]):
    processIdentifier = "run_ntuplization_gamma_copy{i}".format(i=copy_index)
    jdlInterface = tmJDLInterface.tmJDLInterface(processName=processIdentifier, scriptPath=script_name, outputDirectoryRelativePath=condor_directory)
    jdlInterface.addFilesToTransferFromList(filesToTransfer)
    jdlInterface.addScriptArgument("{ep}/{eer}/genAOD/gamma/gamma_back_to_back_cfg_py_GEN_SIM_DIGI_L1_DIGI2RAW_HLT_RAW2DIGI_L1Reco_RECO_copy{i}.root".format(ep=e2e_env.eos_prefix, eer=e2e_env.e2e_eos_root, i=copy_index)) # Argument 1: input path
    jdlInterface.addScriptArgument("{ep}/{eer}/genAOD_ntuples/gamma".format(ep=e2e_env.eos_prefix, eer=e2e_env.e2e_eos_root)) # Argument 2: output EOS directory with prefix for xrdcp
    jdlInterface.addScriptArgument("copy{i}".format(i=copy_index)) # Argument 3: output ID
    if (e2e_env.habitat == "lxplus"):
        jdlInterface.setFlavor("tomorrow")
    # # Write JDL
    jdlInterface.writeToFile()
    submissionCommand = "cd {cd}/ && condor_submit {pI}.jdl && cd {er}".format(cd=condor_directory, pI=processIdentifier, er=e2e_env.e2e_root)
    if (inputArguments.isProductionRun):
        subprocess.check_call(submissionCommand, executable="/bin/bash", shell=True)
        print ("Submitted.")
    else:
        print("Not submitting because isProductionRun flag was not set:")
        print(submissionCommand)

# Now pi0
mass_points = settings.values_["generate_pi0"]["mass_points"]
for mass_point_title in mass_points:
    mass = mass_points[mass_point_title]
    for copy_index in range(settings.values_["generate_pi0"]["nCopiesPerMassPoint"]):
        processIdentifier = "run_ntuplization_pi0_{t}_copy{i}".format(t=mass_point_title, i=copy_index)
        jdlInterface = tmJDLInterface.tmJDLInterface(processName=processIdentifier, scriptPath=script_name, outputDirectoryRelativePath=condor_directory)
        jdlInterface.addFilesToTransferFromList(filesToTransfer)
        jdlInterface.addScriptArgument("{ep}/{eer}/genAOD/pi0/pi0_back_to_back_cfg_py_GEN_SIM_DIGI_L1_DIGI2RAW_HLT_RAW2DIGI_L1Reco_RECO_{mpt}_copy{i}.root".format(ep=e2e_env.eos_prefix, eer=e2e_env.e2e_eos_root, mpt=mass_point_title, i=copy_index)) # Argument 1: input path
        jdlInterface.addScriptArgument("{ep}/{eer}/genAOD_ntuples/pi0".format(ep=e2e_env.eos_prefix, eer=e2e_env.e2e_eos_root)) # Argument 2: output EOS directory with prefix for xrdcp
        jdlInterface.addScriptArgument("{mpt}_copy{i}".format(mpt=mass_point_title, i=copy_index)) # Argument 3: output ID
        if (e2e_env.habitat == "lxplus"):
            jdlInterface.setFlavor("tomorrow")
        # # Write JDL
        jdlInterface.writeToFile()
        submissionCommand = "cd {cd}/ && condor_submit {pI}.jdl && cd {er}".format(cd=condor_directory, pI=processIdentifier, er=e2e_env.e2e_root)
        if (inputArguments.isProductionRun):
            subprocess.check_call(submissionCommand, executable="/bin/bash", shell=True)
            print ("Submitted.")
        else:
            print("Not submitting because isProductionRun flag was not set:")
            print(submissionCommand)

print("All done!")
