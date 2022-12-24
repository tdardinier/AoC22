# f = open("test_input.txt", "r").readlines()
f = open("input.txt", "r").readlines()
moves = []
for x in f:
    l = x.split(" ")
    moves.append((l[0], l[1][:-1]))

translation = {}
translation["X"] = 0
translation["A"] = 0
translation["Y"] = 1
translation["B"] = 1
translation["Z"] = 2
translation["C"] = 2

def points(mine):
    return translation[mine] + 1

def score(opponent, mine):
    r = (translation[mine] - translation[opponent] + 1) % 3
    return r * 3

def achieve_res(opponent, res):
    if res == "Y":
        return opponent
    elif res == "X": # lose
        return (opponent - 1) % 3
    else: # win
        return (opponent + 1) % 3

s = 0
for (a, bb) in moves:
    #b = bb # first mode
    print(a)
    b = ["A", "B", "C"][achieve_res(translation[a], bb)]
    s += points(b) + score(a, b) # first mode
