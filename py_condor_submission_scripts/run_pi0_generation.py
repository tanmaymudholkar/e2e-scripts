#!/usr/bin/env python

from __future__ import print_function, division

import os, sys, subprocess, argparse
import tmJDLInterface
import e2e_env, e2e_common

inputArgumentsParser = argparse.ArgumentParser(description='Submit generation jobs for various mass points.')
inputArgumentsParser.add_argument('--nEvtsPerJob', default=500, help="Number of events for each condor job.", type=int)
inputArgumentsParser.add_argument('--nCopiesPerMassPoint', default=20, help="Number of copies for each mass point.", type=str)
inputArgumentsParser.add_argument('--isProductionRun', action='store_true', help="By default, this script does not submit the actual jobs and instead only prints the shell command that would have been called. Passing this switch will execute the commands.")
inputArguments = inputArgumentsParser.parse_args()

condor_directory = "{cA}/e2e_pi0_generation".format(cA=e2e_env.condor_work_area_root)
script_directory = "sh_condor_wrappers"
script_name = "generate_pi0.sh"
template_directory = "{ecb}/src/Configuration/GenProduction/python/Guns".format(ecb=e2e_env.e2e_cmssw_base)

mass_points = {
    "100MeV": 0.1,
    "200MeV": 0.2,
    "300MeV": 0.3,
    "500MeV": 0.5,
    "1GeV": 1.0
}

# Make sure all tarballs are up to date
e2e_common.update_and_upload_e2e_tarballs()

# Make condor folder if it doesn't exist
subprocess.check_call("mkdir -p {cd}".format(cd=condor_directory), executable="/bin/bash", shell=True)

# Copy script over to condor folder
subprocess.check_call("cp -u {sd}/{sn} {cd}/.".format(sd=script_directory, sn=script_name, cd=condor_directory), executable="/bin/bash", shell=True)

# First pass to create all new needed cfgs
for mass_point_title in mass_points:
    mass = mass_points[mass_point_title]
    create_cfg_command = "cd {td} && sed \"s|FixedMass = cms.double(FIXEDMASS)|FixedMass = cms.double({m:.3f})|\" pi0_back_to_back_template_cfg.py > pi0_back_to_back_{mpt}_cfg.py 2>&1".format(m=mass, td=template_directory, mpt=mass_point_title)
    subprocess.check_call(create_cfg_command, executable="/bin/bash", shell=True)

# Second pass to submit jobs
for mass_point_title in mass_points:
    mass = mass_points[mass_point_title]
    for copy_index in range(inputArguments.nCopiesPerMassPoint):
        processIdentifier = "generate_pi0_{t}_copy{i}".format(t=mass_point_title, i=copy_index)
        filesToTransfer = [e2e_env.x509Proxy, "{er}/sh_snippets/setup_environment_remote.sh".format(er=e2e_env.e2e_root)]
        jdlInterface = tmJDLInterface.tmJDLInterface(processName=processIdentifier, scriptPath=script_name, outputDirectoryRelativePath=condor_directory)
        jdlInterface.addFilesToTransferFromList(filesToTransfer)
        jdlInterface.addScriptArgument("pi0_back_to_back_{mpt}_cfg.py".format(mpt=mass_point_title)) # Argument 1: name of cfg
        jdlInterface.addScriptArgument(str(inputArguments.nEvtsPerJob)) # Argument 2: nEvts
        jdlInterface.addScriptArgument("copy{i}".format(i=copy_index)) # Argument 3: identifier
        jdlInterface.addScriptArgument("{ep}/{eer}/genAOD/pi0".format(ep=e2e_env.eos_prefix, eer=e2e_env.e2e_eos_root)) # Argument 4: output EOS directory with prefix for xrdcp
        if (e2e_env.habitat == "lxplus"):
            jdlInterface.setFlavor("tomorrow")
        # # Write JDL
        jdlInterface.makeExplicitMemoryRequest(3500) # gen step requires about 2 GB of memory
        jdlInterface.writeToFile()
        submissionCommand = "cd {cd}/ && condor_submit {pI}.jdl && cd {er}".format(cd=condor_directory, pI=processIdentifier, er=e2e_env.e2e_root)
        if (inputArguments.isProductionRun):
            subprocess.check_call(submissionCommand, executable="/bin/bash", shell=True)
            print ("Submitted.")
        else:
            print("Not submitting because isProductionRun flag was not set:")
            print(submissionCommand)

print("All done!")
