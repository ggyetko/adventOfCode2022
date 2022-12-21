from os import system,name
import re

def clear():
    _ = system('clear')

monkeyDict = {}

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
            print (" "*indent,self.name,"=",self.value)
            return self.value
        print (" "*indent,self.name,"=",self.operands[0],self.operation,self.operands[1])
        o1 = monkeyDict[self.operands[0]].getValue(indent + 1)
        o2 = monkeyDict[self.operands[1]].getValue(indent + 1)
        if self.operation == "+":
            self.value = o1 + o2
        if self.operation == "-":
            self.value = o1 - o2
        if self.operation == "*":
            self.value = o1 * o2
        if self.operation == "/":
            self.value = o1 / o2
        return self.value
        
clear()
file = open("advent2022_data21.txt","r")
for line in file:
    data = re.split(":| |\n", line)
    m = Monkey(data[0])
    if data[2].isalpha():
        m.setOps(data[2], data[4], data[3])
    else:
        m.setValue(int(data[2]))
    monkeyDict[data[0]] = m

print ("Root monkey yells out",monkeyDict["root"].getValue(0))