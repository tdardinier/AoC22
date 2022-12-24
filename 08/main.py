f = "test_input.txt"
f = "input.txt"
l = [[int(x) for x in line[:-1]] for line in open(f, "r").readlines()]

n = len(l)
m = len(l[0])

vis_left = [ [True for _ in range(m)] for _ in range(n)]
for i in range(n):
    current_max = -1
    for j in range(m):
        if l[i][j] <= current_max:
            vis_left[i][j] = False
        current_max = max(current_max, l[i][j])

vis_right = [ [True for _ in range(m)] for _ in range(n)]
for i in range(n):
    current_max = -1
    for j in range(m - 1, -1, -1):
        if l[i][j] <= current_max:
            vis_right[i][j] = False
        current_max = max(current_max, l[i][j])

vis_top = [ [True for _ in range(m)] for _ in range(n)]
for j in range(m):
    current_max = -1
    for i in range(n):
        if l[i][j] <= current_max:
            vis_top[i][j] = False
        current_max = max(current_max, l[i][j])

vis_bot = [ [True for _ in range(m)] for _ in range(n)]
for j in range(m):
    current_max = -1
    for i in range(n-1, -1, -1):
        if l[i][j] <= current_max:
            vis_bot[i][j] = False
        current_max = max(current_max, l[i][j])

c = 0
for i in range(n):
    for j in range(m):
        if vis_left[i][j] or vis_right[i][j] or vis_top[i][j] or vis_bot[i][j]:
            c += 1
print(c)

m_scenic_score = 0
for i0 in range(n):
    for j0 in range(m):
        scenic_score = 1

        # How many trees above?
        i = i0 - 1
        while i >= 0 and l[i0][j0] > l[i][j0]:
            i -= 1
        i = max(i, 0)
        scenic_score *= (i0 - i)

        # How many trees below?
        i = i0 + 1
        while i < n and l[i0][j0] > l[i][j0]:
            i += 1
        i = min(i, n - 1)
        scenic_score *= (i - i0)

        # How many trees left?
        j = j0 - 1
        while j >= 0 and l[i0][j0] > l[i0][j]:
            j -= 1
        j = max(j, 0)
        scenic_score *= (j0 - j)

        # How many trees below?
        j = j0 + 1
        while j < m and l[i0][j0] > l[i0][j]:
            j += 1
        j = min(j, m - 1)
        scenic_score *= (j - j0)

        m_scenic_score = max(m_scenic_score, scenic_score)

print(m_scenic_score)
