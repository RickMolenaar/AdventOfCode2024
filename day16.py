from copy import deepcopy
from AoCHelpers.optimization import Pathfinder, ORTHOGONAL

def parse_input(file = 'day16.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day16example.txt')

def format_input(inp: list[str]):
    grid = {}
    for y, line in enumerate((inp)):
        for x, c in enumerate(line):
            grid[x, y] = c
            if c == 'E':
                end = (x, y)
                grid[x, y] = '.'
            elif c == 'S':
                start = (x, y)
                grid[x, y] = '.'
    return grid, start, end

class ReindeerRacer(Pathfinder):
    def __init__(self, map, starting_location, target_location, *args, **kwargs):
        self.min_cost = 10**99
        self.target_location = target_location
        super().__init__(map, ((starting_location, 0, 1, 0),), target_location, *args, **kwargs)
    
    def get_valid_moves(self, state):
        c = self.total_cost(state) 
        for (x, y), d0, df, cost in self.map[state[-1][0]]:
            if (x, y) in [loc for loc, _, _, _ in state] or c + cost > self.min_cost:
                continue
            yield ((x, y), d0, df, cost)
    
    def apply_move(self, state, move):
        return state + (move,)
    
    def total_cost(self, state):
        _, _, d, total = state[0]
        for _, dn, df, cost in state[1:]:
            if dn != d:
                total += 1000
            total += cost
            d = df
        return total

    def score_state(self, state):
        x, y = state[-1][0]
        return 500 * (x - y) - self.total_cost(state)
    
    def is_finished(self, state):
        if state[-1][0] == self.target_location:
            if self.total_cost(state) < self.min_cost:
                self.min_cost = self.total_cost(state)
                print('New best:', self.min_cost)
            # self.min_cost = min(self.min_cost, self.total_cost(state))
            return True
        return False

def build_map(grid, start, end) -> dict[list[tuple[tuple, int, int]]]:
    ### connections is a list of (connected_node, starting_dir, final_dir, cost) for each node
    nodes = set([start, end])
    for (x, y) in grid:
        if grid[x, y] == '#':
            continue
        neighbors = [n for n in ORTHOGONAL((x, y)) if grid[n] == '.']
        if len(neighbors) > 2:
            nodes.add((x, y))

    connections = {n: [] for n in nodes}
    while nodes:
        n = nodes.pop()
        dirs = ((0, -1), (1, 0), (0, 1), (-1, 0))
        for d0, (dx, dy) in enumerate(dirs):
            d = d0
            nx, ny = n[0] + dx, n[1] + dy
            if grid[nx, ny] == '#':
                continue
            cost = 1
            valid = True
            while (nx, ny) not in connections:
                cost += 1
                d_prev = d
                for d, (dx, dy) in enumerate(dirs):
                    if abs(d - d_prev) == 2:
                        continue
                    if grid[nx + dx, ny + dy] == '.':
                        if d != d_prev:
                            cost += 1000
                        break
                else:
                    valid = False
                    break
                nx, ny = nx + dx, ny + dy
            if valid:
                connections[n].append(((nx, ny), d0, d, cost))
    return connections

paths = {}

def solve(inp, part, example):
    grid, start, end = inp
    map = build_map(grid, start, end)
    if part == 2:
        seats = set()
        for sol in paths[example]:
            loc = sol[0][0]
            path = [loc]
            for next, d, _, _ in sol[1:]:
                dx, dy = ((0, -1), (1, 0), (0, 1), (-1, 0))[d]
                loc = (loc[0] + dx, loc[1] + dy)
                while loc != next:
                    # print(loc)
                    path.append(loc)
                    for n in ORTHOGONAL(loc):
                        if n not in path and grid[n] =='.':
                            break
                    loc = n
                path.append(loc)
            seats.update(path)
        return len(seats)
    p = ReindeerRacer(map, start, end, find_all_solutions = True, states_to_keep = 100_000, max_steps = 150)
    p.min_cost = 73404
    sols = p.get_minimal_path()
    s_min = 10**999
    for steps, sol in sols:
        score = p.total_cost(sol)
        if score < s_min:
            s_min = score
    paths[example] = []
    for steps, sol in sols:
        if p.total_cost(sol) == s_min:
            paths[example].append(sol)
    print(len(paths[example]))
    return s_min

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
