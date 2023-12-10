directions = {
    "|": ("s", "n"),
    "-": ("w", "e"),
    "L": ("n", "e"),
    "J": ("n", "w"),
    "7": ("s", "w"),
    "F": ("s", "e"),
    ".": (),
}

pipes = {tuple(sorted(v)): k for (k, v) in directions.items()}

opposite = {"s": "n", "n": "s", "w": "e", "e": "w"}


def read_input():
    with open("input") as file:
        return list(map(list, file))


def find_start(grid):
    for i in range(len(grid)):
        try:
            return i, grid[i].index("S")
        except ValueError:
            pass


def move(i, j, d):
    match d:
        case "s":
            return i + 1, j
        case "n":
            return i - 1, j
        case "w":
            return i, j - 1
        case "e":
            return i, j + 1
        case _:
            raise ValueError(d)


def start_pipe(grid, i, j):
    ds = []
    for d in "nswe":
        di, dj = move(i, j, d)
        if opposite[d] in directions[grid[di][dj]]:
            ds.append(d)
    return pipes[tuple(sorted(ds))]


def part1():
    grid = read_input()
    si, sj = find_start(grid)
    grid[si][sj] = start_pipe(grid, si, sj)
    d = directions[grid[si][sj]][0]
    i, j = move(si, sj, d)
    length = 1
    while (i, j) != (si, sj):
        d1, d2 = directions[grid[i][j]]
        if d1 == opposite[d]:
            i, j = move(i, j, d2)
            d = d2
        else:
            i, j = move(i, j, d1)
            d = d1
        length += 1
    return length / 2


def loop_tiles(grid):
    si, sj = find_start(grid)
    grid[si][sj] = start_pipe(grid, si, sj)
    d = directions[grid[si][sj]][0]
    i, j = move(si, sj, d)
    tiles = [(si, sj)]
    while (i, j) != (si, sj):
        tiles.append((i, j))
        d1, d2 = directions[grid[i][j]]
        if d1 == opposite[d]:
            i, j = move(i, j, d2)
            d = d2
        else:
            i, j = move(i, j, d1)
            d = d1
    return tiles


def part2():
    grid = read_input()
    loop = set(loop_tiles(grid))
    i = min(loop, key=(lambda x: x[0]))[0]
    j = jstart = min(loop, key=(lambda x: x[1]))[1]
    ilim = max(loop, key=(lambda x: x[0]))[0]
    jlim = max(loop, key=(lambda x: x[1]))[1]
    depth = area = 0
    while i < ilim:
        if j >= jlim:
            j = jstart
            i += 1
            depth = 0
        elif (i, j) not in loop:
            if depth % 2 == 1:
                area += 1
            j += 1
        elif grid[i][j] == "|":
            depth += 1
            j += 1
        else:
            d = directions[grid[i][j]]
            j += 1
            while grid[i][j] == "-":
                j += 1
            d += directions[grid[i][j]]
            if "n" in d and "s" in d:
                depth += 1
            j += 1
    return area
