"""
.. module:: utils
    :synopsis: Common utility functions
"""
import os
import sys
import importlib
import json
from jsonschema import Draft3Validator
scriptDir=os.path.dirname(os.path.realpath(__file__))
sys.path.append(scriptDir)
import appNetworkConfigSchema

def separatePathAndModule(fullPath):
    """
    Tries to dynamically import module at specified path.  If successful,
    then the process list retrieved
    :param fullPath: full path to the config file 
    :type fullPath: str
    :return: list of process dictionaries
    :raises: ValueError
    """
    processList = []
    try:
        moduleName, path = getModuleName(fullPath)
        sys.path.append(path)
        module = importlib.import_module(moduleName)
        processList = getattr(module, 'processList')
    except:
        raise ValueError("Unable to import module at specified path")

    return processList

def importConfigJson(fullPath):
    """
    Reads JSON formatted master configuration file
    :param fullPath: full path of the JSON file to load
    :type fullPath: str
    :raises: jsonschema.exceptions.ValidationError
    :returns: dictionary of master configuration information
    """
    configDict = {}

    file = open(fullPath, 'r')

    configDict = json.loads(file.read())
    validator = Draft3Validator(appNetworkConfigSchema.schema)
    
    # this will raise jsonschema.exceptions.ValidationError exception
    validator.validate(configDict)

    file.close()

    return configDict

def getModuleName(fullPath):
    path, fileName = os.path.split(fullPath)
    moduleName = fileName.rstrip('.py')
    return moduleName, path

def getDateTimeNoSpaces():
    from datetime import datetime
    return datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

def getDateTimeWithSpacesAndPrecision():
    from datetime import datetime
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')

def convLogLevelNumToString(logLevelNum):
    numString = ''
    if (logLevelNum == 0):
        numString = 'DEBUG'
    elif (logLevelNum == 1):
        numString = 'INFO'
    elif (logLevelNum == 2):
        numString = 'WARNING'
    elif (logLevelNum == 3):
        numString = 'ERROR'
    elif (logLevelNum == 4):
        numString = 'CRITICAL'
    else:
        numString = 'Log Level unrecognized'

    return numString   

def _convertIDToAddress(endPointID, endPointIdsList):
    endPointFound = False
    for item in endPointIdsList:
        if (item['id'] == endPointID):
            endPointAddress = item['address']
            endPointFound = True

    if (not(endPointFound)):
        raise ValueError("can't match 'endPoint' in 'endPointIds'")

    return endPointAddress 

def getHostIP():
    import socket
    return socket.gethostbyname(socket.gethostname())
