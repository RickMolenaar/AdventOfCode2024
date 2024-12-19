from collections import defaultdict
from copy import deepcopy
from AoCHelpers.optimization import Cache

def parse_input(file = 'day19.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day19example.txt')

def format_input(inp: list[str]):
    patterns = defaultdict(list)
    for p in inp[0].split(', '):
        patterns[p[0]].append(p)
    
    designs = inp[2:]
    return patterns, designs

@Cache(key_length = 1)
def is_possible(design, patterns):
    s = 0
    for p in patterns[design[0]]:
        if p == design:
            s += 1
        elif design.startswith(p):
            s += is_possible(design[len(p):], patterns)

    return s

def solve(inp, part, example):
    patterns, designs = inp
    s = 0
    for d in designs:
        if is_possible(d, patterns):
            s += is_possible(d, patterns) if part == 2 else 1
    return s

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
