import math
import sys
import AStar

use_A_star = True
use_Dijkstra = False

f = "test_input.txt"
f = "test_input_hard.txt"
f = "input.txt"
lines = [line[1:-2] for line in open(f, "r").readlines()]

# We can memoize with the map of blizzards (should repeat every gcd(width, height))
# We can compute, at each timestep, if a cell is empty
start = None
for (x, s) in enumerate(lines[0]):
    if s == ".":
        start = (x, -1)

n = len(lines) - 2
m = len(lines[0])
n_total = min(n * m, 700)
# n_total = 700
# n_total *= 2
# n_total = 20

end = None
for (x, s) in enumerate(lines[-1]):
    if s == ".":
        end = (x, n)

blizzards = [{}]
blizzards[0][">"] = set([])
blizzards[0]["^"] = set([])
blizzards[0]["<"] = set([])
blizzards[0]["v"] = set([])

y = 0
for line in lines[1:-1]:
    for (x, s) in enumerate(line):
        if s != ".":
            blizzards[0][s].add((x, y))
    y += 1

directions = {}
directions[">"] = (1, 0)
directions["<"] = (-1, 0)
directions["^"] = (0, -1)
directions["v"] = (0, 1)

# Computing blizzards
for i in range(n_total):
    b = {}
    for direct in blizzards[-1]:
        (dx, dy) = directions[direct]
        s = set([])
        for (x, y) in blizzards[-1][direct]:
            s.add(((x + dx) % m, (y + dy) % n))
        b[direct] = s
    blizzards.append(b)

all_blizzards = []
for i in range(n_total):
    all_blizzards.append(set([]))
    for x in blizzards[i]:
        all_blizzards[-1] = all_blizzards[-1].union(blizzards[i][x])



# Returns the neighbours
def neighbours(node):
    # print("Getting neighbours...", node)
    if node in ["start", "finish"]:
        return []
    (x, y, t) = node
    neigh = []
    for (dx, dy) in [(0, 0), (0, -1), (0, 1), (-1, 0), (1, 0)]:
        nx, ny = x + dx, y + dy
        nt = (t + 1) % n_total
        if (nx, ny) not in all_blizzards[nt]:
            if (nx, ny) == end:
                # Special node 1
                neigh.append("finish")
                neigh.append((nx, ny, nt))
            elif (nx, ny) == start:
                # Special node 2
                neigh.append("start")
                neigh.append((nx, ny, nt))
            elif (nx >= 0 and nx < m and ny >= 0 and ny < n):
                neigh.append((nx, ny, nt))
    return neigh

def heur_to_finish(node):
    x, y = None, None
    if node == "finish":
        return 0
    elif node == "start":
        x, y = start
    else:
        (x, y, _) = node
    return abs(x - end[0]) + abs(y - end[1])



def heur_to_start(node):
    x, y = None, None
    if node == "finish":
        x, y = end
    elif node == "start":
        return 0
    else:
        (x, y, _) = node
    return abs(x - start[0]) + abs(y - start[1])


if use_A_star:
    node1 = AStar.find_path(neighbours, (start[0], start[1], 0), "finish", heur_to_finish)
    t1 = node1.cost
    print("First path (A*)", t1)

    node2 = AStar.find_path(neighbours, (end[0], end[1], t1 % n_total), "start", heur_to_start)
    t2 = node2.cost
    print("Second path (A*)", t2)

    node3 = AStar.find_path(neighbours, (start[0], start[1], (t1 + t2) % n_total), "finish", heur_to_finish)
    t3 = node3.cost
    print("Third path (A*)", t3)

    print("Solution (A*)", t1 + t2 + t3)

if use_Dijkstra:
    import networkx as netx
    G = netx.DiGraph()

    if True:
        for t in range(n_total):
            for x in range(m):
                for y in range(-1, n + 1):
                    if (y >= 0 and y < n) or (x, y) == start or (x, y) == end:
                        for nei in neighbours((x, y, t)):
                           G.add_edge((x, y, t), nei)

    path1 = netx.shortest_path(G, (start[0], start[1], 0), "finish")
    t1 = len(path1) - 1
    print("First path (Dijkstra)", t1)

    path2 = netx.shortest_path(G, (end[0], end[1], t1 % n_total), "start")
    t2 = len(path2) - 1
    print("Second path (Dijkstra)", t2)

    path3 = netx.shortest_path(G, (start[0], start[1], (t1 + t2) % n_total), "finish")
    t3 = len(path3) - 1
    print("Third path (Dijkstra)", t3)

    print("Solution (Dijkstra)", t1 + t2 + t3)
#import astar
#A_path = astar.find_path((start[0], start[1], 0), "finish", neighbors_fnct=neighbours)
#                    heuristic_cost_estimate_fnct=cost, distance_between_fnct=distance))
#print("A*", len(list(A_path)) - 1)
