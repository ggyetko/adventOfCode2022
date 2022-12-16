from os import system, name
import re

# wrong answer 7970833 too high (dumb, I was using row 10)

WHITE = "\033[097m"
GREEN = "\033[092m"
RED   = "\033[091m"
BLUE  = "\033[094m"
YELLOW= "\033[093m"
CYAN  = "\033[093m"
UP = "\033[A"

def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
        
        
class SparseRange:
    def __init__(self):
        self.ranges = []
    def addRange(self, x1, x2):
        containedTuples = []
        startTuple = None
        endTuple = None
        for range in self.ranges:
            if range[0] <= x1 and range[1] >= x1:
                # starts inside this range
                x1 = range[0]
                startTuple = range
            if range[0] <= x2 and range[1] >= x2:
                # ends inside this range
                x2 = range[1]
                endTuple = range
            if range[0] >= x1 and range[1] <= x2:
                containedTuples.append(range)
        if startTuple != None:
            self.ranges.remove(startTuple)
        if endTuple in self.ranges and endTuple != None:
            self.ranges.remove(endTuple)
        for tup in containedTuples:
            if tup in self.ranges:
                self.ranges.remove(tup)
        self.ranges.append((x1,x2))
        self.ranges.sort()
        print ("Beacon can not be in these ranges:",self.ranges)
    def delSpot(self, x):
        for range in self.ranges:
            if range[0] == x:
                self.ranges.append((x+1,range[1]))
                self.ranges.remove(range)
                return
            elif range[1] == x:
                self.ranges.append((range[0],x-1))
                self.ranges.remove(range)
                return
            elif range[0] < x and range[1] > x:
                self.ranges.append((range[0],x-1))
                self.ranges.append((x+1,range[1]))
                self.ranges.remove(range)
                return
    def getNumSpotsinRange(self):
        count = 0
        for range in self.ranges:
            count += range[1] - range[0] + 1
        return count

class Grid:
    def __init__(self):
        self.sensorFinds = {}
    def addPair(self,sensorTuple,beaconTuple):
        self.sensorFinds[sensorTuple] = beaconTuple
    def getNoBeaconRange(self, row):
        spotsBlocked = SparseRange()
        for sensor in self.sensorFinds:
            (x,y) = sensor 
            (bx,by) = self.sensorFinds[sensor]
            sensorRange = abs(bx-x) + abs(by-y)
            distToRow = abs(row-y)
            remainingRadius = sensorRange - distToRow
            if remainingRadius > 0:
                spotsBlocked.addRange(x-remainingRadius, x+remainingRadius)
        # Now unblock actual beacons
        for sensor in self.sensorFinds:
            beacon = self.sensorFinds[sensor]
            if beacon[1] == row:
                spotsBlocked.delSpot(beacon[0])
        return spotsBlocked

def getInts(line):
    data = re.split(" |=|,|:|\n", line)
    outList = []
    for d in data:
        if d.isnumeric() or len(d) > 0 and d[0] == "-":
            outList.append(int(d))
    return outList
    
grid = Grid()
file = open("advent2022_data15.txt","r")
for line in file:
    data = getInts(line)
    grid.addPair((data[0],data[1]),(data[2],data[3]))

noSensorSpots = grid.getNoBeaconRange(2000000)
print ("Total number of spaces wher no beacons can be:",noSensorSpots.getNumSpotsinRange())