from map_loader import load_map, find_positions
from search_utils import create_initial_state, MOVES, get_step_cost
import heapq

rows, cols, grid = load_map()
start, goals = find_positions(grid)


def ucs(grid, start, goals):
    visited = dict()
    start_state = create_initial_state(start)
    queue = []
    heapq.heappush(queue, (0, start_state))

    expanded = 0

    while queue:
        cost_so_far, (current_pos, visited_goals, path_so_far, _) = heapq.heappop(queue)
        expanded += 1

        if set(visited_goals) == set(goals):
            return path_so_far, cost_so_far, expanded

        time_mod = cost_so_far % 20
        key = (current_pos, tuple(visited_goals), time_mod)

        prev_best = visited.get(key)
        if prev_best is not None and cost_so_far >= prev_best:
            continue
        visited[key] = cost_so_far

        for move, (dr, dc) in MOVES.items():
            nr, nc = current_pos[0] + dr, current_pos[1] + dc
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
                cell = grid[nr][nc]
                new_path = path_so_far.copy()
                current_time = cost_so_far

                if move == 'STAY':
                    new_path.append('STAY')
                    new_cost = current_time + 1
                elif cell == 'L':
                    while current_time % 20 >= 10:  
                        new_path.append('STAY')
                        current_time += 1
                    new_path.append(move)
                    current_time += 1
                    new_cost = current_time
                else:
                    step = get_step_cost(cell, current_time)
                    new_path.append(move)
                    new_cost = current_time + step

                new_visited = list(visited_goals)
                if cell == 'G' and (nr, nc) not in visited_goals:
                    new_visited.append((nr, nc))

                new_state = ((nr, nc), tuple(new_visited), new_path, new_cost)
                heapq.heappush(queue, (new_cost, new_state))

    return None, None, expanded

path, cost, expanded = ucs(grid, start, goals)

if path is None:
    print("No solution found.")
else:
    print(f"\nCost: {cost} min")
    print("Actions:", path)
    print("Expanded States:", expanded)
