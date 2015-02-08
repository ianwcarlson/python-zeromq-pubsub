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
import processManager
sys.path.append(os.path.join(scriptDir,'testFixtures'))
import appNetworkConfig



class TestZeroMQInterface(unittest.TestCase):
	def setUp(self):
		self.processManager = processManager.ProcessManager()
		newProcess = {
			'processName': os.path.join(scriptDir,'testFixtures','pub.py'),
			'endPoint': appNetworkConfig.PUB_ENDPOINT_ADDR
		}
		self.processManager.addProcess(newProcess)
		newProcess = {
			'processName': os.path.join(scriptDir,'testFixtures','sub.py'),
			'endPoint': appNetworkConfig.SUB_ENDPOINT_ADDR
		}
		#self.processManager.addProcess(newProcess)
		#self.publisher = zeroMQInterface.zeroMQPublisher(appNetworkConfig.PUB_ENDPOINT_ADDR)
		self.subscriber = zeroMQInterface.ZeroMQSubscriber()
		self.subscriber.connectSubscriber(appNetworkConfig.PUB_ENDPOINT_ADDR)
		self.subscriber.subscribeToTopic('fancy')


	def test_send_basic_message(self):
		self.processManager.run()

		time.sleep(2)
		count = 0
		stallCnt = 0
		while(True):
			if (stallCnt = 100000):
				break
				
			response = self.subscriber.receive()
			if (len(response)>0):
				#print ('response: ' + str(response))
				responseCount = response[0]['contents']['count']
				self.assertEqual(responseCount, count)
				count += 1
				if (responseCount >= 10000):
					break
			else:
				stallCnt += 1
			time.sleep(0.000001)




if __name__ == '__main__':
	unittest.main()