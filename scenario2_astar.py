from map_loader import load_map, find_positions
from search_utils import MOVES, get_step_cost, create_initial_state, heuristic_mst
import heapq

rows, cols, grid = load_map()
start, goals = find_positions(grid)

log_file = open("scenario2_log.txt", "w")
expanded_states = 0

def astar(grid, start, goals):
    visited = set()
    start_state = create_initial_state(start)
    g_score = { (start, tuple()): 0 }
    f_score = { (start, tuple()): heuristic_mst(start, goals, tuple()) }

    queue = []
    heapq.heappush(queue, (f_score[(start, tuple())], 0, start_state))

    while queue:
        _, cost_so_far, (current_pos, visited_goals, path_so_far, _) = heapq.heappop(queue)
        expanded_states = 1

        key = (current_pos, tuple(visited_goals))
        if key in visited:
            continue
        visited.add(key)
        expanded_states += 1
        log_file.write(f"Pop: {current_pos}, g: {cost_so_far}, visited: {visited_goals}\n")

        if set(visited_goals) == set(goals):
            log_file.write(f"Total expanded: {expanded_states}\n")
            return path_so_far, cost_so_far

        for move, (dr, dc) in MOVES.items():
            nr, nc = current_pos[0]+dr, current_pos[1]+dc
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
                cell = grid[nr][nc]
                new_path = path_so_far.copy()
                current_time = cost_so_far

                if cell == 'L':
                    while current_time % 20 >= 10:
                        new_path.append('STAY')
                        current_time += 1
                    new_path.append(move)
                    new_g = current_time + 1
                else:
                    new_path.append(move)
                    new_g = current_time + get_step_cost(cell, current_time)

                new_visited = list(visited_goals)
                if cell == 'G' and (nr, nc) not in visited_goals:
                    new_visited.append((nr, nc))

                new_state = ((nr, nc), tuple(new_visited), new_path, new_g)
                new_f = new_g + heuristic_mst((nr,nc), goals, tuple(new_visited))
                heapq.heappush(queue, (new_f, new_g, new_state))

    return None, None

path, cost = astar(grid, start, goals)
log_file.close()

print("\nCost:", cost, "min")
print("Actions:", path)
