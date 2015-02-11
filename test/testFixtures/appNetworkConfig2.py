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
LOGGER_ENDPOINT_ADDR = 'tcp://127.0.0.1:5558'

processList = [
    {
        'processName': os.path.join(scriptDir, 'testPub.py'),
        'endPoint': PUB_ENDPOINT_ADDR
    },
    {
        'processName': os.path.join(scriptDir, 'testSub.py'),
        'endPoint': SUB_ENDPOINT_ADDR,
        'subscriptions': [
        	{
        		'endPoint': PUB_ENDPOINT_ADDR,
        		'topics:' : ['fancy']
        	}
        ]
    },
    {
    	'processName': os.path.join(scriptDir, 'logger.py'),
    	'endPoint': LOGGER_ENDPOINT_ADDR,
    	'subscriptions': [
    		{
    			'endPoint': PUB_ENDPOINT_ADDR,
    			'topics': ['log']
    		},
    		{
    			'endPoint': SUB_ENDPOINT_ADDR,
    			'topics': ['log']
    		}
    	]

    }
]