from os import system,name
import sys
import os
import re
from itertools import permutations
from time import sleep

# 15265 is too low

WHITE = "\033[097m"
GREEN = "\033[092m"
RED   = "\033[091m"
BLUE  = "\033[094m"
YELLOW= "\033[093m"
CYAN  = "\033[093m"
UP = "\033[A"

def clear():
    _ = system('clear')

dirs = [(1,0),(0,1),(-1,0),(0,-1)] # clockwise is one positive step
icon = [">","v","<","^"]

conn = []

class Connection:
    def __init__(self, codeIn, min, max, codeOut, minOut, maxOutDir):
        self.codeIn = codeIn  # "x-1","xmax","y-1","ymax"
        self.min = min
        self.max = max        # inclusive range
        self.codeOut = codeOut # "x-1","xmax","y-1","ymax"
        self.minOut = minOut 
        self.maxOutDir = maxOutDir # -1 if inverted
    def getMapping(self, x, y):
        if self.codeIn[0] == "x":
            diff = y-self.min
        else:
            diff = x-self.min
        if self.codeOut == "x-1":
            x = 0
            y = self.minOut + (self.maxOutDir * diff)
            dir = dirs[0]
        elif self.codeOut == "xmax":
            x = 149
            y = self.minOut + (self.maxOutDir * diff)
            dir = dirs[2]
        elif self.codeOut == "y-1":
            y = 0
            x = self.minOut + (self.maxOutDir * diff)
            dir = dirs[1]
        elif self.codeOut == "ymax":
            y = 199
            x = self.minOut + (self.maxOutDir * diff)
            dir = dirs[3]
        #print ("Move to {} direction {}".format((x,y), icon[dirs.index(dir)]))
        return (x,y), dir

def findConnection(spot):
    global conn
    #print ("FindConnection:",spot)
    x = spot[0]
    y = spot[1]
    otherVar = 0
    if x == -1:
        code = "x-1"
        otherVar = y
    elif x == 150:
        code = "xmax"
        otherVar = y
    elif y == -1:
        code = "y-1"
        otherVar = x
    elif y == 200:
        code = "ymax"
        otherVar = x
    for c in conn:
        if c.codeIn == code and c.min <= otherVar and c.max >= otherVar:
            return c.getMapping(x,y)

