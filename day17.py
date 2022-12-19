from os import system, name
import re

# 3543 wrong guess too high

WHITE = "\033[097m"
GREEN = "\033[092m"
RED   = "\033[091m"
BLUE  = "\033[094m"
YELLOW= "\033[093m"
CYAN  = "\033[093m"
UP = "\033[A"

notBlueArray = [GREEN, WHITE, RED, BLUE, YELLOW, CYAN]

def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
        
class Grid:
    def __init__(self):
        self.grid = []
        self.highest = 0
    def placeRock(self, rock, x, y):
        #print ("Placing,",x,y,len(self.grid))
        for newRow in range(len(self.grid)-1, y+rock.tall):
            self.grid.append(["."]*7)
        for coord in rock.array:
            self.grid[y+coord[1]][x+coord[0]] = "#"
        self.highest = max(self.highest, y+rock.tall+1)
        #print ("Highest = ",self.highest)
    def isRoomForRock(self, rock, x, y):
        for coord in rock.array:
            checky = y+coord[1]
            checkx = x+coord[0]
            if checky < 0:
                return False
            if checky < len(self.grid):
                if self.grid[checky][checkx] != ".":
                    return False
        return True
    def show(self, rock, x, y):
        if rock != None:
            for newRow in range(len(self.grid)-1, y+rock.tall):
                self.grid.append(["."]*7)
            # add rock to grid
            for coord in rock.array:
                self.grid[y+coord[1]][x+coord[0]] = BLUE+"#"+WHITE

        print ("Grid\n====")
        for rowIndex in range(len(self.grid)-1, -1, -1):
            myStr = ""
            for c in self.grid[rowIndex]:
                myStr += c
            print (myStr)
        # add rock to grid
        if rock != None:
            for coord in rock.array:
                self.grid[y+coord[1]][x+coord[0]] = "."

class Rock:
    def __init__(self, array):
        self.array = array
        self.tall = 0
        self.wide = 0
        for coords in array:
            self.wide = max(self.wide, coords[0])
            self.tall = max(self.tall, coords[1])

rocks = [Rock([[0,0],[1,0],[2,0],[3,0]]),\
         Rock([[1,0],[0,1],[1,1],[2,1],[1,2]]),\
         Rock([[0,0],[1,0],[2,0],[2,1],[2,2]]),\
         Rock([[0,0],[0,1],[0,2],[0,3]]),\
         Rock([[0,0],[0,1],[1,0],[1,1]])]
         
file = open("advent2022_data17.txt","r")
jets = file.readline().replace("\n","")
rockCount = 0
jIndex = 0
currRock = None

grid = Grid()

while rockCount < 100000:
    # Place rock if necessary
    if currRock == None:
        currRock = rocks[rockCount % 5]
        currLoc = (2, grid.highest+3)
        rockCount += 1
    #grid.show(currRock, currLoc[0], currLoc[1])
    # move rock with wind
    wind = jets[jIndex]
    jIndex = (jIndex + 1) % len(jets)
    if jIndex == 0:
        print (grid.highest)
    if wind == "<":
        if currLoc[0] > 0 and grid.isRoomForRock(currRock, currLoc[0]-1, currLoc[1]):
            currLoc = (currLoc[0]-1, currLoc[1])
    elif wind == ">":
        if currLoc[0] + currRock.wide < 6 and grid.isRoomForRock(currRock, currLoc[0]+1, currLoc[1]):
            currLoc = (currLoc[0]+1, currLoc[1])
    # try to drop rock
    #grid.show(currRock, currLoc[0], currLoc[1])
    if grid.isRoomForRock(currRock, currLoc[0], currLoc[1]-1):
        currLoc = (currLoc[0], currLoc[1]-1)
    else:
        grid.placeRock(currRock, currLoc[0], currLoc[1])
        currRock = None

print (grid.highest)

        
    