from os import system,name
import sys
import os
import re
from itertools import permutations
from time import sleep

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
    def showLocal(self, distance):
        print (UP*41, "Moving {}".format(distance))
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
            xMin = xMax - 40
        for yIndex in range(yMin, yMax):
            row = self.map[yIndex]
            if self.location[1] == yIndex:
                row = row[:self.location[0]] + WHITE + icon[dirs.index(self.dir)] + BLUE + row[self.location[0]+1:]
            #    row = row[xMin:xMax+3]
            #else:
            #    row = row[xMin:xMax+1]
            if (len(row) < 41):
                row += " "*(41-len(row))
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
        if len(row) < 150:
            row += " "*(150-len(row))
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
            nextSpot = ((self.location[0]+self.dir[0]) % self.maxX, (self.location[1]+self.dir[1]) % self.maxY)
            if not self.isInGrid(nextSpot):
                while not self.isInGrid(nextSpot):
                    nextSpot = ((nextSpot[0]+self.dir[0]) % self.maxX, (nextSpot[1]+self.dir[1]) % self.maxY)
            if self.map[nextSpot[1]][nextSpot[0]] == "#":
                break
            self.location = nextSpot
            self.showLocal(distance)
            sleep(0.025)
    def getPassword(self):
        row = self.location[1] + 1
        col = self.location[0] + 1
        facing = dirs.index(self.dir)
        return row*1000 + col*4 + facing
        
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
        
