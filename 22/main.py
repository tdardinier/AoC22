f = "test_input.txt"
f = "input.txt"
lines = [line[:-1] for line in open(f, "r").readlines()]

second_round = True
second_round = False

n_face = 4
if second_round:
    n_face = 50

# Gives the transition and the orientation
edges = {}
edges[(1, "<")] = (3, "v")
edges[(1, "^")] = (2, "v")
edges[(1, ">")] = (6, "<")

edges[(2, "^")] = (1, "v")
edges[(2, "<")] = (6, "^")
edges[(2, "v")] = (5, "^")

edges[(3, "^")] = (1, ">")
edges[(3, "v")] = (5, ">")

edges[(4, ">")] = (6, "v")

edges[(5, "<")] = (3, "^")
edges[(5, "v")] = (2, "^")

edges[(6, "^")] = (4, "<")
edges[(6, ">")] = (1, "<")
edges[(6, "v")] = (2, ">")

if second_round:
    edges = {}

    edges[(1, "^")] = (6, ">")
    edges[(1, "<")] = (4, ">")

    edges[(2, "^")] = (6, "^")
    edges[(2, ">")] = (5, "<")
    edges[(2, "v")] = (3, "<")

    edges[(3, "<")] = (4, "v")
    edges[(3, ">")] = (2, "^")

    edges[(4, "^")] = (3, ">")
    edges[(4, "<")] = (1, ">")

    edges[(5, ">")] = (2, "<")
    edges[(5, "v")] = (6, "<")

    edges[(6, ">")] = (5, "^")
    edges[(6, "v")] = (2, "v")
    edges[(6, "<")] = (1, "v")

rev = {}
rev[">"] = "<"
rev["<"] = ">"
rev["^"] = "v"
rev["v"] = "^"

# Need sanity check
for (fin, rin) in edges:
    (fout, rout) = edges[(fin, rin)]
    print("Checking", (fin, rin), (fout, rout))
    assert edges[(fout, rev[rout])][0] == fin




# from enum import Enum

walls = set([])
tiles = set([])

i = 0
x_min = 10000
x_max = 0
y_min = 10000
y_max = 0
pos = None
for line in lines[:-2]:
    l = []
    j = 0
    for x in line:
        if x == ".":
            tiles.add((j, i))
            if pos is None:
                pos = (j, i)
            x_min = min(x_min, j)
            x_max = max(x_max, j)
            y_min = min(y_min, i)
            y_max = max(y_max, i)
        elif x == "#":
            walls.add((j, i))
        j += 1
    i += 1

instructions = []
c = 0
for x in lines[-1]:
    if x == "R" or x == "L":
        instructions.append((True, c))
        instructions.append((False, x))
        c = 0
    else:
        c = 10 * c + int(x)

if c > 0:
    instructions.append((True, c))

direction = (1, 0)

direction_rev = {}
direction_rev[">"] = (1, 0)
direction_rev["<"] = (-1, 0)
direction_rev["^"] = (0, -1)
direction_rev["v"] = (0, 1)

def get_dir(direct):
    if direction == (1, 0):
        return ">"
    elif direction == (-1, 0):
        return "<"
    elif direction == (0, -1):
        return "^"
    elif direction == (0, 1):
        return "v"
    else:
        print(direct)
        return "?"

last_visit = {}
last_visit[pos] = ">"

def print_grid():
    for y in range(y_min, y_max + 1):
        s = ""
        for x in range(x_min, x_max + 1):
            if (x, y) in last_visit:
                s += last_visit[(x, y)]
            #if (x, y) == pos:
            #   s += get_dir(direction)
            elif (x, y) in tiles:
                s += "."
            elif (x, y) in walls:
                s += "#"
            else:
                s += " "
        print(s)

def get_other_side(pos, direct):
    dx, dy = -direct[0], -direct[1]
    x, y = pos
    while (x + dx, y + dy) in tiles or (x + dx, y + dy) in walls:
        x, y = x + dx, y + dy
    return (x, y)



