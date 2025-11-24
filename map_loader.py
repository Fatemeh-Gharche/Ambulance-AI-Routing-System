def load_map():

    rows, cols = map(int, input().split())
    
    grid = []
    for _ in range(rows):
        line = input().strip()
        grid.append(list(line))

    return rows, cols, grid
