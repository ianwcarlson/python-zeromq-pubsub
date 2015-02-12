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

class TestZeroLoggerMQ(unittest.TestCase):
	def __init__(self):
		print('')



if __name__ == '__main__':
	unittest.main()