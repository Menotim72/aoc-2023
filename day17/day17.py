import heapq


def read_input():
    with open("input") as file:
        return [[int(i) for i in line.strip()] for line in file]


directions = {"n", "s", "w", "e"}

opposite = {"n": "s", "w": "e", "s": "n", "e": "w"}


def move(i, j, d):
    match d:
        case "n":
            return i - 1, j
        case "s":
            return i + 1, j
        case "w":
            return i, j - 1
        case "e":
            return i, j + 1


def in_grid(grid, i, j):
    return 0 <= i < len(grid) and 0 <= j < len(grid[i])


def next_directions(d, ld, ultra):
    if ld == 0:
        return directions
    elif not ultra and ld < 3:
        return directions - {opposite[d]}
    elif not ultra:
        return directions - {d, opposite[d]}
    elif ld < 4:
        return {d}
    elif ld < 10:
        return directions - {opposite[d]}
    elif ld == 10:
        return directions - {d, opposite[d]}


def add_direction(heap, grid, nd, i, j, d, ld, ln, ei, ej):
    ni, nj = move(i, j, nd)
    if not in_grid(grid, ni, nj):
        return
    nln = ln + grid[ni][nj]
    nld = ld + 1 if d == nd else 1
    priority = nln + abs(ei - ni) + abs(ej - nj)
    heapq.heappush(heap, (priority, ni, nj, nd, nld, nln, (i, j, d, ld)))


def find_path(grid, start, end, ultra):
    # i, j, direction, prev length in direction
    closed = {}
    # priority, i, j, direction, prev length in direction, length
    heap = [(0, *start, None, 0, 0, None)]
    while True:
        _, i, j, d, ld, ln, prev = heapq.heappop(heap)
        if (i, j, d, ld) in closed:
            continue
        closed[i, j, d, ld] = prev
        if (i, j) == end and (not ultra or ld >= 4):
            return ln, (i, j, d, ld), closed
        for nd in next_directions(d, ld, ultra):
            add_direction(heap, grid, nd, i, j, d, ld, ln, *end)


def reconstruct_path(end, closed):
    ls = []
    while closed[end] is not None:
        ls.append(end)
        end = closed[end]
    ls.reverse()
    return ls


def part1():
    grid = read_input()
    return find_path(grid, (0, 0), (len(grid) - 1, len(grid[0]) - 1), False)[0]


def part2():
    grid = read_input()
    return find_path(grid, (0, 0), (len(grid) - 1, len(grid[0]) - 1), True)[0]
