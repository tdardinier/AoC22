n_steps = 28
max_blueprints = 3

b1 = []
b1.append((4, 0, 0))
b1.append((2, 0, 0))
b1.append((3, 14, 0))
b1.append((2, 0, 7))

b2 = []
b2.append((2, 0, 0))
b2.append((3, 0, 0))
b2.append((3, 8, 0))
b2.append((3, 0, 12))


f = "input.txt"
lines = [line[:-1] for line in open(f, "r").readlines()]

blueprints = []
id_resource = {}
id_resource["ore"] = 0
id_resource["clay"] = 1
id_resource["obsidian"] = 2

for line in lines:
    b = []
    l = line.split(".")
    for x in l[:-1]:
        res = [0, 0, 0]
        for y in x.split("costs ")[1].split(" and "):
            rr = y.split(" ")
            res[id_resource[rr[1]]] = int(rr[0])
        b.append((res[0], res[1], res[2]))
    blueprints.append(b)



blueprints = [b1, b2]

robots = [1, 0, 0, 0]

maxis = {}

# Resources: Ore, clay, obsidian
# Let's take the last robot out of the equation
def maximize_geodes(b, time_left, resources, robots):
    if time_left == 0:
        return 0
    k = (time_left, resources, robots)
    if not k in maxis:
        new_resources = resources

        # each robot creates one resource
        new_resources = (resources[0] + robots[0], resources[1] + robots[1], resources[2] + robots[2])

        # First we do nothing
        m = maximize_geodes(b, time_left - 1, new_resources, robots)
        
        l_robots = list(robots)
        # Let's compare with building robots
        for i in range(4):
            # We try to create stuff...
            new_resources = (resources[0] - b[i][0], resources[1] - b[i][1], resources[2] - b[i][2])
            is_valid = True
            for x in new_resources:
                is_valid = is_valid and x >= 0
            if is_valid:
                if i < 3:
                    l_robots[i] += 1
                    new_robots = (l_robots[0], l_robots[1], l_robots[2])
                    new_resources = (new_resources[0] + robots[0], new_resources[1] + robots[1], new_resources[2] + robots[2])
                    new_geodes = maximize_geodes(b, time_left - 1, new_resources, new_robots)
                    m = max(m, new_geodes)
                    l_robots[i] -= 1
                elif i == 3:
                    new_resources = (new_resources[0] + robots[0], new_resources[1] + robots[1], new_resources[2] + robots[2])
                    new_geodes = time_left - 1 + maximize_geodes(b, time_left - 1, new_resources, robots)
                    m = max(m, new_geodes)
        maxis[k] = m
    return maxis[k]

import math

maxis_fast = {}
# Resources: Ore, clay, obsidian
def maximize_geodes_fast(b, time_left, resources, robots):
    if time_left == 0:
        return 0
    k = (time_left, resources, robots)
    if not k in maxis_fast:
        new_resources = resources

        # First we do nothing until the end, that's the baseline...
        # The other geodes are counted before
        m = 0

        # We now build...
        for i in range(4):
            # let's compute when is the next time we can create robot i
            #minimum_steps = [0, 0, 0]
            n = 0
            for i_res in range(3):
                # We have right now resources[i_res]
                # In n steps we will have "resources[i_res] + n * robots[i_res]"
                # We need "b[i][i_res] <= resources[i_res] + n * robots[i_res]"
                # We need "ceil(b[i][i_res] - resources[i_res]) / robots[i_res] <= n" (if robots[i_res] > 0)
                if robots[i_res] > 0:
                    n_steps = float(b[i][i_res] - resources[i_res]) / robots[i_res]
                    n = max(n, int(math.ceil(n_steps)))
                elif b[i][i_res] > resources[i_res]:
                    n = 50
            # We actually need "n + 1" steps, because one to construct the robot
            n += 1
            if n < time_left: # otherwise useless
                new_resources = (resources[0] + n * robots[0] - b[i][0], resources[1] + n * robots[1] - b[i][1], resources[2] + n * robots[2] - b[i][2])
                if i < 3:
                    # Normal case
                    new_robots = list(robots)
                    new_robots[i] += 1
                    new_robots = (new_robots[0], new_robots[1], new_robots[2])
                    c = maximize_geodes_fast(b, time_left - n, new_resources, new_robots)
                    m = max(m, c)
                elif i == 3:
                    c = maximize_geodes_fast(b, time_left - n, new_resources, robots)
                    c += time_left - n # after n time steps, the robot is created, everybody is happy
                    m = max(m, c)
        maxis_fast[k] = m
    return maxis_fast[k]

i = 1
cc = 0
while i - 1 < min(len(blueprints), max_blueprints):
    b = blueprints[i - 1]
    print("Starting with", b, "...")
    #maxis = {}
    maxis_fast = {}
    resources = (0, 0, 0)
    robots = (1, 0, 0)
    # r = maximize_geodes(b, n_steps, resources, robots)
    r = maximize_geodes_fast(b, n_steps, resources, robots)
    print(i, r, i * r)
    cc += i * r
    i += 1
print("Solution", cc)

if False:

    # Minute 15
    resources = (1, 5, 4)
    robots = (1, 4, 2, 0)
    print(maximize_geodes_fast(b1, 9, resources, robots))

    # Minute 13
    resources = (2, 11, 2)
    robots = (1, 4, 1, 0)
    print(maximize_geodes_fast(b1, 11, resources, robots))

    # Minute 10
    resources = (4, 15, 0)
    robots = (1, 3, 0, 0)
    print(maximize_geodes_fast(b1, 14, resources, robots))

    # Minute 8
    resources = (2, 9, 0)
    robots = (1, 3, 0, 0)
    print(maximize_geodes_fast(b1, 16, resources, robots))

    # Minute 6
    resources = (2, 4, 0)
    robots = (1, 2, 0, 0)
    print(maximize_geodes_fast(b1, 18, resources, robots))

    # Minute 5
    resources = (1, 2, 0)
    robots = (1, 2, 0, 0)
    print(maximize_geodes_fast(b1, 19, resources, robots))

    resources = (0, 0, 0)
    robots = (1, 0, 0, 0)
    print(maximize_geodes_fast(b1, 24, resources, robots))

