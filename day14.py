from copy import deepcopy
import time

def parse_input(file = 'day14.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day14example.txt')

def format_input(inp: list[str]):
    robots = []
    for line in inp:
        p, v = line.split()
        p = p.lstrip('p=')
        p = p.split(',')
        v = v.lstrip('v=')
        v = v.split(',')
        robots.append(((int(p[0]), int(p[1])), (int(v[0]), int(v[1]))))
    return robots

def print_robots(robots, step):
    s = ''
    for y in range(103):
        row = []
        for x in range(101):
            row.append('#' if any(r[0] == x and r[1] == y for r, v in robots) else '.')
        s += ''.join(row) + '\n'
    with open('day14output.txt', 'a') as f:
        f.write(str(step) + '\n')
        f.write(s)
        f.write('\n\n\n')      

def get_quadrants(robots, space):
    q = [0, 0, 0, 0]
    for p, _ in robots:
        if p[0] < space[0] // 2 and p[1] < space[1] // 2:
            q[0] += 1
        elif p[0] < space[0] // 2 and p[1] > space[1] // 2:
            q[2] += 1
        elif p[0] > space[0] // 2 and p[1] < space[1] // 2:
            q[1] += 1
        elif p[0] > space[0] // 2 and p[1] > space[1] // 2:
            q[3] += 1
    return q

def solve(robots, part, example):
    open('day14output.txt', 'w').close()
    if part == 2 and example:
        return
    space = (11, 7) if example else (101, 103)
    s0 = robots
    print_robots(robots, 0)
    for step in range(100 if part == 1 else 100_000_000):
        if part == 2:
            q = get_quadrants(robots, space)
            if abs(q[0] - q[1]) < 15 and abs(q[2] == q[3]) < 15 and q[0] < 0.7 * q[2]:
                print_robots(robots, step)
        new = []
        for p, v in robots:
            np = (((p[0] + v[0]) % space[0], (p[1] + v[1]) % space[1]), v)
            new.append(np)
        robots = new
        if part == 2 and robots == s0:
            print(f'state is starting state, {step=}')
            return
    q = get_quadrants(robots, space)
    return q[0] * q[1] * q[2] * q[3]
            


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
