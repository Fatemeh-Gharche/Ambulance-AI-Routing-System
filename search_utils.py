import itertools

MOVES = {
    'UP': (-1, 0),
    'DOWN': (1, 0),
    'LEFT': (0, -1),
    'RIGHT': (0, 1),
    'STAY': (0, 0)
}

def get_step_cost(cell, time_so_far):
    if cell.isdigit():
        return int(cell)

    if cell in ('S', 'G'):
        return 1

    if cell == 'L':
        cycle = 20
        t = time_so_far % cycle
        if t < 10:
            return 1
        else:
            return 10

    return 999999


def create_initial_state(start):
   
    current_position = start
    visited_goals = tuple()
    path_so_far = []
    cost_so_far = 0
    return (current_position, visited_goals, path_so_far, cost_so_far)


def manhattan(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def heuristic_mst(current_pos, goals, visited):
    remaining = [g for g in goals if g not in visited]
    if not remaining:
        return 0
    h = min(manhattan(current_pos, g) for g in remaining)
    
    if len(remaining) > 1:
        connected = {remaining[0]}
        edges = []
        total = 0
        while len(connected) < len(remaining):
            min_edge = None
            min_dist = float('inf')
            for u in connected:
                for v in remaining:
                    if v not in connected:
                        d = manhattan(u, v)
                        if d < min_dist:
                            min_dist = d
                            min_edge = (u, v)
            total += min_dist
            connected.add(min_edge[1])
        h += total
    return h
