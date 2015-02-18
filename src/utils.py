"""
.. module:: utils
    :synopsis: Common utility functions
"""
import os
import sys
import importlib
import json

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
    """
    configDict = {}
    try:
        file = open(fullPath, 'r')
        fileStr = file.read()
        configDict = json.loads(fileStr)
    except:
        raise UnicodeDecodeError('Unable to open and import json file')

    if ('processList' not in processConfig or 
        'endPointsIds' not in processConfig):
        raise ValueError("'processList' or 'endPointIds' keys not found in config")

    if (len(processConfig['processList']) == 0):
        raise ValueError("'processList' empty")

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
