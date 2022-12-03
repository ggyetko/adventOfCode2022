import string 
alphaPrio = "0" + string.ascii_lowercase + string.ascii_uppercase

class Rucksack:
    def __init__(self, items):
        self.items = items
    def findMisplacedPrio(self):
        for x in self.items[:int(len(self.items)/2)]:
            if x in self.items[int(len(self.items)/2):]:
                return alphaPrio.index(x)
    def getPriorityOfBadgeInCommon(self, elf2, elf3):
        for x in self.items:
            if x in elf2.items and x in elf3.items:
                return alphaPrio.index(x)

file = open("advent2022_data03.txt","r")

rucksacks = []
misplacedSumPrio = 0
badgeSumPrio = 0
for line in file:
    rucksacks.append(Rucksack(line))
    misplacedSumPrio += rucksacks[-1].findMisplacedPrio()
    if len(rucksacks) % 3 == 0:
        badgeSumPrio += rucksacks[-1].getPriorityOfBadgeInCommon(rucksacks[-2],rucksacks[-3])

print ("Part 1")
print ("Misplaced Items. Sum of priorities:",misplacedSumPrio)

print ("Part 2")
print ("Badges in Common. Sum of priorities:",badgeSumPrio)