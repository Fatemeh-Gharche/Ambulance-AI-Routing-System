from map_loader import load_map

rows, cols, grid = load_map()

print("Rows:", rows)
print("Cols:", cols)
print("Map:")
for row in grid:
    print(row)
