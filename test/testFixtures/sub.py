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

processNodeObj = processNode.ProcessNode('appNetworkConfig3.py', sys.argv[1])

time.sleep(0.001)
while(True):
	response = processNodeObj.receive()
	for item in response:
		processNodeObj.log(logLevel=1, message=item)
		if (response[0]['contents']['count'] >= appNetworkConfig.NUM_TEST_MSGS):
			processNodeObj.send('proc', {'action': 'stop'})
			break

	
	#time.sleep(0.0001)