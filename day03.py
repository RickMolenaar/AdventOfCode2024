from copy import deepcopy

def parse_input(file = 'day03.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day03example.txt')

def format_input(inp: list[str]):
    return inp

def solve(inp, part, example):
    s = 0
    enabled = True
    for line in inp:
        op = ''
        for c in line:
            op += c
            if not (op.startswith('mul('[:len(op)]) or op.startswith('do()'[:len(op)]) or op.startswith('don\'t()'[:len(op)])):
                op = ''
            else:
                if op == 'do()':
                    enabled = True
                    op = ''
                elif op == 'don\'t()':
                    enabled = False
                    op = ''
                elif op == 'mul(':
                    continue
                elif op.startswith('mul('):
                    if c not in '0123456789,':
                        if c == ')':
                            op = op.rstrip(')')
                            if part == 1 or enabled:
                                s += int(op[4:op.index(',')]) * int(op[op.index(',') + 1:])
                            op = ''
                        else:
                            op = ''
                    elif c == ',':
                        if op.count(',') > 1:
                            op = ''
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
