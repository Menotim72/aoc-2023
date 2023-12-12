import functools


def parse_input():
    rows = []
    with open("input") as file:
        for line in file:
            springs, nums = line.strip().split()
            rows.append((springs, tuple(map(int, nums.split(",")))))
    return rows


@functools.cache
def possibs(row, nums, bbef=0):
    if not nums:
        return 0 if "#" in row else 1
    elif not row:
        return 0
    elif row[0] == ".":
        if bbef == 0:
            return possibs(row[1:], nums, 0)
        elif bbef == nums[0]:
            return possibs(row[1:], nums[1:], 0)
        else:
            return 0
    elif row[0] == "#":
        return possibs(row[1:], nums, bbef + 1)
    elif row[0] == "?":
        return possibs("." + row[1:], nums, bbef) + possibs("#" + row[1:], nums, bbef)


def part1():
    return sum(map((lambda x: possibs(x[0] + ".", x[1])), parse_input()))


def unfold(row, nums):
    return ((row + "?") * 5)[:-1] + ".", nums * 5


def part2():
    return sum(map((lambda x: possibs(*unfold(*x), 0)), parse_input()))
