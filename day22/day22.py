from collections import defaultdict
import heapq


def read_input():
    bricks = []
    with open("input") as file:
        for line in file:
            if not line:
                continue
            p0, p1 = line.strip().split("~")
            x0, y0, z0 = p0.split(",")
            x1, y1, z1 = p1.split(",")
            bricks.append((int(x0), int(y0), int(z0), int(x1), int(y1), int(z1)))
    return bricks


def overlaps(b1, b2):
    return b1[0] <= b2[3] and b2[0] <= b1[3] and b1[1] <= b2[4] and b2[1] <= b1[4]


def measure_z(b):
    return b[5] - b[2] + 1


def support_graph(bricks):
    heights = {}
    support = {}
    bricks = sorted(bricks, key=(lambda x: x[2]))
    for i, brick in enumerate(bricks):
        below = []
        for j in range(i):
            if overlaps(brick, bricks[j]):
                below.append(bricks[j])
        sup = []
        sup_height = -1
        for b in below:
            h = heights[b]
            if h > sup_height:
                sup = [b]
                sup_height = h
            elif h == sup_height:
                sup.append(b)
        support[bricks[i]] = sup
        heights[bricks[i]] = sup_height + measure_z(bricks[i])
    return support


def amount_safely_desintegrable(bricks, support):
    safe = set(bricks)
    for b in support:
        if len(support[b]) == 1 and support[b][0] in safe:
            safe.remove(support[b][0])
    return len(safe)


def part1():
    bricks = read_input()
    return amount_safely_desintegrable(bricks, support_graph(bricks))


def invert_graph(graph):
    inverse = defaultdict(list)
    for k in graph:
        for v in graph[k]:
            inverse[v].append(k)
    return inverse


def falling_bricks(brick, support, inv_support):
    fallen = {brick}
    unsupported = list(map((lambda x: (x[2], x)), inv_support[brick][:]))
    heapq.heapify(unsupported)
    while unsupported:
        _, b = heapq.heappop(unsupported)
        for bel in support[b]:
            if bel not in fallen:
                break
        else:
            fallen.add(b)
            for uns in inv_support[b]:
                heapq.heappush(unsupported, (uns[2], uns))
    return len(fallen) - 1


def part2():
    bricks = read_input()
    support = support_graph(bricks)
    inv_support = invert_graph(support)
    tot = 0
    return sum(falling_bricks(brick, support, inv_support) for brick in bricks)
