from collections import defaultdict
from copy import deepcopy

def parse_input(file = 'day05.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day05example.txt')

def format_input(inp: list[str]):
    ordering = defaultdict(list)
    updates = []
    for line in inp:
        if '|' in line:
            p0, p1 = line.split('|')
            ordering[int(p0)].append(int(p1))
        elif ',' in line:
            updates.append(list(map(int, line.split(','))))
    return ordering, updates

def solve(inp, part, example):
    s = 0
    ordering, updates = inp
    for update in updates:
        valid = True
        for i, v in enumerate(update):
            for v2 in ordering[v]:
                if v2 in update and update.index(v2) < i:
                    valid = False
                    break
            if not valid:
                if part == 2:
                    correct = []
                    while update:
                        v = update.pop(0)
                        for v2 in update:
                            if v in ordering[v2]:
                                update.append(v)
                                break
                        else:
                            correct.append(v)
                    s += correct[len(correct) // 2]
                break
        else:
            if part == 1:
                s += update[len(update) // 2]
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
