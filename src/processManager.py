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
import utils
import pdb

class ProcessManager():
    def __init__(self):
        """
        Constructor.  Initializes class variables.
        """
        self.processHandleList = []
        self.processInputList = []

    def getProcessList(self):
        """
        Gets current list.  Mainly used for testing to check accessor.
        :returns: list
        """ 
        return self.processInputList

    def getProcessStatusList(self):
        """
        Gets process status list. Need to further refine this to be more useful.
        :returns: list of type subprocess.Popen
        """ 
        return self.processHandleList

    def addProcess(self, inProcessDict):
        """
        Add process executable to managed list

        :param inProcessDict: dictionary containing 'processName' and 'endPoint' 
        keys that correspond to the python file to run and the IP address of each
        node in the system respectively
        :type inProcessDict: dictionary
        :raises ValueError
        """
        if ('processPath' in inProcessDict and 'endPoint' in inProcessDict):
            self.processInputList.append(inProcessDict)
        else:
            raise ValueError("'processName' or 'endPoint' keys don't exist in input dictionary")

    def importProcessConfig(self, fullConfigPath):
        """
        Imports process configuration file and tries to add all the processes to the master
        list (to be used for spinning up each process).
        :param fullConfigPath: full file path to process config file
        :type fullConfigPath: str
        :raises: ValueError
        """
        self.fullConfigPath = fullConfigPath
        masterProcessConfig = utils.importConfigJson(fullConfigPath)
        processList = masterProcessConfig['processList']

        for process in processList:
            #if ('processPath' in process):
            self.processInputList.append(process)
            #else:
            #    raise ValueError("'processPath' not provided in config file")

    def getInterpreter(self, processPath):
        '''
        Determines which interpretor to run
        '''
        interpreter = 'unknown'
        fileName, fileExtension = os.path.splitext(processPath)
        if (fileExtension == '.py'):
            interpreter = 'python3'
        elif (fileExtension == '.js'):
            interpreter = 'node'

        return interpreter
      
    def run(self):
        """
        Run all processes in process list.  This should evolve to be more responsive 
        to subprocess handling.  For now, this class assumes python processes but could 
        be extended to any executable if the permissions and sourced interpretor was 
        configured properly

        """
        # start processes
        for idx in range(len(self.processInputList)):
            path = os.path.join(scriptDir,self.processInputList[idx]['processPath'])
            interpreter = self.getInterpreter(path)
            print ('Starting process: ' + str(path) + ' ' + self.processInputList[idx]['processName'])
            self.processHandleList.append(subprocess.Popen([
                interpreter, path, self.processInputList[idx]['processName'], self.fullConfigPath], 
                stdout=True))

        # monitor processes to see if they're still alive
        while(True):
            if (len(self.processHandleList) == 0):
                break

            for idx in range(len(self.processHandleList)):
                if (self.processHandleList[idx].poll() != None):
                    print('Process done')
                    # only pop one at a time because doing so screws up indexing
                    self.processHandleList.pop(idx)
                    break

            time.sleep(0.01)
