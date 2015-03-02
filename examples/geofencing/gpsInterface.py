import gpxpy
import gpxpy.gpx
import pdb
import os
import sys
import time
scriptDir=os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(scriptDir,'..','..','src'))
import processNode

class GpsInterface():
	def __init__(self, processName, fullConfigPath):		
		gpsInterfaceNode = processNode.ProcessNode(fullConfigPath, processName)
		inputFilePath = os.path.join(scriptDir, 'inputData/Track on 2015-03-01 at 15-30 MST.gpx')

		gpx_file = open(inputFilePath, 'r')

		gpx = gpxpy.parse(gpx_file)
		for track in gpx.tracks:
			for segment in track.segments:
				for point in segment.points:
						gpsDataMsg = {
							'latitude': point.latitude,
							'longitude': point.longitude,
							'altitude': point.elevation				
						}
						gpsInterfaceNode.send('gpsData', gpsDataMsg)
						gpsInterfaceNode.log(logLevel=0, message=gpsDataMsg)
						time.sleep(0.25)

		gpsInterfaceNode.send('proc', {'action': 'stop'})


if __name__ == '__main__':
	gpsInterface = GpsInterface(sys.argv[1], sys.argv[2])
