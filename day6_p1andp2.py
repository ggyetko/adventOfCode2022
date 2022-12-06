line = ""

class Packet:
    def __init__(self,data):
        self.data = data
    def findStartOfSomethingIndex(self, sizeOfString, distinctChars):
        for index in range(0,len(self.data)-sizeOfString):
            uniqueChars = ""
            checkString = self.data[index:index+sizeOfString]
            #print (checkString)
            for char in checkString:
                if char not in uniqueChars:
                    uniqueChars += char
            #print (uniqueChars)
            if len(uniqueChars) == distinctChars:
                return (index + sizeOfString)
    def findIndexAfterStartOfPacket(self):
        return self.findStartOfSomethingIndex(4, 4)
    def findIndexAfterStartOfMessage(self):
        return self.findStartOfSomethingIndex(14, 14)

file = open("advent2022_data06.txt","r")
p = Packet(file.readline())
print (p.data)
print ("First Packet-Start-Marker ends at:", p.findIndexAfterStartOfPacket())
print ("First Message-Start-Marker ends at:", p.findIndexAfterStartOfMessage())


