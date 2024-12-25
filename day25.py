from copy import deepcopy

def parse_input(file = 'day25.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day25example.txt')

def format_input(inp: list[str]):
    keys = []
    locks = []
    schematic = []
    for line in inp:
        if not line:
            continue
        schematic.append(line)
        if len(schematic) == 7:
            heights = []
            for i in range(5):
                heights.append([l[i] for l in schematic].count('#') - 1)
            if all(c == '.' for c in schematic[0]):
                keys.append(heights)
            else:
                locks.append(heights)
            schematic = []
    return keys, locks

def solve(inp, part, example):
    if part == 2:
        return
    keys, locks = inp
    n = 0
    for key in keys:
        for lock in locks:
            for pin in range(len(key)):
                if key[pin] + lock[pin] > 5:
                    break
            else:
                n+=1
    return n

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
