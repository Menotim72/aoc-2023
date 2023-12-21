from collections import defaultdict, deque


def read_input():
    with open("input") as file:
        lines = [()]
        types = ["b"]
        for line in file:
            name, dests = line.strip().split(" -> ")
            if name == "broadcaster":
                lines[0] = ("broadcaster", dests.split(", "))
            else:
                lines.append((name[1:], dests.split(", ")))
                types.append(name[0])
    indexes = {lines[i][0]: i for i in range(len(lines))}
    dests = []
    source_counts = defaultdict(int)
    for line in lines:
        destl = []
        for x in line[1]:
            if x == "rx":
                destl.append(-2)
            elif x not in indexes:
                destl.append(-1)
            elif types[indexes[x]] == "&":
                destl.append((indexes[x], source_counts[indexes[x]]))
                source_counts[indexes[x]] += 1
            else:
                destl.append(indexes[x])
        dests.append(destl)
    state = []
    for i in range(len(types)):
        match types[i]:
            case "b":
                state.append(None)
            case "%":
                state.append(False)
            case "&":
                state.append([False] * source_counts[i])
    return types, dests, state


def press_button(types, dests, state):
    # returns low signals, high signals
    # mutates state
    queue = deque(((0, False),))
    lo = hi = 0
    while queue:
        mod, sig = queue.popleft()
        # print(f'{"High" if sig else "Low"} signal received by {mod}')
        if sig:
            hi += 1
        else:
            lo += 1
        if mod == -1:  # doesn't send further
            continue
        elif isinstance(mod, tuple):  # conjunction
            mod, i = mod
            state[mod][i] = sig
            outsig = not all(state[mod])
        elif types[mod] == "b":  # broadcaster
            outsig = False
        elif sig:  # flip-flop
            continue
        else:
            state[mod] = not state[mod]
            outsig = state[mod]
        for outmod in dests[mod]:
            # print(f'{"High" if outsig else "Low"} signal sent from {mod} to {outmod}')
            queue.append((outmod, outsig))
    return lo, hi


def part1():
    types, dests, state = read_input()
    lo = hi = 0
    for i in range(1000):
        ilo, ihi = press_button(types, dests, state)
        lo += ilo
        hi += ihi
    return lo * hi


def find_cycle_length(types, dests, start):
    cycle_bits = [True]
    for i in dests[start]:
        if not isinstance(i, tuple):
            cur = i
            break
    while True:
        bit = False
        for i in dests[cur]:
            if isinstance(i, tuple):
                bit = True
            else:
                nxt = i
        cycle_bits.append(bit)
        if nxt == cur:
            break
        cur = nxt
    return sum(cycle_bits[i] << i for i in range(len(cycle_bits)))


def part2():
    types, dests, _ = read_input()
    total = 1
    for i in dests[0]:
        total *= find_cycle_length(types, dests, i)
    return total
