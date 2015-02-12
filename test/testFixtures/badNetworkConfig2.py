import os
import sys

scriptDir=os.path.dirname(os.path.realpath(__file__))

PUB_ENDPOINT_ADDR = 'tcp://127.0.0.1:5556'
SUB_ENDPOINT_ADDR = 'tcp://127.0.0.1:5557'
LOGGER_ENDPOINT_ADDR = 'tcp://127.0.0.1:5558'

processList = [
    {
        'processName': os.path.join(scriptDir, 'pub.py'),
        'endPoint': PUB_ENDPOINT_ADDR
    },
    {
        'processName': os.path.join(scriptDir, 'sub.py'),
        'endPoint': SUB_ENDPOINT_ADDR,
        'subscriptions!!!!!': [
        	{
        		'endPoint': PUB_ENDPOINT_ADDR,
        		'topics' : ['fancy']
        	}
        ]
    }
]