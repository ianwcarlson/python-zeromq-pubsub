"""
.. module:: pointInPolygon
    :synopsis: ray casting algorithm, currently doesn't detect right on
    boundaries.  Refer to http://www.ariel.com.au/a/python-point-int-poly.html
    and http://geospatialpython.com/2011/08/point-in-polygon-2-on-line.html
    for more info.  Just needed a quick implementation to demonstrate
    the architecture
"""
import os
import sys
import time
scriptDir=os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(scriptDir,'..','..','src'))
import processNode

class PointInAPolygon():
    def __init__(self, processName, fullConfigPath):
        self.polygon = [(-33.416032,-70.593016), (-33.415370,-70.589604),
            (-33.417340,-70.589046), (-33.417949,-70.592351),
            (-33.416032,-70.593016)]
        self.pointInPolygonNode = processNode.ProcessNode(fullConfigPath, processName)

    def run(self):
        """
        Main run function receives gpsData, processes them, and sends them to
        subscribers
        """
        done = False
        while(not(done)):
            responseListDict = self.pointInPolygonNode.receive()
            for itemDict in responseListDict:
                topic = itemDict['topic']
                if (topic == 'proc'):
                    if (itemDict['contents']['action'] == 'stop'):
                        done = True
                        break
                elif(topic == 'gpsData'):
                    gpsDataDict = itemDict['contents']
                    isInside = self.pointInsidePolygon(gpsDataDict['latitude'], 
                        gpsDataDict['longitude'], self.polygon)

                    logMsg = 'Inside' if (isInside) else 'Outside'
                    self.pointInPolygonNode.log(logLevel=0, message=logMsg)
                    self.pointInPolygonNode.send('pointInPolygon', isInside)
                elif(topic == 'newPolygonPoints'):
                    self.pointInPolygonNode.log(logLevel=0, message=itemDict['contents'])
                    listOfTuples = self.convertDictsToTuples(itemDict['contents'])
                    self.polygon = listOfTuples

    @staticmethod
    def convertDictsToTuples(listOfDicts):
        listOfTuples = []
        for dictItem in listOfDicts:
            listOfTuples.append((dictItem['lat'],dictItem['lng']))

        return listOfTuples

    @staticmethod
    def pointInsidePolygon(x,y,poly):
        '''
        Find point inside of polygon
        :param x: latitude of test point
        :type x: float
        :param y: longitude of test point
        :type y: float
        :param poly: list of latitude/longitude pairs
        :type poly: list of tuple pairs
        :returns: boolean
        '''

        n = len(poly)
        inside =False
        if (n != 0):
            p1x,p1y = poly[0]
            for i in range(n+1):
                p2x,p2y = poly[i % n]
                if y > min(p1y,p2y):
                    if y <= max(p1y,p2y):
                        if x <= max(p1x,p2x):
                            if p1y != p2y:
                                xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                            if p1x == p2x or x <= xinters:
                                inside = not inside
                p1x,p1y = p2x,p2y

        return inside

if __name__ == '__main__':
    pointInAPolygon = PointInAPolygon(sys.argv[1], sys.argv[2])
    pointInAPolygon.run()