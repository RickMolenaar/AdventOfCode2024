from collections import defaultdict
from copy import deepcopy

def parse_input(file = 'day23.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day23example.txt')

def format_input(inp: list[str]):
    connections = defaultdict(set)
    for line in inp:
        c1, c2 = line.split('-')
        connections[c1].add(c2)
        connections[c2].add(c1)
    return connections

def get_networks(c1, connections, to_check):
    if len(to_check) == 0:
        yield [c1]
    for c2 in to_check:
        new_to_check = [c3 for c3 in connections[c2] if c3 > c2 and c3 in to_check]
        for network in get_networks(c2, connections, new_to_check):
            yield [c1] + network

def solve(connections, part, example):
    if part == 1:
        threesets = set()
        for c1 in connections:
            for c2 in connections[c1]:
                for c3 in connections[c1]:
                    if c3 in connections[c2]:
                        threesets.add(tuple(sorted([c1, c2, c3])))
        n = 0
        for s in threesets:
            if any(c.startswith('t') for c in s):
                n += 1
        return n
    best = (0, None)
    for c1 in sorted(connections):
        for network in get_networks(c1, connections, [c for c in connections[c1] if c > c1]):
            if len(network) > best[0]:
                best = (len(network), network)
    return ','.join(sorted(best[1]))
        

def main():
    example_input = format_input(parse_example())
    actual_input = format_input(parse_input())
    for part in (1, 2):
        for example in (True, False):
            inp = deepcopy(example_input if example else actual_input)
            try:
                yield solve(inp, part, example)
            except KeyboardInterrupt:
                raise
            except Exception as e:
                yield e
