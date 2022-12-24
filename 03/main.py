f = open("test_input.txt", "r").readlines()
f = open("input.txt", "r").readlines()
alphabet = [x for x in "abcdefghijklmnopqrstuvwxyz"]
alphabet += [x.upper() for x in "abcdefghijklmnopqrstuvwxyz"]

priority = {}
i = 1
for x in alphabet:
    priority[x] = i
    i += 1

s = 0
s2 = 0
salphabet = set(alphabet)
current_intersection = salphabet
i = 0
for l in f:
    m = len(l) // 2
    a = set(l[:m])
    b = set(l[m:-1])
    current_intersection = current_intersection.intersection(set(l[:-1]))
    common = a.intersection(b)
    x = common.pop()
    s += priority[x]
    i += 1
    if i % 3 == 0:
        assert len(current_intersection) == 1
        x = current_intersection.pop()
        s2 += priority[x]
        current_intersection = salphabet


print(s)
print(s2)
