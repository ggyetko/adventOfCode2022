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

moves = [(0,-1),(1,0),(0,1),(-1,0),(0,0)]
symbol = ["^", ">", "v", "<"]

class Blizzard:
    def __init__(self,loc,dir):
        self.loc = loc
        self.dirIndex = symbol.index(dir)
    def oneStep(self, grove):
        x = self.loc[0]+moves[self.dirIndex][0]
        y = self.loc[1]+moves[self.dirIndex][1]
        if not grove.inGrove((x,y)):
            if x==0:
                x = grove.rowRanges[y][1]
            elif y == 0:
                y = grove.yCount - 2
            elif y == grove.yCount - 1:
                y = 1
            elif x > grove.rowRanges[y][1]:
                x = 1
        self.loc =(x,y)
    def __repr__(self):
        print (self.loc)

class Grove:
    def __init__(self):
        self.rowRanges = []
        self.yCount = 0
        self.xCount = 0
    def addTextRow(self, text):
        start = None
        end = None
        for index in range(0,len(text)):
            if text[index] != "#":
                if start == None:
                    start = index
            elif start and not end and text[index] == "#":
                end = index-1
        self.rowRanges.append((start,end))
        self.yCount = len(self.rowRanges)
        self.xCount = max(end, self.xCount)
    def inGrove(self, location):
        if location[1] < 0 or location[1] >= len(self.rowRanges):
            return False
        if location[0] < self.rowRanges[location[1]][0]:
            return False
        if location[0] > self.rowRanges[location[1]][1]:
            return False
        return True

class WeatherTracker:
    def __init__(self):
        self.blizzards = []
        self.occupied = {}
    def addBlizzard(self, blizzard):
        self.blizzards.append(blizzard)
        self.occupied[blizzard.loc] = symbol[blizzard.dirIndex]
    def oneStep(self, grove):
        self.occupied = {}
        for b in self.blizzards:
            b.oneStep(grove)
            self.occupied[b.loc] = symbol[b.dirIndex]
    def isSafe(self, loc):
        return loc not in self.occupied
    def showBliz(self, grove):
        for y in range(0, grove.yCount):
            myStr = ""
            for x in range(0, grove.xCount+2):
                if not grove.inGrove((x,y)):
                    myStr += "#"
                elif (x,y) in self.occupied:
                    myStr += self.occupied[(x,y)]
                else:
                    myStr += " "
            print (myStr)
    def showAccessible(self, grove, accessible):
        for y in range(0, grove.yCount):
            myStr = ""
            for x in range(0, grove.xCount+2):
                if not grove.inGrove((x,y)):
                    myStr += "#"
                elif (x,y) in accessible:
                    myStr += "X"
                else:
                    myStr += " "
            print (myStr)
    

clear()
grove = Grove()
weather = WeatherTracker()

file = open("advent2022_data24.txt","r")
for line in file:
    line = line.replace("\n","")
    for charIndex in range(0, len(line)):
        char = line[charIndex]
        if char in symbol:
            weather.addBlizzard(Blizzard((charIndex, grove.yCount),char))
    grove.addTextRow(line)
    
    
start = (grove.rowRanges[0][0], 0)
finish = (grove.rowRanges[-1][0], grove.yCount-1)

begin = [start,finish,start]
ending = [finish,start,finish]
turn = 0

for it in range(0,3):
    accessible = [begin[it]]
    final = ending[it]

    while final not in accessible:
        turn += 1
        print (UP * (grove.yCount+4))
        print ("Turn #",turn)
        print (begin[it]," to ", final )
        weather.oneStep(grove)
        weather.showAccessible(grove, accessible)
        newAccessible = []
        for a in accessible:
            for m in moves:
                spot = (a[0] + m[0],a[1] + m[1])
                if grove.inGrove(spot) and spot not in newAccessible and weather.isSafe(spot):
                    newAccessible.append(spot)
        accessible = newAccessible
        #a = input()
        
    print ("End reached in {} turns".format(turn))


        