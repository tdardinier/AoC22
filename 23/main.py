f = "test_input.txt"
# f = "test_input2.txt"
f = "input.txt"
lines = [line[:-1] for line in open(f, "r").readlines()]

elves = set([])
for (y, line) in enumerate(lines):
    for (x, s) in enumerate(line):
        if s == "#":
            elves.add((x, y))

directions = {}
directions["N"] = (0, -1)
directions["S"] = (0, 1)
directions["E"] = (1, 0)
directions["W"] = (-1, 0)

def get_vect_dir(s):
    vx, vy = 0, 0
    for d in s:
        vx, vy = vx + directions[d][0], vy + directions[d][1]
    return (vx, vy)

def is_elf_around(x, y):
    for xx in [x - 1, x, x + 1]:
        for yy in [y - 1, y, y + 1]:
            if (xx, yy) != (x, y) and (xx, yy) in elves:
                return True
    return False

def is_elf_in_directions(x, y, directs):
    for (dx, dy) in directs:
        if (x + dx, y + dy) in elves:
            return True
    return False

dN = [get_vect_dir(d) for d in ["N", "NE", "NW"]]
dS = [get_vect_dir(d) for d in ["S", "SE", "SW"]]
dW = [get_vect_dir(d) for d in ["W", "NW", "SW"]]
dE = [get_vect_dir(d) for d in ["E", "NE", "SE"]]
all_dirs = [("N", dN), ("S", dS), ("W", dW), ("E", dE)]

def first_half():
    global all_dirs, elves
    # Consider eight positions adjacent
    # In this order
   

    propositions = []
    for (x, y) in elves:
        #print("Checking...", x, y)
        if is_elf_around(x, y):
            # Else we do nothing
            #print("Elf around!")
            proposition = None
            for (name, dP) in all_dirs:
                if proposition is None and (not is_elf_in_directions(x, y, dP)):
                    proposition = name
            # print(proposition)
            if proposition is not None:
                #print("????????")
            #else:
                (vx, vy) = get_vect_dir(proposition)
                propositions.append(((x, y), (x + vx, y + vy)))

    all_dirs = all_dirs[1:] + [all_dirs[0]]
    return propositions

def second_half(propositions):
    global elves
    moved = False
    unique = {}
    for (_, y) in propositions:
        if y in unique:
            unique[y] = False
        else:
            unique[y] = True
    for (old, new) in propositions:
        if unique[new]:
            elves.remove(old)
            elves.add(new)
            moved = True
    return moved

def print_grid():
    global elves
    min_x = 0
    min_y = 0
    max_x = 0
    max_y = 0
    for (x, y) in elves:
        min_x = min(x, min_x)
        min_y = min(y, min_y)
        max_x = max(x, max_x)
        max_y = max(y, max_y)
    for y in range(min_y, max_y + 1):
        s = ""
        for x in range(min_x, max_x + 1):
            if (x, y) in elves:
                s += "#"
            else:
                s += "."
        print(s)

def count():
    global elves
    min_x = 0
    min_y = 0
    max_x = 0
    max_y = 0
    for (x, y) in elves:
        min_x = min(x, min_x)
        min_y = min(y, min_y)
        max_x = max(x, max_x)
        max_y = max(y, max_y)
    n_empty = 0
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) not in elves:
                n_empty += 1
    return n_empty

moved = True
print_grid()

i = 1
while moved:
    propositions = first_half()
    moved = second_half(propositions)
    print("End of round", i)
    # print_grid()
    if (i == 10):
        print(count())
    i += 1
