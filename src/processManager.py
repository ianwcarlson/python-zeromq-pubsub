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
import toZeroMQ
import appConfigConstants

import pdb

def run():

    processHandleList = []

    # start processes
    for idx in range(len(appConfigConstants.processList)):
        path = os.path.join(scriptDir,appConfigConstants.processList[idx]['processName'])
        print ('opening process: ' + str(path))
        processHandleList.append(subprocess.Popen(['python3', path], stdout=True))

    # monitor processes to see if they're still aliveps
    while(True):
        if (len(processHandleList) == 0):
            break

        for idx in range(len(processHandleList)):
            if (processHandleList[idx].poll() != None):
                print('process done')
                # only pop one at a time because doing so screws up indexing
                processHandleList.pop(idx)
                break

        time.sleep(0.1)

run()