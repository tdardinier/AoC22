f = "test_input.txt"
n_monkeys = 4


second_round = True

f = "input.txt"
n_monkeys = 8

lines = [line[:-1] for line in open(f, "r").readlines()]


def evaluate(exp, val):
    return eval(exp.replace("old", str(val)))

monkeys = []
items = []
for i in range(n_monkeys):
    ii = i * 7
    items.append([])
    monkeys.append([None, None, None, None])
    # print(lines[ii + 1])
    for x in lines[ii + 1].split(": ")[1].split(", "):
        items[-1].append(int(x) % common)
    monkeys[-1][0] = lines[ii + 2].split(" = ")[1]
    monkeys[-1][1] = int(lines[ii + 3].split(" by ")[1])
    monkeys[-1][2] = int(lines[ii + 4].split(" monkey ")[1])
    monkeys[-1][3] = int(lines[ii + 5].split(" monkey ")[1])

common = 1
for m in monkeys:
    common *= m[1]

numbers = [0 for _ in range(n_monkeys)]

# Let's do a round
def exec_round():
    for i in range(n_monkeys):
        # print("Monkey", i)
        m = monkeys[i]
        for x in items[i]:
            numbers[i] += 1
            r = evaluate(m[0], x)
            if not second_round:
                r = r // 3
            # r = evaluate(m[0], x) // 3
            # print("Item", x, r)
            if r % m[1] == 0:
                items[m[2]].append(r % common)
                # print(r, "sent to", m[2])
            else:
                items[m[3]].append(r % common)
                # print(r, "sent to", m[3])
        items[i] = []

n_turn = 20
if second_round:
    n_turn = 10000
for i_turn in range(n_turn):
    if i_turn % 50 == 0:
        print(i_turn)
    exec_round()
    # print(items)

l = sorted(numbers)
print(l[-1] * l[-2])
