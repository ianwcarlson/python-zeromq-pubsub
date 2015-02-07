"""
.. module:: testProcessManager
	:synopsis: tests the ProcessManager module/clas
"""

import os
import sys
import unittest
import pdb
import time
scriptDir=os.path.dirname(os.path.realpath(__file__))
sys.path.append(scriptDir)
sys.path.append(os.path.join(scriptDir,'..','src'))
import processManager


class TestProcessManager(unittest.TestCase):
	def setUp(self):
		self.processManager = processManager.ProcessManager()

	def _add_known_good_process1(self):
		newProcess = {
			'processName': os.path.join(scriptDir,'testFixtures','process1.py'),
			'endPoint': 'tcp://127.0.0.1:5556'
		}
		self.processManager.addProcess(newProcess)
		return newProcess

	def _add_known_good_process2(self):
		newProcess = {
			'processName': os.path.join(scriptDir,'testFixtures','process2.py'),
			'endPoint': 'tcp://127.0.0.1:5557'
		}
		self.processManager.addProcess(newProcess)
		return newProcess

	def test_add_good_process(self):
		newProcess = self._add_known_good_process1()
		getNewProcess = self.processManager.getProcessList()

		for key in newProcess:
			self.assertEqual(newProcess[key], getNewProcess[0][key], 
				str(newProcess[key]) + " did not match " + str(getNewProcess[0][key]))

	def test_add_bad_process(self):
		newProcess = {
			'processme': os.path.join(scriptDir,'testFixtures','process1.py'),
			'endint': 'tcp://127.0.0.1:5556'
		}
		self.assertRaises(ValueError, self.processManager.addProcess, newProcess)

	def test_smoke_run(self):
		self._add_known_good_process1()
		self._add_known_good_process2()
		self.processManager.run()
		time.sleep(0.1)
		getProcessList = self.processManager.getProcessStatusList()
		self.assertEqual(len(getProcessList), 0)

if __name__ == '__main__':
	unittest.main()