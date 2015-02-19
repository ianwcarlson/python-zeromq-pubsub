"""
.. module:: log
    :synopsis: logger instance
"""

import os
import sys
scriptDir=os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(scriptDir,'..','..','src'))
import loggerNode
import time
import pdb
import time

logger = loggerNode.Logger(os.path.join(scriptDir,'appNetworkConfig3.json'), sys.argv[1])
logger.setLogConfig(os.path.join(scriptDir,'logs','testLog'))

time.sleep(0)
logger.run()

print ('logger done processing')

