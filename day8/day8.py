def parse_input():
    graph = {}
    with open("input") as file:
        instructions = file.readline().strip()
        file.readline()
        for line in file:
            graph[line[0:3]] = (line[7:10], line[12:15])
    return instructions, graph


def step(pos, inst, graph):
    if inst == "L":
        return graph[pos][0]
    elif inst == "R":
        return graph[pos][1]
    else:
        raise ValueError


def part1():
    instructions, graph = parse_input()
    steps = 0
    position = "AAA"
    while position != "ZZZ":
        i = instructions[steps % len(instructions)]
        position = step(position, i, graph)
        steps += 1
    return steps


def find_cycle(graph, instructions, pos):
    repeats = ind = 0
    li = len(instructions)
    path = {}
    while (pos, ind) not in path:
        path[(pos, ind)] = repeats
        pos = step(pos, instructions[ind], graph)
        ind += 1
        if ind == li:
            ind = 0
            repeats += 1
    cycle_length = li * (repeats - path[(pos, ind)])
    length_before = ind + li * path[(pos, ind)]
    (p, i), r = next(filter((lambda x: x[0][0][-1] == "Z"), path.items()))
    z_l = r * li + i - length_before
    return length_before, cycle_length, z_l


def lcm(a, b):
    a_, b_ = max(a, b), min(a, b)
    while b_ != 0:
        a_, b_ = b_, a_ % b_
    return a * b // a_


def part2():
    instructions, graph = parse_input()
    cycs = [find_cycle(graph, instructions, pos) for pos in graph if pos[-1] == "A"]
    steps = cycs[0][0] + cycs[0][2]
    cycle = cycs[0][1]
    for lb, cl, zl in cycs[1:]:
        while steps < lb or (steps - lb) % cl != zl:
            steps += cycle
        cycle = lcm(cycle, cl)
    return steps
