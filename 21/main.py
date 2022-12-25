f = "test_input.txt"
f = "input.txt"
lines = [line[:-1] for line in open(f, "r").readlines()]

monkeys_numbers = {}
monkeys_eq = {}

for line in lines:
    r = line.split(": ")
    exp = r[1]
    if " " in exp:
        monkeys_eq[r[0]] = exp.split(" ")
    else:
        monkeys_numbers[r[0]] = int(exp)

orig_monkeys_numbers = {}
for x in monkeys_numbers:
    orig_monkeys_numbers[x] = monkeys_numbers[x]

monkeys_eq["root"][1] = "="

def evaluate(monkey):
    if monkey not in monkeys_numbers:
        eq = monkeys_eq[monkey]
        x = evaluate(eq[0])
        y = evaluate(eq[2])
        res = None
        if eq[1] == "+":
            res = x + y
        elif eq[1] == "-":
            res = x - y
        elif eq[1] == "/":
            res = int(x // y)
        elif eq[1] == "*":
            res = x * y
        elif eq[1] == "=":
            res = (x == y)
        monkeys_numbers[monkey] = res
    return monkeys_numbers[monkey]

def compute_dependencies(monkey):
    if monkey in monkeys_eq:
        x = monkeys_eq[monkey][0]
        y = monkeys_eq[monkey][2]
        return set([x, y]).union(compute_dependencies(x)).union(compute_dependencies(y))
    else:
        return set([])

left = compute_dependencies(monkeys_eq["root"][0])
right = compute_dependencies(monkeys_eq["root"][2])

def compute_relevant_subset(monkey, target):
    if monkey in monkeys_eq:
        x = monkeys_eq[monkey][0]
        y = monkeys_eq[monkey][2]
        s = set([])
        # print(x, compute_dependencies(x))
        if target in compute_dependencies(x):
            print("It is!")
            s.add(x)
            s = s.union(compute_relevant_subset(x, target))
        if target in compute_dependencies(y):
            print("It is!")
            s.add(y)
            s = s.union(compute_relevant_subset(y, target))
        return s
    else:
        return set([])

subset = compute_relevant_subset("root", "humn")
subset.add("root")
print(len(monkeys_numbers.keys()) + len(monkeys_eq.keys()))
print(len(subset))

def reset():
    global monkeys_numbers
    for monkey in subset:
        if monkey not in orig_monkeys_numbers:
            monkeys_numbers.pop(monkey, None)
        #monkeys_numbers = dict(orig_monkeys_numbers)


subset.add("humn")
def must_equal(monkey, res):
    print(monkey, "must equal", res)
    assert monkey in subset
    if monkey == "humn":
        print(res)
        return
    x = monkeys_eq[monkey][0]
    ope = monkeys_eq[monkey][1]
    y = monkeys_eq[monkey][2]
    if x in subset and y in subset:
        print("OK...", x, y)
    assert (x in subset) or (y in subset)
    print("OK, good")
    rev = False
    if y in subset:
        # we need to reverse x and y
        assert y in subset
        (x, y) = (y, x)
        assert x in subset
        rev = True
    assert x in subset
    # Then x is the one we try to find
    # res == x ope y
    # x == res rev_ope y
    yy = monkeys_numbers[y]
    if ope == "+":
        must_equal(x, res - yy)
    elif ope == "*":
        must_equal(x, res / yy)
    elif ope == "/":
        if rev:
            # y / x = res
            # y = x * res
            # x = y / res
            must_equal(x, yy / res)
        else:
            # x / y = res
            # x = res * y
            must_equal(x, res * yy)
    elif ope == "-":
        if rev:
            # y - x = res
            # x = y - res
            must_equal(x, yy - res)
        else:
            # x - y = res
            must_equal(x, res + yy)

# 7570725974392 too high
# 7570725974393.526

evaluate("root")

x = monkeys_eq["root"][0]
y = monkeys_eq["root"][2]

if x in subset:
    must_equal(x, monkeys_numbers[y])
elif y in subset:
    must_equal(y, monkeys_numbers[x])



i = 0
while False:
    if i % 100000 == 0:
        print("Trying...", i)
    reset()
    monkeys_numbers["humn"] = i
    if evaluate("root"):
        print("Found solution", i)
        break
    i -= 1



print("humn" in left, "humn" in right)
