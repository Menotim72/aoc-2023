from bisect import bisect


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
    # returns a list of tuples
    # the first element of each tuple is the start of a range
    # all ranges last until the next number in the list
    # so [(0, 1), (3, 10), (7, 100)]
    # has ranges from 0 to 2, 3 to 6 and 7 to infinity
    # the second element of the tuples is a difference for each range
    # so that if a number n is in a range with a difference d
    # it will map to the number n + d
    # if a range isn't in the original list of ranges it will
    # get a difference of zero
    ranges.sort(key=(lambda x: x[1]))
    proc_ranges = []
    last_range_end = 0
    for dest_start, source_start, length in ranges:
        if source_start > last_range_end:
            proc_ranges.append((last_range_end, 0))
        elif source_start < last_range_end:
            raise ValueError
        proc_ranges.append((source_start, dest_start - source_start))
        last_range_end = source_start + length
    proc_ranges.append((last_range_end, 0))
    return proc_ranges


def map_range(start, length, ranges):
    ls = []
    i = bisect(ranges, start, key=(lambda x: x[0])) - 1
    if not 0 <= i < len(ranges):
        print(i, ranges, start, length)
        raise ValueError
    while i + 1 < len(ranges) and ranges[i + 1][0] < start + length:
        ls.append((start + ranges[i][1], ranges[i + 1][0] - start))
        length -= ranges[i + 1][0] - start
        start = ranges[i + 1][0]
        i += 1
    ls.append((start + ranges[i][1], length))
    return ls


def part2():
    seeds, maps = read_input()
    maps = map(process_map, maps)
    seeds = [(seeds[i], seeds[i + 1]) for i in range(0, len(seeds), 2)]
    for ranges in maps:
        nseeds = []
        for seed in seeds:
            nseeds.extend(map_range(*seed, ranges))
        seeds = nseeds
    return nseeds
