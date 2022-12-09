import os

dirDict = {"U":(-1,0), "D":(1,0), "L":(0,-1), "R":(0,1)}

tailVisitedSpots = []
headLocation = (0,0)
tailLocations = []

def clear():
    if(os.name == 'posix'):
       os.system('clear')
    else:
       os.system('cls')

def show(title, radius, showTrail):
    print ('\033[F'*(radius*2+2))
    print (title)
    for y in range(headLocation[1]-radius, headLocation[1]+radius):
        row = ""
        for x in range(headLocation[0]-radius, headLocation[0]+radius):
            tup = (x,y)
            if headLocation == tup:
                row += "H"
            elif tup in tailLocations:
                row += str(tailLocations.index(tup)+1)
            elif showTrail and (tup in tailVisitedSpots):
                row += "#"
            else:
                row += "."
        print (row)


def getNewTail(hTuple, tTuple):
    diffx = hTuple[0] - tTuple[0]
    diffy = hTuple[1] - tTuple[1]
    if abs(diffx) > 1 or abs(diffy) > 1:
        newX = tTuple[0]
        newY = tTuple[1]
        if diffx > 0:
            newX += 1
        elif diffx < 0:
            newX -= 1
        if diffy > 0:
            newY += 1
        elif diffy < 0:
            newY -= 1
        return (newX, newY)
    else:
        return tTuple
    
print("Part 1: 1 tail pieces")
print("Part 2: 9 tail pieces")
print("How many tail pieces?")
tailLength = input() 
tailLength = int(tailLength)
tailLocations = [(0,0)]*tailLength

print("Display progress - This is very slow for tail length of 1! - (y/N)?")
display = input()
radius = 15
print("Radius of Display(15)?")
user = input()
if user.isnumeric():
    radius = int(user)

clear()
file = open("advent2022_data09.txt","r")
movecounter = 0
for line in file:
    dir = dirDict[line.split()[0]]
    moves = int(line.split()[1])
    for m in range(0,moves):
        headLocation = (headLocation[0]+dir[0], headLocation[1]+dir[1])
        for tailIndex in range(0,tailLength):
            movecounter += 1
            if tailIndex == 0:
                tailLocations[tailIndex] = getNewTail(headLocation,tailLocations[tailIndex])
            else:
                tailLocations[tailIndex] = getNewTail(tailLocations[tailIndex-1],tailLocations[tailIndex])
        if tailLocations[-1] not in tailVisitedSpots:
            tailVisitedSpots.append(tailLocations[-1])
        if display == "y":
            show(str(movecounter)+" CMD:"+line.replace("\n",""),radius,True)
            
print ("With a tail length of {}, the end of the tail visits {} places".format(tailLength,len(tailVisitedSpots)))

show(str(movecounter),radius,True)