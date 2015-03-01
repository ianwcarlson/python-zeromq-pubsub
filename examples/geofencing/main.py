import pdb
import os
import sys
import time
scriptDir=os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(scriptDir,'..','..','src'))
import processManager

processManager = processManager.ProcessManager()	
processManager.importProcessConfig(os.path.join(scriptDir,'geofencingExampleConfig.json'))
processManager.run()