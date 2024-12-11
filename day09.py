from copy import deepcopy

def parse_input(file = 'day09.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day09example.txt')

def format_input(inp: list[str]):
    return inp[0]

def solve(inp, part, example):
    data = []
    n_file = 0
    for i, c in enumerate(inp):
        if i % 2 == 0:
            data.append((n_file, int(c)))
        else:
            data.append((None, int(c)))
            n_file += 1
        if int(c) == 0:
            data.pop()
    if part == 1:
        block_id = 0
        while block_id < len(data):
            if example and block_id > 20:
                break
            block = data[block_id]
            if block[0] is not None:
                block_id += 1
                continue
            data.pop(block_id)
            to_fill = block[1]
            new_blocks = []
            while to_fill > 0:
                last = data.pop()
                while last[0] is None:
                    last = data.pop()
                if last[1] > to_fill:
                    new_blocks.append((last[0], to_fill))
                    data.append((last[0], last[1] - to_fill))
                    to_fill = 0
                else:
                    new_blocks.append(last)
                    to_fill -= last[1]
            for b in new_blocks[::-1]:
                data.insert(block_id, b)
            block_id += 1
    else:
        blocks = [block for block in data if block[0] is not None][::-1]
        for id, l in blocks:
            for i, block in enumerate(data):
                if block[0] == id:
                    break
                if block[0] is None and block[1] >= l:
                    data.insert(i, (id, l))
                    data.pop(i+1)
                    if block[1] > l:
                        data.insert(i+1, (None, block[1] - l))
                    loc_from = data.index((id, l), i + 1)
                    empty_l = l
                    try:
                        if data[loc_from + 1][0] == None:
                            _, l1 = data.pop(loc_from + 1)
                            empty_l += l1
                    except IndexError:
                        pass
                    if data[loc_from - 1][0] == None:
                        _, l1 = data.pop(loc_from - 1)
                        empty_l += l1
                        loc_from -= 1
                    data.pop(loc_from)
                    data.insert(loc_from, (None, empty_l))
                    break

    i = 0
    s = 0
    for block in data:
        id, n = block
        if id is None:
            i += n
            continue
        s += id * (n * (2 * i + n - 1) // 2)        # Quick sum formula
        i += n
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
