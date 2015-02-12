"""
.. module:: testAppNetworkConfig2
    :synopsis: Provides enumerations to configure system hookup
"""
import os
import sys

scriptDir=os.path.dirname(os.path.realpath(__file__))

PUB_ENDPOINT_ADDR = 'tcp://127.0.0.1:5556'
#PUB_ENDPOINT_ADDR = "ipc://somename"
SUB_ENDPOINT_ADDR = 'tcp://127.0.0.1:5557'
TEST_SUB_ENDPOINT_ADDR = 'tcp://127.0.0.1:5558'

processList = [
    {
        'processName': 'publisher',
        'processPath': os.path.join(scriptDir, 'pub.py'),
        'endPoint': PUB_ENDPOINT_ADDR
    },
    {
        'processName': 'subscriber1',
        'processPath': os.path.join(scriptDir, 'sub.py'),
        'endPoint': SUB_ENDPOINT_ADDR,
        'subscriptions': [
            {
                'endPoint': PUB_ENDPOINT_ADDR,
                'topics' : ['fancy']
            },
        ]
    },
    {
        'processName': 'subscriber2',
        'processPath': os.path.join(scriptDir, '..', 'testZeroMQInterface.py'),
        'endPoint': TEST_SUB_ENDPOINT_ADDR,
        'subscriptions': [
        	{
        		'endPoint': PUB_ENDPOINT_ADDR,
        		'topics' : ['fancy']
        	},
        ]
    }
]