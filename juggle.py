from itertools import permutations

def print_list(l):
    for i in range(len(l)-1):
        print(l[i]+1,end=' ')
        pass
    print(l[-1]+1)


n = int(input())
l = [x for x in range(n)]

perm = list(permutations(l))
nl = []
for i in perm:
    nl.append(list(i))
    pass
nnl = []
for l in nl:
    c = 0
    for i,v in enumerate(l):
        if i != v:
            c += 1
            pass
        if c == len(l):
            nnl.append(l)

nnl.sort()
print_list(nnl[0])