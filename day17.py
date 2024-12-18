from copy import deepcopy

def parse_input(file = 'day17.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day17example.txt')

def format_input(inp: list[str]):
    registers = {c: 0 for c in 'ABC'}
    for i, line in enumerate(inp):
        if i < 3:
            registers['ABC'[i]] = int(line.split()[-1])
        if i == 4:
            commands = list(map(int, line.split()[-1].split(',')))
    return registers, commands

def run_commands(commands, registers, part, debug = False):
    i = 0
    output = ''
    desired = ','.join(map(str, commands)) + ','
    while i < len(commands):
        command = commands[i]
        if i % 2 == 0:
            op = command
        else:
            if command <= 3 or op in (1, 3, 4):
                value = command
            elif command < 7:
                value = registers['ABC'[command-4]]
            else:
                raise ValueError(f'Invalid combo at {i=}')
            match op:
                case 0:
                    registers['A'] = registers['A'] // 2 ** value
                case 1:
                    registers['B'] = registers['B'] ^ value
                case 2:
                    registers['B'] = value % 8
                case 3:
                    if registers['A'] != 0:
                        i = value - 1
                case 4:
                    registers['B'] = registers['B'] ^ registers['C']
                case 5:
                    output += str(value % 8) + ','
                    if part == 2:
                        if not desired.startswith(output) and not debug:
                            return False
                case 6:
                    registers['B'] = registers['A'] // 2 ** value
                case 7:
                    registers['C'] = registers['A'] // 2 ** value       
        i += 1             
    if part == 1 or debug:
        return output.rstrip(',')
    return output == desired

def print_program(commands):
    for i in range(0, len(commands), 2):
        op = commands[i]
        command = commands[i + 1]
        if op == 4:
            value = 'A'
        elif command <= 3 or op in (1, 3, 4):
            value = str(command)
        elif command < 7:
            value = 'ABC'[command-4]
        else:
            raise ValueError(f'Invalid combo at {i=}')
        print(['adv', 'bxl', 'bst', 'jnz', 'bxc', 'out', 'bdv', 'cdv'][op], value)

def solve(inp, part, example):
    registers, commands = inp
    desired = ','.join(str(c) for c in commands)
    if part == 1:
        return run_commands(commands, registers, part)
    else:
        if example:
            return
        # print_program(commands)
        v = 0
        best_len = 0
        start = '0o'
        while 1:
            start = f'0o56006476540250'
            a = int(start + oct(v)[2:], 8)
            registers = {'A': a, 'B': 0, 'C': 0}
            out = run_commands(commands, registers, part, True)
            if out == desired:
                return a
            if desired.endswith(out):
                if len(out) > best_len:
                    # start = oct(a)[:-3]
                    best_len = len(out)
                    v = -1
                    print(f'{oct(a)}, {out}')
            v += 1

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
