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
scriptDir=os.path.dirname(os.path.realpath(__file__))
sys.path.append(scriptDir)
sys.path.append(os.path.join(scriptDir,'..','src'))
import zeroMQInterface
import processManager


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

		self.subscriber = zeroMQInterface.ZeroMQSubscriber()
		self.configPath = os.path.join(scriptDir,'testFixtures','appNetworkConfig2.py')

	def _testImportProcessConfig(self):
		configPath = self.configPath
		subPath = os.path.join(scriptDir,'testFixtures','sub.py')
		self.subscriber.importProcessConfig(configPath, 'subscriber1')

		configPath = os.path.join(scriptDir,'testFixtures','badNetworkConfig1.py')	
		self.assertRaises(ValueError, self.subscriber.importProcessConfig, configPath, subPath)

		configPath = os.path.join(scriptDir,'testFixtures','badNetworkConfig3.py')	
		self.assertRaises(ValueError, self.subscriber.importProcessConfig, configPath, subPath)

		badSubPath = os.path.join(scriptDir,'testFixtures','sub5.py')
		self.assertRaises(ValueError, self.subscriber.importProcessConfig, configPath, badSubPath)

		self.publisher = zeroMQInterface.ZeroMQPublisher()
		pubPath = os.path.join(scriptDir,'testFixtures','pub.py')
		self.publisher.importProcessConfig(configPath, pubPath)

		badPubPath = os.path.join(scriptDir,'testFixtures','pub5.py')
		self.assertRaises(ValueError, self.publisher.importProcessConfig, configPath, badPubPath)

	def _testSendBasicMessage(self):
		subprocess.Popen([
			'python3', os.path.join(scriptDir,'testFixtures','pub.py'), 'publisher'],
			stdout=True)
		self.subscriber.importProcessConfig(self.configPath, 'subscriber2')

		time.sleep(4)
		count = 0
		stallCnt = 0
		statusPrinter = StatusPrinter(1000)
		print ('Checking each message...')
		while(True):
			if (stallCnt == 100):
				print ('Test stalled out')
				self.assertTrue(False)
				break

			response = self.subscriber.receive()
			#print('response: ' + str(response))
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