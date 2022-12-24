ll = open("input.txt", "r").readlines()
s = 0
l = []
for x in ll:
    if x == '\n':
        print(s)
        l.append(s)
        s = 0
    else:
        s += int(x)

print(sum(sorted(l)[-3:]))
