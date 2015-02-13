"""
.. module:: log
    :synopsis: logger instance
"""

import os
import sys
scriptDir=os.path.dirname(os.path.realpath(__file__))
import appNetworkConfig2
sys.path.append(os.path.join(scriptDir,'..','..','src'))
import loggerMQ
import time
import pdb
import time

logger = loggerMQ.Logger()
logger.setLogConfig(os.path.join(scriptDir,'logs','testLog.log'))
logger.importProcessConfig(os.path.join(scriptDir,'appNetworkConfig3.py'), sys.argv[1])

time.sleep(3)
logger.run()
