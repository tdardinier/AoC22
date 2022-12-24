f = "test_input.txt"
y = 10
f = "input.txt"
y = 2000000

lines = [line[:-1] for line in open(f, "r").readlines()]

pairs = []
beacons = set([])
sensors = set([])
for line in lines:
    sx = int(line.split(",")[0].split("x=")[1])
    sy = int(line.split(": ")[0].split("y=")[1])
    bx = int(line.split(", ")[1].split("x=")[1])
    by = int(line.split(", y=")[-1])
    pairs.append((sx, sy, bx, by))
    beacons.add((bx, by))
    sensors.add((sx, sy))

def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_segments(y):
    segments_cannot_be = []
    for p in pairs:
        sensor = (p[0], p[1])
        beacon = (p[2], p[3])
        
        d = distance(sensor, beacon)
        dy = abs(sensor[1] - y)

        if d - dy >= 0:
            x1 = sensor[0] + d - abs(sensor[1] - y)
            x2 = sensor[0] - d + abs(sensor[1] - y)
            segments_cannot_be.append((min(x1, x2), max(x1, x2)))
    return segments_cannot_be

xmax = 4000000
# xmax = 20
xmin = 0
ymin = 0
ymax = 4000000
# ymax = 20

for y in range(ymin, ymax+1):
    segments_cannot_be = get_segments(y)
    segments_cannot_be.sort()

    x = xmin
    i = 0
    # Candidate
    while x <= xmax and i < len(segments_cannot_be):
        if segments_cannot_be[i][0] <= x <= segments_cannot_be[i][1]:
            x = segments_cannot_be[i][1] + 1
        else:
            i += 1

    if (y % 10000 == 0):
        print(y)
    if x <= xmax:
        print("Solution:", x, y)
        print(x * 4000000 + y)



    # can it be there?

s = set([])

for (a, b) in segments_cannot_be:
    for x in range(a, b+1):
        s.add(x)

for (x, yy) in beacons:
    if yy == y:
        s.remove(x)

#for (x, yy) in sensors:
#    if yy == y:
#        s.remove(x)

print(len(s))
