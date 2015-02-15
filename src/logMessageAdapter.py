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
        self.pubID = pubID

    def genLogMessage(self, logLevel=0, message=''):
        msgDict = {}
        msgDict['pubID'] = self.pubID
        msgDict['logLevel'] = logLevel
        msgDict['message'] = message
        return msgDict
