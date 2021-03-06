#!/usr/bin/env python

from __future__ import print_function, division

import os, sys, subprocess, argparse
import e2e_env, e2e_common, e2e_settings

DEFAULT_OUTPUT_FOLDER = "{ear}/visuals".format(ear=e2e_env.e2e_analysis_root)

inputArgumentsParser = argparse.ArgumentParser(description='Create visualizations for a number of events at various mass points.')
inputArgumentsParser.add_argument('--outputFolder', default=DEFAULT_OUTPUT_FOLDER, help="Path to output directory in which to store visualizations.")
inputArgumentsParser.add_argument('--debugMode', action="store_true", help="Only creates one example visualization, useful for debugging.")
inputArguments = inputArgumentsParser.parse_args()

settings = e2e_settings.Settings("settings.json")

output_folder = inputArguments.outputFolder
if ((output_folder == DEFAULT_OUTPUT_FOLDER) and (inputArguments.debugMode)): output_folder += "_debug"

# Make output folder if it doesn't exist
subprocess.check_call("mkdir -p {o}".format(o=output_folder), executable="/bin/bash", shell=True)

# Make sure target tmp folder exists in scratch area
subprocess.check_call("mkdir -p {d}/e2e_visuals".format(d=e2e_env.scratch_area), executable="/bin/bash", shell=True)

# Photon images not created yet due to possible problems with the preselection

# Create pion images
mass_points = settings.values_["generate_pi0"]["mass_points"]
mass_points_to_loop_over = mass_points
if (inputArguments.debugMode): mass_points_to_loop_over = [settings.values_["visualizations"]["debugMassPointTitle"]]
clone_index_range = range(1, 1+settings.values_["visualizations"]["nCopiesPerMassPoint"])
if (inputArguments.debugMode): clone_index_range = [1]
for mass_point_title in mass_points_to_loop_over:
    mass = mass_points[mass_point_title]
    for clone_index in clone_index_range:
        # Copy file to scratch area
        subprocess.check_call("xrdcp --nopbar --verbose --force --path {ep}/{eer}/genAOD_pq/pi0/converted_{mpt}_{i}.parquet.0 {d}/e2e_visuals/converted_{mpt}_{i}.parquet.0".format(ep=e2e_env.eos_prefix, eer=e2e_env.e2e_eos_root, mpt=mass_point_title, i=clone_index, d=e2e_env.scratch_area), executable="/bin/bash", shell=True)
        # Run wrapper script
        subprocess.check_call("{er}/scripts/create_visualization_from_pq_sh_wrapper.sh {d}/e2e_visuals/converted_{mpt}_{i}.parquet.0 {o} {ofn}".format(er=e2e_env.e2e_root, d=e2e_env.scratch_area, mpt=mass_point_title, i=clone_index, o=output_folder, ofn="visualization_{mpt}_{i}.pdf".format(mpt=mass_point_title, i=clone_index)), executable="/bin/bash", shell=True)
        # Clean up scratch area
        subprocess.check_call("rm -f {d}/e2e_visuals/converted_{mpt}_{i}.parquet.0".format(mpt=mass_point_title, i=clone_index, d=e2e_env.scratch_area), executable="/bin/bash", shell=True)

print("All done!")
