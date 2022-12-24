f = "test_input.txt"
f = "test_input2.txt"
f = "input.txt"
lines = [line[:-1].split(" ") for line in open(f, "r").readlines()]

n_knots = 10

knots = [[0, 0] for _ in range(n_knots)]
#head = [0, 0]
#tail = [0, 0]

directions = {}
directions["U"] = (0, 1)
directions["D"] = (0, -1)
directions["L"] = (-1, 0)
directions["R"] = (1, 0)

visited = set([(0, 0)])

def print_grid():
    for j in range(5, -1, -1):
        s = ""
        for i in range(6):
            c = "."
            if tail[0] == i and tail[1] == j:
                c = "T"
            if head[0] == i and head[1] == j:
                c = "H"
            s += c
        print(s)

def follows(tail, head):
    if head[0] == tail[0] and abs(head[1] - tail[1]) == 2:
        tail[1] = (head[1] + tail[1]) // 2
    elif head[1] == tail[1] and abs(head[0] - tail[0]) == 2:
        tail[0] = (head[0] + tail[0]) // 2
    elif abs(head[0] - tail[0]) >= 2 or abs(head[1] - tail[1]) >= 2:
        # print("DIAGONAL")
        # diagonal
        diag = [1, 1]
        if head[0] < tail[0]:
            diag[0] = -1
        if head[1] < tail[1]:
            diag[1] = -1
        tail[0] += diag[0]
        tail[1] += diag[1]

for l in lines:
    (d, n) = (l[0], int(l[1]))
    print(d, n)
    dd = directions[d]
    for _ in range(n):
        # Head is 0

        # First, move head
        knots[0][0] += dd[0]
        knots[0][1] += dd[1]

        for i in range(1, n_knots):
            follows(knots[i], knots[i-1])
            #follows(tail, head)
        visited.add((knots[-1][0], knots[-1][1]))
        #print_grid()

print(len(visited))

