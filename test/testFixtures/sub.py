"""
.. module:: sub
    :synopsis: subscriber
"""

import os
import sys
scriptDir=os.path.dirname(os.path.realpath(__file__))
import appNetworkConfig
sys.path.append(os.path.join(scriptDir,'..','..','src'))
import zeroMQInterface
import time
import pdb

subscriber = zeroMQInterface.ZeroMQSubscriber()
subscriber.connectSubscriber(appNetworkConfig.PUB_ENDPOINT_ADDR)
subscriber.subscribeToTopic('fancy')
time.sleep(0.001)
while(True):
	response = subscriber.receive()
	if (len(response)>0):
		print ('response: ' + str(response))
		if (response[0]['contents']['count'] >= 100):
			break

	
	#time.sleep(0.0001)