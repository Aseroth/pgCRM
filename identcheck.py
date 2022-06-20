
def checkPesel(pesel):
    controlNumbers = [1,3,7,9,1,3,7,9,1,3,1]
    tempNumber=[]
    for x in range(len(pesel)):
        tempNumber.append(int(pesel[x])*controlNumbers[x])
    y=sum(tempNumber)
    y=str(y)
   
    if int(y[-1])==0:
        return True
    else:
        return False
    
    
def checkRegon(regon):
    wagi8 = [8,9,2,3,4,5,6,7]
    wagi11 = [2,4,8,5,0,9,7,3,6,1,2,4,8]
    tempNumber=[]
    if len(regon)<=9:
        for x in range(len(regon)-1):
            tempNumber.append(int(regon[x])*wagi8[x])
    elif len(regon)>8:
        for x in range(len(regon)-1):
            tempNumber.append(int(regon[x])*wagi11[x])
    y = sum(tempNumber)
    y = y%11
    if y == int(regon[-1]):
        return True
    else:
        return False
    

