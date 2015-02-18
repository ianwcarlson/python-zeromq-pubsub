"""
.. module:: testProcessManager
	:synopsis: tests the ProcessManager module/clas
"""

import os
import sys
import unittest
import pdb
import json
import jsonschema
from jsonschema import Draft3Validator
scriptDir=os.path.dirname(os.path.realpath(__file__))
sys.path.append(scriptDir)
sys.path.append(os.path.join(scriptDir,'..','src'))
import appNetworkConfigSchema


class TestProcessManager(unittest.TestCase):
	def setUp(self):
		self.validator = Draft3Validator(appNetworkConfigSchema.schema)
		
	def testGoodConfig(self):
		fileJson = self._openFileJson('appNetworkConfig.json')
		self.validator.validate(fileJson)

	def testBadConfig(self):
		fileJson = self._openFileJson('badAppNetworkConfig.json')
		#self.validator.validate(fileJson)
		self.assertRaises(jsonschema.exceptions.ValidationError, self.validator.validate, fileJson)

	def testBadConfig2(self):
		fileJson = self._openFileJson('badAppNetworkConfig2.json')
		self.assertRaises(jsonschema.exceptions.ValidationError, self.validator.validate, fileJson)

	def testBadConfig3(self):
		fileJson = self._openFileJson('badAppNetworkConfig3.json')
		self.assertRaises(jsonschema.exceptions.ValidationError, self.validator.validate, fileJson)

	def _openFileJson(self, fileName):
		self.file = open(os.path.join(scriptDir,'testFixtures',fileName), 'r')
		fileJson = json.loads(self.file.read())
		return fileJson

	def tearDown(self):
		self.file.close()


if __name__ == '__main__':
	unittest.main()