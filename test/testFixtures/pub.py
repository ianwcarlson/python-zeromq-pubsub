"""
.. module:: sub
    :synopsis: subscriber
"""

import os
import sys
scriptDir=os.path.dirname(os.path.realpath(__file__))
import testConstants
sys.path.append(os.path.join(scriptDir,'..','..','src'))
import processNode
import time
import pdb
import loggerNode
import logMessageAdapter

processNode = processNode.ProcessNode(os.path.join(scriptDir,'appNetworkConfig3.json'), sys.argv[1])

count = 0
basicMsg = {'count': count}
while(True):
	if (basicMsg['count'] > testConstants.NUM_TEST_MSGS):
		break

	processNode.send('fancy', basicMsg)
	processNode.log(logLevel=0, message=basicMsg)
	basicMsg['count'] += 1

processNode.log(logLevel=1, message='Done processing')

