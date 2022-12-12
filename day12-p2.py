import string
from os import system, name
from time import sleep

def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

clear()
file = open("advent2022_data12.txt","r")

heights = string.ascii_lowercase

dirs = [(0,-1),(-1,0),(0,1),(1,0)]
analysed = {}
frontLine = {}
width = 0
height = 0
topoMap = []

WHITE = "\033[097m"
GREEN = "\033[092m"
RED   = "\033[091m"
BLUE  = "\033[094m"
YELLOW= "\033[093m"
CYAN  = "\033[093m"

def showGrid():
    print ("\033[A"*(height+3),WHITE)
    ffDist = 0
    for y in range(0,height):
        row = ""
        for x in range(0,width):
            tup =(x,y)
            if tup == start:
                row += RED+"S"+WHITE
            elif tup in frontLine:
                ffDist = frontLine[tup]
                if tup == end:
                    row += RED+"X"+WHITE # markers[frontLine[tup]]
                else:
                    row += BLUE+"X"+WHITE # markers[frontLine[tup]]
            elif tup in analysed:
                row += GREEN+"#"+WHITE # markers[analysed[tup]]
            else:
                if tup == end:
                    row += RED+topoMap[y][x]+WHITE
                else:
                    row += topoMap[y][x]
        print (row)
    print ("\nDistance from 'S' to all 'X's:",ffDist)
    sleep(0.05)


def isLegalPoint(tup):
    if tup[0] < 0 or tup[0] >= width or tup[1] < 0 or tup[1] >= height:
        return False
    return True

lineNum = 0
start = (-1,-1)
end = (-1,-1)
for line in file:
    data = line.replace("\n","")
    if "S" in data:
        start = (data.index("S"),lineNum)
        data = data.replace("S","a")
    if "E" in data:
        end = (data.index("E"),lineNum)
        data = data.replace("E","z")
    topoMap.append(data)
    lineNum += 1
width = len(topoMap[0])
height = len(topoMap)
frontLine = {end:0}
showGrid()

foundIt = None
while foundIt == None:
    nextBunch = {}
    for point in frontLine:
        for dir in dirs:
            testPoint = (point[0]+dir[0], point[1]+dir[1])
            if isLegalPoint(testPoint) and testPoint not in frontLine and testPoint not in analysed:
                if heights.index(topoMap[testPoint[1]][testPoint[0]]) - heights.index(topoMap[point[1]][point[0]]) >= -1:
                    nextBunch[testPoint] = frontLine[point] + 1
                    if topoMap[testPoint[1]][testPoint[0]] == "a" and foundIt == None:
                        foundIt = testPoint
    analysed.update(frontLine)
    frontLine = nextBunch
    showGrid()
    
print (foundIt, frontLine[foundIt])
