from copy import deepcopy

def parse_input(file = 'day12.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day12example.txt')

def format_input(inp: list[str]):
    grid = {}
    for y, row in enumerate(inp):
        for x, c in enumerate(row):
            grid[x, y] = c
    return grid

def get_area(grid, loc, area = None):
    if area is None:
        area = set([loc])
    plant = grid[loc]
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = loc[0] + dx, loc[1] + dy
        if (nx, ny) in area:
            continue
        try:
            if grid[nx, ny] == plant:
                area.add((nx, ny))
                area.update(get_area(grid, (nx, ny), area))
        except KeyError:
            continue
    return area

def get_price(grid, area: set, price_type):
    edges = set()
    for loc in area:
        plant = grid[loc]
        for dx, dy, dir in [(-1, 0, 'l'), (1, 0, 'r'), (0, -1, 'd'), (0, 1, 'u')]:
            neighbor = (loc[0] + dx, loc[1] + dy)
            if neighbor not in grid or grid[neighbor] != grid[loc]:
                edges.add((*loc, dir))
    if price_type == 'perimeter':
        return len(area) * len(edges)
    
    sides = 0
    while edges:
        x, y, dir = edges.pop()
        sides += 1
        if dir in 'ud':
            dx = -1
            while (x + dx, y, dir) in edges:
                edges.remove((x + dx, y, dir))
                dx -= 1
            dx = 1
            while (x + dx, y, dir) in edges:
                edges.remove((x + dx, y, dir))
                dx += 1
        else:
            dy = -1
            while (x, y + dy, dir) in edges:
                edges.remove((x, y + dy, dir))
                dy -= 1
            dy = 1
            while (x, y + dy, dir) in edges:
                edges.remove((x, y + dy, dir))
                dy += 1
    return len(area) * sides
    

def solve(grid, part, example):
    s = 0
    seen = set()
    for y in range(max(grid)[1] + 1):
        for x in range(max(grid)[0] + 1):
            if (x, y) in seen:
                continue
            area = get_area(grid, (x, y))
            seen.update(set(area))
            s += get_price(grid, area, 'perimeter' if part == 1 else 'sides')
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
