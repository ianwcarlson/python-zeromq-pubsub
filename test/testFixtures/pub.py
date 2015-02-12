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

print('sending ' + str(appNetworkConfig.NUM_TEST_MSGS) + ' messages')
count = 0
publisher = zeroMQInterface.ZeroMQPublisher(appNetworkConfig.PUB_ENDPOINT_ADDR)
basicMsg = {
	'count': count
}
time.sleep(2)
while(True):
	if (basicMsg['count'] > appNetworkConfig.NUM_TEST_MSGS):
		break

	publisher.send('fancy', basicMsg)
	basicMsg['count'] += 1

