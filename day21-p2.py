from os import system,name
import re

def clear():
    _ = system('clear')

monkeyDict = {}

class Operation:
    def __init__(self, op, value):
        self.op = op
        self.value = value
    def __str__(self):
        print (op,value)
    def __repr__(self):
        return self.op + str(self.value)

class Monkey:
    def __init__(self, name):
        self.value = None
        self.name = name
        self.operands = []
        self.operation = ""
    def setValue(self, value):
        self.value = value
    def setOps(self, op1, op2, operation):
        self.operands = [op1, op2]
        self.operation = operation
    def getValue(self, indent):
        if self.value != None:
            if indent:
                print (" "*indent,self.name,"=",self.value)
            return self.value
        if indent:
            print (" "*indent,self.name,"=",self.operands[0],self.operation,self.operands[1])
        o1 = monkeyDict[self.operands[0]].getValue(indent + 1 if indent else None)
        o2 = monkeyDict[self.operands[1]].getValue(indent + 1 if indent else None)
        if type(o1) == type([]):
            if self.operation == "+":
                o1.insert(0,Operation("-",o2)) 
            if self.operation == "-":
                o1.insert(0,Operation("+",o2)) 
            if self.operation == "*":
                o1.insert(0,Operation("/",o2)) 
            if self.operation == "/":
                o1.insert(0,Operation("*",o2))
            if self.operation == "?":
                o1.insert(0,Operation("",o2)) 
            self.value = o1
        elif type(o2) == type([]):
            if self.operation == "+":
                o2.insert(0,Operation("-",o1)) 
            if self.operation == "-":
                o2.insert(0,Operation("+",o1)) 
                o2.insert(0,Operation("*",-1)) 
            if self.operation == "*":
                o2.insert(0,Operation("/",o1)) 
            if self.operation == "/":
                o2.insert(0,Operation("//",o1)) 
            if self.operation == "?":
                o2.insert(0,Operation("",o1)) 
            self.value = o2
        else:
            if self.operation == "+":
                self.value = o1 + o2
            if self.operation == "-":
                self.value = o1 - o2
            if self.operation == "*":
                self.value = o1 * o2
            if self.operation == "/":
                self.value = o1 / o2
            if self.operation == "?":
                print (o1,"=",o2,"?")
                self.value = (o1 == o2)
        return self.value
        
clear()
file = open("advent2022_data21.txt","r")
for line in file:
    data = re.split(":| |\n", line)
    m = Monkey(data[0])
    if data[2].isalpha():
        if data[0] == "root":
            m.setOps(data[2], data[4], "?")
        else:
            m.setOps(data[2], data[4], data[3])
    else:
        if data[0] == "humn":
            m.setValue([])
        else:
            m.setValue(int(data[2]))
    monkeyDict[data[0]] = m
file.close()

operations = monkeyDict["root"].getValue(1)

print ("\nReverse the operations:\n-----------------------\n")
value = None
for op in operations:
    print (value, op.op, op.value, end="")
    if op.op == "":
        value = op.value
    elif op.op == "+":
        value += op.value
    elif op.op == "-":
        value -= op.value
    elif op.op == "*":
        value *= op.value
    elif op.op == "/":
        value /= op.value
    elif op.op == "//":
        value = op.value / value
    print (" = ",value)
print (value)
        
print ("\nRetest with:",value,"\n")

monkeyDict = {}
file = open("advent2022_data21.txt","r")
for line in file:
    data = re.split(":| |\n", line)
    m = Monkey(data[0])
    if data[2].isalpha():
        if data[0] == "root":
            m.setOps(data[2], data[4], "?")
        else:
            m.setOps(data[2], data[4], data[3])
    else:
        if data[0] == "humn":
            m.setValue(value)
        else:
            m.setValue(int(data[2]))
    monkeyDict[data[0]] = m
file.close()

print ("Result:")
print (monkeyDict["root"].getValue(0))
print ("The human must give the input:",value)