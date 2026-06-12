import heapq
import itertools

from dijkstra import (
    GHOST,
    build_heuristic_map,
    find_all_symbols,
    find_symbol,
    get_neighbors,
    in_bounds,
    is_walkable,
    manhattan_distance,
)

FOOD = "F"
PACMAN = "P"
EXIT = "E"

def reconstruct_path(came_from, current_node):
    path = [current_node]
    while current_node in came_from:
        current_node = came_from[current_node]
        path.append(current_node)
    path.reverse()
    return path

def get_heuristic(heuristic_map, node, goal):
    if heuristic_map is not None:
        value = heuristic_map.get(goal, {}).get(node)
        if value is not None and value != float("inf"):
            return value

    return manhattan_distance(node, goal)


def count_adjacent_ghosts(grid, position):
    row, col = position
    possible_neighbors = [
        (row - 1, col),
        (row + 1, col),
        (row, col - 1),
        (row, col + 1),
    ]

    ghost_count = 0
    for next_position in possible_neighbors:
        if in_bounds(grid, next_position):
            next_row, next_col = next_position
            if grid[next_row][next_col] == GHOST:
                ghost_count += 1

    return ghost_count

def movement_cost(grid, next_position, danger_penalty=0):
    return 1 + (danger_penalty * count_adjacent_ghosts(grid, next_position))

def a_star(grid, start, goal, heuristic_map=None, avoid_ghosts=True, danger_penalty=0):
    if not is_walkable(grid, start, avoid_ghosts=avoid_ghosts):
        return None, float("inf")

    if not is_walkable(grid, goal, avoid_ghosts=avoid_ghosts):
        return None, float("inf")

    g_costs = {start: 0}

    came_from = {}

    pq = []
    tie_breaker = 0

    start_f_cost = get_heuristic(heuristic_map, start, goal)
    heapq.heappush(pq, (start_f_cost, tie_breaker, start))

    visited = set()

    while pq:
        _, _, current_node = heapq.heappop(pq)

        if current_node in visited:
            continue

        if current_node == goal:
            return reconstruct_path(came_from, current_node), g_costs[current_node]

        visited.add(current_node)

        for neighbor in get_neighbors(grid, current_node, avoid_ghosts=avoid_ghosts):
            tentative_g_cost = g_costs[current_node] + movement_cost(
                grid,
                neighbor,
                danger_penalty=danger_penalty,
            )

            if tentative_g_cost < g_costs.get(neighbor, float("inf")):
                came_from[neighbor] = current_node
                g_costs[neighbor] = tentative_g_cost

                h_cost = get_heuristic(heuristic_map, neighbor, goal)
                f_cost = tentative_g_cost + h_cost

                tie_breaker += 1
                heapq.heappush(pq, (f_cost, tie_breaker, neighbor))

    return None, float("inf")

def path_to_movements(path):
    if not path or len(path) == 1:
        return []

    movements = []

    for index in range(1, len(path)):
        previous_row, previous_col = path[index - 1]
        current_row, current_col = path[index]

        row_change = current_row - previous_row
        col_change = current_col - previous_col

        if row_change == -1 and col_change == 0:
            movements.append("UP")
        elif row_change == 1 and col_change == 0:
            movements.append("DOWN")
        elif row_change == 0 and col_change == -1:
            movements.append("LEFT")
        elif row_change == 0 and col_change == 1:
            movements.append("RIGHT")

    return movements

def join_paths(path_segments):
    full_path = []

    for segment in path_segments:
        if not segment:
            continue

        if not full_path:
            full_path.extend(segment)
        else:
            full_path.extend(segment[1:])

    return full_path

def evaluate_food_sequence(grid, start, food_sequence, exit_position, heuristic_map, avoid_ghosts=True, danger_penalty=0):
    current_position = start
    total_cost = 0
    path_segments = []

    targets = list(food_sequence) + [exit_position]

    for target in targets:
        path, cost = a_star(
            grid,
            current_position,
            target,
            heuristic_map=heuristic_map,
            avoid_ghosts=avoid_ghosts,
            danger_penalty=danger_penalty,
        )

        if path is None or cost == float("inf"):
            return float("inf"), None

        total_cost += cost
        path_segments.append(path)
        current_position = target

    full_path = join_paths(path_segments)
    return total_cost, full_path

