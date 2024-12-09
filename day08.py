from collections import defaultdict
from copy import deepcopy

def parse_input(file = 'day08.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day08example.txt')

def format_input(inp: list[str]):
    grid = []
    antennas = defaultdict(list)
    for y, line in enumerate(inp):
        r = []
        for x, c in enumerate(line):
            r.append(c)
            if c != '.':
                antennas[c].append((x, y))
        grid.append(r)
    return grid, antennas
        

def solve(inp, part, example):
    grid, antennas = inp
    zeros = set()
    for freq in antennas:
        ants = antennas[freq]
        for i, a in enumerate(ants):
            for b in ants[i+1:]:
                dx, dy = a[0] - b[0], a[1] - b[1]
                in_range = True
                d = 0 if part == 2 else 1
                while in_range:
                    in_range = False
                    z1 = (a[0] + d * dx, a[1] + d * dy)
                    z2 = (b[0] - d * dx, b[1] - d * dy)
                    if 0 <= z1[0] < len(grid[0]) and 0 <= z1[1] < len(grid):
                        in_range = True
                        zeros.add(z1)
                    if 0 <= z2[0] < len(grid[0]) and 0 <= z2[1] < len(grid):
                        in_range = True
                        zeros.add(z2)
                    d += 1
                    if part == 1:
                        break
    return len(zeros)

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
