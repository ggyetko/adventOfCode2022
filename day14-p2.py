from os import system, name

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
            # the row needs one column on either side of the known limits
            row = ["."] * (3 + maxx - minx)
            self.grid.append(row)
        self.maxy = maxy
        self.minx = minx-1
        self.maxx = maxx
        self.sandTotal = 0
    def addLine(self,x1,y1,x2,y2):
        if x1 == x2:
            for y in range(min(y1,y2),max(y1,y2)+1):
                self.grid[y][x1-self.minx] = BLUE+"#"+WHITE
        elif y1 == y2:
            for x in range(min(x1,x2),max(x1,x2)+1):
                self.grid[y1][x-self.minx] = BLUE+"#"+WHITE
    def dropSandFrom(self,x,y):
        moved = False
        while y < maxy:
            if self.grid[y+1][x-self.minx] == ".":
                moved = True
                y += 1
            elif self.grid[y+1][x-1-self.minx] == ".":
                moved = True
                y += 1
                x -= 1
            elif self.grid[y+1][x+1-self.minx] == ".":
                moved = True
                y += 1
                x += 1
            else:
                self.grid[y][x-self.minx] = YELLOW+"o"+WHITE
                self.sandTotal += 1
                if moved == False:
                    return False
                return True
        # the program failed if sand falls off the edge in Part 2
        print ("Failure! Final:",x,y)    
        print ("X edges:", self.minx, self.maxx)
        exit(1)
        return None
    def show(self):
        print(UP*(self.maxy+3))
        for y in self.grid:
            row = ""
            for x in y:
                row += x
            print (row)
        print("Total Sand:",self.sandTotal)

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
    
maxy += 2    # room for the infinite floor
maxx += maxy # widen the space for a super huge cone of sand 
minx -= maxy # widen this, too
    
grid = Grid(minx, maxx, maxy)
for line in allLines:
    for segIndex in range(0,len(line)-1):
        grid.addLine(line[segIndex][0],line[segIndex][1],line[segIndex+1][0],line[segIndex+1][1])

grid.addLine(minx,maxy,maxx,maxy) #infinite line along bottom

clear()
grid.show()

while grid.dropSandFrom(500,0):
    if grid.sandTotal % 50 == 0:  # print out every 200 or it's too slow to watch
        grid.show()

grid.show()