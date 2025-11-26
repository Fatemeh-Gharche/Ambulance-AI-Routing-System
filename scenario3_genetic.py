import sys
import random
import heapq
from map_loader import load_map
from map_loader import find_positions_multi
from search_utils import MOVES, get_step_cost, heuristic_mst

def astar_multi_goals(grid, start, goals):
    goals_set = set(goals)
    if not goals:
        return 0.0, []

    start_state = (start, tuple())  # (pos, visited_goals)
    open_heap = []
    start_h = heuristic_mst(start, goals, tuple())
    heapq.heappush(open_heap, (start_h, 0, start_state, []))
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

        for move, (dr, dc) in MOVES.items():
            nr, nc = pos[0] + dr, pos[1] + dc
            if not (0 <= nr < len(grid) and 0 <= nc < len(grid[0])):
                continue
            cell = grid[nr][nc]
            new_path = path + [move]
            current_time = g

            if move == 'STAY':
                new_g = current_time + 1
            elif cell == 'L':
                t = current_time
                while t % 20 >= 10:
                    new_path = new_path[:-1] + ['STAY']
                    t += 1
                new_g = t + 1
            else:
                step = get_step_cost(cell, current_time)
                new_g = current_time + step

            new_visited = visited.copy()
            if cell == 'G':
                new_visited.add((nr, nc))
            new_state = ((nr, nc), tuple(sorted(new_visited)))
            h = heuristic_mst((nr, nc), goals, tuple(sorted(new_visited)))
            heapq.heappush(open_heap, (new_g + h, new_g, new_state, new_path))

    return float('inf'), []

def initialize_population(pop_size, num_incidents, num_ambulances):
    population = [ [random.randrange(num_ambulances) for _ in range(num_incidents)] for _ in range(pop_size) ]
    return population

def tournament_selection(pop, scores, k=3):
    idxs = random.sample(range(len(pop)), k)
    best = idxs[0]
    for i in idxs:
        if scores[i] < scores[best]:
            best = i
    return pop[best]

def uniform_crossover(a, b):
    child = []
    for i in range(len(a)):
        child.append(a[i] if random.random() < 0.5 else b[i])
    return child

def mutate(chrom, num_ambulances, mutation_rate):
    for i in range(len(chrom)):
        if random.random() < mutation_rate:
            chrom[i] = random.randrange(num_ambulances)

def evaluate_chromosome(chrom, starts, incidents, grid, astar_cache, verbose=False):
    num_ambulances = len(starts)
    assignments = [[] for _ in range(num_ambulances)]
    for inc_idx, amb in enumerate(chrom):
        assignments[amb].append(inc_idx)

    per_times = []
    for amb_idx in range(num_ambulances):
        assigned = assignments[amb_idx]
        if not assigned:
            per_times.append(0.0)
            continue
        assigned_coords = [incidents[i] for i in assigned]
        key = (starts[amb_idx], tuple(sorted(assigned_coords)))
        if key in astar_cache:
            t = astar_cache[key]
        else:
            t, _ = astar_multi_goals(grid, starts[amb_idx], assigned_coords)
            astar_cache[key] = t
        per_times.append(t)
    makespan = max(per_times) if per_times else 0.0
    return makespan, per_times

def run_ga(grid, starts, incidents, pop_size=120, generations=300, crossover_rate=0.9, mutation_rate=0.07, seed=42, verbose=False):
    random.seed(seed)
    num_ambulances = len(starts)
    num_incidents = len(incidents)
    if num_ambulances == 0:
        raise ValueError("No ambulances (S) found on the map for scenario 3")

    population = initialize_population(pop_size, num_incidents, num_ambulances)
    astar_cache = dict()

    scores = [ evaluate_chromosome(ch, starts, incidents, grid, astar_cache)[0] for ch in population ]
    best_idx = min(range(len(population)), key=lambda i: scores[i])
    best_chrom = population[best_idx].copy()
    best_score = scores[best_idx]

    stagnation = 0
    for gen in range(generations):
        newpop = []
        while len(newpop) < pop_size:
            p1 = tournament_selection(population, scores, k=3)
            p2 = tournament_selection(population, scores, k=3)
            if random.random() < crossover_rate:
                child = uniform_crossover(p1, p2)
            else:
                child = p1.copy()
            mutate(child, num_ambulances, mutation_rate)
            newpop.append(child)
        population = newpop
        scores = [ evaluate_chromosome(ch, starts, incidents, grid, astar_cache)[0] for ch in population ]

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

    best_makespan, per_times = evaluate_chromosome(best_chrom, starts, incidents, grid, astar_cache)
    assignments = [[] for _ in range(num_ambulances)]
    for inc_idx, amb in enumerate(best_chrom):
        assignments[amb].append(inc_idx)
    result = {
        'makespan': best_makespan,
        'assignments': assignments,
        'per_times': per_times,
        'starts': starts,
        'incidents': incidents,
        'chrom': best_chrom
    }
    return result

def print_result(res):
    print(f"Best makespan (minutes): {res['makespan']:.2f}")
    for i, start in enumerate(res['starts']):
        assigned = res['assignments'][i]
        ids = [f'I{idx+1}' for idx in assigned]
        coords = [res['incidents'][idx] for idx in assigned]
        print(f"  S{i+1} at {start} assigned incidents: {ids} -> coords: {coords}")
        print(f"  S{i+1} route time = {res['per_times'][i]:.1f} minutes (visiting {len(assigned)} incidents)")

def main():
    rows, cols, grid = load_map()
    starts, incidents = find_positions_multi(grid)
    if not incidents:
        print("No incidents (G) found. Exiting.")
        return
    res = run_ga(grid, starts, incidents, pop_size=120, generations=300, crossover_rate=0.9, mutation_rate=0.07, seed=42, verbose=False)
    print_result(res)

if __name__ == '__main__':
    main()
