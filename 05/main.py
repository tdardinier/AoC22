lines = open("test_input.txt", "r").readlines()
n = 3
n_lines = 3

lines = open("input.txt", "r").readlines()
n = 9
n_lines = 8

order_reversed = False

stacks = [[] for _ in range(n)]
for i in range(n_lines):
    line = lines[i][:-1]
    for j in range(n):
        if 4*j + 1 < len(line):
            x = line[4*j + 1]
            if x != " ":
                stacks[j].append(x)

instructions = []
for i in range(n_lines + 2, len(lines)):
    l = lines[i][5:-1].split(" ")
    instructions.append((int(l[0]), int(l[2]) - 1, int(l[4]) - 1))

for (n, i1, i2) in instructions:
    #print(n, stacks[i1], stacks[i2])
    l = stacks[i1][:n]
    stacks[i1] = stacks[i1][n:]
    if order_reversed:
        l.reverse()
    stacks[i2] = l + stacks[i2]
    #print(stacks[i1], stacks[i2])

s = ""
for x in stacks:
    if len(x) > 0:
        s += x[0]
print(s)
