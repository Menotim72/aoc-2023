import numpy as np


def parse_input():
    with open("input") as file:
        return [list(map(int, line.split())) for line in file]


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


def part1():
    s = 0
    for line in parse_input():
        s += round(evaluate_at(polynomial(line), len(line)))
    return s


def part2():
    s = 0
    for line in parse_input():
        s += round(evaluate_at(polynomial(line), -1))
    return s