class Grove:
    def __init__(self):
        self.map = []
        self.dir = dirs[0]
        self.location = None
        self.maxY = 0
        self.maxX = 0
    def show(self, playerOn):
        for yIndex in range(0,len(self.map)):
            row = self.map[yIndex]
            if playerOn and self.location[1] == yIndex:
                row = row[:self.location[0]] + "X" + row[self.location[0]+1:]
            print (row)
    def showLocal(self):
        '''
        yMin = self.location[1] - 20
        yMax = self.location[1] + 20
        if yMin < 0:
            yMin = 0
            yMax = 40
        if yMax >= self.maxY:
            yMax = self.maxY - 1
            yMin = yMax - 40
        xMin = self.location[0] - 20
        xMax = self.location[0] + 20
        if xMin < 0:
            xMin = 0
            xMax = 40
        if xMax >= self.maxX:
            xMax = self.maxX- 1
            xMin = xMax - 40'''
        print (UP*201)
        yMin = 0
        yMax = 199
        xMin = 0
        xMax = 149
        for yIndex in range(yMin, yMax+1):
            row = ""
            for xIndex in range(xMin, xMax+1):
                if xIndex >= len(self.map[yIndex]):
                    break
                if self.location == (xIndex,yIndex):
                    row += RED + (icon[dirs.index(self.dir)] * 3) + BLUE
                else:
                    showing = self.map[yIndex][xIndex]
                    if showing == "X":
                        row += GREEN + self.map[yIndex][xIndex] * 3 + BLUE
                    else:
                        row += self.map[yIndex][xIndex] * 3
            print (row)
    def isInGrid(self, xyTuple):
        (x,y) = xyTuple
        if x < 0 or y < 0:
            return False
        if y >= len(self.map):
            return False
        row = self.map[y]
        if x >= len(row):
            return False
        if row[x] == " ":
            return False
        return True
    def addRow(self, row):
        self.map.append(row)
        if self.location == None:
            self.location = (row.find("."),0)
        self.maxX = max(self.maxX,len(row))
        self.maxY += 1
    def turn(self, turnDir):
        currDir = dirs.index(self.dir)
        if turnDir == "R" or turnDir == 1:
            currDir = (currDir + 1) % 4
        if turnDir == "L" or turnDir == -11:
            currDir = (currDir - 1) % 4
        self.dir = dirs[currDir]
    def move(self, distance):
        for step in range(0,distance):
            nextSpot = (self.location[0]+self.dir[0], self.location[1]+self.dir[1])
            nextDir = self.dir
            if not self.isInGrid(nextSpot):
                while nextSpot[0] >= 0 and nextSpot[0] < 150 and nextSpot[1] >= 0 and nextSpot[1] < 200:
                    nextSpot = ((nextSpot[0]+self.dir[0]), (nextSpot[1]+self.dir[1]) )
                nextSpot, nextDir = findConnection(nextSpot)
                while not self.isInGrid(nextSpot):
                    nextSpot = ((nextSpot[0]+nextDir[0]) % self.maxX, (nextSpot[1]+nextDir[1]) % self.maxY)
            if self.map[nextSpot[1]][nextSpot[0]] == "#":
                break
            self.dir = nextDir
            self.map[nextSpot[1]] = self.map[nextSpot[1]][:nextSpot[0]] + "X" + self.map[nextSpot[1]][nextSpot[0]+1:]
            self.location = nextSpot
        self.showLocal()
        sleep(0.025)
    def getPassword(self):
        row = self.location[1] + 1
        col = self.location[0] + 1
        facing = dirs.index(self.dir)
        print ("{},{}, facing={}= +{}".format(row,col,self.dir,facing))
        return row*1000 + col*4 + facing

conn.append(Connection("x-1", 0 ,   49, "x-1" , 149, -1))
conn.append(Connection("x-1", 50 ,  99, "y-1" ,   0,  1))
conn.append(Connection("x-1", 100, 149, "x-1" ,  49, -1))
conn.append(Connection("x-1", 150, 199, "y-1" ,  50,  1))

conn.append(Connection("xmax", 0 ,  49, "xmax", 149, -1))
conn.append(Connection("xmax", 50 , 99, "ymax", 100,  1))
conn.append(Connection("xmax", 100,149, "xmax",  49, -1))
conn.append(Connection("xmax", 150,199, "ymax",  50,  1))

conn.append(Connection("y-1", 0  ,  49, "x-1" ,  50,  1))
conn.append(Connection("y-1", 50 ,  99, "x-1" , 150,  1))
conn.append(Connection("y-1", 100, 149, "ymax",   0,  1))

conn.append(Connection("ymax", 0  ,  49, "y-1", 100,  1))
conn.append(Connection("ymax", 50 ,  99, "xmax",150,  1))
conn.append(Connection("ymax", 100, 149, "xmax", 50,  1))

clear()
grove = Grove()
file = open("advent2022_data22.txt","r")
for line in file:
    data = line.split("\n")
    if data[0] == "":
        break
    grove.addRow(data[0])


instr = file.readline().replace("\n","") + "X"
nextIndex = 0
accumStr = ""
while nextIndex < len(instr):
    char = instr[nextIndex]
    if char.isdigit():
        accumStr += char
        nextIndex += 1
    else:
        moves = int(accumStr)
        grove.move(moves)
        nextIndex += 1
        if char != "X":
            grove.turn(char)
        else:
            break
        accumStr = ""
            
print ("Password:",grove.getPassword())
        
