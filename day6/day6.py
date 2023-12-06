import math


def parse_input_1():
    with open("input") as file:
        times = list(map(int, file.readline().split()[1:]))
        distances = list(map(int, file.readline().split()[1:]))
    return times, distances


def winning_range(n, r):
    # duration = n, record = r
    # if you charge for x you go x(n-x)
    # so you win if x(n-x) - r > 0
    # which meanx x^2 - nx + r < 0
    # so the range is between the solutions of that equation
    # returns two ints a and b
    # an int x is winning if a <= x < b

    delta = n * n - 4 * r
    if delta <= 0:
        raise ValueError
    x1 = (n - math.sqrt(delta)) / 2
    x2 = (n + math.sqrt(delta)) / 2
    return math.ceil(x1), math.floor(x2) + 1


def part1():
    prod = 1
    for n, r in zip(*parse_input_1()):
        a, b = winning_range(n, r)
        prod *= b - a
    return prod


def parse_input_2():
    with open("input") as file:
        time = int("".join(filter(str.isdigit, file.readline())))
        distance = int("".join(filter(str.isdigit, file.readline())))
    return time, distance


def part2():
    n, r = parse_input_2()
    a, b = winning_range(n, r)
    return b - a
