lines = ["498,4 -> 498,6 -> 496,6", "503,4 -> 502,4 -> 502,9 -> 494,9"]
lines = [line[:-1] for line in open("input.txt", "r").readlines()]

rocks = []

second_round = True

abyss = 0
for line in lines:
    rocks.append([])
    for x in line.split(" -> "):
        xx = x.split(",")
        x = int(xx[0])
        y = int(xx[1])
        abyss = max(abyss, y + 2)
        rocks[-1].append((x, y))


sand = 500,0

mapp = {}
mapp[sand] = "+"

def print_grid():
    mx = sand[0]
    Mx = sand[0]
    my = sand[1]
    My = sand[1]
    for (x, y) in mapp:
        mx = min(mx, x)
        Mx = max(Mx, x)
        my = min(my, y)
        My = max(My, y)
    for y in range(my, My + 1):
        s = ""
        for x in range(mx, Mx + 1):
            if (x, y) in mapp:
                s += mapp[x, y]
            else:
                s += "."
        print(s)

# mapp = [["." for _ in range(my, My)] for _ in range(mx, Mx)]
for r in rocks:
    for i in range(len(r) - 1):
        (x1, y1) = r[i]
        (x2, y2) = r[i+1]
        if x1 == x2:
            if y1 > y2:
                y1, y2 = y2, y1
            for y in range(y1, y2 + 1):
                mapp[(x1, y)] = "#"
        else:
            if x1 > x2:
                x1, x2 = x2, x1
            for x in range(x1, x2 + 1):
                mapp[(x, y1)] = "#"

# print_grid()

def empty(k):
    return (not (k in mapp)) and k[1] != abyss
    # and k[1] != abyss

def next_pos(x, y):
    k = (x, y + 1)
    if empty(k):
        return k
    k = (x - 1, y + 1)
    if empty(k):
        return k
    k = (x + 1, y + 1)
    if empty(k):
        return k
    return (x, y)

def iterate():
    x, y = -1, -1
    nx, ny = sand
    b = True
    while (x, y) != (nx, ny):
        x, y = nx, ny
        nx, ny = next_pos(x, y)
    print("fallen", x, y)
    mapp[x, y] = "o"
    # print_grid()

    if second_round:
        return (x, y) == sand
    else:
        return y >= abyss - 1

i = 0
b = False
while not b:
    b = iterate()
    i += 1

if second_round:
    i += 1
print(i - 1)

