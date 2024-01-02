from collections import defaultdict, deque
import random


def read_input():
    graph = defaultdict(list)
    with open("input") as file:
        for line in file:
            if not line:
                continue
            fro, to = line.strip().split(": ")
            to = to.split()
            graph[fro].extend(to)
            for t in to:
                graph[t].append(fro)
    return graph


def shortest_path(graph, a, b):
    opens = deque([(a, ())])
    closed = set()
    while opens:
        c, p = opens.popleft()
        if c == b:
            return c, p
        elif c in closed:
            continue
        closed.add(c)
        for d in graph[c]:
            opens.append((d, (c, p)))


def common_connections(graph):
    conns = defaultdict(int)
    for i, j in zip(random.sample(sorted(graph), 20), random.sample(sorted(graph), 20)):
        if i == j:
            continue
        path = shortest_path(graph, i, j)
        while path[1]:
            conns[min(path[0], path[1][0]), max(path[0], path[1][0])] += 1
            path = path[1]
    return conns


def snip(graph, a, b):
    graph[a].remove(b)
    graph[b].remove(a)


def connect(graph, a, b):
    graph[a].append(b)
    graph[b].append(a)


def connected_set_size(graph, pos):
    conn = set()
    stack = [pos]
    while stack:
        p = stack.pop()
        if p in conn:
            continue
        conn.add(p)
        stack.extend(graph[p])
    return len(conn)


def part1():
    graph = read_input()
    for i in range(3):
        snip(graph, *max(common_connections(graph).items(), key=(lambda x: x[1]))[0])
    s = connected_set_size(graph, next(iter(graph)))
    return s * (len(graph) - s)
