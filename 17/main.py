s = open("input.txt", "r").readlines()[0][:-1]
# Left bottom = (0, 0)

n_rocks = 200000

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
current_highest_y_in_field = 0

i_rock = 0
i_jet = 0

current_rock = []

def maxi_y():
    global current_highest_y_in_field
    return current_highest_y_in_field
    m = -1
    for (_, y) in field:
        m = max(m, y)
    for (_, y) in current_rock:
        m = max(m, y)
    return m

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

heights = [0]
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

for i in range(n_rocks):
    if (i % 1000 == 0):
        print(i, n_rocks)
    make_next_rock_fall()
    heights.append(current_highest_y_in_field)

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

offset = 1000
heights = heights[offset:]

period = None
for potential_period in range(20000):
    # We check 10 things
    b = True
    sets = []

    for i in range(4):
        da = heights[(i + 2) * potential_period] - heights[(i + 1) * potential_period]
        db = heights[(i + 1) * potential_period] - heights[i * potential_period]
        b = b and (da == db)
    if b:
        print("Found!", potential_period)
        if potential_period > 0 and period is None:
            period = potential_period


def compute_with_period(x):
    x -= offset
    return heights[x % period] + (x // period) * (heights[period] - heights[0])
print("Answer to first task", compute_with_period(2022))
print("Answer to second task", compute_with_period(1000000000000))
