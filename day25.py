from os import system,name
import sys
import os
import re
from itertools import permutations
from time import sleep

WHITE = "\033[097m"
GREEN = "\033[092m"
RED   = "\033[091m"
BLUE  = "\033[094m"
YELLOW= "\033[093m"
CYAN  = "\033[093m"
UP = "\033[A"

def clear():
    _ = system('clear')

fiveDict = {"2":2, "1":1, "0":0, "-":-1, "=":-2}
def convertSnafuToDec(string):
    number = 0
    for co in range(0, len(string)):
        char = string[-1 * (co + 1)]
        number += fiveDict[char] * (5**co)
    print (string,number)
    return number
    
def getPossible(string, number, charsRemaining):
    maxNum = string + "2"*charsRemaining
    minNum = string + "="*charsRemaining
    if convertSnafuToDec(maxNum) >= number and convertSnafuToDec(minNum) <= number:
        return True

def convertDecToSnafu(number):
    leftMostPower = 0
    while 5**leftMostPower < number:
        leftMostPower += 1
    leftMostPower -= 1
    string = ""
    for digitPower in range(leftMostPower, -1, -1):
        print ("Digit {} String so far {}".format(digitPower, string))
        for key in fiveDict:
            myStr = string + key
            if getPossible(myStr, number, digitPower):
                string += key
                break
        print ("Digit {} String so far {}".format(digitPower, string))
    return string
            

file = open("advent2022_data25.txt","r")

sum = 0
for line in file:
    string = line.replace("\n","")
    number = convertSnafuToDec (string)
    sum += number
    
print ("Total is:",sum)
convertDecToSnafu(sum)