faces = {}
faces[1] = (2 * n_face, 0)
faces[2] = (0, n_face)
faces[3] = (n_face, n_face)
faces[4] = (2 * n_face, n_face)
faces[5] = (2 * n_face, 2 * n_face)
faces[6] = (3 * n_face, 2 * n_face)

if second_round:
    faces[1] = (n_face, 0)
    faces[2] = (2 * n_face, 0)
    faces[3] = (n_face, n_face)
    faces[4] = (0, 2 * n_face)
    faces[5] = (n_face, 2 * n_face)
    faces[6] = (0, 3 * n_face)

def get_face(x, y):
    if second_round:
        if y < n_face:
            if n_face <= x < 2 * n_face:
                return 1
            elif x >= 2 * n_face:
                return 2
            else:
                assert false
        elif y < 2 * n_face:
            return 3
        elif y < 3 * n_face:
            if x < n_face:
                return 4
            else:
                return 5
        else:
            return 6
    else:
        if y < n_face:
            return 1
        elif y < 2 * n_face:
            if x < n_face:
                return 2
            elif x < 2 * n_face:
                return 3
            else:
                return 4
        else:
            if x < n_face * 3:
                return 5
            else:
                return 6

def rotate_once_right(x, y):
    return (n_face - 1 - y, x)

# def get_new_face_cube(pos, direct):


# (11, 5) -> (12, 5)
# instead: (11, 5) --> 

def rotate_symbol_once(s):
    if s == ">":
        return "v"
    elif s == "v":
        return "<"
    elif s == "<":
        return "^"
    elif s == "^":
        return ">"

def how_many_rotations(before, after):
    i = 0
    while before != after:
        before = rotate_symbol_once(before)
        i += 1
    return i


def move(n):
    global pos, last_visit, direction
    done = False
    i = 0
    while i < n and not done:
        print("Direction", direction)
        nx, ny = pos[0] + direction[0], pos[1] + direction[1]
        if (nx, ny) not in walls and (nx, ny) not in tiles:
            # Let's go to the other side...
            if second_round:
                print("The current position is", pos, "the new would be", (nx, ny))
                face = get_face(pos[0], pos[1])
                before = get_dir(direction)
                next_face = edges[(face, before)]
                #print("The current face is", face)
                #print("The next face is", edges[(face, get_dir(direction))])
                #print("Relative coordinates...", pos[0] % n_face, pos[1] % n_face)
                #print("New relative coordinates...", nx % n_face, ny % n_face)
                after = edges[(face, before)][1]
                n_rotations = how_many_rotations(before, after)
                
                nx, ny = (nx % n_face, ny % n_face)
                for _ in range(n_rotations):
                    (nx, ny) = rotate_once_right(nx, ny)
                # Adding face...
                (nx, ny) = (nx + faces[next_face[0]][0], ny + faces[next_face[0]][1])
                if (nx, ny) not in walls:
                    direction = direction_rev[next_face[1]]
                #print("How many times to rotate?", n)
                # (nx, ny) = get_other_side(pos, direction)
            else:
                (nx, ny) = get_other_side(pos, direction)
        if (nx, ny) in walls:
            done = True
        elif (nx, ny) in tiles:
            pos = (nx, ny)
            last_visit[pos] = get_dir(direction)
        i += 1

def reorient(rotation):
    global direction, last_visit, pos
    dx, dy = direction[0], direction[1]
    if rotation == "R":
        direction = (-dy, dx)
    elif rotation == "L":
        direction = (dy, -dx)
    else:
        assert false
    last_visit[pos] = get_dir(direction)


for (b, x) in instructions:
    if b:
        move(x)
    else:
        reorient(x)

print_grid()

final_row = pos[1] + 1
final_column = pos[0] + 1

facing = {}
facing[">"] = 0
facing["v"] = 1
facing["<"] = 2
facing["^"] = 3

print(1000 * final_row + 4 * final_column + facing[get_dir(direction)])
