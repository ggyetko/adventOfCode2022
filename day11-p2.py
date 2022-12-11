from os import system, name
import re

def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

monkeys = []       # keep track of monkeys
moduliNeeded = []  # during the start, find all the numbers I have to divide by later

class Item:
    def __init__(self, initNum):
        self.initNum = initNum # do not reference!  Only set during init pt 1, used in pt 2
        self.remainders = {}   # dictionary keyed off modulus, contains remainders
    def addModulus(self, modulus):
        self.remainders[modulus] = self.initNum % modulus  # only called once for each modulus at init pt 2
    def handleOperation(self, op, num):
        for r in self.remainders:
            oldRemainder = self.remainders[r]
            # you can just do all these ops to the remainder. Yay, math!
            if op == "square":
                self.remainders[r] = (oldRemainder*oldRemainder) % r
            elif op == "mult":
                self.remainders[r] = (oldRemainder*num) % r
            elif op == "add":
                self.remainders[r] = (oldRemainder+num) % r
    def isDivisibleBy(self, mod):
        # callers never need the remainder, just want to know if it's zero.
        return self.remainders[mod] == 0

class Monkey:
    def __init__(self, monkeyNum):
        self.num = monkeyNum
        self.items = []
        self.operation = ""  # my python-fu is not up to using a lambda f'n for this and opNum
        self.opNum = 0
        self.testDiv = 0
        self.trueTarg = -1
        self.falseTarg = -1
        self.itemsProcessed = 0
    def processModuliList(self, listOfMods):
        for i in self.items:
            for m in listOfMods:
                i.addModulus(m) # update the items' remainder lists in init pt 2
    def processItems(self):
        while len(self.items) > 0:
            i = self.items.pop(0)
            self.itemsProcessed += 1
            i.handleOperation(self.operation,self.opNum)
            if i.isDivisibleBy(self.testDiv):
                monkeys[self.trueTarg].giveItem(i)
            else:
                monkeys[self.falseTarg].giveItem(i)
    def giveItem(self, i):
        self.items.append(i)
    def show(self):
        print ("M# {}, items:{}".format(self.num,self.itemsProcessed) )
    def __lt__(self,other):
        return self.itemsProcessed < other.itemsProcessed

def showMonkeys(title):
    print(title)
    for m in monkeys:
        m.show()
        
# Init Part 1 - set up the Monkeys and empty Items (no remainders calculated)
file = open("advent2022_data11.txt","r")
currMonkey = -1
for line in file:
    data = re.split(" |:|,",line.replace("\n",""))
    if len(data) <= 1:
        currMonkey = -1
    elif currMonkey == -1:
        if "Monkey" in data:
            currMonkey = int(data[1])
            monkeys.append(Monkey(currMonkey))
    else:
        if "Starting" in data:
            for i in data:
                if i.isdigit():
                    monkeys[currMonkey].items.append(Item(int(i)))
        elif "Operation" in data:
            if data[-1] == "old":
                monkeys[currMonkey].operation = "square"
            elif "*" in data:
                monkeys[currMonkey].operation = "mult"
                monkeys[currMonkey].opNum = int(data[-1])
            else:
                monkeys[currMonkey].operation = "add"
                monkeys[currMonkey].opNum = int(data[-1])
        elif "Test" in data:
            monkeys[currMonkey].testDiv = int(data[-1])
            moduliNeeded.append(int(data[-1]))
        elif "true" in data:
            monkeys[currMonkey].trueTarg = int(data[-1])
        elif "false" in data:
            monkeys[currMonkey].falseTarg = int(data[-1])

# Init Part 2 - all moduli known, set up all remainders in Items
for m in monkeys:
    m.processModuliList(moduliNeeded)

# Begin the game
for x in range(0,10000):
    for m in monkeys:
        m.processItems()
    if x==19 or x % 1000 == 999:
        showMonkeys ("Round {}\n=======".format(x+1))

showMonkeys ("Round {}\n=======".format(x+1))

monkeys.sort()
print ("Score = {}".format(monkeys[-1].itemsProcessed * monkeys[-2].itemsProcessed))