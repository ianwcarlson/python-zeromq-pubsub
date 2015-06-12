"""
.. module:: processManager
    :synopsis: starts and stops all the processes
"""

import os
import sys
import subprocess
import time
import signal
scriptDir=os.path.dirname(os.path.realpath(__file__))
sys.path.append(scriptDir)
import processNode
import processNodeUtils
import pdb

# reserved name
PROCESSMANAGERNAME = "processManager"

class ProcessManager():
    def __init__(self):
        """
        Constructor.  Initializes class variables.
        """
        self.processHandleList = []
        self.processInputList = []
        self.fullConfigPath = ''

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
        self.processNode = processNode.ProcessNode(fullConfigPath, PROCESSMANAGERNAME)
        masterProcessConfig = processNodeUtils.importConfigJson(fullConfigPath)
        processList = masterProcessConfig['processList']

        for process in processList:
            #if ('processPath' in process):
            if (process['processName'] != PROCESSMANAGERNAME):
                self.processInputList.append(process)
            #else:
            #    raise ValueError("'processPath' not provided in config file")
            #    
    def startProcess(self, processDict):
        path = os.path.join(scriptDir,processDict['processPath'])
        interpreter = processNodeUtils.getInterpreter(path)
        logMsg = 'Starting process: ' + str(path) + ' ' + processDict['processName']
        print (logMsg)
        self.processNode.log(logLevel=1, message=logMsg)
        self.processHandleList.append(subprocess.Popen([
            interpreter, path, processDict['processName'], self.fullConfigPath], 
            stdout=True))
        
    def run(self, autoRestart=False):
        """
        Run all processes in process list.  This should evolve to be more responsive 
        to subprocess handling.  For now, this class assumes python processes but could 
        be extended to any executable if the permissions and sourced interpretor was 
        configured properly
        """
        # start processes
        for idx in range(len(self.processInputList)):
            self.startProcess(self.processInputList[idx])

        # monitor processes to see if they're still alive
        while(True):
            try:
                if (len(self.processHandleList) == 0):
                    break
                idx = 0
                while (idx < len(self.processHandleList)):
                    returnValue = self.processHandleList[idx].poll()
                    if (returnValue != None):
                        stoppedProcessDict = self.processInputList[idx]
                        logMsg = self.processInputList[idx]['processName'] + \
                            ' process done with return value of ' + str(returnValue)
                        print(logMsg)
                        self.processNode.log(logLevel=3, message=logMsg)
                        # only pop one at a time because doing so screws up indexing
                        self.processInputList.pop(idx)
                        self.processHandleList.pop(idx)
                        if (returnValue != 0 and autoRestart):
                            self.processInputList.append(stoppedProcessDict)
                            self.startProcess(stoppedProcessDict)
                        break
                    idx += 1
                time.sleep(1)
            except:
                print ('Exception Occurred.  KILLING ALL PROCESSES.')
                # if ctrl+c or exception occurs, ensure all processes killed
                for process in self.processHandleList:
                    os.kill(process.pid, signal.SIGTERM)

                sys.exit(1)