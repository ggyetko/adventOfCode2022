from functools import reduce
import operator
grid = []                                 # Grid of Tree Heights
direction = [(0,1),(0,-1),(1,0),(-1,0)]   # single step in every direction

file = open("advent2022_data08.txt","r")
height = 0
width = 0
for line in file:
    grid.append(line.replace("\n",""))
    width = len(line)
    height += 1

bestScenicScore = 0
visibleCount = 0
for y in range(0, height):
    for x in range (0,width):
        finalVisible = False # assume NOT VISIBLE until one of the directions is found visible
        scenicDists = []     # we will put one distance in here for each direction
        for d in direction:
            testX = x+d[0]
            testY = y+d[1]
            visible = True # assume VISIBLE until we find a tree blocking this direction
            scenicDist = 0 # each distance starts at zero and we count outwards from the treehouse
            while testX >= 0 and testX < width and testY >= 0 and testY < height:
                scenicDist += 1
                if int(grid[testY][testX]) >= int(grid[y][x]):
                    visible = False
                    break
                testX += d[0]
                testY += d[1]
            scenicDists.append(scenicDist)
            if visible:
                finalVisible = True
                #break - can't break here, Part2 needs to do all four directions
        if finalVisible:
            visibleCount += 1
        # the scenic "score" is the product of the four distances
        scenicScore = reduce(operator.mul,scenicDists)
        bestScenicScore = max(bestScenicScore, scenicScore)

print ("\nPart 1")
print ("Visible:",visibleCount)

print ("\nPart 2")
print ("Best for Part2:",bestScenicScore)