"""
.. module:: testAppNetworkConfig3
    :synopsis: Provides enumerations to configure system hookup
"""
import os
import sys

scriptDir=os.path.dirname(os.path.realpath(__file__))

PUB_ENDPOINT_ADDR = 'tcp://127.0.0.1:5556'
#PUB_ENDPOINT_ADDR = "ipc://somename"
SUB_ENDPOINT_ADDR = 'tcp://127.0.0.1:5557'
LOGGER_ENDPOINT_ADDR = 'tcp://127.0.0.1:5558'

processList = [
    {
        'processName': 'log',
        'processPath': os.path.join(scriptDir, 'log.py'),
        'endPoint': LOGGER_ENDPOINT_ADDR,
        'subscriptions': [
            {
                'endPoint': PUB_ENDPOINT_ADDR,
                'topics': ['log', 'proc']
            },
            {
                'endPoint': SUB_ENDPOINT_ADDR,
                'topics': ['log', 'proc']
            }
        ]

    },
    {
        'processName': 'Pub',
        'processPath': os.path.join(scriptDir, 'pub.py'),
        'endPoint': PUB_ENDPOINT_ADDR
    },
    {
        'processName': 'Sub',
        'processPath': os.path.join(scriptDir, 'sub.py'),
        'endPoint': SUB_ENDPOINT_ADDR,
        'subscriptions': [
        	{
        		'endPoint': PUB_ENDPOINT_ADDR,
        		'topics' : ['fancy']
        	},
        ]
    }
]