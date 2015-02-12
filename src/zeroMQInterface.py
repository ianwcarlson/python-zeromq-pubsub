"""
.. module:: zeroMQInterface
    :synopsis: Wraps ZeroMQ library with a simplified publish/subscribe
    interface.  The serialize data protocol is MessagePack.  The python 
    dictionary is used as a standardized format.  The subscribe gets the 
    contents of messages, but also the publisher address and the topic.
"""
import os
import sys
scriptDir=os.path.dirname(os.path.realpath(__file__))
sys.path.append(scriptDir)
import zmq
import json
import msgpack
import importlib
import pdb
import utils
PUB_BUFF_SIZE = 100000

# static functions
def _extractProcessConfig(processList, processPath):
    """
    Tries to find specific process dictionary settings at supplied
    process path.
    :param processList: list of processes dictionaries
    :type processList: list 
    :return: dictionary of process settings
    :raises: ValueError
    """
    processDict = {}
    for process in processList:
        if (process['processName'] == processPath):
            processDict = process
            break
    
    if (not(processDict)):
        raise ValueError("Process configuration not found in config file")

    return processDict

class ZeroMQPublisher():
    def __init__(self, endPointAddress=None):
        """
        Constructor.  Sets up ZeroMQ publisher socket.

        :param number port: integer designating the port number of the publisher
        """
        self.context = zmq.Context()
        self.publisher = self.context.socket(zmq.PUB)
        self.publisher.set_hwm(PUB_BUFF_SIZE)
        if (endPointAddress is not(None)):
            self.endPointAddress = endPointAddress
            self.publisher.bind(endPointAddress)

    def __del__(self):
        """
        Destructor.  Closes sockets
        """
        self.publisher.close()
        self.context.term()

    def importProcessConfig(self, configFilePath, publisherPath=os.path.realpath(__file__)):
        """
        Registers publisher settings based off config file
        :param configFilePath: full config file path
        :type configFilePath: str
        :param publisherPath: path to publisher process file (defaults to current file)
        :type publisherPath: str
        :raises: ValueError    
        """

        self.processList = utils.separatePathAndModule(configFilePath)
        self.processConfigDict = _extractProcessConfig(self.processList, publisherPath)

        if ('endPoint' in self.processConfigDict):
            self.endPointAddress = self.processConfigDict['endPoint']
        else:
            raise ValueError("'endPoint' missing from process config")

    def send(self, topic, dict):
        """
        Main send function over ZeroMQ socket.  Input dictionary gets
        serialized and sent over wire.

        :param str topic: string representing the message topic
        :param dictionary dict: data payload input
        """

        serialDict = msgpack.dumps(dict)
        self.publisher.send_multipart([str.encode(topic),str.encode(self.endPointAddress),
            serialDict])


class ZeroMQSubscriber():
    def __init__(self):
        """
        Constructor.  Sets up ZeroMQ subscriber socket and poller object
        :return:
        """
        self.context = zmq.Context()
        self.subscriberList = []
        self.poller = zmq.Poller()

    def __del__(self):
        """
        Destructor.  Closes ZeroMQ connections.
        """
        for item in self.subscriberList:
            item.close()

        self.context.term()

    def importProcessConfig(self, configFilePath, subscriberPath=os.path.realpath(__file__)):
        """
        Registers subscriber settings based off config file
        :param configFilePath: full config file path
        :type configFilePath: str
        :param subscriberPath: path to subscriber process file (defaults to current file)
        :type subscriberPath: str
        :raises: ValueError    
        """
        self.processList = utils.separatePathAndModule(configFilePath)
        self.processConfigDict = _extractProcessConfig(self.processList, subscriberPath)

        if ('subscriptions' in self.processConfigDict):
            for subDict in self.processConfigDict['subscriptions']:
                if ('endPoint' in subDict):
                    self.connectSubscriber(subDict['endPoint'])
                    if ('topics' in subDict):
                        for topic in subDict['topics']:
                            self.subscribeToTopic(topic)
                    else:
                        print('Warning: No topics found for subscribed endpoint: ' + str(subDict['endPoint']))
                else:
                    raise ValueError("No endpoint specified in process config")
        else:
            raise ValueError("No subscriptions specified in process config")

    def connectSubscriber(self, endPointAddress):
        """
        Method to create subscriber connection to a particular publisher
        :param number port: integer representing the port number of the publisher to connect to
        :param str topic: string that is used to filter unwanted messages from publisher
        """
        self.subscriberList.append(self.context.socket(zmq.SUB))
        self.subscriberList[-1].connect(endPointAddress)
        self.poller.register(self.subscriberList[-1], zmq.POLLIN)

    def subscribeToTopic(self, topic):
        """
        Subscribes class instance to most recently connected subscriber
        :param topic: topic to subscriber to (filters other topics if not subscribed)
        :type topic: str
        """
        self.subscriberList[-1].setsockopt(zmq.SUBSCRIBE, str.encode(topic))

    @staticmethod
    def _convert_keys_to_string(inDict):
        """
        Converts byte encoded keys to string.  Need this because msgpack unpack 
        doesn't decode all the elements in the serialized data stream
        :param dictionary inDict: any non-nested key value dictionary
        :return: dictionary 
        """
        newDict = {}
        for key, value in inDict.items():
            newDict[key.decode()] = value   

        return newDict

    def receive(self):
        """
        Method that polls all available connections and returns a dictionary.  This should
        get called continuously to continue receiving messages.  Currently, this function
        will not block if no messages are available.  
        :return: list of nested dictionaries
        """
        socks = []
        try:
            socks = dict(self.poller.poll(0))
        except:
            print ('exception occurred on subscribed receive function')

        responseList = []
        if (len(socks)>0):
            for listItem in self.subscriberList:
                if listItem in socks:
                    topic, pubAddress, contents = listItem.recv_multipart()
                    convertedContents = self._convert_keys_to_string(msgpack.loads(contents))

                    responseList.append({
                        'topic': topic.decode(), 
                        'pubAddress': pubAddress.decode(), 
                        'contents': convertedContents
                    })                   

        return responseList