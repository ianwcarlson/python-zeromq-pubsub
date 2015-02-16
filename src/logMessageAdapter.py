"""
.. module:: logMessageAdapter
    :synopsis: Small adapter class to help reinforce log message format
"""

import os
import sys
scriptDir=os.path.dirname(os.path.realpath(__file__))
sys.path.append(scriptDir)

class LogMessageAdapter:
    def __init__(self, pubID=os.path.realpath(__file__)):
        """
        Constructor for adapter class
        :param pubID: publisher name
        :type pubID: str  
        """
        self.pubID = pubID

    def genLogMessage(self, logLevel=0, message=''):
        """
        Construct a dictionary with the correct format for the logger to parse
        :param logLevel: logging level of the message (0-4)
        :type logLevel: int 
        :param message: message to be sent
        :type message: str
        """
        msgDict = {}
        msgDict['pubID'] = self.pubID
        msgDict['logLevel'] = logLevel
        msgDict['message'] = message
        return msgDict
