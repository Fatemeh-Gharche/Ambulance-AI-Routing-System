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

    if cell == 'L':# 10 دقیقه باز - 10 دقیقه بسته (چرخه 20)
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
