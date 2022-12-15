import sys
import string
from os import system, name
from time import sleep

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

class Grid():
    def __init__(self,minx,maxx,maxy):
        self.grid = []
        for row in range(0,maxy+1):
            row = ["."] * (3 + maxx - minx)
            self.grid.append(row)
        self.maxy = maxy
        self.minx = minx-1
        self.sandTotal = 0
        self.lastPlaced = 0
        self.lastCentre = -100
    def addLine(self,x1,y1,x2,y2):
        if x1 == x2:
            for y in range(min(y1,y2),max(y1,y2)+1):
                self.grid[y][x1-self.minx] = BLUE+"#"+WHITE
        elif y1 == y2:
            for x in range(min(x1,x2),max(x1,x2)+1):
                self.grid[y1][x-self.minx] = BLUE+"#"+WHITE
    def dropSandFrom(self,x,y):
        while y < maxy:
            if self.grid[y+1][x-self.minx] == ".":
                y += 1
            elif self.grid[y+1][x-1-self.minx] == ".":
                y += 1
                x -= 1
            elif self.grid[y+1][x+1-self.minx] == ".":
                y += 1
                x += 1
            else:
                self.grid[y][x-self.minx] = YELLOW+"o"+WHITE
                self.sandTotal += 1
                self.lastPlaced = y
                return True
        return False
    def show(self, viewRadius):
        print(UP*(self.maxy+3))
        # Is the current centre row going to show the new drop?
        startRow = self.lastCentre - viewRadius
        endRow = self.lastCentre + viewRadius
        if self.lastPlaced < startRow or self.lastPlaced > endRow:
            self.lastCentre = max(min(self.lastPlaced,self.maxy-viewRadius+1),viewRadius)
            startRow = self.lastCentre - viewRadius
            endRow = self.lastCentre + viewRadius
        for yIndex in range(startRow, endRow):
            row = ""
            for x in self.grid[yIndex]:
                row += x
            print (row)
        print("Total Sand:",self.sandTotal, "Centre Row:", self.lastCentre)

clear()
file = open("advent2022_data14.txt","r")

allLines = []
minx = 500
maxx = 0
maxy = 0
for line in file:
    line = line.replace("\n","")
    data = line.split(" -> ")
    segments = []
    for d in data:
        xy = d.split(",")
        segments.append((int(xy[0]),int(xy[1])))
        minx = min(segments[-1][0], minx)
        maxx = max(segments[-1][0], maxx)
        maxy = max(segments[-1][1], maxy)
    allLines.append(segments)
    
grid = Grid(minx, maxx, maxy)
for line in allLines:
    for segIndex in range(0,len(line)-1):
        grid.addLine(line[segIndex][0],line[segIndex][1],line[segIndex+1][0],line[segIndex+1][1])

clear()
viewRadius = 30
if len(sys.argv) == 2:
    if sys.argv[1].isnumeric():
        viewRadius = int(sys.argv[1])
grid.show(viewRadius)

while grid.dropSandFrom(500,0):
    grid.show(viewRadius)
    sleep(0.01)
    
grid.show(viewRadius)