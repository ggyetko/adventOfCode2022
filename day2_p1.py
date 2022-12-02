translatDict = {"X":"A","Y":"B","Z":"C"} # turn XYZ into ABC
victoryDict = {"A":"C","B":"A","C":"B"}  # A beats C, B beats A, C beats B
pointsDict = {"A":1,"B":2,"C":3}

file = open("advent2022_data02.txt","r")

pts = 0
for line in file:
    them = line[0]
    me = translatDict[line[2]]
    pts += pointsDict[me]
    if me == them:
        pts += 3
    elif victoryDict[me] == them:
        pts += 6

print ("Total points:",pts)

    