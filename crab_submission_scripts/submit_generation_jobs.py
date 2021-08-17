#!/usr/bin/env python

from __future__ import print_function, division

import os, sys, subprocess, argparse
import e2e_env, e2e_common, e2e_settings

inputArgumentsParser = argparse.ArgumentParser(description='Submit photon generation jobs.')
inputArgumentsParser.add_argument('--genParticle', required=True, choices=["gamma", "pi0"], help="Type of particle to be generated.", type=str)
inputArgumentsParser.add_argument('--isProductionRun', action='store_true', help="By default, this script does not submit the actual crab jobs for production, only a dry run. Passing this switch will submit the job to production.")
inputArguments = inputArgumentsParser.parse_args()

settings = e2e_settings.Settings("settings.json")

# Copy crab cfg over to output folder
subprocess.check_call("cp -u {r}/cmssw_interface/crab_config_event_generation.py cached/.".format(r=e2e_env.e2e_root), executable="/bin/bash", shell=True)

# Make sure all tarballs are up to date
e2e_common.update_and_upload_e2e_tarballs()

# Step 1: generate required cfgs
command_generate_cfg = "cd {r}/cached &&".format(r=e2e_env.e2e_root)
command_generate_cfg += " cmsDriver.py"
cfg_path = "Configuration/GenProduction/python/Guns/{gp}_back_to_back_cfg.py".format(gp=inputArguments.genParticle)
command_generate_cfg += (" " + cfg_path)
command_generate_cfg += " --conditions 102X_upgrade2018_realistic_v15"
command_generate_cfg += " --mc"
command_generate_cfg += " --era Run2_2018"
command_generate_cfg += " --eventcontent AODSIM"
command_generate_cfg += " --runUnscheduled"
command_generate_cfg += " --step GEN,SIM,DIGI,L1,DIGI2RAW,HLT:@fake,RAW2DIGI,L1Reco,RECO"
command_generate_cfg += " --geometry DB:Extended"
command_generate_cfg += " --datatier GEN-SIM-DIGI-RAW-RECO"
command_generate_cfg += " --beamspot Realistic25ns13TeVEarly2018Collision"
command_generate_cfg += " --no_exec"
if (inputArguments.genParticle == "gamma"):
    command_to_run = command_generate_cfg
    command_to_run += " --python_filename gen_particle_gamma.py"
    e2e_env.execute_in_env(commandToRun=command_to_run, isDryRun=not(inputArguments.isProductionRun))
elif (inputArguments.genParticle == "pi0"):
    mass_points = settings.values_["generate_pi0"]["mass_points"]
    for mass_point_title in mass_points:
        mass = mass_points[mass_point_title]
        command_to_run = command_generate_cfg
        command_to_run += " --python_filename gen_particle_pi0_{t}.py".format(t=mass_point_title)
        command_to_run += " --customise_commands \"process.generator.PGunParameters.FixedMass={m:.3f}\"".format(m=mass)
        e2e_env.execute_in_env(commandToRun=command_to_run, isDryRun=not(inputArguments.isProductionRun))
else:
    sys.exit("ERROR: unsupported genParticle: {gp}".format(gp=inputArguments.genParticle))

# Step 2: Submit crab jobs
command_submit_crab_job = "cd {r}/cached &&".format(r=e2e_env.e2e_root)
command_submit_crab_job += " crab submit"
if (inputArguments.isProductionRun):
    command_submit_crab_job += " --wait"
else:
    command_submit_crab_job += " --dryrun"
command_submit_crab_job += " -c crab_config_event_generation.py"
# General.requestName=ntuplizer_10210_data_{did} General.workArea=crab_workArea_ntuplizer_10210_data_{did} JobType.psetName={p} Data.inputDataset={d} Data.unitsPerJob={uPJ} Data.lumiMask={lM} Data.outLFNDirBase={lDB} 
if (inputArguments.genParticle == "gamma"):
    command_to_run = command_submit_crab_job
    command_to_run += " General.requestName=generation_gamma"
    command_to_run += " General.workArea=crab_workArea_generation_gamma"
    command_to_run += " JobType.psetName=gen_particle_gamma.py"
    command_to_run += " Data.outputPrimaryDataset=gamma"
    command_to_run += " Data.unitsPerJob={u}".format(u=settings.values_["generate_gamma"]["nEvtsPerJob"])
    command_to_run += " Data.totalUnits={u}".format(u=(settings.values_["generate_gamma"]["nCopies"])*(settings.values_["generate_gamma"]["nEvtsPerJob"]))
    command_to_run += " Data.outLFNDirBase={l}".format(l="/store/user/tmudholk/genAOD/gamma/")
    e2e_env.execute_in_env(commandToRun=command_to_run, isDryRun=not(inputArguments.isProductionRun))
