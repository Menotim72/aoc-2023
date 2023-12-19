from operator import gt, lt, mul
from functools import reduce

CATEGORIES = {"x": 0, "m": 1, "a": 2, "s": 3}
TESTS = {">": gt, "<": lt}
RESULTS = {"A": True, "R": False}


def read_input():
    workflows = {}
    parts = []
    in_parts = False
    with open("input") as file:
        for line in file:
            if not line.strip():
                in_parts = True
                continue
            if in_parts:
                parts.append(parse_part(line.strip()))
            else:
                name, work = parse_workflow(line.strip())
                workflows[name] = work
    return workflows, parts


def parse_part(line):
    return tuple(map((lambda x: int(x[2:])), line[1:-1].split(",")))


def parse_workflow(line):
    name, works = line.split("{", 1)
    works = works.split(",")
    work = []
    for step in works[:-1]:
        cond, res = step.split(":")
        work.append(
            (
                TESTS[cond[1]],
                CATEGORIES[cond[0]],
                int(cond[2:]),
                RESULTS.get(res, res),
            )
        )
    work.append(RESULTS.get(works[-1][:-1], works[-1][:-1]))
    return name, work


def evaluate_part(part, workflows):
    workflow = workflows["in"]
    i = 0
    while True:
        if i == len(workflow) - 1:
            res = workflow[i]
            if isinstance(res, bool):
                return res
            workflow = workflows[res]
            i = 0
            continue
        test, cat, comp, res = workflow[i]
        if not test(part[cat], comp):
            i += 1
            continue
        if isinstance(res, bool):
            return res
        workflow = workflows[res]
        i = 0


def part1():
    wfs, ps = read_input()
    s = 0
    for p in ps:
        if evaluate_part(p, wfs):
            s += sum(p)
    return s


def work_on_range(prn, wf):
    prns = []
    prn = prn[:]
    for test, cat, comp, res in wf[:-1]:
        rn = prn[cat]
        if test == gt:
            frn = rn[0], comp + 1
            trn = comp + 1, rn[1]
        else:  # test == lt
            trn = rn[0], comp
            frn = comp, rn[1]
        if trn[0] < trn[1]:  # nonempty
            tprn = prn[:]
            tprn[cat] = trn
            prns.append((tprn, res))
        if frn[0] >= frn[1]:  # empty
            return prns
        prn[cat] = frn
    prns.append((prn, wf[-1]))
    return prns


def count_parts(prn):
    return reduce(mul, map((lambda x: x[1] - x[0]), prn))


def count_accepted_parts(prn, wfs):
    prns = [(prn, "in")]
    s = 0
    while prns:
        prn, wf = prns.pop()
        if wf is False:
            continue
        elif wf is True:
            s += count_parts(prn)
        else:
            prns.extend(work_on_range(prn, wfs[wf]))
    return s


def part2():
    return count_accepted_parts([(1, 4001)] * 4, read_input()[0])
