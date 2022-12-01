file = open("advent2022_data1.txt","r")

class Elf:
    def __init__(self):
        self.cal = 0
    def addCal(self,cal):
        self.cal += cal
    def __lt__(self,other):
        return self.cal<other.cal

elves = [Elf()]
for line in file:
    data = line.split("\n")[0]
    if len(data):
        elves[-1].addCal(int(data))
    else:
        elves.append(Elf())

elves.sort(reverse=True)

print ("Part 1",elves[0].cal)
print ("Part 2 {}+{}+{} = {}".format(
    elves[0].cal, elves[1].cal, elves[2].cal,
    elves[0].cal + elves[1].cal + elves[2].cal))
        
    
