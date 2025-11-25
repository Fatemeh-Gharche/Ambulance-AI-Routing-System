from map_loader import load_map, find_positions
from search_utils import create_initial_state, MOVES, get_cost
from collections import deque

rows, cols, grid = load_map()

start, goals = find_positions(grid)

print("Rows:", rows)
print("Cols:", cols)
print("Map:")
for row in grid:
    print(row)

print("Start position:", start)
print("Victims:", goals) 

state = create_initial_state(start)
print("Initial state:")
print(state)

print("\nMoves:")
print(MOVES)


def initialize_bfs(start):
    queue = deque()
    visited = set()

    start_state = create_initial_state(start)
    queue.append(start_state)

    visited.add((start_state[0], start_state[1]))  

    return queue, visited


queue, visited = initialize_bfs(start)
print("Initial queue:", queue)
print("Visited set:", visited)
