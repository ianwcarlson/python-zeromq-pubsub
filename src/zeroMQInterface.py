"""
.. module:: dictToZeroMQ
    :synopsis: Takes in dictionary and sends out over ZeroMQ
"""

import zmq
import json
import msgpack
import pdb
PUB_BUFF_SIZE = 100000

class zeroMQPublisher():
    def __init__(self, endPointAddress):
        """
        Constructor.  Sets up ZeroMQ publisher socket.

        :param number port: integer designating the port number of the publisher
        """
        self.context = zmq.Context()
        self.endPointAddress = endPointAddress
        self.publisher = self.context.socket(zmq.PUB)
        self.publisher.bind(endPointAddress)
        self.publisher.set_hwm(PUB_BUFF_SIZE)

    def __del__(self):
        """
        Destructor.  Closes sockets
        """
        self.publisher.close()
        self.context.term()

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
        self.subscriberList[-1].setsockopt(zmq.SUBSCRIBE, str.encode(topic))

    @staticmethod
    def _convert_keys_to_string(inDict):
        """
        Converts byte encoded keys to string.  Need this because msgpack unpack \
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
        get called continuously to continue receiving messages.
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