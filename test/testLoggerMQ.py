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
import shutil
import glob
scriptDir=os.path.dirname(os.path.realpath(__file__))
sys.path.append(scriptDir)
sys.path.append(os.path.join(scriptDir,'..','src'))
import zeroMQInterface
import processManager
sys.path.append(os.path.join(scriptDir,'testFixtures'))
import testConstants

logsDir = os.path.join(scriptDir,'testFixtures','logs')

class TestZeroLoggerMQ(unittest.TestCase):
	def setUp(self):
		try:
			shutil.rmtree(logsDir)
		except:
			print('')
			
		self.processManager = processManager.ProcessManager()	
		self.processManager.importProcessConfig(os.path.join(scriptDir,'testFixtures','appNetworkConfig3.json'))

	def testProcessManager(self):
		self.processManager.run()
		done = False
		stallCnt = 50
		while(not(done)):
			logList = glob.glob(os.path.join(logsDir,'*.log'))
			if (len(logList)>0):
				for idx in range(testConstants.NUM_TEST_MSGS):
					self._scanFileForToken(logList[0], "'count': " + str(idx))
					self._scanFileForToken(logList[0], "'contents': {'count': " + str(idx))
				done = True

			time.sleep(0.1)

	# open and closing file is slower but ok for now
	def _scanFileForToken(self, filePath, searchToken):
		file = open(filePath, 'r')
		fileContents = file.read()
		foundIdx = fileContents.find(searchToken)
		self.assertNotEqual(foundIdx, -1)
		file.close()

if __name__ == '__main__':
	unittest.main()