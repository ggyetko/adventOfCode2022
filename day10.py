from os import system, name
from time import sleep
 
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

xReg = 1
clock = 1
sumOfProds = 0

file = open("advent2022_data10.txt","r")
clockCyclesLeft = 0
while True:
    #print ("During Clock {} X is {}".format(clock,xReg))
    if (clock+20) % 40 == 0:
        print ("During Clock {} X is {}".format(clock,xReg))
        sumOfProds += xReg * clock
    if clockCyclesLeft == 0:
        command = file.readline().split()
        if len(command) == 0:
            break
        if command[0] == "noop":
            clockCyclesLeft = 1
            nextXReg = xReg
        elif command[0] == "addx":
            clockCyclesLeft = 2
            nextXReg = xReg + int(command[1])
    clockCyclesLeft -= 1
    clock += 1
    if clockCyclesLeft == 0:
        xReg = nextXReg
       
print("Final: clock cycle {} X is {}".format(clock,xReg))
    
print("Product is:",sumOfProds)
    