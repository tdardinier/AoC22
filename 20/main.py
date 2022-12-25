l = [1, 2, -3, 3, -2, 0, 4]


f = "input.txt"
l = [int(line[:-1]) for line in open(f, "r").readlines()]

key = 811589153
l = [key * x for x in l]


ll = []
for i in range(len(l)):
    ll.append((i, l[i]))
l = list(ll)

import math

def move(x, l, n):
    index = l.index(x)
    new_pos = (index + n) % (len(l) - 1)
    ll = l[:index] + l[index + 1:]
    ll.insert(new_pos, x)
    return ll

for _ in range(10):
    for x in l:
        ll = move(x, ll, x[1])

i = 0
while ll[i][1] != 0:
    i += 1

x = ll[(i + 1000) % len(ll)][1]
y = ll[(i + 2000) % len(ll)][1]
z = ll[(i + 3000) % len(ll)][1]
print(x + y + z)
