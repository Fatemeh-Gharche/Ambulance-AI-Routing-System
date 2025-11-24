from map_loader import load_map, find_positions
from search_utils import create_initial_state, MOVES, get_cost

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