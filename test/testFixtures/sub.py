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

processNodeObj = processNode.ProcessNode(os.path.join(scriptDir,'appNetworkConfig3.json'), sys.argv[1])

done = False
while(not(done)):
	response = processNodeObj.receive()
	for item in response:
		processNodeObj.log(logLevel=0, message=item)
		if (response[0]['contents']['count'] >= testConstants.NUM_TEST_MSGS):
			processNodeObj.log(logLevel=1, message='Done processing')
			processNodeObj.send('proc', {'action': 'stop'})
			done = True
			break

