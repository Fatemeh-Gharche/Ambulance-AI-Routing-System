from map_loader import load_map, find_positions

rows, cols, grid = load_map()

start, goals = find_positions(grid)

print("Rows:", rows)
print("Cols:", cols)
print("Map:")
for row in grid:
    print(row)

print("Start position:", start)
print("Victims:", goals) 

