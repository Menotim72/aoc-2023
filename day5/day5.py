from bisect import bisect_right


def read_input():
    with open("input") as file:
        seeds = list(map(int, file.readline().split()[1:]))
        file.readline()  # skip empty line
        maps = []
        curr_map = []
        header_next = True
        for line in file:
            if header_next:
                header_next = False
            elif not line.strip():
                maps.append(curr_map)
                curr_map = []
                header_next = True
            else:
                curr_map.append(tuple(map(int, line.split())))
    return seeds, maps


def process_map(ranges):
    # returns two lists
    # the first list has a number for the start of each range
    # all ranges last until the next number in the list
    # so [0, 3, 7] has ranges from 0 to 2, 3 to 6 and 7 to infinity
    # so if a range isn't in the original list of ranges it will
    # get a mapping with a difference of zero
    # the second list has a difference for each range
    # so that if a number n is in a range with a difference d
    # it will map to the number n + d
    ranges.sort(key=(lambda x: x[1]))
    range_starts = []
    differences = []
    last_range_end = 0
    for dest_start, source_start, length in ranges:
        if source_start > last_range_end:
            range_starts.append(last_range_end)
            differences.append(0)
        elif source_start < last_range_end:
            raise ValueError
        range_starts.append(source_start)
        differences.append(dest_start - source_start)
        last_range_end = source_start + length
    range_starts.append(last_range_end)
    differences.append(0)
    return range_starts, differences


def map_number(num, range_starts, differences):
    ind = bisect_right(range_starts, num) - 1
    if ind < 0:
        raise ValueError
    return num + differences[ind]


def part1():
    seeds, maps = read_input()
    maps = list(map(process_map, maps))
    for rs, diff in maps:
        seeds = list(map((lambda s: map_number(s, rs, diff)), seeds))
    return min(seeds)


def map_range(start, length, range_starts, differences):
    outs = []
    ind = bisect_right(range_starts, start) - 1
    while ind + 1 < len(range_starts) and start + length > range_starts[ind + 1]:
        outs.append((start + differences[ind], range_starts[ind + 1] - start))
        length -= range_starts[ind + 1] - start
        start = range_starts[ind + 1]
        ind += 1
    outs.append((start + differences[ind], length))
    return outs


def part2():
    seeds, maps = read_input()
    seeds = [(seeds[i], seeds[i + 1]) for i in range(0, len(seeds), 2)]
    maps = list(map(process_map, maps))
    alls = []
    for rs, diff in maps:
        alls.append(seeds)
        nseeds = []
        for start, length in seeds:
            nseeds.extend(map_range(start, length, rs, diff))
        seeds = nseeds
    # return seeds
    alls.append(seeds)
    return alls
    return min(seeds, key=(lambda x: x[0]))[0]
