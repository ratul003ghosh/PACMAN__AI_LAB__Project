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
