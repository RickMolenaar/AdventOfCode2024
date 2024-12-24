from collections import defaultdict
from copy import deepcopy
from AoCHelpers.optimization import Cache

def parse_input(file = 'day22.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day22example.txt')

def format_input(inp: list[str]):
    return [int(l) for l in inp]

def mix(n1, n2):
    return n1 ^ n2

def prune(n):
    return n % 16777216

@Cache()
def secrets(n):
    res = [n]
    for i in range(2000):
        n = mix(n, n * 64)
        n = prune(n)
        n = mix(n, n // 32)
        n = mix(n, n * 2048)
        n = prune(n)
        res.append(n)
    return res

def solve(inp, part, example):
    s = 0
    total_prices = defaultdict(int)
    for n in inp:
        if part == 1:
            s += secrets(n)[-1]
        else:
            prices = [v % 10 for v in secrets(n)]
            changes = []
            seen = set()
            for i in range(1, len(prices)):
                changes.append(prices[i] - prices[i-1])
            for i in range(len(changes) - 3):
                seq = tuple(changes[i:i+4])
                if seq in seen:
                    continue
                total_prices[seq] += prices[i+4]
                seen.add(seq)
    if part == 2:
        s = max(total_prices[k] for k in total_prices)
        return s        
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
