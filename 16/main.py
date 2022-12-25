f = "test_input.txt"
f = "input.txt"
lines = [line[:-1] for line in open(f, "r").readlines()]
valves = {}
for line in lines:
    l = line.split(" ")
    name = l[1]
    rate = int(l[4][5:-1])
    tunnels = [x.split(",")[0] for x in l[9:]]
    valves[name] = (rate, tunnels)

# Solution is now a list, and we remove the time_left
# cannot work
solutions = {}


# Let's prune

def hash_set(s):
    return "".join(sorted(list(s)))

upper_bounds = {}
def upper_bound_score(time_left, valves_left):
    return 100000
    k = hash_set(valves_left)
    if k not in upper_bounds:
        l = list(valves_left)
        if len(l) > 0:
            upper_bounds[k] = max(l, key = lambda x: -valves[x][0])
        else:
            upper_bounds[k] = 0
    return upper_bounds[k] * time_left * (time_left // 2)

# Need to compute and compare *all neighbours transitively*
import networkx as nx
G = nx.Graph()
for x in valves:
    for y in valves[x][1]:
        G.add_edge(x, y)

paths = dict(nx.all_pairs_shortest_path(G))
cost_to_open = {}
for x in valves:
    cost_to_open[x] = {}
    for y in valves:
        cost_to_open[x][y] = len(paths[x][y])

maxi = {}
def find_max(valves_left, k):
    if k not in maxi:
        maxi[k] = max(valves_left, key = lambda x: -valves[x][0])
    return maxi[k]

def solve_max(valve, time_left, valves_left):
    if time_left <= 1:
        return 0
    else:
        hh = hash_set(valves_left)
        if len(valves_left) == 0:
            return 0
        k = (valve, time_left, hash_set(valves_left))
        if k not in solutions:
            best_score = 0
            for x in valves_left:
                if best_score < (time_left - cost_to_open[valve][x]) * valves[x][0] * (time_left - cost_to_open[valve][x]):
                    c = (time_left - cost_to_open[valve][x]) * valves[x][0]
                    valves_left.remove(x)
                    c += solve_max(x, time_left - cost_to_open[valve][x], valves_left)
                    valves_left.add(x)
                    best_score = max(best_score, c)
            solutions[k] = best_score
        return solutions[k]

def estimate_double(v1, x, v2, t1, t2, valves_left):
    valves_left.remove(x)
    c = (t1 - cost_to_open[v1][x]) * valves[x][0]
    c += solve_max(x, t1 - cost_to_open[v1][x], valves_left)
    c += solve_max(v2, t2, valves_left)
    valves_left.add(x)
    return c

solutions_double = {}
def solve_max_double(v1, v2, t1, t2, valves_left, max_score):
    if t1 < t2:
        return solve_max_double(v2, v1, t2, t1, valves_left, max_score)
    if t1 <= 1 and t2 <= 1:
        return 0
    else:
        assert t1 >= t2
        hh = hash_set(valves_left)
        if len(valves_left) == 0:
            return 0
        k = (v1, v2, t1, t2, hash_set(valves_left))
        if k not in solutions_double:
            best_score = 0
            #candidates = list(valves_left)
            #candidates.sort(key = lambda x: -estimate_double(v1, x, v2, t1, t2, valves_left))
            for x in valves_left:
            #for x in candidates:
                # Both players do the best with what is remaining
                estimate = estimate_double(v1, x, v2, t1, t2, valves_left)
                if estimate > max_score:
                    valves_left.remove(x)
                    c = (t1 - cost_to_open[v1][x]) * valves[x][0]
                    c += solve_max_double(x, v2, t1 - cost_to_open[v1][x], t2, valves_left, max_score - c)
                    valves_left.add(x)
                    best_score = max(best_score, c)
                    max_score = max(max_score, best_score)
            solutions_double[k] = best_score
        return solutions_double[k]



all_valves = set(valves.keys())
print(solve_max("AA", 30, all_valves))
print(solve_max_double("AA", "AA", 26, 26, all_valves, 0))
