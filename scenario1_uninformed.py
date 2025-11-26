from map_loader import MapLoader
from search_utils import SearchUtils, State
import heapq
import itertools


class UCS:
    def __init__(self, grid, start, goals):
        self.grid = grid
        self.start = start
        self.goals = goals
        self.utils = SearchUtils()
        self.counter = itertools.count()

    def search(self):
        visited = {}

        start_state = State(
            position=self.start,
            visited_goals=(),
            path=[],
            cost=0
        )

        queue = []
        heapq.heappush(queue, (0, next(self.counter), start_state))
        expanded = 0

        while queue:
            cost_so_far, _, state = heapq.heappop(queue)

            current_pos = state.position
            visited_goals = state.visited_goals
            path_so_far = state.path
            expanded += 1

            if set(visited_goals) == set(self.goals):
                return path_so_far, cost_so_far, expanded

            time_mod = cost_so_far % 20
            key = (current_pos, visited_goals, time_mod)

            prev_cost = visited.get(key)
            if prev_cost is not None and cost_so_far >= prev_cost:
                continue

            visited[key] = cost_so_far

            for move, (dr, dc) in self.utils.MOVES.items():
                nr, nc = current_pos[0] + dr, current_pos[1] + dc

                if 0 <= nr < len(self.grid) and 0 <= nc < len(self.grid[0]):
                    cell = self.grid[nr][nc]

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
                        step_cost = self.utils.step_cost(cell, current_time)
                        new_path.append(move)
                        new_cost = current_time + step_cost

                    new_visited = list(visited_goals)
                    if cell == 'G' and (nr, nc) not in visited_goals:
                        new_visited.append((nr, nc))

                    new_state = State(
                        position=(nr, nc),
                        visited_goals=tuple(new_visited),
                        path=new_path,
                        cost=new_cost
                    )

                    heapq.heappush(
                        queue,
                        (new_cost, next(self.counter), new_state)
                    )

        return None, None, expanded

def main():
    loader = MapLoader()
    rows, cols, grid = loader.load_map()

    start, goals = loader.find_positions(grid)

    ucs = UCS(grid, start, goals)
    path, cost, expanded = ucs.search()

    if path is None:
        print("No solution found.")
    else:
        print(f"\nCost: {cost} min")
        print("Actions:", path)
        print("Expanded States:", expanded)


if __name__ == "__main__":
    main()
