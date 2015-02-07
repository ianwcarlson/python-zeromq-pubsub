"""
.. module:: processManager
    :synopsis: starts and stops all the processes
"""

import os
import sys
import subprocess
import time

scriptDir=os.path.dirname(os.path.realpath(__file__))
sys.path.append(scriptDir)

import pdb

class ProcessManager():
    def __init__(self):
        """
        Constructor.  Initializes class variables.
        """
        self.processHandleList = []

    def getProcessList(self):
        """
        Gets current list.  Mainly used for testing.
        :returns: list
        """ 
        return self.processHandleList

    def addProcess(self, inProcessDict):
        """
        Add process executable to managed list

        :param inProcessDict: dictionary containing 'processName' and 'endPoint' \
        keys that correspond to the python file to run and the IP address of each
        node in the system respectively
        :type inProcessDict: dictionary
        :raises ValueError
        """
        if ('processName' in inProcessDict and 'endPoint' in inProcessDict):
            self.processHandleList.append(inProcessDict)
        else:
            raise ValueError("'processName' or 'endPoint' keys don't exist in input dictionary")
        

    def run(self):
        """
        Run all processes in process list.  This should evolve to be more responsive \
        to subprocess handling.  For now, this class assumes python processes but could \
        be extended to any executable if the permissions and sourced interpretor was \
        configured properly

        """
        # start processes
        for idx in range(len(self.processHandleList)):
            path = os.path.join(scriptDir,self.processHandleList[idx]['processName'])
            print ('opening process: ' + str(path))
            processHandleList.append(subprocess.Popen(['python3', path], stdout=True))

        # monitor processes to see if they're still aliveps
        while(True):
            if (len(self.processHandleList) == 0):
                break

            for idx in range(len(self.processHandleList)):
                if (self.processHandleList[idx].poll() != None):
                    print('process done')
                    # only pop one at a time because doing so screws up indexing
                    self.processHandleList.pop(idx)
                    break

            time.sleep(0.1)
