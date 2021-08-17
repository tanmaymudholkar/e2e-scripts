from CRABClient.UserUtilities import config
config = config()

config.General.requestName = "gen_step"
config.General.workArea = "crab_workArea"

config.JobType.pluginName = "PrivateMC"
config.JobType.psetName = ""
config.JobType.maxMemoryMB = 3500

config.Data.outputPrimaryDataset = ""
config.Data.splitting = "EventBased"
config.Data.unitsPerJob = 10
NJOBS = 1
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.publication = False
config.Data.outLFNDirBase = ""
config.Site.storageSite = "T3_US_FNALLPC"
