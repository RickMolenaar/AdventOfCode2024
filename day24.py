from copy import deepcopy

def parse_input(file = 'day24.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day24example.txt')

def format_input(inp: list[str]):
    states = {}
    operands = {}
    to_check = set()
    for line in inp:
        if '->' in line:
            s1, op, s2, _, target = line.split()
            operands[target] = (s1, op, s2)
        elif ':' in line:
            target, value = line.split(': ')
            states[target] = value == '1'
        if target.startswith('z'):
            to_check.add(target)
    return states, operands, to_check

def get_wire(wire, states, operands):
    if wire in states:
        return states[wire]
    s1, op, s2 = operands[wire]
    s1 = get_wire(s1, states, operands)
    s2 = get_wire(s2, states, operands)
    match op:
        case 'XOR':
            return s1 ^ s2
        case 'OR': 
            return s1 or s2
        case 'AND':
            return s1 and s2

def get_output(states, operands, to_check):
    zs = ''
    for wire in sorted(to_check, reverse=True):
        zs += str(int(get_wire(wire, states, operands)))
    return zs

def get_input(states):
    xs = ''
    ys = ''
    for wire in sorted(states, reverse=True):
        if wire.startswith('x'):
            xs += str(int(states[wire]))
        else:
            ys += str(int(states[wire]))
    return xs, ys

def set_input(xs, ys):
    states = {}
    for i in range(len(xs)):
        states[f'x{i:0>2}'] = xs[-(i+1)]
    for i in range(len(ys)):
        states[f'y{i:0>2}'] = ys[-(i+1)]
    return states

def check_correctness(xs, ys, zs):
    max_len = max(len(xs), len(ys), len(zs))
    xs = ('0' * (max_len - len(xs))) + xs
    ys = ('0' * (max_len - len(ys))) + ys
    zs = ('0' * (max_len - len(zs))) + zs
    carry = 0
    correct = 0
    false_bits = []
    for i in range(len(zs) - 1, -1, -1):
        expected = int(xs[i]) + int(ys[i]) + carry
        carry = expected >= 2
        if expected >= 2:
            expected -= 2
        correct += zs[i] == str(expected)
        if zs[i] != str(expected):
            false_bits.append(len(zs) - 1 - i)
    return correct, false_bits

def find_roots(wire, operands):
    if wire.startswith('x') or wire.startswith('y'):
        return [wire]
    s1, _, s2 = operands[wire]
    return find_roots(s1, operands) + find_roots(s2, operands)

def reduce(wire, operands, ignore_z = True, depth = 99):
    if wire.startswith('x') or wire.startswith('y') or (wire.startswith('z') and not ignore_z) or depth == 0:
        return wire
    s1, op, s2 = operands[wire]
    return f'({reduce(s1, operands, False, depth - 1)} {op} {reduce(s2, operands, False, depth - 1)})'

def solve(inp: tuple[dict, dict, set], part, example):
    states, operands, to_check = inp
    xs, ys = get_input(states)
    zs = ''
    zs = get_output(states, operands, to_check)
    if part == 1:
        return int(zs, 2)
    if example:
        return
    operands['vdc'], operands['z12'] = operands['z12'], operands['vdc']
    operands['nhn'], operands['z21'] = operands['z21'], operands['nhn']
    operands['tvb'], operands['khg'] = operands['khg'], operands['tvb']
    operands['gst'], operands['z33'] = operands['z33'], operands['gst']
    zs = get_output(states, operands, to_check)
    amount, to_correct = check_correctness(xs, ys, zs)
    for i in to_correct:
        wire = f'z{i:0>2}'

        exp = reduce(wire, operands, depth = 2)
        if exp.count(' XOR ') != 2 or exp.count(' OR ') != 1:
            print(wire, exp, operands[wire])
    return ','.join(sorted(['vdc', 'nhn', 'tvb', 'gst', 'z12', 'z21', 'khg', 'z33']))


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
