from copy import deepcopy

def parse_input(file = 'day07.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day07example.txt')

def format_input(inp: list[str]):
    eqs = []
    for line in inp:
        v0, vr = line.split(': ')
        eqs.append((int(v0), list(map(int, vr.split()))))
    return eqs

part1_solved = {}

def can_solve_equation(result, operands, operators):
    if operands[0] > result:
        return False
    for op in operators:
        match op:
            case '+':
                r = operands[0] + operands[1]
            case '*':
                r = operands[0] * operands[1]
            case '|':
                r = int(str(operands[0]) + str(operands[1]))
        if len(operands) == 2:
            if r == result:
                return True
        elif can_solve_equation(result, [r] + operands[2:], operators):
            return True
    return False

def solve(inp, part, example):
    s = 0
    for result, operands in inp:
        if (result, tuple(operands)) in part1_solved:
            s += result
            continue
        if can_solve_equation(result, operands, '*+' if part == 1 else '*|+'):
            s += result
            if part == 1:
                part1_solved[(result, tuple(operands))] = True
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
