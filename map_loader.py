from typing import List, Tuple


class MapLoader:
    def load_map(self) -> Tuple[int, int, List[List[str]]]:
        rows, cols = map(int, input().split())
        grid = [list(input().strip()) for _ in range(rows)]
        return rows, cols, grid

    def find_positions(self, grid: List[List[str]]) -> Tuple[Tuple[int, int], List[Tuple[int, int]]]:
        start = None
        goals = []

        for r in range(len(grid)):
            for c in range(len(grid[0])):
                cell = grid[r][c]

                if cell == 'S':
                    start = (r, c)
                elif cell == 'G':
                    goals.append((r, c))

        return start, goals

    def find_positions_multi(self, grid: List[List[str]]) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
        starts = []
        goals = []

        for r in range(len(grid)):
            for c in range(len(grid[0])):
                cell = grid[r][c]

                if cell == 'S':
                    starts.append((r, c))
                elif cell == 'G':
                    goals.append((r, c))

        return starts, goals
