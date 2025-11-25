def load_map():

    rows, cols = map(int, input().split())
    
    grid = []
    # for _ in range(rows):
    #     line = input().strip()
    #     grid.append(list(line))
    for _ in range(rows):
        grid.append(list(input().strip()))

    return rows, cols, grid



def find_positions(grid):
    start = None
    goals = []

    for r in range(len(grid)):
        for c in range(len(grid[0])):
            cell = grid[r][c]

            if cell == 'S':
                start = (r, c)

            if cell == 'G':
                goals.append((r, c))

    return start, goals
