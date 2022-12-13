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
            return True
        if i == len2:
            return False
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
sumOfCorrect = 0
count = 0
while 1:
    count += 1
    item1 = file.readline().replace("\n","")
    item2 = file.readline().replace("\n","")
    if len(item1)==0 or len(item2)==0:
        break
    file.readline() #blank
    
    list1 = breakIntoList(item1[1:-1])  # remove outer brackets
    list2 = breakIntoList(item2[1:-1])  # remove outer brackets
    if compare(list1,list2):
        sumOfCorrect += count

print ("Sum of Correct:",sumOfCorrect)