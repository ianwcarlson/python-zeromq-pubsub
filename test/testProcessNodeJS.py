"""
.. module:: testZeroMQInterface
	:synopsis: tests the zeroMQInterface module
"""

import os
import sys
import unittest
import pdb
import time
import subprocess
import signal
scriptDir=os.path.dirname(os.path.realpath(__file__))
sys.path.append(scriptDir)
sys.path.append(os.path.join(scriptDir,'..','src'))
import zeroMQInterface
import processManager
sys.path.append(os.path.join(scriptDir,'testFixtures'))
import mockPubSub

class TestZeroMQInterface(unittest.TestCase):
	def setUp(self):
		self.configPath = os.path.join(scriptDir,'testFixtures','appNetworkConfig5.json')
		self.publisher = mockPubSub.MockPublisher(self.configPath, 'Pub')
		self.subscriber = mockPubSub.MockSubscriber(self.configPath, 'Sub')

	def testSendBasicMessage(self):
		testModulePath = os.path.join(scriptDir,'testFixtures','jsProcessNode.js')
		processHandle = subprocess.Popen(['node', testModulePath, 'NodeUnderTest', 
			self.configPath], stdout=True)

		time.sleep(1)

		self.publisher.loadMsgQueue([{
			'topic': 'toNode',
			'message': 'untouched'
		}])
		self.publisher.run()

		time.sleep(0.5)

		self.subscriber.runOnce()
		responseList = self.subscriber.getResponseList()

		self.assertEqual(responseList[0]['topic'], 'fromNode');
		self.assertEqual(responseList[0]['contents'], 'untouched');
		os.kill(processHandle.pid, signal.SIGTERM)

if __name__ == '__main__':
	unittest.main()