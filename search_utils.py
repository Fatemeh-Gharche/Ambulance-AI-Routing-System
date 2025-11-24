MOVES = {
    'UP': (-1, 0),
    'DOWN': (1, 0),
    'LEFT': (0, -1),
    'RIGHT': (0, 1)
}


def get_cost(cell):
    if cell.isdigit():
        return int(cell)
    if cell == 'L':
        return 15
    if cell in ('S', 'G'):
        return 0
    return 999999  


def create_initial_state(start):
    current_position = start
    visited_goals = tuple()   
    path_so_far = []          
    cost_so_far = 0           
    
    return (current_position, visited_goals, path_so_far, cost_so_far)
