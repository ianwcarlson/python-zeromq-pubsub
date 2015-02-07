"""
.. module:: testZeroMQInterface
	:synopsis: tests the zeroMQInterface module
"""

import os
import sys
import unittest
import pdb
import time
scriptDir=os.path.dirname(os.path.realpath(__file__))
sys.path.append(scriptDir)
sys.path.append(os.path.join(scriptDir,'..','src'))
import zeroMQInterface
sys.path.append(os.path.join(scriptDir,'testFixtures'))
import appNetworkConfig

TOPIC = 'fancyTopic'

class TestZeroMQInterface(unittest.TestCase):
	def setUp(self):
		self.publisher = zeroMQInterface.zeroMQPublisher(appNetworkConfig.PUB_ENDPOINT_ADDR)
		self.subscriber = zeroMQInterface.ZeroMQSubscriber()
		self.subscriber.connectSubscriber(appNetworkConfig.PUB_ENDPOINT_ADDR)
		self.subscriber.subscribeToTopic(TOPIC)

	def test_send_basic_message(self):
		basicMsg = {
			'message': 'I made it to the other side'
		}
		self.publisher.send(TOPIC, basicMsg)
		time.sleep(0.1)
		response = []

		response = self.subscriber.receive()
		pdb.set_trace()


if __name__ == '__main__':
	unittest.main()