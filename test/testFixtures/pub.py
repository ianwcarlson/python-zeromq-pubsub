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

publisher = zeroMQInterface.ZeroMQPublisher()
publisher.importProcessConfig(os.path.join(scriptDir,'appNetworkConfig2.py'), sys.argv[1])

print('sending ' + str(appNetworkConfig.NUM_TEST_MSGS) + ' messages')
count = 0

basicMsg = {
	'count': count
}
time.sleep(2)
while(True):
	if (basicMsg['count'] > appNetworkConfig.NUM_TEST_MSGS):
		break

	#print ('sending: ' + str(basicMsg))
	publisher.send('fancy', basicMsg)
	basicMsg['count'] += 1

