import abc
import logging
from time import sleep, time
from subprocess import call, check_output
from config import sim_dump_location, safe_location, devel
import infoli_diagnostics
import sys
class countermeasure(object):
    ''' Countermeasure class '''
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def perform(self):
        return


''' defines an ordering among the different countermeasures, based on MTTR '''
countermeasure_enum = {
    'restartSimulation':0
}


def wait_for_cores(core_names, timeout):
    ''' Utility function that blocks until a set of cores is available
        or until the timeout is reached
    '''
    if devel:
        return True

    t0 = time()
    available_cores = 0

    while available_cores < len(core_names):
        status = check_output(['sccBoot', '-s'])

        if status[-11:-8] == "All":
            available_cores = 48
        elif status[-10:-8] == "No":
            available_cores = 0
        else:
            available_cores = int(status[-10:-8])

        if time() - t0 > timeout:
            logging.error("Timeout exceeded for %s cores", expected)
            return False
    sleep(10)
    status = check_output(['sccBoot', '-s'])
    print status
    return True


class restartSimulation(countermeasure):
    """ Restarts the simulation """
    __name__ = 'restartSimulation'

    def __init__(self, manager):
        self.manager = manager

    def perform(self):
        logging.info("performing the Restart Simulation countermeasure")
        print self.manager.checkpoints
        if any(isinstance(x, infoli_diagnostics.infoliOutputDivergence) for x in self.manager.failed_diagnostics()):   #infoli-specific
            # check if the SDC detection diagnostic has failed, and use the SDC checkpoint
            print sorted(self.manager.checkpoints)
            checkpoint = max(self.manager.checkpoints)
        else:
            checkpoint = max(self.manager.checkpoints)

        print("The mttr_values are:",self.manager.mttr_values)
        print("Calling dvfs: ")
        self.manager.dvfs.dvfsOperation(checkpoint)

        print "Restarting from step" + str(checkpoint)
        logging.info("Restarting from step " + str(checkpoint))

        with self.manager.lock:
            # Copy safe checkpoints
            #for i in range(self.manager.num_cores):
            #    call( ['cp', '-f', '-u', safe_location + str(checkpoint) + '/ckptFile%d.bin' %i, sim_dump_location])
            #    call( ['cp', '-f', '-u', safe_location + str(checkpoint) + '/InferiorOlive_Output%d.txt' %i, sim_dump_location])
            self.manager.rccerun([self.manager.restart_exec] + self.manager.exec_list[1:]) # use False as extra last argument to avoid piping stdout for diagnostics - useful for measurements
        logging.info("Restart Simulation countermeasure completed")
        return True
