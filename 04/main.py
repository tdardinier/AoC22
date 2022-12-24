f = open("test_input.txt", "r").readlines()
f = open("input.txt", "r").readlines()

pairs = []
for l in f:
    p = l[:-1].split(",")
    pa = p[0].split("-")
    pb = p[1].split("-")
    pairs.append((int(pa[0]), int(pa[1]), int(pb[0]), int(pb[1])))
print(pairs)

c1 = 0
c2 = 0
for (a1, a2, b1, b2) in pairs:
    if a1 <= b1 and b2 <= a2:
        c1 += 1
    elif b1 <= a1 and a2 <= b2:
        c1 += 1
    # [a1, a2], [b1, b2]
    if a1 >= b1 and a1 <= b2:
        c2 += 1
    elif b1 >= a1 and b1 <= a2:
        c2 += 1

print(c1)
print(c2)
