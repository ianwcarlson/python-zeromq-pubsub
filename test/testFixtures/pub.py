"""
.. module:: sub
    :synopsis: subscriber
"""

import os
import sys
scriptDir=os.path.dirname(os.path.realpath(__file__))
import appNetworkConfig
sys.path.append(os.path.join(scriptDir,'..','..','src'))
import processNode
import time
import pdb
import loggerMQ
import logMessageAdapter

processNode = processNode.ProcessNode('appNetworkConfig3.py', sys.argv[1])

count = 0
basicMsg = {'count': count}
time.sleep(2)
while(True):
	if (basicMsg['count'] > appNetworkConfig.NUM_TEST_MSGS):
		break

	processNode.send('fancy', basicMsg)
	#logMessage = logAdapter.genLogMessage(logLevel=3, message=basicMsg)
	processNode.log(logLevel=3, message=basicMsg)
	basicMsg['count'] += 1

