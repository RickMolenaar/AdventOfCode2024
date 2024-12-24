from collections import defaultdict
from copy import deepcopy
from AoCHelpers.optimization import Pathfinder, ORTHOGONAL

def parse_input(file = 'day20.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day20example.txt')

def format_input(inp: list[str]):
    grid = {}

    for y, line in enumerate(inp):
        for x, c in enumerate(line):
            grid[x, y] = False if c == '#' else True
            if c == 'S':
                start = (x, y)
            elif c == 'E':
                end = (x, y)
    return grid, start, end

def solve(inp, part, example):
    grid, start, end = inp
    distances = {k: None for k in grid}
    distances[start] = 0
    to_update = set([start])
    while to_update:
        node = to_update.pop()
        d0 = distances[node]
        for n in ORTHOGONAL(node):
            if distances[n] is None and grid[n] == True:
                distances[n] = d0 + 1
                to_update.add(n)
    max_x = max(t[0] for t in grid)
    max_y = max(t[1] for t in grid)
    time_saved = defaultdict(int)
    max_time_skip = 2 if part == 1 else 20
    for (x, y) in grid:
        if not grid[x, y]:
            continue
        if x == 0 or x == max_x:
            continue
        if y == 0 or y == max_y:
            continue
        for dx in range(-max_time_skip, max_time_skip + 1):
            nx = x + dx
            if not 0 < nx < max_x:
                continue
            for dy in range(-max_time_skip + abs(dx), max_time_skip - abs(dx) + 1):
                ny = y + dy
                if not 0 < ny < max_y:
                    continue
                if not grid[nx, ny]:
                    continue
                d = abs(dx) + abs(dy)
                old_time = distances[nx, ny] - distances[x, y]
                if old_time > d:
                    time_saved[old_time - d] += 1
    res = 0
    for k in sorted(time_saved):
        if k >= 100:
            res += time_saved[k]
    return res

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
