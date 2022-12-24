f = "test_input.txt"
f = "input.txt"
lines = [line[:-1] for line in open(f, "r").readlines()[1:]]

sizes = {}
contents = {}
contents["/"] = set([]) # Root
current_path = [] # Root

def stringify_path(path):
    s = "/"
    for x in path:
        s += x
        s += "/"
    return s

for line in lines:
    if line == "$ ls":
        pass # We ignore
    elif line[:3] == "dir":
        name = stringify_path(current_path) + line[4:] + "/"
        contents[stringify_path(current_path)].add(("DIR", name))
    elif line == "$ cd ..":
        current_path = current_path[:-1]
        name = stringify_path(current_path)
        if name not in contents:
            contents[name] = set([])
    elif line[:4] == "$ cd":
        current_path.append(line[5:])
        name = stringify_path(current_path)
        if name not in contents:
            contents[name] = set([])
    else:
        l = line.split(" ")
        size = int(l[0])
        name = stringify_path(current_path) + l[1]
        sizes[name] = size
        contents[stringify_path(current_path)].add(("FILE", name))

computed_size = {}
def compute_size(name):
    if name not in computed_size:
        s = 0
        for (t, k) in contents[name]:
            if t == "FILE":
                s += sizes[k]
            else:
                s += compute_size(k)
        computed_size[name] = s
    return computed_size[name]

s = 0
for d in contents.keys():
    ss = compute_size(d)
    if ss <= 100000:
        s += ss

print(s)

unused = 70000000 - compute_size("/")
minimum = 30000000 - unused
s = compute_size("/")
for d in contents.keys():
    ss = compute_size(d)
    if ss <= s and ss >= minimum:
        s = ss

print(s)
