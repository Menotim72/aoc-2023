from collections import defaultdict
from math import log


def read_input():
    with open("input") as file:
        return [line.strip() for line in file if line.strip()]


def neighbors(i, j, m, n):
    if 0 <= i - 1:
        yield i - 1, j
    if i + 1 < m:
        yield i + 1, j
    if 0 <= j - 1:
        yield i, j - 1
    if j + 1 < n:
        yield i, j + 1


def can_move(grid, i, j, ni, nj):
    if grid[ni][nj] == "#":
        return False
    elif grid[ni][nj] == ".":
        return True
    elif grid[ni][nj] == ">":
        return j < nj
    elif grid[ni][nj] == "<":
        return nj < j
    elif grid[ni][nj] == "v":
        return i < ni
    elif grid[ni][nj] == "^":
        return ni < i


def movable_neighbors(grid, i, j):
    return filter(
        (lambda x: can_move(grid, i, j, *x)),
        neighbors(i, j, len(grid), len(grid[0])),
    )


def longest_walk(grid):
    i = 1
    walks = [((0, 0), (0, 1), 0)]  # previous, here, length
    end = (len(grid) - 1, len(grid[0]) - 2)
    max_total = 0
    while walks:
        prev, here, ln = walks.pop()
        if here == end:
            max_total = max(max_total, ln)
            continue
        for neigh in movable_neighbors(grid, *here):
            if neigh != prev:
                walks.append((here, neigh, ln + 1))
    return max_total


def part1():
    return longest_walk(read_input())


def move(grid, prev, here):
    for i, j in neighbors(*here, len(grid), len(grid[0])):
        if (i, j) != prev and grid[i][j] != "#":
            return i, j


def follow_path(grid, pos0, pos1):
    pos0, pos1 = pos1, move(grid, pos0, pos1)
    ln = 2
    while grid[pos1[0]][pos1[1]] == ".":
        mv = move(grid, pos0, pos1)
        if mv is None:
            return pos0, pos1, ln
        pos0, pos1 = pos1, mv
        ln += 1
    return pos1, move(grid, pos0, pos1), ln + 1


def distance_graph(grid):
    graph = defaultdict(list)
    explored = defaultdict(list)
    prev, here, ln = follow_path(grid, (0, 1), (1, 1))
    graph[0, 1].append((here, ln))
    graph[here].append(((0, 1), ln))
    explored[here].append(prev)
    stack = [(here)]
    while stack:
        here = stack.pop()
        for i, j in neighbors(*here, len(grid), len(grid[0])):
            if grid[i][j] != "#" and (i, j) not in explored[here]:
                pend, end, ln = follow_path(grid, here, (i, j))
                graph[here].append((end, ln))
                graph[end].append((here, ln))
                explored[here].append((i, j))
                explored[end].append(pend)
                stack.append(end)
    return graph


def ll_contains(ll, x):
    return ll and (x == ll[0] or ll_contains(ll[1], x))


def longest_path(graph, start, end):
    paths = [(start, 0, ())]
    max_total = 0
    while paths:
        pos, ln, before = paths.pop()
        if pos == end:
            max_total = max(max_total, ln)
            continue
        for nxt, li in graph[pos]:
            if ll_contains(before, nxt):
                continue
            paths.append((nxt, ln + li, (pos, before)))
    return max_total


def part2():
    grid = read_input()
    return longest_path(distance_graph(grid), (0, 1), (len(grid) - 1, len(grid[0]) - 2))
