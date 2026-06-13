import heapq
WALL = "W"
GHOST = "G"
FOOD = "F"
PACMAN = "P"
EXIT = "E"

def in_bounds(grid, position):
    row, col = position
    return 0 <= row < len(grid) and 0 <= col < len(grid[row])

def find_symbol(grid, symbol):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == symbol:
                return (row, col)
    return None

def find_all_symbols(grid, symbol):
    positions = []
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == symbol:
                positions.append((row, col))
    return positions

def get_key_points(grid):
    return {
        "start": find_symbol(grid, PACMAN),
        "exit": find_symbol(grid, EXIT),
        "foods": find_all_symbols(grid, FOOD),
        "ghosts": find_all_symbols(grid, GHOST),
    }

def is_walkable(grid, position, avoid_ghosts=True):
    if not in_bounds(grid, position):
        return False
    row, col = position
    cell = grid[row][col]
    if cell == WALL:
        return False
    if avoid_ghosts and cell == GHOST:
        return False
    return True

def get_neighbors(grid, position, avoid_ghosts=True):
    row, col = position

    possible_moves = [
        (row - 1, col),  #Up
        (row + 1, col),  #Down
        (row, col - 1),  #Left
        (row, col + 1),  #Right
    ]

    neighbors = []
    for next_position in possible_moves:
        if is_walkable(grid, next_position, avoid_ghosts=avoid_ghosts):
            neighbors.append(next_position)
    return neighbors

def manhattan_distance(position_a, position_b):
    row_a, col_a = position_a
    row_b, col_b = position_b
    return abs(row_a - row_b) + abs(col_a - col_b)

def dijkstra_grid(grid, start, avoid_ghosts=True):
    distances = {}
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            position = (row, col)
            if is_walkable(grid, position, avoid_ghosts=avoid_ghosts):
                distances[position] = float("inf")

    distances[start] = 0
    previous = {}
    pq = []
    heapq.heappush(pq, (0, start))
    visited = set()
    while pq:
        current_distance, current_position = heapq.heappop(pq)
        if current_position in visited:
            continue
        visited.add(current_position)
        for neighbor in get_neighbors(grid, current_position, avoid_ghosts=avoid_ghosts):
            new_distance = current_distance + 1
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current_position
                heapq.heappush(pq, (new_distance, neighbor))
    return distances, previous

def reconstruct_path(previous, start, goal):
    if start == goal:
        return [start]
    if goal not in previous:
        return None
    path = [goal]
    current = goal
    while current != start:
        current = previous[current]
        path.append(current)
    path.reverse()
    return path

def shortest_path(grid, start, goal, avoid_ghosts=True):
    distances, previous = dijkstra_grid(grid, start, avoid_ghosts=avoid_ghosts)
    cost = distances.get(goal, float("inf"))
    if cost == float("inf"):
        return None, float("inf")
    path = reconstruct_path(previous, start, goal)
    return path, cost

def build_heuristic_map(grid, targets=None, avoid_ghosts=True):     
    key_points = get_key_points(grid)
    if targets is None:
        targets = []
        targets.extend(key_points["foods"])
        if key_points["exit"] is not None:
            targets.append(key_points["exit"])

    heuristic_map = {}
    for target in targets:
        if target is None:
            continue

        if not is_walkable(grid, target, avoid_ghosts=avoid_ghosts):
            continue

        distances, _ = dijkstra_grid(grid, target, avoid_ghosts=avoid_ghosts)
        heuristic_map[target] = distances

    return heuristic_map

def get_heuristic_value(heuristic_map, node, target):
    return heuristic_map.get(target, {}).get(node, float("inf"))