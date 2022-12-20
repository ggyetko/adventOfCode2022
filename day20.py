numberDict = {}
array = []
indexOfZero = -1

file = open("advent2022_data20.txt","r")
co = 0
for line in file:
    numberDict[co] = int(line)
    array.append(co)
    if numberDict[co] == 0:
        indexOfZero = co
    co += 1

numEntries = co

for co in range(0,numEntries):
    startIndex = array.index(co)
    array.remove(co)
    newIndex = (startIndex+numberDict[co]) % len(array)
    array.insert(newIndex, co)

start = array.index(indexOfZero)
desired = [1000,2000,3000]
total = 0
for d in desired:
    total += numberDict[array[(start + d) % len(array)]]
    print ("adding ", numberDict[array[(start + d) % len(array)]])
print ("Total=",total)
