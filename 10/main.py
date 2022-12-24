#f = "test_input.txt"
f = "test_input2.txt"
f = "input.txt"
lines = [line[:-1] for line in open(f, "r").readlines()]

X = 1
cycle = 0
s = 0

image = [["." for _ in range(40)] for _ in range(6)]

def incr_cycle():
    global cycle, s
    rcycle = cycle % 40
    cycle += 1
    if abs(X - rcycle) <= 1:
        image[cycle // 40][rcycle] = "#"
    if cycle % 40 == 20:
        print(cycle, X, cycle * X)
        s += cycle * X

for line in lines:
    if line == "noop":
        incr_cycle()
    else:
        n = int(line.split(" ")[1])
        incr_cycle()
        incr_cycle()
        X += n

print(s)
for row in ["".join(row) for row in image]:
    print(row)
