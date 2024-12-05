from copy import deepcopy

def parse_input(file = 'day04.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day04example.txt')

def format_input(inp: list[str]):
    return inp

def get_words(inp, x, y, r):
    words = []
    try:
        words.append(''.join(inp[y+d][x] for d in r))
    except IndexError:
        words.append('....')
    if x >= max(r):
        try:
            words.append(''.join(inp[y+d][x-d] for d in r))
        except IndexError:
            words.append('....')
        words.append(''.join(inp[y][x-d] for d in r))
        if y >= max(r):
            words.append(''.join(inp[y-d][x-d] for d in r))
        else:
            words.append('....')
    else:
        words.extend(['....', '....', '....'])
    if y >= max(r):
        words.append(''.join(inp[y-d][x] for d in r))
        try:
            words.append(''.join(inp[y-d][x+d] for d in r))
        except IndexError:
            words.append('....')
    else:
        words.extend(['....', '....',])
    try:
        words.append(''.join(inp[y][x+d] for d in r))
    except IndexError:
        words.append('....')
    try:
        words.append(''.join(inp[y+d][x+d] for d in r))
    except IndexError:
        words.append('....')
    return words

def solve(inp, part, example):
    s = 0
    for y, row in enumerate(inp):
        if part == 2 and y in (0, len(inp) - 1):
            continue
        for x, c in enumerate(row):
            if part == 2 and x in (0, len(row) - 1):
                continue
            if part == 1:
                r = [0, 1, 2, 3,]
                s += get_words(inp, x, y, r).count('XMAS')
            else:
                words = get_words(inp, x, y, [-1, 0, 1])
                for i in range(1, 8, 2):
                    if words[i] == 'MAS' and words[i-2] == 'MAS':
                        s += 1
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
