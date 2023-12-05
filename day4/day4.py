def parse_line(line):
    line = line.split(":")[1]
    before, after = line.split("|")
    before = set(map(int, before.split()))
    after = set(map(int, after.split()))
    return (before, after)


def matches(line):
    before, after = parse_line(line)
    return len(before & after)


def part1():
    s = 0
    with open("input") as file:
        ms = list(map(matches, file))
    for i in ms:
        if i:
            s += 2 ** (i - 1)
    return s


def part2():
    with open("input") as file:
        ms = list(map(matches, file))
    card_count = [1] * len(ms)
    for i in range(len(ms)):
        for j in range(1, ms[i] + 1):
            # for the next (match count at i) cards
            # add one of that card for each ith card we have
            card_count[i + j] += card_count[i]
    return sum(card_count)
