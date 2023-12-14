from itertools import product

CYCLE_COUNT = 1000000000


def parse_input():
    with open("input") as file:
        return [list(line.strip()) for line in file]


def find_last_empty(grid, i, j, di, dj):
    while (
        0 <= i + di < len(grid)
        and 0 <= j + dj < len(grid[i + di])
        and grid[i + di][j + dj] == "."
    ):
        i += di
        j += dj
    return i, j


def swap(grid, i0, j0, i1, j1):
    grid[i0][j0], grid[i1][j1] = grid[i1][j1], grid[i0][j0]


def tilt_direction(grid, di, dj):
    if di > 0:
        ri = range(len(grid) - 1, -1, -1)
    else:
        ri = range(len(grid))
    if dj > 0:
        rj = range(len(grid[0]) - 1, -1, -1)
    else:
        rj = range(len(grid[0]))
    for i, j in product(ri, rj):
        if grid[i][j] == "O":
            swap(grid, i, j, *find_last_empty(grid, i, j, di, dj))


def north_load(grid):
    s = 0
    for i, j in product(range(-1, -len(grid) - 1, -1), range(len(grid))):
        if grid[i][j] == "O":
            s -= i
    return s


def part1():
    grid = parse_input()
    tilt_direction(grid, -1, 0)
    return north_load(grid)


def spin_cycle(grid):
    tilt_direction(grid, -1, 0)
    tilt_direction(grid, 0, -1)
    tilt_direction(grid, 1, 0)
    tilt_direction(grid, 0, 1)


def part2():
    grid = parse_input()
    cache = {}
    i = 0
    while i < CYCLE_COUNT and tuple(map(tuple, grid)) not in cache:
        cache[tuple(map(tuple, grid))] = i
        spin_cycle(grid)
        i += 1
    cyc_len = i - cache[tuple(map(tuple, grid))]
    remainder = (CYCLE_COUNT - i) % cyc_len
    for _ in range(remainder):
        spin_cycle(grid)
    return north_load(grid)
