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
import time

class ProcessNode():
    def __init__(self, appNetworkConfig, processName, minLogLevel=0):
        """
        Instantiates pub and sub by composition using the path to the network configuration
        file and the process name, which is the second argument passed in each process by design.
        When constructed, this will pause for one second because it takes some time for the
        ZeroMQ sockets to initially.  Further investigation should be done to see if a 
        non-static wait can be used, since any static value might vary depending on the
        circumstances.
        """

        self.publisher = zeroMQInterface.ZeroMQPublisher()
        self.publisher.importProcessConfig(os.path.join(scriptDir,appNetworkConfig), processName)

        self.subscriber = zeroMQInterface.ZeroMQSubscriber()
        # all subscribers are publishers for logging, so a reference to the publisher needs
        # to be passed in
        self.subscriber.setPublisherRef(self.publisher)
        self.subscriber.importProcessConfig(os.path.join(scriptDir,appNetworkConfig), processName)

        self.minLogLevel = minLogLevel
        self.logAdapter = logMessageAdapter.LogMessageAdapter(processName)

        # need to wait until zeroMQ socket connections establish, otherwise
        # messages will be initially lost
        time.sleep(1)

        self.publisher.logPubConnections()
        self.subscriber.logSubConnections()


    def send(self, topic, message):
        """
        Wrapper for publisher send method.
        :param topic: topic of the message to send
        :type topic: str 
        :param message: dictionary to be sent.  string also work.
        :type message: dict 
        """
        self.publisher.send(topic, message)

    def receive(self):
        """
        Wrapper for subscriber read
        :returns: list of nested dictionaries
        """
        return self.subscriber.receive()

    def log(self, logLevel, message):
        """
        Wrapper to send logs to subscribers
        :param logLevel: the logging priority level of the message
        :type logLevel: int
        :param message: the log message to be sent
        :type message: str
        """
        if (logLevel >= self.minLogLevel):
            self.publisher.send('log', self.logAdapter.genLogMessage(logLevel, message))
