
# names of the diagnostics
diagnostics = ['processExit']

# Location of infoli files
sim_dump_location = '/shared/apostolis/brain/'

# Safe location to keep backup files
safe_location = '/home/apostolis/bak/'

# rccerun path
rccerun_path = '/shared/apostolis/brain/rccerun'

# Infoli kill script path - RELATIVE TO RCCERUN
killfoli_path = '../killfoli'

# injector input files
processExitInjectorFile = sim_dump_location + 'injectors/procexitjector.txt'

# True if running on a development environment rather than the SCC
devel = False

# max number of elements to utilize for the MTTF estimation
moving_avg_N = 50

# if False, only DUE checkpoints will be used.
use_SDC_checkpoints = True

## also these lines where here in the source folder of SCC
# Checkpointing latency for the target application - in seconds
#latency = 0.23

#Checkpoint interval optimization precision - selected intervals will be divisible by:
#prec_interv = 100
