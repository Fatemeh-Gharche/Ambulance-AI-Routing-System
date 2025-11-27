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
        self.log = open("scenario1_log.txt", "w")

    def search(self):
        visited = {}
        expanded = 0

        start_state = State(self.start, (), [], 0)

        queue = []
        heapq.heappush(queue, (0, next(self.counter), start_state))
        self.log.write(f"PUSH -> pos={self.start}, g=0, visited=()\n")

        while queue:
            cost_so_far, _, state = heapq.heappop(queue)
            current_pos = state.position
            visited_goals = state.visited_goals
            path_so_far = state.path

            expanded += 1
            self.log.write(f"POP -> pos={current_pos}, g={cost_so_far}, visited={visited_goals}\n")

            if set(visited_goals) == set(self.goals):
                self.log.write(f"TOTAL EXPANDED: {expanded}\n")
                self.log.close()
                return path_so_far, cost_so_far, expanded

            key = (current_pos, visited_goals, cost_so_far % 20)
            if key in visited and visited[key] <= cost_so_far:
                continue
            visited[key] = cost_so_far

            for move, (dr, dc) in self.utils.MOVES.items():
                nr, nc = current_pos[0] + dr, current_pos[1] + dc
                if not (0 <= nr < len(self.grid) and 0 <= nc < len(self.grid[0])):
                    continue

                cell = self.grid[nr][nc]
                current_time = cost_so_far
                new_path = path_so_far.copy()

                if cell == 'L':
                    while current_time % 20 >= 10:
                        new_path.append("STAY")
                        current_time += 1
                        self.log.write(f"PUSH -> pos={current_pos}, g={current_time}, move=STAY (delay)\n")

                    new_path.append(move)
                    new_cost = current_time + 1
                else:
                    step = self.utils.step_cost(cell, current_time)
                    new_path.append(move)
                    new_cost = current_time + step

                new_visited = list(visited_goals)
                if cell == 'G' and (nr, nc) not in new_visited:
                    new_visited.append((nr, nc))
                new_visited = tuple(new_visited)

                new_state = State((nr, nc), new_visited, new_path, new_cost)
                heapq.heappush(queue, (new_cost, next(self.counter), new_state))
                self.log.write(
                    f"PUSH -> pos={(nr,nc)}, g={new_cost}, move={move}, visited={new_visited}\n"
                )

        self.log.write("NO SOLUTION\n")
        self.log.close()
        return None, None, expanded


def main():
    loader = MapLoader()
    _, _, grid = loader.load_map()
    start, goals = loader.find_positions(grid)

    ucs = UCS(grid, start, goals)
    path, cost, expanded = ucs.search()

    if path is None:
        print("No solution found.")
    else:
        print(f"Cost: {cost}")
        print("Actions:", path)
        print("Expanded:", expanded)


if __name__ == "__main__":
    main()
