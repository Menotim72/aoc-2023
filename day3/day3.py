DIGITS = "0123456789"
NONSYM = DIGITS + ".\n"


def neighbors(m, n, line, start, end):
    neighs = []
    if line > 0:
        if start > 0:
            neighs.append((line - 1, start - 1))
        if end < n:
            neighs.append((line - 1, end))
        for i in range(start, end):
            neighs.append((line - 1, i))
    if start > 0:
        neighs.append((line, start - 1))
    if end < n:
        neighs.append((line, end))
    if line < m - 1:
        if start > 0:
            neighs.append((line + 1, start - 1))
        if end < n:
            neighs.append((line + 1, end))
        for i in range(start, end):
            neighs.append((line + 1, i))
    return neighs


def next_to_sym(lines, line, start, end):
    for i, j in neighbors(len(lines), len(lines[line]), line, start, end):
        if lines[i][j] not in NONSYM:
            return True
    return False


def get_nums(lines):
    nums = []
    for i in range(len(lines)):
        j = 0
        while j < len(lines[i]):
            if lines[i][j] in DIGITS:
                start = j
                while lines[i][j] in DIGITS:
                    j += 1
                nums.append((i, start, j))
            else:
                j += 1
    return nums


def sum_of_sym_adjacent(lines):
    s = 0
    for line, start, end in get_nums(lines):
        if next_to_sym(lines, line, start, end):
            s += int(lines[line][start:end])
    return s


def part1():
    with open("input") as file:
        lines = file.readlines()
    return sum_of_sym_adjacent(lines)


def is_digit(lines, i, j):
    return 0 <= i < len(lines) and 0 <= j < len(lines[i]) and lines[i][j] in DIGITS


def get_num(lines, i, j):
    if not is_digit(lines, i, j):
        return None
    start = j
    while is_digit(lines, i, start):
        start -= 1
    end = j
    while is_digit(lines, i, end):
        end += 1
    return int(lines[i][start + 1 : end])


def add_num(nums, lines, i, j):
    n = get_num(lines, i, j)
    if n is None:
        return False
    nums.append(n)
    return True


def neighboring_nums(lines, i, j):
    nums = []
    # before
    add_num(nums, lines, i, j - 1)
    # after
    add_num(nums, lines, i, j + 1)
    # above
    pa = add_num(nums, lines, i - 1, j)
    if not pa:
        add_num(nums, lines, i - 1, j - 1)
        add_num(nums, lines, i - 1, j + 1)
    # below
    pb = add_num(nums, lines, i + 1, j)
    if not pb:
        add_num(nums, lines, i + 1, j - 1)
        add_num(nums, lines, i + 1, j + 1)
    return nums


def part2():
    with open("input") as file:
        lines = file.readlines()
    s = 0
    ns = (
        (i, j)
        for i in range(len(lines))
        for j in range(len(lines[i]))
        if lines[i][j] not in NONSYM
    )
    for i, j in ns:
        nnums = neighboring_nums(lines, i, j)
        if len(nnums) == 2:
            s += nnums[0] * nnums[1]
    return s
