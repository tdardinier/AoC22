f = "test_input.txt"
f = "input.txt"
lines = [line[:-1] for line in open(f, "r").readlines()]

cubes = set([])
for line in lines:
    l = line.split(",")
    cubes.add((int(l[0]), int(l[1]), int(l[2])))

# Naive method
sides = []
sides.append((1, 0, 0))
sides.append((-1, 0, 0))
sides.append((0, 1, 0))
sides.append((0, -1, 0))
sides.append((0, 0, 1))
sides.append((0, 0, -1))

c = 0
for (x, y, z) in cubes:
    for (sx, sy, sz) in sides:
        if (x + sx, y + sy, z + sz) not in cubes:
            c += 1
print(c)

# Let's find (and remove?) cubes that are inside...
# We can do all paths an Dijkstra and stuff

mins = [2, 2, 2]
maxs = [2, 2, 2]

# First we compute outside
for c in cubes:
    for i in range(3):
        mins[i] = min(mins[i], c[i])
        maxs[i] = max(maxs[i], c[i])

# mins = [x - 1 for x in mins]
# maxs = [x - 1 for x in maxs]

import networkx as nx

G = nx.DiGraph()
for x in range(mins[0] - 1, maxs[0] + 2):
    for y in range(mins[1] - 1, maxs[1] + 2):
        for z in range(mins[2] - 1, maxs[2] + 2):
            for (sx, sy, sz) in sides:
                (xx, yy, zz) = (x + sx, y + sy, z + sz)
                if (xx, yy, zz) not in cubes:
                    #G.add_edge((x, y, z), (xx, yy, zz))
                    G.add_edge((xx, yy, zz), (x, y, z))

# Constructing the set of all nodes reachable from some outside node
can_reach_outside = set(nx.shortest_path(G, (mins[0] - 1, mins[1] - 1, mins[2] - 1)).keys())

counter = 0
for (x, y, z) in cubes:
    for (sx, sy, sz) in sides:
        (xx, yy, zz) = (x + sx, y + sy, z + sz)
        cc = (xx, yy, zz)
        if (cc not in cubes):
            if cc in can_reach_outside:
                counter += 1
print(counter)
