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

def sort_update(rules: dict[int, list[int]], update: list[int]) -> list[int]:
    correct = []
    update = update[:]
    while update:
        v = update.pop(0)
        for v2 in update:
            if v in rules[v2]:
                update.append(v)
                break
        else:
            correct.append(v)
    return correct

def solve(inp, part, example):
    s = 0
    ordering, updates = inp
    for update in updates:
        correct = sort_update(ordering, update)
        if part == 1:
            s += correct[len(correct) // 2] if update == correct else 0
        else:
            s += correct[len(correct) // 2] if update != correct else 0
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
