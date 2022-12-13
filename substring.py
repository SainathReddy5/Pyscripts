s = input()

res = [ s[i: j] for i in range(len(s)) for j in range(i + 1, len(s) + 1)]
res2 =[x for x in res if len(x) >= 2]

for i in res2:
    if i == i[::-1]:
        print('pal')
        quit()
        pass
print('no')    