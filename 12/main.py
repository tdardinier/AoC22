from dijkstar import Graph, find_path

f = "test_input.txt"
f = "input.txt"
lines = [line[:-1] for line in open(f, "r").readlines()]

letters = [x for x in "abcdefghijklmnopqrstuvwxyz"]
reverse = {}
for i in range(26):
    reverse[letters[i]] = i

mapp = []
start = None
goal = None
for (i, line) in enumerate(lines):
    mapp.append([])
    for (j, x) in enumerate(line):
        if x == "S":
            mapp[-1].append(0)
            start = i, j
        elif x == "E":
            mapp[-1].append(25)
            goal = i, j
        else:
            mapp[-1].append(reverse[x])

graph = Graph()

n = len(mapp)
m = len(mapp[0])
for i in range(n):
    for j in range(m):
        # Compute neighbours
        if i - 1 >= 0 and mapp[i - 1][j] <= mapp[i][j] + 1:
            graph.add_edge((i, j), (i-1, j), 1)
        if i + 1 < n and mapp[i + 1][j] <= mapp[i][j] + 1:
            graph.add_edge((i, j), (i+1, j), 1)
        if j - 1 >= 0 and mapp[i][j - 1] <= mapp[i][j] + 1:
            graph.add_edge((i, j), (i, j-1), 1)
        if j + 1 < m and mapp[i][j + 1] <= mapp[i][j] + 1:
            graph.add_edge((i, j), (i, j+1), 1)

c = find_path(graph, start, goal).total_cost
print(c)
for i in range(n):
    for j in range(m):
        if mapp[i][j] == 0:
            try:
                cost = find_path(graph, (i, j), goal).total_cost
                c = min(c, cost)
            except:
                pass
print(c)
