from copy import deepcopy

def parse_input(file = 'day06.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day06example.txt')

def format_input(inp: list[str]):
    grid = []
    for y, line in enumerate(inp):
        r = []
        for x, c in enumerate(line):
            if c == '^':
                guard = (x, y)
                r.append('.')
            else:
                r.append(c)
        grid.append(r)
    return grid, guard

def get_next(pos, dir):
    match dir:
        case 0:
            return (pos[0], pos[1] - 1)
        case 1:
            return (pos[0] + 1, pos[1])
        case 2:
            return (pos[0], pos[1] + 1)
        case 3:
            return (pos[0] - 1, pos[1])

def has_loop(guard, guard_dir, grid, example):
    visited = set()
    visited.add((guard, 0))
    next = guard[0], guard[1] - 1
    while (next, guard_dir) not in visited:
        assert next[0] >= 0 and next[1] >= 0
        visited.add((next, guard_dir))
        guard = next
        next = get_next(guard, guard_dir)
        if next[0] < 0 or next[1] < 0 or next[0] == len(grid[0]) or next[1] == len(grid):
            return False
        while grid[next[1]][next[0]] == '#':
            guard_dir += 1
            guard_dir %= 4
            next = get_next(guard, guard_dir)
    return True

def solve(inp, part, example):
    grid, guard = inp
    g0 = guard
    guard_dir = 0
    visited = set([guard])
    next = guard[0], guard[1] - 1
    opts = set()
    possible = set()
    while True:
        visited.add(next)
        opts.add(next)
        guard = next
        next = get_next(guard, guard_dir)
        if not (0 <= next[0] < len(grid[0]) and 0 <= next[1] < len(grid)):
            break
        while grid[next[1]][next[0]] == '#':
            guard_dir += 1
            guard_dir %= 4
            next = get_next(guard, guard_dir)
        if not (0 <= next[0] < len(grid[0]) and 0 <= next[1] < len(grid)):
            break
    if part == 1:
        return len(visited)
    
    for opt in opts:
        if grid[opt[1]][opt[0]] == '#' or opt == g0:
            continue
        grid[opt[1]][opt[0]] = '#'
        if has_loop(g0, 0, grid, example):
            possible.add(opt)
        grid[opt[1]][opt[0]] = '.'
    return len(possible)

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
