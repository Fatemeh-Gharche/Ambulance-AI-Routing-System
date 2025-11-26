import sys
import random
import heapq
from map_loader import MapLoader
from search_utils import SearchUtils, State

class AStarMultiGoal:
    def __init__(self, grid):
        self.grid = grid
        self.moves = SearchUtils.MOVES

    def search(self, start, goals):
        goals_set = set(goals)
        if not goals:
            return 0.0, []

        start_state = (start, tuple())
        open_heap = []
        h_start = SearchUtils.heuristic_mst(start, goals, tuple())
        heapq.heappush(open_heap, (h_start, 0, start_state, []))
        closed = set()

        while open_heap:
            f, g, (pos, visited_tuple), path = heapq.heappop(open_heap)
            key = (pos, visited_tuple, g % 20)
            if key in closed:
                continue
            closed.add(key)

            visited = set(visited_tuple)
            if visited == goals_set:
                return g, path

            for move, (dr, dc) in self.moves.items():
                nr, nc = pos[0] + dr, pos[1] + dc
                if not (0 <= nr < len(self.grid) and 0 <= nc < len(self.grid[0])):
                    continue
                cell = self.grid[nr][nc]
                new_path = path + [move]
                current_time = g

                if move == 'STAY':
                    new_g = current_time + 1
                elif cell == 'L':
                    t = current_time
                    while t % 20 >= 10:
                        new_path[-1] = 'STAY'
                        t += 1
                    new_g = t + 1
                else:
                    new_g = current_time + SearchUtils.step_cost(cell, current_time)

                new_visited = visited.copy()
                if cell == 'G':
                    new_visited.add((nr, nc))
                new_state = ((nr, nc), tuple(sorted(new_visited)))
                h = SearchUtils.heuristic_mst((nr, nc), goals, tuple(sorted(new_visited)))
                heapq.heappush(open_heap, (new_g + h, new_g, new_state, new_path))

        return float('inf'), []

class GAForAmbulanceRouting:
    """Genetic Algorithm for multi-ambulance routing problem."""
    def __init__(self, grid, starts, incidents, pop_size=120, generations=300, crossover_rate=0.9, mutation_rate=0.07, seed=42):
        self.grid = grid
        self.starts = starts
        self.incidents = incidents
        self.pop_size = pop_size
        self.generations = generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.num_ambulances = len(starts)
        self.num_incidents = len(incidents)
        self.random = random.Random(seed)
        self.astar_solver = AStarMultiGoal(grid)
        self.astar_cache = {}

    def initialize_population(self):
        return [[self.random.randrange(self.num_ambulances) for _ in range(self.num_incidents)] for _ in range(self.pop_size)]

    def tournament_selection(self, pop, scores, k=3):
        idxs = self.random.sample(range(len(pop)), k)
        best = idxs[0]
        for i in idxs:
            if scores[i] < scores[best]:
                best = i
        return pop[best]

    def uniform_crossover(self, a, b):
        return [a[i] if self.random.random() < 0.5 else b[i] for i in range(len(a))]

    def mutate(self, chrom):
        for i in range(len(chrom)):
            if self.random.random() < self.mutation_rate:
                chrom[i] = self.random.randrange(self.num_ambulances)

    def evaluate_chromosome(self, chrom):
        assignments = [[] for _ in range(self.num_ambulances)]
        for inc_idx, amb in enumerate(chrom):
            assignments[amb].append(inc_idx)

        per_times = []
        for amb_idx in range(self.num_ambulances):
            assigned = assignments[amb_idx]
            if not assigned:
                per_times.append(0.0)
                continue
            assigned_coords = [self.incidents[i] for i in assigned]
            key = (self.starts[amb_idx], tuple(sorted(assigned_coords)))
            if key in self.astar_cache:
                t = self.astar_cache[key]
            else:
                t, _ = self.astar_solver.search(self.starts[amb_idx], assigned_coords)
                self.astar_cache[key] = t
            per_times.append(t)
        makespan = max(per_times) if per_times else 0.0
        return makespan, per_times

    def run(self, verbose=False):
        if self.num_ambulances == 0:
            raise ValueError("No ambulances (S) found on the map for scenario 3")

        population = self.initialize_population()
        scores = [self.evaluate_chromosome(ch)[0] for ch in population]
        best_idx = min(range(len(population)), key=lambda i: scores[i])
        best_chrom = population[best_idx].copy()
        best_score = scores[best_idx]

        stagnation = 0
        for gen in range(self.generations):
            newpop = []
            while len(newpop) < self.pop_size:
                p1 = self.tournament_selection(population, scores)
                p2 = self.tournament_selection(population, scores)
                if self.random.random() < self.crossover_rate:
                    child = self.uniform_crossover(p1, p2)
                else:
                    child = p1.copy()
                self.mutate(child)
                newpop.append(child)
            population = newpop
            scores = [self.evaluate_chromosome(ch)[0] for ch in population]

            gen_best_idx = min(range(len(population)), key=lambda i: scores[i])
            gen_best_score = scores[gen_best_idx]
            if gen_best_score < best_score:
                best_score = gen_best_score
                best_chrom = population[gen_best_idx].copy()
                stagnation = 0
            else:
                stagnation += 1
            if verbose and gen % 10 == 0:
                print(f"Gen {gen}: best makespan = {best_score:.2f}", file=sys.stderr)
            if stagnation >= 80:
                break

        best_makespan, per_times = self.evaluate_chromosome(best_chrom)
        assignments = [[] for _ in range(self.num_ambulances)]
        for inc_idx, amb in enumerate(best_chrom):
            assignments[amb].append(inc_idx)
        result = {
            'makespan': best_makespan,
            'assignments': assignments,
            'per_times': per_times,
            'starts': self.starts,
            'incidents': self.incidents,
            'chrom': best_chrom
        }
        return result

    @staticmethod
    def print_result(res):
        print(f"Best makespan (minutes): {res['makespan']:.2f}")
        for i, start in enumerate(res['starts']):
            assigned = res['assignments'][i]
            ids = [f'I{idx+1}' for idx in assigned]
            coords = [res['incidents'][idx] for idx in assigned]
            print(f"  S{i+1} at {start} assigned incidents: {ids} -> coords: {coords}")
            print(f"  S{i+1} route time = {res['per_times'][i]:.1f} minutes (visiting {len(assigned)} incidents)")

def main():
    loader = MapLoader()
    rows, cols, grid = loader.load_map()
    starts, incidents = loader.find_positions_multi(grid)
    if not incidents:
        print("No incidents (G) found. Exiting.")
        return
    ga = GAForAmbulanceRouting(grid, starts, incidents, pop_size=120, generations=300, crossover_rate=0.9, mutation_rate=0.07, seed=42)
    res = ga.run(verbose=False)
    GAForAmbulanceRouting.print_result(res)

if __name__ == '__main__':
    main()
