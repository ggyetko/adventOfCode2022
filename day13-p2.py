packets = []

class Packet:
    def __init__(self,string):
        self.string = string
    def __lt__(self, other):
        return compare(breakIntoList(self.string),breakIntoList(other.string))

def compare(list1, list2):
    if '' in list1:
        list1.remove('')
    if '' in list2:
        list2.remove('')
    len1 = len(list1)
    len2 = len(list2)
    if len1 == 0 and len2 > 0:
        return True
    elif len2 == 0 and len1 > 0:
        return False
    for i in range(0,max(len1,len2)):
        if i == len1:
            return True # matched up to here, and list1 is shorter - good!
        if i == len2:
            return False # matched up to here, and list2 is shorter - bad!
        if list1[i].isnumeric() and not list2[i].isnumeric():
            list1[i] = "["+list1[i]+"]"
        elif not list1[i].isnumeric() and list2[i].isnumeric():
            list2[i] = "["+list2[i]+"]"
        if list1[i].isnumeric() and list2[i].isnumeric():
            num1 = int(list1[i])
            num2 = int(list2[i])
            if num1 < num2:
                return True
            elif num1 > num2:
                return False
        elif not list1[i].isnumeric() and not list2[i].isnumeric():
            relist1 = breakIntoList(list1[i][1:-1])
            relist2 = breakIntoList(list2[i][1:-1])
            output = compare(relist1,relist2)
            if output == True:
                return True
            elif output == False:
                return False
    return None

def breakIntoList(myStr):
    myList = []
    depth = 0
    currString = ""
    for char in myStr:
        if depth == 0 and char == ",":
            myList.append(currString)
            currString = ""
        else:
            currString += char
            if char == "[":
                depth += 1
            elif char == "]":
                depth -= 1
    myList.append(currString)
    return myList

file = open("advent2022_data13.txt","r")
for line in file:
    line = line.replace("\n","")
    if len(line) > 1:
        packets.append(Packet(line))
packets.append(Packet("[[2]]"))
packets.append(Packet("[[6]]"))

packets.sort()

product = 1
for index in range(0, len(packets)):
    if packets[index].string == "[[2]]":
        product *= index + 1
    if packets[index].string == "[[6]]":
        product *= index + 1
    
print ("Product of inserted packet locations:",product)