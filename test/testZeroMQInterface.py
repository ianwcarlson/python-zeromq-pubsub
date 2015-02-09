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

class StatusPrinter():
	def __init__(self, printCount):
		self.counter = 0
		self.printCount = printCount

	def incrementCounter(self):
		if (self.counter%self.printCount==0):
			sys.stdout.write('.')
		self.counter += 1

	def resetCounter(self):
		self.counter = 0
		print('.')

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
		self.subscriber = zeroMQInterface.ZeroMQSubscriber()
		self.subscriber.connectSubscriber(appNetworkConfig.PUB_ENDPOINT_ADDR)
		self.subscriber.subscribeToTopic('fancy')


	def test_send_basic_message(self):
		self.processManager.run()

		time.sleep(2)
		count = 0
		stallCnt = 0
		statusPrinter = StatusPrinter(1000)
		print ('Checking each message...')
		while(True):
			if (stallCnt == 100):
				print ('test stalled out')
				break

			response = self.subscriber.receive()
			if (len(response)>0):
				statusPrinter.incrementCounter()
				responseCount = response[0]['contents']['count']
				self.assertEqual(responseCount, count)
				count += 1
				if (responseCount >= appNetworkConfig.NUM_TEST_MSGS):
					break
			else:
				stallCnt += 1


if __name__ == '__main__':
	unittest.main()