class ElfPair:
    def __init__(self, rangeStr1, rangeStr2):
        self.range1 = [int(x) for x in rangeStr1.split("-")]
        self.range2 = [int(x) for x in rangeStr2.split("-")]
    def isFullyOverlapped(self):
        if (self.range1[0] <= self.range2[0] and self.range1[1] >= self.range2[1]) or \
           (self.range2[0] <= self.range1[0] and self.range2[1] >= self.range1[1]):
            return True
        return False
    def isAnyOverlap(self):
        if self.range1[1] < self.range2[0] or self.range2[1] < self.range1[0]:
            return False
        return True
        

numFullyOverlapped = 0
numPartOverlapped = 0
file = open("advent2022_data04.txt","r")
for line in file:
    data = line.split(",")
    elf = ElfPair(data[0],data[1])
    if elf.isFullyOverlapped():
        numFullyOverlapped += 1
    if elf.isAnyOverlap():
        numPartOverlapped += 1

print ("Part 1")
print ("Elves Fully Overlapped:",numFullyOverlapped)
print ("Part 2")
print ("Elves Partially Overlapped",numPartOverlapped)
