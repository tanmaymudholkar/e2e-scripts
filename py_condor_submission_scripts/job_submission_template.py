#!/usr/bin/env python

from __future__ import print_function, division

import os, sys, subprocess, argparse
import tmJDLInterface
import e2e_env, e2e_common

inputArgumentsParser = argparse.ArgumentParser(description='Basic template for job submission.')
inputArgumentsParser.add_argument('--example', default="example", help="Example argument.", type=str)
inputArgumentsParser.add_argument('--isProductionRun', action='store_true', help="By default, this script does not submit the actual jobs and instead only prints the shell command that would have been called. Passing this switch will execute the commands.")
inputArguments = inputArgumentsParser.parse_args()

# Make sure all tarballs are up to date
e2e_common.update_and_upload_e2e_tarballs()

condor_directory = "{cA}/e2e_template".format(cA=e2e_env.condor_work_area_root)
script_directory = "sh_condor_wrappers"
script_name = "minimal_template.sh"

# Make condor folder if it doesn't exist
subprocess.check_call("mkdir -p {cd}".format(cd=condor_directory), executable="/bin/bash", shell=True)

# Copy script over to condor folder
subprocess.check_call("cp -u {sd}/{sn} {cd}/.".format(sd=script_directory, sn=script_name, cd=condor_directory), executable="/bin/bash", shell=True)

processIdentifier = "templateJob"
filesToTransfer = [e2e_env.x509Proxy, "{er}/sh_snippets/setup_environment_remote.sh".format(er=e2e_env.e2e_root), "{er}/sh_condor_wrappers/template_test.txt".format(er=e2e_env.e2e_root)]
jdlInterface = tmJDLInterface.tmJDLInterface(processName=processIdentifier, scriptPath=script_name, outputDirectoryRelativePath=condor_directory)
jdlInterface.addFilesToTransferFromList(filesToTransfer)
jdlInterface.addScriptArgument(inputArguments.example) # Argument 1: test value
if (e2e_env.habitat == "lxplus"):
    jdlInterface.setFlavor("tomorrow")
    # Write JDL
jdlInterface.writeToFile()
submissionCommand = "cd {cd}/ && condor_submit {pI}.jdl && cd {er}".format(cd=condor_directory, pI=processIdentifier, er=e2e_env.e2e_root)
if (inputArguments.isProductionRun):
    subprocess.check_call(submissionCommand, executable="/bin/bash", shell=True)
    print ("Submitted.")
else:
    print("Not submitting because isProductionRun flag was not set:")
    print(submissionCommand)

print("All done!")
