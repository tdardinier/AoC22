f = "test_input.txt"
f = "input.txt"
lines = [line[:-1] for line in open(f, "r").readlines()]

symbols = {}
symbols["2"] = 2
symbols["1"] = 1
symbols["0"] = 0
symbols["-"] = -1
symbols["="] = -2

def to_decimal(s):
    c = 0
    for x in s:
        c = c * 5 + symbols[x]
    return c

def to_SNAFU(x):
    if x == 0:
        return ""
    s = None
    # First thing:
    c = x % 5
    if c <= 2:
        s = str(c)
    elif c == 3:
        s = "="
        x += 2
    elif c == 4:
        s = "-"
        x += 1
    return to_SNAFU(x // 5) + s



c = 0
for line in lines:
    c += to_decimal(line)

print(c)
print(to_SNAFU(c))
