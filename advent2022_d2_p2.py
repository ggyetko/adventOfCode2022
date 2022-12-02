resultDict = {"X":0, "Y":1, "Z":2}  # array position for lose/draw/win (also, points for same if you x3)
calcDict = {"A":["C","A","B"], "B":["A","B","C"], "C":["B","C","A"]} # map lose/draw/win into this array
pointsDict = {"A":1,"B":2,"C":3}

file = open("advent2022_data02.txt","r")

pts = 0
for line in file:
    them = line[0]
    me = calcDict[them][resultDict[line[2]]]
    pts += pointsDict[me] + resultDict[line[2]] * 3

print ("Total points:",pts)

    