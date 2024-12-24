from copy import deepcopy

def parse_input(file = 'day21.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day21example.txt')

def format_input(inp: list[str]):
    codes = []
    map = {'7': (0, 0),
           '8': (1, 0),
           '9': (2, 0),
           '4': (0, 1),
           '5': (1, 1),
           '6': (2, 1),
           '1': (0, 2),
           '2': (1, 2),
           '3': (2, 2),
           '0': (1, 3),
           'A': (2, 3)}
    for line in inp:
        codes.append((int(line[:-1]), [(2, 3)] + [map[key] for key in line]))
    return codes

def get_path_by_locs(locs, forbidden, debug = False):
    if len(locs) == 1:
        return ''
    elif locs[0] == locs[1]:
        return 'A' + get_path_by_locs(locs[1:], forbidden, debug)
    else:
        l1, l2 = locs[:2]
        dx, dy = l2[0] - l1[0], l2[1] - l1[1]
        options = []
        if dx > 0:
            options.append(('>' * dx, (dx, 0)))
        elif dx < 0:
            options.append(('<' * abs(dx), (dx, 0)))
        if dy > 0:
            options.append(('v' * dy, (0, dy)))
        elif dy < 0:
            options.append(('^' * abs(dy), (0, dy)))
        for key, dir in options:
            nx, ny = l1[0] + dir[0], l1[1] + dir[1]
            if (nx, ny) == l2:
                # for path in :
                return key + 'A' + get_path_by_locs(locs[1:], forbidden, debug)
            elif (nx, ny) != forbidden:
                # for path in :
                return key + get_path_by_locs([(nx, ny)] + locs[1:], forbidden, debug)

mapping = {

    }

def get_path(prev_path):
    s = ''
    for block in prev_path.split('A'):
        if block in mapping:
            s += mapping[block]
        else:
            match s[0]:
                case '<':
                    new = 'v<<'
                    end = '>>^'
                case 'v':
                    new = 'v<'
                    end = '>^'
                case '>':
                    new = 'v'
                    end = '^'
                case '^':
                    new = '<'
                

def get_locs(seq):
    map = {
        '^': (1, 0),
        'A': (2, 0),
        '<': (0, 1),
        'v': (1, 1),
        '>': (2, 1),
    }
    locs = [map['A']]
    for c in seq:
        locs.append(map[c])
        # locs.append(map['A'])
    return locs

def solve(inp, part, example):
    if part == 2 and not example:
        return
    s = 0
    for id, locs in inp:
        path = get_path_by_locs(locs, (0, 3))
        # locs = get_locs(path)
        # # path2 = get_paths(locs1, (0, 0))
        # # locs2 = get_locs(path2)
        for robot in range((2 if part == 1 else 1)):
            path = get_path(path)
        # path3 = get_path_by_locs(locs, (0, 0))
        if example:
            print(len(path), id)#.split('A'))
        s += id * len(path)
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
