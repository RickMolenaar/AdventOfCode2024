from copy import deepcopy

def parse_input(file = 'day13.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day13example.txt')

def format_input(inp: list[str]):
    machines = []
    for i in range(0, len(inp), 4):
        l1, l2, l3 = inp[i:i+3]
        l1 = l1.split()
        l2 = l2.split()
        l3 = l3.split()
        m1x = int(l1[2].lstrip('X+').rstrip(','))
        m1y = int(l1[3].lstrip('Y+'))
        m2x = int(l2[2].lstrip('X+').rstrip(','))
        m2y = int(l2[3].lstrip('Y+'))
        px = int(l3[1].lstrip('X=').rstrip(','))
        py = int(l3[2].lstrip('Y='))
        machines.append(((m1x, m1y), (m2x, m2y), (px, py)))
    return machines

''' 
m1x * b1 + m2x * b2 = px
b1 = (px - m2x * b2) / m1x

m1y * b1 + m2y * b2 = py
m1y * (px - m2x * b2) / m1x + m2y * b2 = py
m1y / m1x * px + (m2y - m2x / m1x) * b2 = py
(m2y * m1x - m2x) / m1x * b2 = py - m1y / m1x * px
(m2y * m1x - m2x) * b2 = m1x * py - m1y * px
b2 = (m1x * py - m1y * px) / (m2y * m1x - m2x)
'''

def solve(machines, part, example):
    tokens = 0
    for (m1x, m1y), (m2x, m2y), (px, py) in machines:
        if part == 2:
            px += 10000000000000
            py += 10000000000000
        b2 = (py * m1x - m1y * px) // (m2y * m1x - m1y * m2x)
        b1 = (px - m2x * b2) // m1x
        if m1x * b1 + m2x * b2 == px and m1y * b1 + m2y * b2 == py:
            tokens += 3 * b1 + b2
    return tokens

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
