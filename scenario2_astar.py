from map_loader import MapLoader
from search_utils import SearchUtils, State
import heapq
import itertools


class AStarSearch:
    def __init__(self, grid, start, goals):
        self.grid = grid
        self.start = start
        self.goals = goals
        self.utils = SearchUtils()
        self.counter = itertools.count()
        self.log_file = open("scenario2_log.txt", "w")

    def search(self):
        visited = set()

        start_state = State(
            position=self.start,
            visited_goals=(),
            path=[],
            cost=0
        )

        g_score = {(self.start, ()): 0}
        f_score = {(self.start, ()): self.utils.heuristic_mst(self.start, self.goals, ())}

        queue = []
        heapq.heappush(queue, (f_score[(self.start, ())], next(self.counter), start_state))

        expanded = 0

        while queue:
            _, _, state = heapq.heappop(queue)

            current_pos = state.position
            visited_goals = state.visited_goals
            path_so_far = state.path
            cost_so_far = state.cost

            expanded += 1
            self.log_file.write(f"Pop: {current_pos}, g={cost_so_far}, visited={visited_goals}\n")

            key = (current_pos, visited_goals)
            if key in visited:
                continue

            visited.add(key)

            if set(visited_goals) == set(self.goals):
                self.log_file.write(f"Expanded: {expanded}\n")
                self.log_file.close()
                return path_so_far, cost_so_far

            for move, (dr, dc) in self.utils.MOVES.items():
                nr, nc = current_pos[0] + dr, current_pos[1] + dc

                if 0 <= nr < len(self.grid) and 0 <= nc < len(self.grid[0]):
                    cell = self.grid[nr][nc]
                    new_path = path_so_far.copy()
                    current_time = cost_so_far

                    if cell == 'L':
                        while current_time % 20 >= 10:
                            new_path.append("STAY")
                            current_time += 1
                        new_path.append(move)
                        new_g = current_time + 1
                    else:
                        step_cost = self.utils.step_cost(cell, current_time)
                        new_path.append(move)
                        new_g = current_time + step_cost

                    new_visited = list(visited_goals)
                    if cell == 'G' and (nr, nc) not in new_visited:
                        new_visited.append((nr, nc))

                    new_visited = tuple(new_visited)
                    new_state = State((nr, nc), new_visited, new_path, new_g)

                    h = self.utils.heuristic_mst((nr, nc), self.goals, new_visited)
                    new_f = new_g + h

                    heapq.heappush(queue, (new_f, next(self.counter), new_state))

        self.log_file.close()
        return None, None


def main():
    loader = MapLoader()
    rows, cols, grid = loader.load_map()
    start, goals = loader.find_positions(grid)

    astar = AStarSearch(grid, start, goals)
    path, cost = astar.search()

    if path is None:
        print("No solution found.")
    else:
        print("Cost:", cost)
        print("Actions:", path)


if __name__ == "__main__":
    main()
