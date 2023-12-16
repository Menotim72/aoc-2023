from collections import defaultdict
from itertools import chain


def read_input():
    with open("input") as file:
        return list(map(str.strip, file))


def move(m, n, i, j, d):
    if d == "s" and i + 1 < m:
        return i + 1, j, d
    if d == "n" and i > 0:
        return i - 1, j, d
    if d == "w" and j > 0:
        return i, j - 1, d
    if d == "e" and j + 1 < n:
        return i, j + 1, d


reflect_slash = {"s": "w", "n": "e", "w": "s", "e": "n"}
reflect_backslash = {"s": "e", "n": "w", "w": "n", "e": "s"}
split_dash = {"s": ("w", "e"), "n": ("w", "e"), "w": ("w",), "e": ("e",)}
split_pipe = {"s": ("s",), "n": ("n",), "w": ("s", "n"), "e": ("s", "n")}


def next_directions(s, d):
    match s:
        case ".":
            return (d,)
        case "/":
            return (reflect_slash[d],)
        case "\\":
            return (reflect_backslash[d],)
        case "-":
            return split_dash[d]
        case "|":
            return split_pipe[d]


def propagate_beam(grid, i, j, d):
    # stack: (i, j, beam-direction)
    # cache: (i, j): known-beam-directions
    stack = [(i, j, d)]
    cache = defaultdict(list)
    m, n = len(grid), len(grid[0])
    while stack:
        i, j, d = stack.pop()
        if d in cache[i, j]:
            continue
        if grid[i][j] == "-" and d in ("s", "n"):
            cache[i, j] = ["s", "n", "w", "e"]
        elif grid[i][j] == "|" and d in ("w", "e"):
            cache[i, j] = ["s", "n", "w", "e"]
        else:
            cache[i, j].append(d)
        stack.extend(
            filter(
                (lambda x: x is not None),
                map((lambda d: move(m, n, i, j, d)), next_directions(grid[i][j], d)),
            )
        )
    return len(cache)


def part1():
    return propagate_beam(read_input(), 0, 0, "e")


def part2():
    grid = read_input()
    return max(
        map(
            (lambda x: propagate_beam(grid, *x)),
            chain(
                ((i, 0, "e") for i in range(len(grid))),
                ((i, len(grid[i]) - 1, "w") for i in range(len(grid))),
                ((0, j, "s") for j in range(len(grid[0]))),
                ((len(grid) - 1, j, "n") for j in range(len(grid[-1]))),
            ),
        )
    )
