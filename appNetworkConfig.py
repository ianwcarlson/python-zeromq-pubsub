"""
.. module:: appConfigConstants
    :synopsis: Provides enumerations to configure system hookup
"""


K9_HW_IF_ENDPOINT_ADDR = 'tcp://127.0.0.1:5556'
SQLITE_DB_ENDPOINT_ADDR = 'tcp://127.0.0.1:5557'

processList = [
    {
        'processName': 'fileToK9DatRunner.py',
        'endPoint': K9_HW_IF_ENDPOINT_ADDR
    },
    {
        'processName': 'sqliteDBInterface.py',
        'endPoint': SQLITE_DB_ENDPOINT_ADDR
    }
]

#IN_FILE_EXT = '*_RAW.raw'
IN_FILE_EXT = '*.dat'