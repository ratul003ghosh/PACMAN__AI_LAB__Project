import heapq

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
