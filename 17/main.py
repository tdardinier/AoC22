s = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
s = open("input.txt", "r").readlines()[0][:-1]
# Left bottom = (0, 0)

n_rocks = 100000
#n_rocks = 2022

rocks = []
rocks.append([(2, 0), (3, 0), (4, 0), (5, 0)])
rocks.append([(2, 1), (3, 0), (3, 1), (3, 2), (4, 1)])
rocks.append([(2, 0), (3, 0), (4, 0), (4, 1), (4, 2)])
rocks.append([(2, 0), (2, 1), (2, 2), (2, 3)])
rocks.append([(2, 0), (2, 1), (3, 0), (3, 1)])

directions = {}
directions[">"] = (1, 0)
directions["<"] = (-1, 0)

# From 0 to 6
field = set([])
current_highest_y_in_field = -1

i_rock = 0
i_jet = 0

current_rock = []

def maxi_y():
    global current_highest_y_in_field
    return current_highest_y_in_field
    #m = -1
    #for (_, y) in field:
    #    m = max(m, y)
    #for (_, y) in current_rock:
    #    m = max(m, y)
    #assert m == current_highest_y_in_field
    #return m

def print_grid():
    y_max = maxi_y()
    for y in range(y_max, -1, -1):
        s = "|"
        for x in range(7):
            if (x, y) in field:
                s += "#"
            elif (x, y) in current_rock:
                s += "@"
            else:
                s += "."
        s += "|"
        print(s)
    print("+-------+")

def add_rock(rock):
    global field, current_rock
    # Bottom edge: +3 above highest rock
    offset_y = maxi_y() + 4
    current_rock = []
    for (x, y) in rock:
        current_rock.append((x, y + offset_y))

def is_valid(x, y):
    b = (0 <= x < 7)
    b = b and y >= 0
    b = b and (x, y) not in field
    return b

def push_rock():
    global i_jet, s, current_rock
    (dx, dy) = directions[s[i_jet]]
    new_rock = []
    valid = True
    for (x, y) in current_rock:
        (nx, ny) = (x + dx, y + dy)
        new_rock.append((nx, ny))
        valid = valid and is_valid(nx, ny)
    if valid:
        current_rock = new_rock
    i_jet = (i_jet + 1) % len(s)

def fall_one_step():
    global current_rock
    new_rock = []
    valid = True
    for (x, y) in current_rock:
        ny = y - 1
        new_rock.append((x, ny))
        valid = valid and is_valid(x, ny)
    if valid:
        current_rock = new_rock
    return valid

def make_next_rock_fall():
    global current_rock, i_rock, current_highest_y_in_field
    add_rock(rocks[i_rock])
    i_rock = (i_rock + 1) % 5
    b = True
    while b:
        push_rock()
        b = fall_one_step()
    # Transform current rock into rock
    for (x, y) in current_rock:
        current_highest_y_in_field = max(current_highest_y_in_field, y)
        field.add((x, y))

offset = 1000

heights = []
for i in range(n_rocks):
    if (i % 1000 == 0):
        print(i, n_rocks)
    if (i >= offset):
        heights.append(maxi_y() + 1)
    make_next_rock_fall()

m = maxi_y() + 1
print(m)

per_row = [set([]) for _ in range(m)]
for (x, y) in field:
    per_row[y].add(x)

def collect_x_from_row(y):
    global field
    s = set([])
    for (x, yy) in field:
        if y == yy:
            s.add(x)
    return s


periods = set()
for potential_period in range(2, 20000):
    # We check for period in heights
    b = True
    #offset = 1000
    sets = []

    b = True
    for i in range(500):
        x = heights[i]
        y = heights[i + potential_period]
        z = heights[i + 2 * potential_period]
        b = b and (z - y == y - x)
        # b = b and (heights[offset + i] == heights[offset + i + potential_period])
    if b:
        for x in periods:
            b = b and (potential_period % x != 0)
        if b:
            periods.add(potential_period)
            print("Found!", potential_period)

    # if collect_x_from_row(offset + potential_period) == collect_x_from_row(offset + 2 * potential_period):
    #for i in range(4):
    #    sets.append(per_row[offset + i * potential_period])
    #for x in sets:
    #    for y in sets:
    #        b = b and x == y
    #if b:
    #    print("Found!", potential_period)

# Period = 53
# Period = 2574
def compute_height_with_period(period, xx):
    #say we start at 1000
    x = xx - offset
    return heights[x % period] + (x // period) * (heights[period] - heights[0])

