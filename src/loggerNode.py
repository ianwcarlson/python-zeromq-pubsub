"""
.. module:: loggerMQ
    :synopsis: Receives log messages from ZeroMQ publishers and uses Python logger class.
    Having trouble getting the logger to work in Docker containers, probably because the
    Unix logging service is not actually running
"""

import os
import sys
scriptDir=os.path.dirname(os.path.realpath(__file__))
sys.path.append(scriptDir)
import processNodeUtils as utils
import processNode
import pdb
import logging
import time

class Logger():
    def __init__(self, appNetworkConfig, logProcessName):
        """
        Constructor.  Will use local time for the file name by default.
        :param logFileName: file name to use for logging.
        :type logFileName: str
        """
        self.processNode = processNode.ProcessNode(appNetworkConfig, logProcessName)

    def run(self):
        """
        Main run function that will loop forever.  Calls the log function based on log level.
        """
        done = False
        while(not(done)):
            responseListDict = self.processNode.receive()
            for itemDict in responseListDict:
                if (itemDict['topic']=='proc'):
                    if (itemDict['contents']['action'] == 'stop'):
                        done = True
                        break

                logContentsDict = itemDict['contents']
                logLevel = logContentsDict['logLevel']
                logString = logContentsDict['pubID'] + ' ' + str(logContentsDict['message'])
                if (logLevel >= self.fileLogLevel or logLevel >= self.stdoutLogLevel):
                    fullLogString = utils.getDateTimeWithSpacesAndPrecision() + ' ' + \
                    utils.convLogLevelNumToString(logLevel) + ' ' + \
                    logString
                    if (logLevel >= self.fileLogLevel):
                        self.logFile.write(fullLogString + '\n')
                    if (logLevel >= self.stdoutLogLevel):
                        print(fullLogString)

    def setLogConfig(self, logFileName=os.path.join('logs',time.strftime('%d_%b_%Y_%H:%M:%S_LT', time.localtime())), 
        fileLogLevel=0, stdoutLogLevel=0):
        """
        Set the logger configuration.  Will create a new 'logs' subfolder if necessary.
        :param logFileName: file name to use for logger
        :type logFileName: str
        """
        print('Log directory at ' + str(logFileName)) ()
        try:
            os.mkdir(os.path.dirname(logFileName))
            print ('make dir at ' + logFileName)
        except:
            # do nothing for now
            print('Unable to make log directory at ' + str(logFileName))

        self.fileLogLevel = fileLogLevel
        self.stdoutLogLevel = stdoutLogLevel
        fullLogFileName = logFileName + '_' + utils.getDateTimeNoSpaces() + '.log'
        self.logFile = open(fullLogFileName, 'w')

    def cleanUp(self):
        self.logFile.close()
