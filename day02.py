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
    diffs = [level[i] - level[i-1] for i in range(1, len(level))]
    return all(d in (1, 2, 3) for d in diffs) or all(d in (-1, -2, -3) for d in diffs)

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
