"""
.. module:: loggerMQ
    :synopsis: Receives log messages from ZeroMQ publishers and uses Python logger class
"""

import os
import sys
scriptDir=os.path.dirname(os.path.realpath(__file__))
sys.path.append(scriptDir)
import zeroMQInterface
import pdb
import logging
import time

class Logger(zeroMQInterface.ZeroMQSubscriber):
    #def __init__(self, logFileName=os.path.join('logs',time.strftime('%d_%b_%Y_%H:%M:%S_LT', time.localtime()))):
    #    """
    #    Constructor.  Will use local time for the file name by default.
    #    :param logFileName: file name to use for logging.
    #    :type logFileName: str
    #    """

    #    self.setLogConfig(logFileName)

    def run(self):
        """
        Main run function that will loop forever.  Calls the log function based on log level.
        """
        done = False
        while(not(done)):
            responseListDict = self.receive()
            #print ('responseDict: ', responseListDict)
            for itemDict in responseListDict:
                if (itemDict['topic']=='proc'):
                    if (itemDict['contents']['action'] == 'stop'):
                        done = True
                        break

                logContentsDict = itemDict['contents']
                logLevel = logContentsDict['logLevel']
                logString = logContentsDict['pubID'] + ' ' + str(logContentsDict['message'])
                if (logLevel == 0):
                    logging.debug(logString)
                elif (logLevel == 1):
                    logging.info(logString)
                elif (logLevel == 2):
                    logging.warning(logString)
                elif (logLevel == 3):
                    logging.error(logString)
                elif (logLevel == 4):
                    logging.critical(logString)
                else:
                    logging.debug(logString)

    def setLogConfig(self, logFileName):
        """
        Set the logger configuration.  Will create a new 'logs' subfolder if necessary.
        :param logFileName: file name to use for logger
        :type logFileName: str
        """
        print ('logFileName: ' + logFileName)
        try:
            os.mkdir(os.path.dirname(logFileName))
            print ('make dir at ' + logFileName)
        except:
            # do nothing for now
            print('')

        logging.basicConfig(fileName=logFileName, filemode='w', format='%(asctime)s %(message)s', 
            level=logging.DEBUG)

class LogMessageAdapter:
    def __init__(self, pubID=os.path.realpath(__file__)):
        self.pubID = pubID

    def genLogMessage(self, logLevel=0, message=''):
        msgDict = {}
        msgDict['pubID'] = self.pubID
        msgDict['logLevel'] = logLevel
        msgDict['message'] = message
        return msgDict

#if __name__ == '__main__':
#
#    logger = Logger()
#    logger.run()
