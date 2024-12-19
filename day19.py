from collections import defaultdict
from copy import deepcopy

def parse_input(file = 'day19.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day19example.txt')

max_pattern_length = 0
def format_input(inp: list[str]):
    global max_pattern_length
    patterns = defaultdict(list)
    for p in inp[0].split(', '):
        patterns[p[0]].append(p)
    
    max_pattern_length = max(len(p) for p in patterns)
    designs = inp[2:]
    return patterns, designs

cache = {}

def is_possible(design, patterns):
    if design in cache:
        return cache[design]
    if not design:
        cache[design] = 1
        return 1
    s = 0
    if design in patterns[design[0]]:
        s += 1
    for p in patterns[design[0]]:
        if p == design:
            continue
        if design.startswith(p):
            s += is_possible(design[len(p):], patterns)
            
    cache[design] = s
    return s

def solve(inp, part, example):
    global cache
    cache = {}
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
