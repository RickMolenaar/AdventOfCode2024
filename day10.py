from collections import defaultdict
from copy import deepcopy

def parse_input(file = 'day10.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day10example.txt')

def format_input(inp: list[str]):
    grid = defaultdict(lambda: -1)
    trailheads = []
    for y, r in enumerate(inp):
        for x, c in enumerate(r):
            if c == '.':
                continue
            grid[x, y] = int(c)
            if c == '0':
                trailheads.append((x, y))
    return grid, trailheads

def find_trails(grid, loc):
    if grid[loc] == 9:
        yield loc
    else:
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            newloc = (loc[0] + dx, loc[1] + dy)
            if grid[loc[0] + dx, loc[1] + dy] == grid[loc] + 1:
                for dest in find_trails(grid, newloc):
                    yield dest


def solve(inp, part, example):
    grid, trailheads = inp
    s = 0
    for head in trailheads:
        locs = find_trails(grid, head)
        if part == 1:
            s += len(set(locs))
        else:
            s += len(list(locs))
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
