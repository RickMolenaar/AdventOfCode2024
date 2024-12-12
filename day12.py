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

def get_area(grid, loc, area = None, example = False):
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
                area.update(get_area(grid, (nx, ny), area, example))
        except KeyError:
            continue
    return area

def get_price(grid, area: set, price_type):
    borders = []
    for loc in area:
        plant = grid[loc]
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = loc[0] + dx, loc[1] + dy
            try:
                if grid[nx, ny] != grid[loc]:
                    borders.append((nx, ny))
            except KeyError:
                borders.append((nx, ny))
    if price_type == 'perimeter':
        return len(area) * len(borders)
    
    sides = 0
    checked = set()
    for (x, y) in sorted(area):
        if (x, y, 'u') not in checked:
            if (x, y-1) in borders:
                sides += 1
                checked.add((x, y, 'u'))
                dx = -1
                while (x + dx, y) not in borders and (x + dx, y - 1) in borders:
                    checked.add((x + dx, y, 'u'))
                    dx -= 1
                dx = 1
                while (x + dx, y) not in borders and (x + dx, y - 1) in borders:
                    checked.add((x + dx, y, 'u'))
                    dx += 1
        if (x, y, 'd') not in checked:
            if (x, y+1) in borders:
                sides += 1
                checked.add((x, y, 'd'))
                dx = -1
                while (x + dx, y) not in borders and (x + dx, y + 1) in borders:
                    checked.add((x + dx, y, 'd'))
                    dx -= 1
                dx = 1
                while (x + dx, y) not in borders and (x + dx, y + 1) in borders:
                    checked.add((x + dx, y, 'd'))
                    dx += 1
        if (x, y, 'l') not in checked:
            if (x - 1, y) in borders:
                sides += 1
                checked.add((x, y, 'l'))
                dy = -1
                while (x, y + dy) not in borders and (x - 1, y + dy) in borders:
                    checked.add((x, y + dy, 'l'))
                    dy -= 1
                dy = 1
                while (x, y + dy) not in borders and (x - 1, y + dy) in borders:
                    checked.add((x, y + dy, 'l'))
                    dy += 1
        if (x, y, 'r') not in checked:
            if (x + 1, y) in borders:
                sides += 1
                checked.add((x, y, 'r'))
                dy = -1
                while (x, y + dy) not in borders and (x + 1, y + dy) in borders:
                    checked.add((x, y + dy, 'r'))
                    dy -= 1
                dy = 1
                while (x, y + dy) not in borders and (x + 1, y + dy) in borders:
                    checked.add((x, y + dy, 'r'))
                    dy += 1
    
    return len(area) * sides
    

def solve(grid, part, example):
    s = 0
    seen = set()
    for y in range(max(grid)[1] + 1):
        for x in range(max(grid)[0] + 1):
            if (x, y) in seen:
                continue
            area = get_area(grid, (x, y), example = example)
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
