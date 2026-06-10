import heapq
WALL = "W"
GHOST = "G"
FOOD = "F"
PACMAN = "P"
EXIT = "E"

def in_bounds(grid, position):
    row, col = position
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])

def find_symbol(grid, symbol):
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == symbol:
                return (row, col)
    return None

def find_all_symbols(grid, symbol):
    positions = []
    for row in range(len(grid)):
        for col in range(len(grid[0])):
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