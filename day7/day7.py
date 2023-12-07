from collections import defaultdict


def parse_input():
    hands = []
    with open("input") as file:
        for line in file:
            hand, bid = line.split()
            hands.append((hand, int(bid)))
    return hands


types = [
    [1, 1, 1, 1, 1],
    [2, 1, 1, 1],
    [2, 2, 1],
    [3, 1, 1],
    [3, 2],
    [4, 1],
    [5],
]

cards1 = "23456789TJQKA"
cards2 = "J23456789TQKA"


def hand_type1(hand):
    cmap = defaultdict(int)
    for c in hand:
        cmap[c] += 1
    return types.index(sorted(cmap.values(), reverse=True))


def hand_type2(hand):
    cmap = defaultdict(int)
    for c in hand:
        cmap[c] += 1
    js = cmap["J"]
    del cmap["J"]
    if cmap:
        cmap[max(cmap, key=(lambda x: cmap[x]))] += js
    else:
        cmap = {"J": 5}
    return types.index(sorted(cmap.values(), reverse=True))


def strength(hand, hand_type, cards):
    s = [hand_type(hand)]
    for c in hand:
        s.append(cards.find(c))
    return s


def resolve(hand_type, cards):
    hands = parse_input()
    hands.sort(key=(lambda x: strength(x[0], hand_type, cards)))
    s = 0
    for i in range(len(hands)):
        s += (i + 1) * hands[i][1]
    return s


def part1():
    return resolve(hand_type1, cards1)


def part2():
    return resolve(hand_type2, cards2)
