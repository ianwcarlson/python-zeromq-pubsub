"""
.. module:: processNode
    :synopsis: composition of publisher and subscriber objects which
    auto instantiates logger publisher
"""
import os
import sys
scriptDir=os.path.dirname(os.path.realpath(__file__))
sys.path.append(scriptDir)
import zeroMQInterface
import logMessageAdapter

class ProcessNode():
    def __init__(self, appNetworkConfig, processName):
        self.publisher = zeroMQInterface.ZeroMQPublisher()
        self.publisher.importProcessConfig(os.path.join(scriptDir,appNetworkConfig), processName)

        self.subscriber = zeroMQInterface.ZeroMQSubscriber()
        # all subscribers are publishers for logging, so a reference to the publisher needs
        # to be passed in
        self.subscriber.setPublisherRef(self.publisher)
        self.subscriber.importProcessConfig(os.path.join(scriptDir,appNetworkConfig), processName)

        self.logAdapter = logMessageAdapter.LogMessageAdapter(processName)

    def send(self, topic, message):
        self.publisher.send(topic, message)

    def receive(self):
        return self.subscriber.receive()

    def log(self, logLevel, message):
        self.publisher.send('log', self.logAdapter.genLogMessage(logLevel, message))
