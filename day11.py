from collections import defaultdict
from copy import deepcopy

def parse_input(file = 'day11.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day11example.txt')

def format_input(inp: list[str]):
    return list(map(int, inp[0].split()))

cache = {}

def split_stone(stone0, steps):
    if (stone0, steps) in cache:
        # if steps > 1:
        #     print(f'Using cache for {stone, steps}: {cache[stone, steps]}')
        return cache[stone0, steps]
    stones = [stone0]
    for _ in range(steps):
        new = []
        for stone in stones:
            if stone == 0:
                new.append(1)
            elif len(str(stone)) % 2 == 0:
                s = str(stone)
                l = len(s)
                new.append(int(s[:l//2]))
                new.append(int(s[l//2:]))
            else:
                new.append(stone * 2024)
        stones = new
    cache[stone0, steps] = stones
    return new

def split_stones_smort(stone0, steps):
    # if (stone0, steps) in cache:
    #     # if steps > 1:
    #     #     print(f'Using cache for {stone, steps}: {cache[stone, steps]}')
    #     return cache[stone0, steps]
    stones = {stone0: 1}
    for _ in range(steps):
        new = defaultdict(int)
        for stone in stones:
            amount = stones[stone]
            if stone == 0:
                new[1] += amount
            elif len(str(stone)) % 2 == 0:
                s = str(stone)
                l = len(s)
                new[int(s[:l//2])] += amount
                new[int(s[l//2:])] += amount
            else:
                new[stone * 2024] += amount
        stones = new
    # cache[stone0, steps] = stones
    return new

def solve(stones, part, example):
    if part == 1:
        for s in range(5):
            new = []
            for stone in stones:
                new.extend(split_stone(stone, 5))
            stones = new
        return len(new)
    else:
        stones_dict = defaultdict(int)
        for stone in stones:
            stones_dict[stone] += 1
        for s in range(15):
            new = defaultdict(int)
            for stone in stones_dict:
                d = split_stones_smort(stone, 5)
                for st in d:
                    new[st] += d[st] * stones_dict[stone]
            stones_dict = new
        s = 0
        for stone in stones_dict:
            s += stones_dict[stone]
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