def exact_best_food_order(grid, start, foods, exit_position, heuristic_map, avoid_ghosts=True, danger_penalty=0):
    best_cost = float("inf")
    best_sequence = None
    best_path = None

    for sequence in itertools.permutations(foods):
        cost, path = evaluate_food_sequence(
            grid,
            start,
            sequence,
            exit_position,
            heuristic_map,
            avoid_ghosts=avoid_ghosts,
            danger_penalty=danger_penalty,
        )

        if cost < best_cost:
            best_cost = cost
            best_sequence = list(sequence)
            best_path = path

    return best_cost, best_sequence, best_path


def greedy_food_order(grid, start, foods, exit_position, heuristic_map, avoid_ghosts=True, danger_penalty=0):
    remaining_foods = set(foods)
    current_position = start
    selected_sequence = []
    path_segments = []
    total_cost = 0

    while remaining_foods:
        best_food = None
        best_food_path = None
        best_food_cost = float("inf")

        for food in remaining_foods:
            path, cost = a_star(
                grid,
                current_position,
                food,
                heuristic_map=heuristic_map,
                avoid_ghosts=avoid_ghosts,
                danger_penalty=danger_penalty,
            )

            if cost < best_food_cost:
                best_food = food
                best_food_path = path
                best_food_cost = cost

        if best_food is None or best_food_path is None or best_food_cost == float("inf"):
            return float("inf"), None, None

        selected_sequence.append(best_food)
        path_segments.append(best_food_path)
        total_cost += best_food_cost
        current_position = best_food
        remaining_foods.remove(best_food)

    exit_path, exit_cost = a_star(
        grid,
        current_position,
        exit_position,
        heuristic_map=heuristic_map,
        avoid_ghosts=avoid_ghosts,
        danger_penalty=danger_penalty,
    )

    if exit_path is None or exit_cost == float("inf"):
        return float("inf"), None, None

    path_segments.append(exit_path)
    total_cost += exit_cost

    full_path = join_paths(path_segments)
    return total_cost, selected_sequence, full_path


def solve_pacman(grid, heuristic_map=None, avoid_ghosts=True, danger_penalty=0, exact_limit=8):
    start = find_symbol(grid, PACMAN)
    exit_position = find_symbol(grid, EXIT)
    foods = find_all_symbols(grid, FOOD)

    if heuristic_map is None:
        targets = foods + [exit_position]
        heuristic_map = build_heuristic_map(grid, targets=targets, avoid_ghosts=avoid_ghosts)

    if len(foods) <= exact_limit:
        path_cost, food_sequence, full_path = exact_best_food_order(
            grid,
            start,
            foods,
            exit_position,
            heuristic_map,
            avoid_ghosts=avoid_ghosts,
            danger_penalty=danger_penalty,
        )
    else:
        path_cost, food_sequence, full_path = greedy_food_order(
            grid,
            start,
            foods,
            exit_position,
            heuristic_map,
            avoid_ghosts=avoid_ghosts,
            danger_penalty=danger_penalty,
        )

    if full_path is None or path_cost == float("inf"):
        return float("inf"), [], []

    movement_sequence = path_to_movements(full_path)
    return path_cost, food_sequence, movement_sequence


def solve(grid, heuristic_map=None, avoid_ghosts=True, danger_penalty=0, exact_limit=8):

    start = find_symbol(grid, PACMAN)
    exit_position = find_symbol(grid, EXIT)
    foods = find_all_symbols(grid, FOOD)

    if heuristic_map is None:
        targets = foods + [exit_position]
        heuristic_map = build_heuristic_map(grid, targets=targets, avoid_ghosts=avoid_ghosts)

    if len(foods) <= exact_limit:
        path_cost, food_sequence, full_path = exact_best_food_order(
            grid,
            start,
            foods,
            exit_position,
            heuristic_map,
            avoid_ghosts=avoid_ghosts,
            danger_penalty=danger_penalty,
        )
    else:
        path_cost, food_sequence, full_path = greedy_food_order(
            grid,
            start,
            foods,
            exit_position,
            heuristic_map,
            avoid_ghosts=avoid_ghosts,
            danger_penalty=danger_penalty,
        )

    if full_path is None or path_cost == float("inf"):
        return float("inf"), [], [], []

    movement_sequence = path_to_movements(full_path)
    return path_cost, food_sequence, movement_sequence, full_path