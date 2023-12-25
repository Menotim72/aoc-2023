from z3 import *

MIN_BOUND = 200000000000000
MAX_BOUND = 400000000000000

x0, x1, x2, x3 = Reals("x0 x1 x2 x3")
dx0, dx1, dx2, dx3 = z3.Reals("dx0 dx1 dx2 dx3")
y0, y1, y2, y3 = Reals("y0 y1 y2 y3")
dy0, dy1, dy2, dy3 = Reals("dy0 dy1 dy2 dy3")
z0, z1, z2, z3 = Reals("z0 z1 z2 z3")
dz0, dz1, dz2, dz3 = Reals("dz0 dz1 dz2 dz3")
t1, t2, t3 = Reals("t1 t2 t3")

EQUATIONS = [
    x0 + t1 * dx0 == x1 + t1 * dx1,
    x0 + t2 * dx0 == x2 + t2 * dx2,
    x0 + t3 * dx0 == x3 + t3 * dx3,
    y0 + t1 * dy0 == y1 + t1 * dy1,
    y0 + t2 * dy0 == y2 + t2 * dy2,
    y0 + t3 * dy0 == y3 + t3 * dy3,
    z0 + t1 * dz0 == z1 + t1 * dz1,
    z0 + t2 * dz0 == z2 + t2 * dz2,
    z0 + t3 * dz0 == z3 + t3 * dz3,
    t1 >= 0,
    t2 >= 0,
    t3 >= 0,
]


def read_input():
    stones = []
    with open("input") as file:
        for line in file:
            if not line:
                continue
            p, v = line.strip().split(" @ ")
            px, py, pz = p.split(", ")
            vx, vy, vz = v.split(", ")
            stones.append((int(px), int(py), int(pz), int(vx), int(vy), int(vz)))
    return stones


def intersection(s0, s1):
    x0, y0, _, dx0, dy0, _ = s0
    x1, y1, _, dx1, dy1, _ = s1
    f = dy0 / dx0
    bot = dy1 - dx1 * f
    if bot == 0:
        return None
    t1 = (y0 - x0 * f - y1 + x1 * f) / bot
    if t1 < 0:
        return None
    t0 = (x1 + t1 * dx1 - x0) / dx0
    if t0 < 0:
        return None
    return (x1 + t1 * dx1, y1 + t1 * dy1)


def parallel_same(s0, s1):
    x0, y0, _, dx0, dy0, _ = s0
    x1, y1, _, _, _, _ = s1
    return (y1 - y0) / (x1 - y0) == dy0 / dx0


def part1():
    stones = read_input()
    s = 0
    for i in range(len(stones)):
        for j in range(i):
            ins = intersection(stones[i], stones[j])
            if ins is None:
                continue
            x, y = ins
            if MIN_BOUND < x < MAX_BOUND and MIN_BOUND < y < MAX_BOUND:
                s += 1
    return s


def part2():
    stones = read_input()
    s = Solver()
    for eq in EQUATIONS:
        s.add(eq)
    known = (
        (x1, y1, z1, dx1, dy1, dz1),
        (x2, y2, z2, dx2, dy2, dz2),
        (x3, y3, z3, dx3, dy3, dz3),
    )
    for i in range(3):
        for j in range(6):
            s.add(known[i][j] == stones[i][j])
    s.check()
    mod = s.model()
    return mod[x0] + mod[y0] + mod[z0]
