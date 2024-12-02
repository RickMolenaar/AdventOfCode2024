from copy import deepcopy

def parse_input(file = 'day02.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day02example.txt')

def format_input(inp: list[str]):
    return [list(map(int, line.split())) for line in inp]

def is_safe(level):
    type = None
    old = 0
    for i, v in enumerate(level):
        if i == 0:
            old = v
            continue
        else:
            if abs(v - old) > 3 or v == old:
                return False
            if i == 1:
                if v < old:
                    type = 'dec'
                else:
                    type = 'inc'
            else:
                if v > old and type == 'dec' or v < old and type == 'inc':
                    return False
        old = v
    return True

def solve(inp, part, example):
    s = 0
    for line in inp:
        if is_safe(line):
            s += 1
        elif part == 2:
            for i in range(len(line)):
                if is_safe(line[:i] + line[i+1:]):
                    s += 1
                    break
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
