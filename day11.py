from os import system, name
from time import sleep
import re

def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

monkeys = []
class Monkey:
    def __init__(self, monkeyNum):
        self.num = monkeyNum
        self.items = []
        self.operation = None
        self.opNum = 0
        self.testDiv = 0
        self.trueTarg = -1
        self.falseTarg = -1
        self.itemsProcessed = 0
    def processItems(self):
        while len(self.items) > 0:
            i = self.items.pop(0)
            self.itemsProcessed += 1
            if self.operation == "square":
                i = i*i
            elif self.operation == "mult":
                i = i*self.opNum
            elif self.operation == "add":
                i = i+self.opNum
            i = int(i/3)
            if i % self.testDiv == 0:
                monkeys[self.trueTarg].giveItem(i)
            else:
                monkeys[self.falseTarg].giveItem(i)
    def giveItem(self, i):
        self.items.append(i)
    def show(self):
        print ("Monkey {}, itemsProcessed:{}".format(self.num,self.itemsProcessed) )
    def __lt__(self,other):
        return self.itemsProcessed < other.itemsProcessed

clock = 0
file = open("advent2022_data11.txt","r")

clear()
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
                    monkeys[currMonkey].items.append(int(i))
        elif "Operation" in data:
            if data[-1] == "old":
                print ("Using op old*old")
                monkeys[currMonkey].operation = "square"
            elif "*" in data:
                print ("Using op * {}".format( int(data[-1]) ))
                monkeys[currMonkey].operation = "mult"
                monkeys[currMonkey].opNum = int(data[-1])
            else:
                print ("Using op + {}".format(int(data[-1])))
                monkeys[currMonkey].operation = "add"
                monkeys[currMonkey].opNum = int(data[-1])
        elif "Test" in data:
            monkeys[currMonkey].testDiv = int(data[-1])
        elif "true" in data:
            monkeys[currMonkey].trueTarg = int(data[-1])
        elif "false" in data:
            monkeys[currMonkey].falseTarg = int(data[-1])

print ("Init\n====")
for m in monkeys:
    m.show()

for x in range(0,20):
    for m in monkeys:
        m.processItems()
    print ("Round {}\n=======".format(x+1))
    for m in monkeys:
        m.show()
        
monkeys.sort()
print ("Final\n=====".format(x+1))
for m in monkeys:
    m.show()

print ("Score = {}".format(monkeys[-1].itemsProcessed * monkeys[-2].itemsProcessed))