def apply(l):
    nl = []
    for i in l:
        if i > 0:
            nl.append(i - 1) 
        else:
            nl.append(i)
    return nl       


def checkl(l):
    s = l[0]
    l = l[1:]
    s1 = l.count(1)
    s2 = l.count(2)
    s3 = l.count(3) 
    s4 = l.count(4) 
    s5 = l.count(5) 
    s6 = l.count(6)

    l = [s1,s2,s3,s4,s5,s6]

    while (l.count(0) < 3 ):
        if l.count(0) == 0:
            l = apply(l)
            s = s + 4
        if l.count(0) == 1:
            l = apply(l)
            s = s + 2
        if l.count(0) == 2:
            l = apply(l)
            s = s + 1
    return s

t = int(input())
for i in range(t):
    n = int(input())
    nl=[]
    for j in range(n):
        l = list(map(int,input().split()))
        nl.append(checkl(l))

    m = max(nl)
    if nl.count(m) > 1:
        print('tie')
    else:
        ind = nl.index(m)
        if ind == 0:
            print('raji')
        else:
            print(ind+1)   
