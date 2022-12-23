from os import system, name
import re
from itertools import permutations

# 1556 too low
# 1566 too low

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

def getIntsInLine(line):
    nums = []
    data = re.split(" |:",line)
    for d in data:
        if d.isdigit():
            nums.append(int(d))
    return nums
    
LAST_TURN = 32
names = ["Ore","Clay","Obsidian","Geode"]

class BluePrint:
    def __init__(self, num, oreRCost, clayRCost, obsidianRCost, geodeRCost):
        self.myNum = num
        self.robotCosts = [oreRCost, clayRCost, obsidianRCost, geodeRCost]
        self.geodesCollected = 0
        self.oreRMax = max(oreRCost[0], clayRCost[0], obsidianRCost[0], geodeRCost[0])
        self.clayRMax = obsidianRCost[1]
        
    def turnsToPossible(self, nextRobot, robots, resources):
        needed = self.robotCosts[nextRobot].copy()
        for co in range(0, len(needed)):
            needed[co] -= resources[co]
        turns = 0
        for co  in range(0, len(needed)):
            if not needed[co]:
                continue
            if not robots[co]:
                return 1000000
            turns = max(turns,int((needed[co]+robots[co]-1)/robots[co]))
        return turns + 1
        
    def getMaxPossGeodes(self, robots, resources, time):
        max = resources[3]
        max += robots[3] * (LAST_TURN - time + 1)
        max += (LAST_TURN - time + 1)*(LAST_TURN - time + 2)/2
        return max

    def doTurn(self, robots, resources, time, history):
        robotBuildable = False
        #print (" "*time,"Time", time)
        if self.getMaxPossGeodes(robots, resources,time) < self.geodesCollected:
            return
        for nextRobot in range(len(self.robotCosts)-1,-1,-1):
            #print (" "*time,"Time", time, "may robot",nextRobot, robots, resources)
            if nextRobot == 0 and robots[0] >= self.oreRMax:
                #print ("NO!")
                continue
            if nextRobot == 1 and robots[1] >= self.clayRMax:
                #print ("NO!")
                continue
            turnsToSkip = self.turnsToPossible(nextRobot, robots, resources)
            if turnsToSkip + time > LAST_TURN:
                continue
            #print (" "*time,"Time", time, "try robot",nextRobot, turnsToSkip, "turns")
            newTime = time + turnsToSkip
            newResources = []
            for co in range (0,len(resources)):
                #print (co,resources[co], robots[co]*turnsToSkip, self.robotCosts[nextRobot][co])
                newResources.append(resources[co] + robots[co]*turnsToSkip - self.robotCosts[nextRobot][co])
            newRobots = robots.copy()
            newRobots[nextRobot] += 1
            robotBuildable = True

            h2 = history.copy()
            h2.append((nextRobot,newTime))
            self.doTurn(newRobots, newResources, newTime, h2)
            #print (" "*time,"Time", time, "finished robot",nextRobot)
            
            
        if not robotBuildable:
            #print ("History = ",history, "Time:",time)
            newResources = []
            turnsToSkip = LAST_TURN - time + 1
            for co in range (0,len(resources)):
                newResources.append(resources[co] + robots[co]*turnsToSkip - self.robotCosts[nextRobot][co])
            if len(history) < 5:
                print ("History = ",history,"=",newResources[3])
            if newResources[3] > self.geodesCollected:
                self.geodesCollected = newResources[3]
                print ("New High:",newResources[3])
            return
        
    def run(self):
        robots = [1,0,0,0]
        resources = [0,0,0,0]
        time = 1
        self.doTurn(robots, resources, time, [])
        print ("Geodes collected:",self.geodesCollected)
        
clear()

score = 1
file = open("advent2022_data19.txt","r")
for count in range(0,3):
    line = file.readline()
    data = getIntsInLine(line)
    #print (data)
    bpNum = data[0]
    ore4Ore = data[1]
    ore4Clay = data[2]
    ore4Ob = data[3]
    clay4Ob = data[4]
    ore4Geo = data[5]
    ob4Geo = data[6]
    b=BluePrint(bpNum, [ore4Ore,0,0,0], [ore4Clay,0,0,0], [ore4Ob,clay4Ob,0,0], [ore4Geo, 0, ob4Geo, 0])
    title = ("\nBlueprint #{}".format(bpNum))
    print (title+"\n"+"="*len(title))
    b.run()
    score *= b.geodesCollected
    
print ("\ntotal score:",score)