f = "test_input.txt"
#f = "input.txt"
lines = [line[:-1] for line in open(f, "r").readlines()]
valves = {}
for line in lines:
    l = line.split(" ")
    name = l[1]
    rate = int(l[4][5:-1])
    tunnels = [x.split(",")[0] for x in l[9:]]
    valves[name] = (rate, tunnels)

solutions = {}

def hash_set(s):
    return "".join(sorted(list(s)))

def solve_max(valve, time_left, valves_left):
    # print("Solving", valve, time_left, valves_left)
    # Moving takes 1
    # Opening takes 1
    if time_left <= 1:
        return 0
    else:
        k = (valve, time_left, hash_set(valves_left))
        if k in solutions:
            return solutions[k]
        best_score = 0
        if valve in valves_left:
            # Can open
            c = (time_left - 1) * valves[valve][0]
            v = set(valves_left)
            v.remove(valve)
            c += solve_max(valve, time_left - 1, v)
            best_score = max(best_score, c)
        # Checking all tunnels
        for x in valves[valve][1]:
            c = solve_max(x, time_left - 1, valves_left)
            best_score = max(best_score, c)
        solutions[k] = best_score
        return best_score

all_valves = set(valves.keys())
print(solve_max("AA", 30, all_valves))
