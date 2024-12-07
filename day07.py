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

def solve(inp, part, example):
    s = 0
    base = 2 if part == 1 else 3
    operators = '+*|'
    for result, operands in inp:
        n_ops = len(operands) - 1
        for comb in range(base**n_ops):
            ops = []
            for t in range(n_ops):
                ops.append(operators[comb % base])
                comb -= comb % base
                comb //= base
            res = operands[0]
            for i in range(len(ops)):
                if ops[i] == '+':
                    res += operands[i+1]
                elif ops[i] == '*':
                    res *= operands[i+1]
                else:
                    res = int(str(res) + str(operands[i+1]))
                if res > result:
                    break
            if res == result:
                s += result
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
