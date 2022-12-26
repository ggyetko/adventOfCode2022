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

allDirs = [(-1,-1),(0,-1),( 1,-1),(-1,1),(0,1),(1,1),(-1,0),(1,0)]
dirChoices = []
class DirChoice:
    def __init__(self, empties, move):
        self.empties = empties
        self.move = move
       
class Elf:
    def __init__(self, loc, num):
        self.loc = loc
        self.prop = None
        self.num = num
    def __repr__(self):
        return "{}: {}->{}".format(self.num,self.loc,self.prop)
    def setProposal(self, dirCycle, locations):
        self.prop = None
        empty = True
        # elf only moves if he has at least one neighbour in surrounding 8 spots
        for check in allDirs:
            if (self.loc[0]+check[0], self.loc[1]+check[1]) in locations:
                empty = False
                break
        if not empty:
            # elf goes through all possible directions, looking for first empty side
            for dir in dirCycle:
                empty = True
                for check in dir.empties:
                    if (self.loc[0]+check[0], self.loc[1]+check[1]) in locations:
                        empty = False
                        break
                if empty:
                    self.prop = (self.loc[0]+dir.move[0], self.loc[1]+dir.move[1])
                    break
        return self.prop
    def move(self):
        if self.prop != None:
            self.loc = self.prop
            self.prop = None

    def clearProposal(self):
        self.prop = None

class Grove:
    def __init__(self):
        self.elves = []
    def addElf(self, newElf):
        self.elves.append(newElf)
    def show(self):
        yMax = -1000000
        yMin = 1000000
        xMax = -1000000
        xMin = 1000000
        for elf in self.elves:
            yMax = max(yMax, elf.loc[1]) 
            yMin = min(yMin, elf.loc[1]) 
            xMax = max(xMax, elf.loc[0]) 
            xMin = min(xMin, elf.loc[0])
        locations = {}
        for elf in self.elves:
            locations[elf.loc] = elf.num
        xSize = xMax-xMin+1
        ySize = yMax-yMin+1
        print ("GROVE size={}x{} empties={}\n=====".format(xMax-xMin+1,yMax-yMin+1, xSize*ySize-len(self.elves)))
        for y in range(yMin, yMax+1):
            row = ""
            for x in range(xMin, xMax+1):
                if (x,y) in locations:
                    row += "#" #str(locations[(x,y)])
                else:
                    row += "."
            print (row)
    def doRound(self, dirCycle):
        locations = []
        proposalDict = {}
        # set easy-access location matrix
        for elf in self.elves:
            locations.append(elf.loc)
        # set proposals (with rejections on collisions)
        for elf in self.elves:
            proposalLoc = elf.setProposal(dirCycle, locations)
            if proposalLoc in proposalDict:
                elf.clearProposal()
                proposalDict[proposalLoc].clearProposal()
                del proposalDict[proposalLoc]
            else:
                proposalDict[proposalLoc] = elf
        # move everybody
        for elf in self.elves:
            elf.move()

                
dirChoices.append(DirChoice( [(-1,-1),(0,-1),( 1,-1)], ( 0,-1)))  #North
dirChoices.append(DirChoice( [(-1,1) ,(0,1) ,( 1,1 )], (0 , 1)))  #South
dirChoices.append(DirChoice( [(-1,-1),(-1,0),(-1,1 )], (-1, 0)))  #West
dirChoices.append(DirChoice( [(1,-1) ,(1,0) ,(1 ,1 )], ( 1, 0) )) #East

clear()
grove = Grove()
file = open("advent2022_data23.txt","r")
y = 0
elf = 0
for line in file:
    data = line.replace("\n","")
    for xIndex in range(0, len(data)):
        if data[xIndex] == "#":
            grove.addElf(Elf((xIndex,y), elf))
            elf += 1
    y+=1

for elf in grove.elves:
    print (elf)

grove.show()
for turn in range(0,10):
    grove.doRound(dirChoices)
    dirChoices.append(dirChoices.pop(0))

grove.show()

