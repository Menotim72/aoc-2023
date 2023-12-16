def read_input():
    with open("input") as file:
        return file.read().strip().split(",")


def ascii_hash(string):
    s = 0
    for c in string:
        s += ord(c)
        s = pow(s, 17, 256)
    return s


def part1():
    return sum(map(ascii_hash, read_input()))


def parse_instruction(ins):
    if ins[-1] == "-":
        return ("-", ins[:-1])
    else:
        lbl, n = ins.split("=")
        return ("=", lbl, int(n))


def rem_lens(hashmap, label):
    i = ascii_hash(label)
    for j in range(len(hashmap[i])):
        if hashmap[i][j][0] == label:
            del hashmap[i][j]
            break


def add_lens(hashmap, label, foclen):
    i = ascii_hash(label)
    for j in range(len(hashmap[i])):
        if hashmap[i][j][0] == label:
            hashmap[i][j] = (label, foclen)
            break
    else:
        hashmap[i].append((label, foclen))


def follow_instruction(hashmap, instruction):
    match parse_instruction(instruction):
        case "-", label:
            rem_lens(hashmap, label)
        case "=", label, foclen:
            add_lens(hashmap, label, foclen)


def focusing_power(hashmap):
    s = 0
    for i in range(len(hashmap)):
        for j in range(len(hashmap[i])):
            s += (i + 1) * (j + 1) * hashmap[i][j][1]
    return s


def part2():
    hashmap = [[] for _ in range(256)]
    for instruction in read_input():
        follow_instruction(hashmap, instruction)
    return focusing_power(hashmap)
