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
import logMessageAdapter
import time
PUB_BUFF_SIZE = 100000

# static functions
def _extractProcessConfig(processList, processName):
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

        if (process['processName'] == processName):
            processDict = process
            break
    
    if (not(processDict)):
        raise ValueError("Process configuration not found in config file")

    return processDict

def _extractConfig(configFilePath, publisherName):
    """
    Extracts the endpoint address and the dictionary that contains other connection
    information
    :param configFilePath: path to the network configuration file
    :type configFilePath: str 
    :param publisherName: name of publisher
    :type publisherName: str
    :returns: endPointAddress (str), processConfigDict (dict)
    """
    masterProcessConfig = utils.importConfigJson(configFilePath)
    processConfigDict = _extractProcessConfig(masterProcessConfig['processList'], 
        publisherName)
    endPointIdsList = masterProcessConfig['endPointsIds']

    endPointID = processConfigDict['endPoint']

    endPointAddress = utils._convertIDToAddress(endPointID, endPointIdsList)

    return endPointAddress, processConfigDict, endPointIdsList

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
            self.bind(endPointAddress)

    def __del__(self):
        """
        Destructor.  Closes sockets
        """
        self.publisher.close()
        self.context.term()

    def bind(self, endPointAddress):
        """
        Binds the publisher to the endpoint address
        :param endPointAddress: endpoint address (e.g., 'tcp://127.0.0.1:5555')
        :type endPointAddress: str 
        """
        self.endPointAddress = endPointAddress
        self.publisher.bind(endPointAddress)

    def importProcessConfig(self, configFilePath, 
        publisherName=utils.getModuleName(os.path.realpath(__file__))):
        """
        Registers publisher settings based off config file
        :param configFilePath: full config file path
        :type configFilePath: str
        :param publisherPath: path to publisher process file (defaults to current file)
        :type publisherPath: str
        :raises: ValueError    
        """
        self.endPointAddress, self.processConfigDict, endPointIdsList = _extractConfig(configFilePath, 
            publisherName)
        self.bind(self.endPointAddress)
        self.publisherName = publisherName
        self.logAdapter = logMessageAdapter.LogMessageAdapter(publisherName)

    def logPubConnections(self):
        """
        Method that logs the publisher connection information
        """
        logMsg = 'Binding to address ' + str(self.endPointAddress)
        self.send('log', self.logAdapter.genLogMessage(logLevel=1, message=logMsg))

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
    def __init__(self, publisherRef=None):
        """
        Constructor.  Sets up ZeroMQ subscriber socket and poller object
        :return:
        """
        self.context = zmq.Context()
        self.subscriberList = []
        self.poller = zmq.Poller()
        if (publisherRef is not(None)):
            self.logPublisher = publisherRef

    def __del__(self):
        """
        Destructor.  Closes ZeroMQ connections.
        """
        for item in self.subscriberList:
            item['socket'].close()

        self.context.term()

    def setPublisherRef(self, publisherRef):
        """
        Sets the publisher handle so this class can publish log messages
        :param publisherRef: publisher handle (passed by reference)
        :type: ZeroMQPublisher()
        """
        self.logPublisher = publisherRef

    def importProcessConfig(self, configFilePath, subscriberName=utils.getModuleName(os.path.realpath(__file__))):
        """
        Registers subscriber settings based off config file
        :param configFilePath: full config file path
        :type configFilePath: str
        :param subscriberName: path to subscriber process file (defaults to current file)
        :type subscriberName: str
        :raises: ValueError    
        """
        logMsgsList = []
        self.subscriberName = subscriberName
        self.endPointAddress, self.processConfigDict, endPointsIdsList = _extractConfig(configFilePath, 
            subscriberName)
        self.logAdapter = logMessageAdapter.LogMessageAdapter(subscriberName)

        if ('subscriptions' in self.processConfigDict):
            for subDict in self.processConfigDict['subscriptions']:
                self.connectSubscriber(utils._convertIDToAddress(subDict['endPoint'], endPointsIdsList))
                for topic in subDict['topics']:
                    self.subscribeToTopic(topic)

    def connectSubscriber(self, endPointAddress):
        """
        Method to create subscriber connection to a particular publisher
        :param number port: integer representing the port number of the publisher to connect to
        :param str topic: string that is used to filter unwanted messages from publisher
        """
        self.subscriberList.append({'endPoint': endPointAddress, 
            'socket': self.context.socket(zmq.SUB), 'topics': []})
        self.subscriberList[-1]['socket'].connect(endPointAddress)
        self.poller.register(self.subscriberList[-1]['socket'], zmq.POLLIN)

    def subscribeToTopic(self, topic):
        """
        Subscribes class instance to most recently connected subscriber
        :param topic: topic to subscriber to (filters other topics if not subscribed)
        :type topic: str
        """
        self.subscriberList[-1]['topics'].append(topic)
        self.subscriberList[-1]['socket'].setsockopt(zmq.SUBSCRIBE, str.encode(topic))

    def logSubConnections(self):
        """
        Method that logs the connections list. 
        """
        for sub in self.subscriberList:
            
            topicStr = ''
            for topic in sub['topics']:
                topicStr += str(topic) + ' '
            
            logMsg = 'Connected to ' + sub['endPoint'] + \
                ' under the following topics: ' + topicStr
            self.logPublisher.send('log', self.logAdapter.genLogMessage(logLevel=1, message=logMsg))  

    def _byteToString(self, inBytes):
        """
        Converts bytes to string if needed
        :param inBytes: input bytes
        :type inBytes: bytes
        """
        if (type(inBytes)==bytes):
            return inBytes.decode()
        else:
            return inBytes

    def _convert_keys_to_string(self, inDict):
        """
        Converts byte encoded keys to string.  Need this because msgpack unpack 
        doesn't decode all the elements in the serialized data stream
        :param dictionary inDict: any non-nested key value dictionary
        :return: dictionary 
        """
        newDict = {}
        for key, value in inDict.items():
            if (type(value) == dict):
                # this might blow up, need to test more
                value = self._convert_keys_to_string(value)

            newDict[self._byteToString(key)] = self._byteToString(value)  

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
            socks = dict(self.poller.poll(0.1))
        except:
            print ('exception occurred on subscribed receive function')

        responseList = []
        if (len(socks)>0):
            for listItem in self.subscriberList:
                if listItem['socket'] in socks:
                    topic, pubAddress, contents = listItem['socket'].recv_multipart()

                    convertedContents = self._convert_keys_to_string(msgpack.loads(contents)) 
                    responseList.append({
                        'topic': topic.decode(), 
                        'pubAddress': pubAddress.decode(), 
                        'contents': convertedContents
                    })                   

        return responseList