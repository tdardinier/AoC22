f = "test_input.txt"
f = "input.txt"
lines = [line[:-1] for line in open(f, "r").readlines()]

def special_split(s):
    current = ""
    l = []
    n = 0
    for i in range(len(s)):
        x = s[i]
        if x == "," and n == 0:
            l.append(current)
            current = ""
        else:
            current += x
            if x == "[":
                n += 1
            elif x == "]":
                n -= 1
    if len(current) > 0:
        l.append(current)
    return l

# eval would have worked
def decode(line):
    if line[0] == "[":
        print(line)
        l = []
        for x in special_split(line[1:-1]):
            print("x", x)
            l.append(decode(x))
        return l
    else:
        return int(line)

pairs = []
for i in range(len(lines) // 3 + 1):
    pairs.append((decode(lines[3*i]), decode(lines[3*i+1])))

def compare(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return 1
        elif left == right:
            return 0
        else:
            return -1
    if not isinstance(left, int) and not isinstance(right, int):
        i = 0
        while i < len(left) and i < len(right):
            c = compare(left[i], right[i])
            if c != 0:
                return c
            i += 1
        return compare(len(left), len(right))
    elif isinstance(left, int):
        return compare([left], right)
    elif isinstance(right, int):
        return compare(left, [right])
    else:
        print("Error", left, right)

c = 0
for (i, p) in enumerate(pairs):
    if compare(p[0], p[1]) == 1:
        c += i + 1
print(c)

elements = [[[2]], [[6]]]
for p in pairs:
    elements.append(p[0])
    elements.append(p[1])

import functools

l = sorted(elements, key=functools.cmp_to_key(compare))
l.reverse()
i0 = None
i1 = None
for i in range(len(l)):
    if l[i] == [[2]]:
        i0 = i + 1
    if l[i] == [[6]]:
        i1 = i + 1
print(i0 * i1)
