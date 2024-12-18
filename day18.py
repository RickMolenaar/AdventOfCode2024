from collections import defaultdict
from copy import deepcopy
from AoCHelpers.optimization import Pathfinder, ORTHOGONAL

def parse_input(file = 'day18.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day18example.txt')

def format_input(inp: list[str]):
    bytes = []
    for line in inp:
        x, y = line.split(',')
        bytes.append((int(x), int(y)))
    return bytes

def print_grid(grid, size):
    for y in range(size[1]):
        s = ''
        for x in range(size[0]):
            s += '.' if grid[x, y] else '#'
        print(s)
    print()

def solve(inp, part, example):
    grid = defaultdict(lambda: True)
    sx, sy = (7, 7) if example else (71, 71)
    for x in range(sx):
        grid[x, -1] = False
        grid[x, sx] = False
    for y in range(sy):
        grid[-1, y] = False
        grid[sx, y] = False
    for b in range(12 if example else 1024):
        grid[inp[b]] = False
    p = Pathfinder(grid, (0, 0), (sx - 1, sy - 1))
    p.neighbors = ORTHOGONAL
    s, sol = p.get_minimal_path()
    if part == 2:
        b = 12 if example else 1024
        while True:
            grid[inp[b]] = False
            try:
                p.get_minimal_path()
            except ValueError:
                return ','.join(map(str, inp[b]))
            b += 1
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