elif (inputArguments.genParticle == "pi0"):
    mass_points = settings.values_["generate_pi0"]["mass_points"]
    for mass_point_title in mass_points:
        mass = mass_points[mass_point_title]
        command_to_run = command_submit_crab_job
        command_to_run += " General.requestName=generation_pi0_{t}".format(t=mass_point_title)
        command_to_run += " General.workArea=crab_workArea_generation_pi0_{t}".format(t=mass_point_title)
        command_to_run += " JobType.psetName=gen_particle_pi0_{t}.py".format(t=mass_point_title)
        command_to_run += " Data.outputPrimaryDataset=pi0"
        command_to_run += " Data.unitsPerJob={u}".format(u=settings.values_["generate_pi0"]["nEvtsPerJob"])
        command_to_run += " Data.totalUnits={u}".format(u=(settings.values_["generate_pi0"]["nCopiesPerMassPoint"])*(settings.values_["generate_pi0"]["nEvtsPerJob"]))
        command_to_run += " Data.outLFNDirBase={l}".format(l="/store/user/tmudholk/genAOD/pi0/")
        e2e_env.execute_in_env(commandToRun=command_to_run, isDryRun=not(inputArguments.isProductionRun))
else:
    sys.exit("ERROR: unsupported genParticle: {gp}".format(gp=inputArguments.genParticle))

print("All done!")

# cmsDriver.py ${CFGPATH}/${CFG} --conditions ${GT} -n ${NEVTS} --mc --era ${ERA} --eventcontent ${EVTCONT} --runUnscheduled --step GEN,SIM,DIGI,L1,DIGI2RAW,HLT:@fake,RAW2DIGI,L1Reco,RECO --geometry DB:Extended --datatier GEN-SIM-DIGI-RAW-RECO --beamspot ${BEAM} --customise_commands "process.source.numberEventsInLuminosityBlock=cms.untracked.uint32(2000)\nprocess.RandomNumberGeneratorService.generator.initialSeed=${GENERATOR_SEED}" --fileout file:${OUTPUT_PREFIX}.root --python_filename ${OUTPUT_PREFIX}.py

# condor_directory = "{cA}/e2e_gamma_generation".format(cA=e2e_env.condor_work_area_root)
# script_directory = "sh_condor_wrappers"
# script_name = "generate_gamma.sh"

# # Make condor folder if it doesn't exist
# subprocess.check_call("mkdir -p {cd}".format(cd=condor_directory), executable="/bin/bash", shell=True)

# # Copy script over to condor folder
# subprocess.check_call("cp -u {sd}/{sn} {cd}/.".format(sd=script_directory, sn=script_name, cd=condor_directory), executable="/bin/bash", shell=True)

# # Make sure all tarballs are up to date
# e2e_common.update_and_upload_e2e_tarballs()

# # Create and submit jobs
# masked_seeds = None
# try:
#     masked_seeds = settings.values_["generate_gamma"]["masked_seeds"]
# except KeyError:
#     masked_seeds = []
# for copy_index in range(settings.values_["generate_gamma"]["nCopies"]):
#     processIdentifier = "generate_gamma_copy{i}".format(i=copy_index)
#     filesToTransfer = [e2e_env.x509Proxy, "{er}/sh_snippets/setup_environment_remote.sh".format(er=e2e_env.e2e_root)]
#     jdlInterface = tmJDLInterface.tmJDLInterface(processName=processIdentifier, scriptPath=script_name, outputDirectoryRelativePath=condor_directory)
#     jdlInterface.addFilesToTransferFromList(filesToTransfer)
#     jdlInterface.addScriptArgument(str(settings.values_["generate_gamma"]["nEvtsPerJob"])) # Argument 1: nEvts
#     jdlInterface.addScriptArgument("copy{i}".format(i=copy_index)) # Argument 2: identifier
#     jdlInterface.addScriptArgument("{ep}/{eer}/genAOD/gamma".format(ep=e2e_env.eos_prefix, eer=e2e_env.e2e_eos_root)) # Argument 3: output EOS directory with prefix for xrdcp
#     seed = 12345 + copy_index
#     if seed in masked_seeds:
#         new_seed = seed + settings.values_["generate_gamma"]["nCopies"]
#         print("Seed {s1} masked; trying {s2}".format(s1=seed, s2=new_seed))
#         seed = new_seed
#     jdlInterface.addScriptArgument("{s}".format(s=seed)) # Argument 4: random number generator seed
#     if (e2e_env.habitat == "lxplus"):
#         jdlInterface.setFlavor("tomorrow")
#     # # Write JDL
#     jdlInterface.makeExplicitMemoryRequest(3500) # gen step requires about 2 GB of memory
#     jdlInterface.writeToFile()
#     submissionCommand = "cd {cd}/ && condor_submit {pI}.jdl && cd {er}".format(cd=condor_directory, pI=processIdentifier, er=e2e_env.e2e_root)
#     if (inputArguments.isProductionRun):
#         subprocess.check_call(submissionCommand, executable="/bin/bash", shell=True)
#         print ("Submitted.")
#     else:
#         print("Not submitting because isProductionRun flag was not set:")
#         print(submissionCommand)

# print("All done!")
