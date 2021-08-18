#!/usr/bin/env python

from __future__ import print_function, division

import os, sys, subprocess, argparse
import tmJDLInterface, tmEOSUtils
import e2e_env, e2e_common, e2e_settings

inputArgumentsParser = argparse.ArgumentParser(description='Submit generation jobs for various mass points.')
inputArgumentsParser.add_argument('--isProductionRun', action='store_true', help="By default, this script does not submit the actual jobs and instead only prints the shell command that would have been called. Passing this switch will execute the commands.")
inputArguments = inputArgumentsParser.parse_args()

settings = e2e_settings.Settings("settings.json")

condor_directory = "{cA}/e2e_pi0_minimal_analysis".format(cA=e2e_env.condor_work_area_root)
script_directory = "sh_condor_wrappers"
script_name = "run_minimal_analyzer_pi0.sh"
mass_points = settings.values_["generate_pi0"]["mass_points"]

# Make condor folder if it doesn't exist
subprocess.check_call("mkdir -p {cd}".format(cd=condor_directory), executable="/bin/bash", shell=True)

# Copy script over to condor folder
subprocess.check_call("cp -u {sd}/{sn} {cd}/.".format(sd=script_directory, sn=script_name, cd=condor_directory), executable="/bin/bash", shell=True)

# Make sure all tarballs are up to date
e2e_common.update_and_upload_e2e_tarballs()

# Build list of input folders
def get_parent_folder(full_path):
    return ("/".join(full_path.split("/")[:-1]))
input_eos_paths_without_prefix_pi0 = {}
for mass_point_title in mass_points:
    genAOD_path_generator_pi0 = tmEOSUtils.generate_list_of_files_in_eos_path(eos_path="{r}/genAOD/pi0/pi0/crab_generation_pi0_{t}".format(r=e2e_env.e2e_eos_root, t=mass_point_title), appendPrefix=False)
    input_eos_paths_without_prefix_pi0[mass_point_title] = None
    for eos_candidate_path in genAOD_path_generator_pi0:
        parent_folder = get_parent_folder(eos_candidate_path)
        if (input_eos_paths_without_prefix_pi0[mass_point_title] is None):
            input_eos_paths_without_prefix_pi0[mass_point_title] = parent_folder
        else:
            if (parent_folder != input_eos_paths_without_prefix_pi0[mass_point_title]):
                sys.exit("ERROR in finding input folder paths: two candidates found for pattern \"pi0\". Previous guess: {pg}, current file path: {cfp}, current guess: {cg}".format(pg=input_eos_paths_without_prefix_pi0[mass_point_title], cfp=eos_candidate_path, cg=parent_folder))
    if (input_eos_paths_without_prefix_pi0[mass_point_title] is None):
        sys.exit("ERROR: no ROOT files found at path {p}".format(p="{r}/genAOD/pi0/pi0/crab_generation_pi0_{t}".format(r=e2e_env.e2e_eos_root, t=mass_point_title)))

# Submit jobs
for mass_point_title in mass_points:
    mass = mass_points[mass_point_title]
    for clone_index in range(1, 1+settings.values_["generate_pi0"]["nCopiesPerMassPoint"]):
        processIdentifier = "run_minimal_analyzer_pi0_{t}_{i}".format(t=mass_point_title, i=clone_index)
        filesToTransfer = [e2e_env.x509Proxy, "{er}/sh_snippets/setup_environment_remote.sh".format(er=e2e_env.e2e_root)]
        jdlInterface = tmJDLInterface.tmJDLInterface(processName=processIdentifier, scriptPath=script_name, outputDirectoryRelativePath=condor_directory)
        jdlInterface.addFilesToTransferFromList(filesToTransfer)
        jdlInterface.addScriptArgument("{p}/{ip}/pi0_back_to_back_cfg_py_GEN_SIM_DIGI_L1_DIGI2RAW_HLT_RAW2DIGI_L1Reco_RECO_{i}.root".format(p=e2e_env.eos_prefix, ip=input_eos_paths_without_prefix_pi0[mass_point_title], i=clone_index)) # Argument 1: input path
        jdlInterface.addScriptArgument("{ep}/{eer}/pi0_analysis/minimal".format(ep=e2e_env.eos_prefix, eer=e2e_env.e2e_eos_root)) # Argument 2: output EOS directory with prefix for xrdcp
        jdlInterface.addScriptArgument("{mpt}_{i}".format(mpt=mass_point_title, i=clone_index)) # Argument 3: output ID
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
