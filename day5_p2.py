numStacks = 0
crateStacks = []

def printAll():
    for c in range(0,len(crateStacks)):
        print (c+1," ",crateStacks[c])
def printTops():
    tops = ""
    for c in crateStacks:
        tops += c[-1]
    print ("Tops only:",tops)
    
lines = []
file = open("advent2022_data05.txt","r")
for line in file:
    if "1" in line:
        break
    else:
        lines.append(line)
print (lines)

for num in line:
    if num.isdigit() and int(num) > numStacks:
        numStacks = int(num)

for index in range (0,numStacks):
    crateStacks.append([])

for index in range(len(lines)-1, -1, -1):
    print ("Index:",index)
    for crateIndex in range (0, numStacks):
        textCol = 1 + 4*crateIndex
        print ("    Column:",textCol)
        if lines[index][textCol] != " ":
            print ('Adding', lines[index][textCol])
            crateStacks[crateIndex].append(lines[index][textCol])
    
printAll()

while 1:
    data = file.readline()
    if len(data) == 0:
        break
    if data == "\n":
        continue
    print (data)
    command = data.split()
    moves = int(command[1])
    source = int(command[3])-1
    dest = int(command[5])-1
    temp = []
    for m in range(0,moves):
        temp.append(crateStacks[source].pop())
    for m in range(0,moves):
        crateStacks[dest].append(temp.pop())
    printAll()
    
printTops()