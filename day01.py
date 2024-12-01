from copy import deepcopy

def parse_input(file = 'day01.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day01example.txt')

def format_input(inp: list[str]):
    l1 = []
    l2 = []
    for line in inp:
        l1.append(int(line.split()[0]))
        l2.append(int(line.split()[1]))
    return l1, l2

def solve(inp, part, example):
    s = 0
    if part == 1:
        inp = zip(sorted(inp[0]), sorted(inp[1]))
        for pair in inp:
            s += abs(pair[0] - pair[1])
        return s
    for v in inp[0]:
        s += v * inp[1].count(v)
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
