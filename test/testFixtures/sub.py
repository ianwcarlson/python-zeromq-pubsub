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
import loggerMQ

subscriber = zeroMQInterface.ZeroMQSubscriber()
subscriber.importProcessConfig(os.path.join(scriptDir,'appNetworkConfig3.py'), sys.argv[1])

publisher = zeroMQInterface.ZeroMQPublisher()
publisher.importProcessConfig(os.path.join(scriptDir,'appNetworkConfig3.py'), sys.argv[1])

logAdapter = loggerMQ.LogMessageAdapter(sys.argv[1])

time.sleep(0.001)
while(True):
	response = subscriber.receive()
	for item in response:
		publisher.send('log', logAdapter.genLogMessage(logLevel=3, message=item))
		if (response[0]['contents']['count'] >= appNetworkConfig.NUM_TEST_MSGS):
			publisher.send('proc', {'action': 'stop'})
			break

	
	#time.sleep(0.0001)