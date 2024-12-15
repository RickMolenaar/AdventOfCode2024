from copy import deepcopy

def parse_input(file = 'day15.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day15example.txt')

def format_input(inp: list[str]):
    map = []
    commands = ''
    map_done = False
    for line in inp:
        if not line:
            map_done = True
        if map_done:
            commands += line
        else:
            map.append(line)
    return map, commands

def read_map(inp, part):
    map = {}
    for y, line in enumerate(inp):
        for x, c in enumerate(line):
            if part == 2:
                x *= 2
            map[x, y] = c
            if c == '@':
                robot = (x, y)
                map[x, y] = '.'
            if part == 2:
                match c:
                    case '@':
                        map[x + 1, y] = '.'
                    case 'O':
                        map[x, y] = '['
                        map[x + 1, y] = ']'
                    case _:
                        map[x + 1, y] = c

    return map, robot

def attempt_move(map, command, robot, part, debug = False):
    match command:
        case '^':
            dx, dy = 0, -1
        case '>': 
            dx, dy = 1, 0
        case 'v':
            dx, dy = 0, 1
        case '<':
            dx, dy = -1, 0
    to_move = []
    px, py = robot
    to_check = [robot]
    while 1:
        px += dx
        py += dy
        can_move = True
        if part == 1 or dy == 0:
            if map[px, py] == '#':
                return robot
            if map[px, py] != '.':
                to_move.append((px, py))
                can_move = False
        else:
            new_to_check = set()
            for lx, ly in to_check:
                match map[lx, ly + dy]:
                    case '#':
                        return robot
                    case ']':
                        new_to_check.add((lx, ly + dy))
                        new_to_check.add((lx - 1, ly + dy))
                    case '[':
                        new_to_check.add((lx, ly + dy))
                        new_to_check.add((lx + 1, ly + dy))
            if new_to_check:
                can_move = False
                to_check = new_to_check
                to_move.extend(to_check)
        if can_move:
            new = [(x + dx, y + dy, map[x, y]) for x, y in to_move]
            for old in to_move:
                map[old] = '.'
            for x, y, c in new:
                map[x, y] = c
            return (robot[0] + dx, robot[1] + dy)

def draw_map(map: dict, robot: tuple):
    ly = 0
    s = ''
    for x, y in sorted(map, key = lambda t: t[::-1]):
        if y > ly:
            s += '\n'
            ly = y
        s += map[x, y] if (x, y) != robot else '@'
    with open('day15output.txt', 'a') as f:
        f.write(s + '\n\n')
    
def gps_score(map):
    gps_sum = 0
    for x, y in map:
        if map[x, y] in '[O':
            gps_sum += 100 * y + x
    return gps_sum

def solve(inp, part, example):
    # open('day15output.txt', 'w').close()
    map, commands = inp
    map, robot = read_map(map, part)
    for i, command in enumerate(commands):
        robot = attempt_move(map, command, robot, part)

    return gps_score(map)

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
