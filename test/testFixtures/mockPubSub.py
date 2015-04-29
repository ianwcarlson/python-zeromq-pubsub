"""
.. module:: genericPublisherSubscriber
    :synopsis: generic programmable publisher for testing
"""

import os
import sys
scriptDir=os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(scriptDir,'..','..','src','facilities'))
import processNode
import time
import pdb
#import loggerNode
#import logMessageAdapter

class MockPublisher():
	def __init__(self, pathToNetworkConfig, processName):
		self.processNode = processNode.ProcessNode(pathToNetworkConfig, processName)
		self.msgQueueList = []


	def loadMsgQueue(self, msgList):
		self.msgQueueList = msgList

	def flushMsgQueue(self):
		self.msgQueueList = []

	def run(self):
		for itemDict in self.msgQueueList:
			self.processNode.send(itemDict['topic'], itemDict['message'])


class MockSubscriber():
	def __init__(self, pathToNetworkConfig, processName):
		self.processNode = processNode.ProcessNode(pathToNetworkConfig, processName)
		self.responseList = []

	def getResponseList(self):
		return self.responseList

	def flushMsgQueue(self):
		self.responseList = []

	def runOnce(self):
		#done = False
		#while(not(done)):
		response = self.processNode.receive()
		for item in response:
				#if (item['topic'] == 'proc'):
				#	action = item['contents']['action']
				#	if (action == 'stop' or action == 'softStop'):
				#		done = True
				#		break
				#else:	
			self.responseList.append(item)
