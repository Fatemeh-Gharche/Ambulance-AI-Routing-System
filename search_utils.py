# search_utils.py
from dataclasses import dataclass, field
from typing import List, Sequence, Tuple

Position = Tuple[int, int]


@dataclass
class State:
    position: Position
    visited_goals: Tuple[Position, ...] = field(default_factory=tuple)
    path: List[str] = field(default_factory=list)
    cost: int = 0

    def to_tuple(self):
        return self.position, self.visited_goals, list(self.path), self.cost


class SearchUtils:

    MOVES = {
        'UP': (-1, 0),
        'DOWN': (1, 0),
        'LEFT': (0, -1),
        'RIGHT': (0, 1),
        'STAY': (0, 0)
    }

    @staticmethod
    def step_cost(cell: str, time_so_far: int) -> int:
        if cell.isdigit():
            return int(cell)

        if cell in ('S', 'G'):
            return 1

        if cell == 'L':
            cycle_mod = time_so_far % 20
            return 1 if cycle_mod < 10 else 10

        # unreachable or invalid cell
        return 10**9

    @staticmethod
    def create_initial_state(start: Position) -> State:
        return State(position=start, visited_goals=tuple(), path=[], cost=0)

    @staticmethod
    def manhattan(a: Position, b: Position) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    @staticmethod
    def heuristic_mst(current_pos: Position,
                      goals: Sequence[Position],
                      visited: Sequence[Position]) -> int:
        remaining = [g for g in goals if g not in visited]
        if not remaining:
            return 0

        h = min(SearchUtils.manhattan(current_pos, g) for g in remaining)

        if len(remaining) > 1:
            connected = {remaining[0]}
            total = 0
            while len(connected) < len(remaining):
                best_dist = float('inf')
                best_node = None
                for u in connected:
                    for v in remaining:
                        if v in connected:
                            continue
                        d = SearchUtils.manhattan(u, v)
                        if d < best_dist:
                            best_dist = d
                            best_node = v
                total += best_dist
                connected.add(best_node)
            h += total

        return int(h)
