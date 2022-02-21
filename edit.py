from stringcolor import *
def Display(row):
    for i in row:
        print(i, end=" ")
        
def editDistance(source, target):
    for i in source:
        print(i)
    slen = len(source)
    tlen = len(target)
    
    D = []
    for i in range(slen + 1):
        tmp = []
        print("first loop")
        for j in range(tlen + 1):
            tmp.append(0)
        D.append(tmp)
    print(cs(D,"red"))
    for i in range(1, slen + 1):
        print("second loop")
        D[i][0] = D[i-1][0] + 1
    print(cs(D,"red"))
    for j in range(1, tlen + 1):
        print("third loop")
        D[0][j] = D[0][j-1] + 1
    print(cs(D,"red"))
    for i in range(1, slen + 1):
        print("forth loop")
        for j in range(1, tlen + 1):
            if source[i-1] == target[j-1]:
                D[i][j] = D[i-1][j-1]
            else:
                D[i][j] = min(D[i-1][j] + 1,
                D[i][j-1] + 1,
                D[i-1][j-1] + 2)
    print(cs(D,"red"))
    Display(D)
def recursiveEditDistance(source, target, slen, tlen):
    if slen == 0:
        return tlen
    if tlen == 0:
        return slen
    for i in source:
        if source[slen - 1] == target[tlen - 1]:
            return recursiveEditDistance(source, target, slen - 1, tlen - 1)
    return min(recursiveEditDistance(source, target, slen, tlen - 1) + 1,
              recursiveEditDistance(source, target, slen - 1, tlen) + 1,
                recursiveEditDistance(source, target, slen - 1, tlen - 1) + 2)

city=['lahore','execution']
count=dict()
for i in city:
    x=recursiveEditDistance(i, "lahore", len(i), len("execution"))
    count[i]=x
print(count)
print(min(count, key=count.get))
