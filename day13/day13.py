import pprint


def parse_input():
    patterns = []
    pattern = []
    with open("input") as file:
        for line in file:
            if line.strip():
                pattern.append(list(line.strip()))
            else:
                patterns.append(pattern)
                pattern = []
    patterns.append(pattern)
    return patterns


def find_reflection(pattern, ignore=()):
    for i in range(1, len(pattern)):
        if i in ignore:
            continue
        length = min(i, len(pattern) - i)
        downlim = i - length - 1
        if downlim == -1:
            downlim = None
        if pattern[i : i + length] == pattern[i - 1 : downlim : -1]:
            return i
    return 0


def transpose(pattern):
    return [
        [pattern[i][j] for i in range(len(pattern))] for j in range(len(pattern[0]))
    ]


def summary(pattern):
    if h := 100 * find_reflection(pattern):
        return h
    if v := find_reflection(transpose(pattern)):
        return v
    raise ValueError


def smudge(pattern, i, j):
    pattern[i][j] = "#" if pattern[i][j] == "." else "."


def part1():
    return sum(map(summary, parse_input()))


def smudge_fixed_summary(pattern):
    orig = (find_reflection(pattern), find_reflection(transpose(pattern)))
    for i in range(len(pattern)):
        for j in range(len(pattern[i])):
            smudge(pattern, i, j)
            if s := find_reflection(pattern, (orig[0],)):
                return 100 * s
            elif s := find_reflection(transpose(pattern), (orig[1],)):
                return s
            smudge(pattern, i, j)
    raise ValueError


def part2():
    return sum(map(smudge_fixed_summary, parse_input()))
