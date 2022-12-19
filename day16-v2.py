from os import system, name
import re
from itertools import permutations

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

valves = {}
valveFlowList = ["AA"]
mostFlow = 0

class Valve:
    def __init__(self, name, flow, neighbours):
        self.name = name
        self.flow = flow
        self.neighbours = neighbours
        self.distances = {}
        self.open = False
    def show(self):
        print ("Valve {} {} FLOW: {:-2} Connects to:{}".format(self.name,self.open,self.flow,self.neighbours))
    def createDistances(self):
        global valveFlowList
        global valves
        distance = 0
        visited = {}
        frontLine = {self.name : 0}
        while len(self.distances) < len(valveFlowList) - 1:
            newValves = {}
            distance += 1
            for v in frontLine:
                currValve = valves[v]
                for n in currValve.neighbours:
                    if n not in frontLine and n not in visited:
                        newValves[n] = distance
                        if n in valveFlowList:
                            self.distances[n] = distance + 1

            visited.update(frontLine)
            frontLine = newValves
    def getBestFlow(self, timeLeft):
        global valves
        bestFlow = 0
        bestValve = ""
        for v in self.distances:
            potentialFlow = (timeLeft - self.distances[v] - 1) * valves[v].flow
            print (v, potentialFlow, bestFlow, bestValve)
            if potentialFlow > bestFlow:
                bestFlow = potentialFlow
                bestValve = v
        return bestValve

def runTrial(order):
    totalFlow = 0
    currValve = valves["AA"]
    timeLeft = 30
    for move in order:
        nextValveName = move
        timeToTurnNextValve = currValve.distances[nextValveName]
        timeLeft -= timeToTurnNextValve
        currValve = valves[nextValveName]
        totalFlow += timeLeft*currValve.flow
    return totalFlow

def testAllSuborders(currentOrder, remainingValves, timeRemaining):
    global mostFlow
    doAnyFit = False
    for r in remainingValves:
        timeToReachR =  valves[currentOrder[-1]].distances[r]
        if timeRemaining > timeToReachR:
            doAnyFit = True
            forward = remainingValves.copy()
            forward.remove (r)
            testAllSuborders(currentOrder + [r], forward, timeRemaining - timeToReachR)
    if not doAnyFit:
        thisFlow = runTrial(currentOrder[1:])
        if (thisFlow > mostFlow):
            mostFlow = thisFlow
            print ("Highest Flow so far", mostFlow, currentOrder)

file = open("advent2022_data16.txt","r")
for line in file:
    data = re.split(" |,|=|;|\n", line)
    name = data[1]
    flow = int(data[5])
    neighbours = []
    for x in range(11,len(data),2):
        neighbours.append(data[x])
    valves[name] = Valve(name, flow, neighbours)
    if flow:
        valveFlowList.append(name)
    
for v in valves:
    valves[v].createDistances()

valveFlowList.remove("AA")
options = len(valveFlowList)
print(valveFlowList)

testAllSuborders(["AA"], valveFlowList, 30)
print ("Highest Flow:", mostFlow)