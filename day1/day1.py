p1_digits = [(i, int(i)) for i in "0123456789"]

p2_digits = p1_digits + [
    ("zero", 0),
    ("one", 1),
    ("two", 2),
    ("three", 3),
    ("four", 4),
    ("five", 5),
    ("six", 6),
    ("seven", 7),
    ("eight", 8),
    ("nine", 9),
]


def calibration_value(line, digits):
    first = None
    latest = None
    for i in range(len(line)):
        for s, d in digits:
            if line[i:].startswith(s):
                if first is None:
                    first = d
                latest = d
    return 10 * first + latest


def sum_of_values(digits):
    s = 0
    with open("input") as inp:
        for line in inp:
            s += calibration_value(line, digits)
    return s


def part1():
    return sum_of_values(p1_digits)


def part2():
    return sum_of_values(p2_digits)
