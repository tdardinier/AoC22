f = open("test_input.txt", "r").readlines()
f = open("input.txt", "r").readlines()

from enum import Enum

class Cell(Enum):
    NOTHING = 0
    OPEN = 1
    WALL = 2

mapp = []
for line in f[:-2]:
    l = []
    for x in line[:-1]:
        if x == " ":
            l.append(Cell.NOTHING)
        elif x == ".":
            l.append(Cell.OPEN)
        elif x == "#":
            l.append(Cell.WALL)
        else:
            assert false
    mapp.append(line)
