from collections import deque
import numpy as np

STEP_COUNT = 26501365


def read_input():
    grid = []
    i = 0
    with open("input") as file:
        for line in file:
            if not line:
                continue
            if "S" in line:
                start = (i, line.find("S"))
                line = line.replace("S", ".")
            grid.append(line.strip())
            i += 1
    return grid, start


def neighbors(i, j):
    return ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1))


def reachable(grid, start, steps, infinite):
    # returns set of places reachable with at most steps steps
    reached = set()
    queue = deque([(start[0], start[1], 0)])
    while queue:
        i, j, s = queue.popleft()
        if (i, j) in reached:
            continue
        reached.add((i, j))
        if s >= steps:
            continue
        for ii, jj in neighbors(i, j):
            if grid[ii % len(grid)][jj % len(grid[0])] != ".":
                continue
            if infinite or 0 <= ii < len(grid) and 0 <= jj < len(grid[ii]):
                queue.append((ii, jj, s + 1))
    return reached


def parity(i, j):
    return (i + j) % 2


def amount_reachable(grid, start, steps, infinite):
    # returns amount of places reachable in EXACTLY steps steps
    p = parity(*start) + steps % 2
    return len([x for x in reachable(grid, start, steps, infinite) if parity(*x) == p])


def part1():
    return amount_reachable(*read_input(), 64, False)


def polynomial(seq):
    # produces a list [a0, a1, ..., an]
    # such that a0 + a1*i + ... + an*i^n == seq[i]
    evaluator = np.array(
        [[float(i**j) for j in range(len(seq))] for i in range(len(seq))]
    )
    # evaluator @ a == seq
    return np.linalg.solve(evaluator, seq)


def evaluate_at(polynomial, value):
    total = 0
    for i in polynomial[::-1]:
        total *= value
        total += i
    return total


def part2():
    grid, start = read_input()
    ln = len(grid)
    n = STEP_COUNT % ln
    a = amount_reachable(grid, start, n, True)
    b = amount_reachable(grid, start, n + ln, True)
    c = amount_reachable(grid, start, n + 2 * ln, True)
    p = polynomial([a, b, c])
    return int(evaluate_at(p, STEP_COUNT // ln))
