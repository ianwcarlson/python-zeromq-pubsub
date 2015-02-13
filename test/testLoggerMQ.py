"""
.. module:: testZeroMQInterface
	:synopsis: tests the zeroMQInterface module
"""

import os
import sys
import unittest
import pdb
import time
import unittest
scriptDir=os.path.dirname(os.path.realpath(__file__))
sys.path.append(scriptDir)
sys.path.append(os.path.join(scriptDir,'..','src'))
import zeroMQInterface
import processManager
sys.path.append(os.path.join(scriptDir,'testFixtures'))
import appNetworkConfig

class TestZeroLoggerMQ(unittest.TestCase):
	def setUp(self):
		self.processManager = processManager.ProcessManager()	
		self.processManager.importProcessConfig(os.path.join(scriptDir,'testFixtures','appNetworkConfig3.py'))


	def testProcessManager(self):
		self.processManager.run()


if __name__ == '__main__':
	unittest.main()