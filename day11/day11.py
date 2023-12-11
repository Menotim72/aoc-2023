def parse_input():
    gals = []
    with open("input") as file:
        grid = file.readlines()
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "#":
                gals.append((i, j))
    return gals


def inc_at(tpl, d, i):
    if d == 0:
        return (tpl[0] + i, tpl[1])
    elif d == 1:
        return (tpl[0], tpl[1] + i)


def expand_universe(gals, d, g):
    # d is the direction, 0 for x or 1 for y
    gals = sorted(gals, key=(lambda x: x[d]))
    xgals = []
    ind = growth = 0
    for dist in range(gals[0][d], gals[-1][d] + 1):
        if gals[ind][d] != dist:
            growth += g
        while ind < len(gals) and gals[ind][d] == dist:
            xgals.append(inc_at(gals[ind], d, growth))
            ind += 1
    return xgals


def sum_of_distances(gals):
    s = 0
    for i in range(1, len(gals)):
        for j in range(i):
            s += abs(gals[i][0] - gals[j][0])
            s += abs(gals[i][1] - gals[j][1])
    return s


def solve(g):
    return sum_of_distances(expand_universe(expand_universe(parse_input(), 0, g), 1, g))


def part1():
    return solve(1)


def part2():
    return solve(999999)
