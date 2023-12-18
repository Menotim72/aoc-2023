from bisect import bisect_left


def read_input():
    plan = []
    with open("input") as file:
        for line in file:
            d, ln, c = line.strip().split()
            plan.append((d, int(ln), c[2:8]))
    return plan


directions = "RDLU"


def small_plan(plan):
    return [(d, ln) for d, ln, _ in plan]


def large_plan(plan):
    return [(directions[int(c[-1])], int(c[:-1], 16)) for _, _, c in plan]


def move(i, j, d, ln):
    match d:
        case "U":
            return i - ln, j
        case "D":
            return i + ln, j
        case "L":
            return i, j - ln
        case "R":
            return i, j + ln


def find_corners(plan):
    cs = []
    i = j = 0
    for d, ln in plan:
        i, j = move(i, j, d, ln)
        cs.append((i, j))
    mini = min(cs, key=(lambda x: x[0]))[0]
    minj = min(cs, key=(lambda x: x[1]))[1]
    cs = [(i - mini, j - minj) for i, j in cs]
    if cs[0][0] != cs[1][0]:
        cs.insert(0, cs.pop())
    return cs


def extra_area(plan):
    a = 0
    for d, ln in plan:
        if d in ("R", "D"):
            a += ln
    return a + 1  # what


def area(corners):
    a = 0
    for p in range(0, len(corners), 2):
        i, j1 = corners[p]
        _, j2 = corners[p + 1]
        a += i * (j1 - j2)
    return a


def part1():
    plan = small_plan(read_input())
    return area(find_corners(plan)) + extra_area(plan)


def part2():
    plan = large_plan(read_input())
    return area(find_corners(plan)) + extra_area(plan)
