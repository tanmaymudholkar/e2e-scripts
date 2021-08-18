#!/usr/bin/env python

from __future__ import print_function, division

import os, sys, subprocess, argparse
import e2e_env, e2e_common, e2e_settings

inputArgumentsParser = argparse.ArgumentParser(description='Submit generation jobs for various mass points.')
inputArgumentsParser.add_argument('--outputFolder', default="{ear}/deltaRPlots".format(ear=e2e_env.e2e_analysis_root), help="Path to output directory in which to store deltaR plots.")
inputArguments = inputArgumentsParser.parse_args()

settings = e2e_settings.Settings("settings.json")

mass_points = settings.values_["generate_pi0"]["mass_points"]

# Make output folder if it doesn't exist
subprocess.check_call("mkdir -p {o}".format(o=inputArguments.outputFolder), executable="/bin/bash", shell=True)

# Run "make"
subprocess.check_call("make", executable="/bin/bash", shell=True)

for mass_point_title in mass_points:
    mass = mass_points[mass_point_title]
    # Create file with list of input paths
    inputFilePaths_deltaR_minimalAnalyzer_path = "cpp_options_interface/inputFilePaths_deltaR_minimalAnalyzer_{mpt}.dat".format(mpt=mass_point_title)
    inputFilePaths_deltaR_minimalAnalyzer_handler = open(inputFilePaths_deltaR_minimalAnalyzer_path, 'w')
    for clone_index in range(1, 1+settings.values_["generate_pi0"]["nCopiesPerMassPoint"]):
        inputFilePaths_deltaR_minimalAnalyzer_handler.write("{ep}/{eer}/pi0_analysis/minimal/histograms_{mpt}_{i}.root\n".format(ep=e2e_env.eos_prefix, eer=e2e_env.e2e_eos_root, mpt=mass_point_title, i=clone_index))
    inputFilePaths_deltaR_minimalAnalyzer_handler.close()
    extract_command = "./bin/processDeltaRHistograms inputFilePaths={p} outputFolder={f} outputFileName=deltaR_{mpt}.pdf".format(p=inputFilePaths_deltaR_minimalAnalyzer_path, f=inputArguments.outputFolder, mpt=mass_point_title)
    subprocess.check_call(extract_command, executable="/bin/bash", shell=True)

print("All done!")
