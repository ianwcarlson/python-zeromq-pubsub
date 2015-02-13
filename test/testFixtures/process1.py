"""
.. module:: process1
    :synopsis: dummy test process
"""

print("Running process1")

import logging
logging.basicConfig(filename='example.log',level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')

print("Running process1")