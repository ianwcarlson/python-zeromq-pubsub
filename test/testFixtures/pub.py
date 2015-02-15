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

publisher = zeroMQInterface.ZeroMQPublisher()
publisher.importProcessConfig(os.path.join(scriptDir,'appNetworkConfig3.py'), sys.argv[1])

logAdapter = logMessageAdapter.LogMessageAdapter(sys.argv[1])

print('Sending ' + str(appNetworkConfig.NUM_TEST_MSGS) + ' messages')

count = 0
basicMsg = {'count': count}
time.sleep(2)
while(True):
	if (basicMsg['count'] > appNetworkConfig.NUM_TEST_MSGS):
		break

	publisher.send('fancy', basicMsg)
	logMessage = logAdapter.genLogMessage(logLevel=3, message=basicMsg)
	publisher.send('log', logMessage)
	basicMsg['count'] += 1

