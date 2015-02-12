"""
.. module:: loggerMQ
    :synopsis: Receives log messages from ZeroMQ publishers and uses Python logger class
"""

import os
import sys
scriptDir=os.path.dirname(os.path.realpath(__file__))
sys.path.append(scriptDir)
import toZeroMQ
import appConfigConstants

sys.path.append(os.path.join(scriptDir,'scripts','lib'))
import k9Mod
import pdb
import logging
import time

class Logger:
    def __init__(self, logFileName=os.path.join('logs',time.strftime('%d_%b_%Y_%H:%M:%S_LT', time.localtime()))):
        """
        Constructor.  Initializes logger class with subscriptions.  Will use local time for the file name by default.
        :param logFileName: file name to use for logging.
        :type logFileName: str
        """
        self.subscriber = toZeroMQ.ZeroMQSubscriber()
        self.subscriber.connectSubscriber(appConfigConstants.K9_HW_IF_ENDPOINT_ADDR)
        self.subscriber.subscribeToTopic('log')

        self.subscriber.connectSubscriber(appConfigConstants.SQLITE_DB_ENDPOINT_ADDR)
        self.subscriber.subscribeToTopic('log')   

        self.setLogConfig(logFileName)

    def run(self):
        """
        Main run function that will loop forever.  Calls the log function based on log level.
        """
        done = False
        while(not(done)):
            responseListDict = self.subscriber.receive()
            #print ('responseDict: ', responseListDict)
            for itemDict in responseListDict:
                logContentsDict = itemDict['contents']
                logLevel = logContentsDict['logLevel']
                logString = logContentsDict['pubID'] + ' ' + logContentsDict['message']
                if (logLevel == 0):
                    logger.debug(logString)
                elif (logLevel == 1):
                    logger.info(logString)
                elif (logLevel == 2):
                    logger.warning(logString)
                elif (logLevel == 3):
                    logger.error(logString)
                elif (logLevel == 4):
                    logger.critical(logString)
                else:
                    logger.debug(logString)

    def setLogConfig(self, logFileName):
        """
        Set the logger configuration.  Will create a new 'logs' subfolder if necessary.
        :param logFileName: file name to use for logger
        :type logFileName: str
        """
        try:
            os.mkdir(os.path.join(scriptDir,'logs'))
        except:
            # do nothing for now
            print('')

        logging.basicConfig(fileName=logFileName, format='%(asctime)s %(message)s')

class LogMessageAdapter:
    def __init__(self, pubID=os.path.realpath(__file__)):
        self.pubID = pubID

    def genLogMessage(self, logLevel=0, message=''):
        msgDict = {}
        msgDict['pubID'] = self.pubID
        msgDict['logLevel'] = self.logLevel
        msgDict['message'] = message
        return msgDict

if __name__ == '__main__':

    logger = Logger()
    logger.run()