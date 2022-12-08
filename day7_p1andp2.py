# wrong answer 1529185 (too low)
# forgot about duplicate dirs

import re

fileSystem = {}

class FsEntry:
    def __init__(self, parentFs, name, isDir, size):
        self.name = name
        self.isDir = isDir
        self.entries = {}
        self.size = size
        self.parentFs = parentFs
    def add(self, fsEntry):
        self.entries[fsEntry.name] = fsEntry
    def getSize(self):
        if not self.isDir:
            return self.size
        else:
            sz = 0
            for e in self.entries:
                sz += self.entries[e].getSize()
            return sz
    def cd(self, name):
        if name == "..":
            return self.parentFs
        return self.entries[name]
    def show(self, indent):
        if self.isDir:
            print ("-"*indent,self.name,"DIR:",self.getSize())
            for e in self.entries:
                self.entries[e].show(indent+2)
        else:
            print ("-"*indent,self.name,self.getSize())
    def getPath(self):
        if self.name == "/":
            return "/"
        else:
            return self.parentFs.getPath()+self.name+"/"

root = FsEntry(None, "/", True, 0)
fileSystem["/"] = root
cwd = root

file = open("advent2022_data07.txt","r")
for line in file:
    #print (line)
    if "$" in line:
        # a command
        cmd = re.split(" |\n",line)
        #print (cmd)
        if cmd[1] == "cd":
            if cmd[2] == "/":
                cwd = root
            else:
                cwd = cwd.cd(cmd[2])
        elif cmd[1] == "ls":
            pass
        else:
            print("What")
            exit(0)
    else:
        # we must be in an "ls" output
        output = line.split()
        fn = output[1]
        if output[0] == "dir":
            newEntry = FsEntry(cwd,fn,True,0)
            cwd.add(newEntry)
            pathName = newEntry.getPath()
            print (pathName)
            fileSystem[pathName] = newEntry
        else:
            sz = int(output[0])
            cwd.add(FsEntry(cwd,fn,False,sz))
            
root.show(0)
print ("PART 1")
print ("SIZES")
sum = 0
for e in fileSystem:
    sz = fileSystem[e].getSize()
    if sz <= 100000:
        print (e,sz)
        sum += sz
print ("Size of all 100000 or less:",sum)

print ("PART 2")
totalMem = 70000000
neededMem = 30000000
currMemAvail = totalMem-fileSystem["/"].getSize()
mustFreeUp = neededMem-currMemAvail
print ("Need to free up:", mustFreeUp)
smallestSoFar = 70000000
for e in fileSystem:
    sz = fileSystem[e].getSize()
    if sz < smallestSoFar and sz >= mustFreeUp:
        print (e,sz)
        smallestSoFar = sz
