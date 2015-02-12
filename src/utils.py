"""
.. module:: utils
    :synopsis: Common utility functions
"""
import os
import sys
import importlib

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

def getModuleName(fullPath):
    path, fileName = os.path.split(fullPath)
    moduleName = fileName.rstrip('.py')
    return moduleName, path