from __future__ import print_function, division

import e2e_env

def update_and_upload_e2e_tarballs():
    # E2E root folder
    e2e_env.execute_in_env(commandToRun="cd {e2er}/.. && ./upload_tarball_to_e2e_eos_area.sh".format(e2er=e2e_env.e2e_root))
    # CMSSW
    e2e_env.execute_in_env(commandToRun="cd {e2eCB}/.. && ./upload_tarball_to_e2e_eos_area.sh".format(e2eCB=e2e_env.e2e_cmssw_base))
    # tmUtils
    e2e_env.execute_in_env(commandToRun="cd {tUP} && ./update_tmUtilsTarball.sh && ./upload_tmUtils_tarball_to_e2e_eos_area.sh".format(tUP=e2e_env.tmUtils_parent))
