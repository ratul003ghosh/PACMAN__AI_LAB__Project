import pygame
import sys

pygame.init()

# =========================
# WINDOW SETTINGS
# =========================
CELL_SIZE = 40
ROWS = 15
COLS = 15

WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Pac-Man Maze Environment")

# =========================
# COLORS
# =========================
BLACK = (10, 10, 10)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 60, 60)
GREEN = (0, 255, 100)
GRAY = (50, 50, 50)

# =========================
# MAZE 1 (EASY - OPEN + SIMPLE PATHS)
# =========================
maze1 = [
list("WWWWWWWWWWWWWWW"),
list("WP   F     F  W"),
list("W WWW   WWWW W"),
list("W   G        W"),
list("W WWWWW WWWW W"),
list("W F       G  W"),
list("W WWW WWWWW W"),
list("W     W      W"),
list("W WWW W WWWW W"),
list("W   G     F  W"),
list("W WWWWWWWWWW W"),
list("W            W"),
list("W   F    E   W"),
list("W            W"),
list("WWWWWWWWWWWWWWW")
]

# =========================
# MAZE 2 (MEDIUM - BRANCHES + TRAPS)
# =========================
maze2 = [
list("WWWWWWWWWWWWWWW"),
list("WP W   F   W  W"),
list("W W WWWWW W W W"),
list("W   G   W   F W"),
list("WWWWW W WWWWW W"),
list("W   W     G   W"),
list("W W WWWWW W W W"),
list("W F W   W   W W"),
list("W WWWWW W WWW W"),
list("W   G   F   W W"),
list("W W WWWWWWW W W"),
list("W   W     W   W"),
list("W WWWW W WWWW W"),
list("W    E        W"),
list("WWWWWWWWWWWWWWW")
]

# =========================
# MAZE 3 (HARD - LABYRINTH + CHOKE POINTS)
# =========================
maze3 = [
list("WWWWWWWWWWWWWWW"),
list("WP W   F   W  W"),
list("W W W WWW W W W"),
list("W G W   W   W W"),
list("W WWWWW W WWWWW"),
list("W   W   G   W W"),
list("WW W WWWWW W WW"),
list("W  F W   W F  W"),
list("W WWWW W WWWW W"),
list("W   G   W   W W"),
list("WWW W WWW W WWW"),
list("W   W   G   W W"),
list("W W WWWWWWW W W"),
list("W   F   E     W"),
list("WWWWWWWWWWWWWWW")
]

# =========================
# STORE MAZES
# =========================
mazes = [maze1, maze2, maze3]
current_maze = 0

# =========================
# DRAW FUNCTION
# =========================
def draw_maze(grid):

    for row in range(len(grid)):
        for col in range(len(grid[row])):

            x = col * CELL_SIZE
            y = row * CELL_SIZE
            cell = grid[row][col]

            # background
            pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE))

            # WALL
            if cell == "W":
                pygame.draw.rect(
                    screen,
                    (20, 20, 180),
                    (x, y, CELL_SIZE, CELL_SIZE),
                    border_radius=8
                )

                pygame.draw.rect(
                    screen,
                    (100, 200, 255),
                    (x + 4, y + 4, CELL_SIZE - 8, CELL_SIZE - 8),
                    2,
                    border_radius=6
                )

            # PACMAN
            elif cell == "P":
                pygame.draw.circle(
                    screen,
                    YELLOW,
                    (x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                    CELL_SIZE // 3
                )

            # FOOD
            elif cell == "F":
                pygame.draw.circle(
                    screen,
                    WHITE,
                    (x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                    5
                )

                pygame.draw.circle(
                    screen,
                    (120, 200, 255),
                    (x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                    10,
                    1
                )

            # GHOST (3 ghosts supported automatically)
            elif cell == "G":
                pygame.draw.circle(
                    screen,
                    RED,
                    (x + CELL_SIZE // 2, y + 15),
                    12
                )

                pygame.draw.rect(
                    screen,
                    RED,
                    (x + 8, y + 15, CELL_SIZE - 16, CELL_SIZE - 12)
                )

                pygame.draw.circle(screen, WHITE, (x + 14, y + 18), 4)
                pygame.draw.circle(screen, WHITE, (x + 26, y + 18), 4)

                pygame.draw.circle(screen, BLUE, (x + 15, y + 19), 2)
                pygame.draw.circle(screen, BLUE, (x + 27, y + 19), 2)

            # EXIT
            elif cell == "E":
                pygame.draw.rect(
                    screen,
                    GREEN,
                    (x + 5, y + 5, CELL_SIZE - 10, CELL_SIZE - 10),
                    border_radius=5
                )

            # GRID
            pygame.draw.rect(screen, GRAY, (x, y, CELL_SIZE, CELL_SIZE), 1)

# =========================
# GAME LOOP
# =========================
running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_1:
                current_maze = 0
            elif event.key == pygame.K_2:
                current_maze = 1
            elif event.key == pygame.K_3:
                current_maze = 2

    screen.fill(BLACK)
    draw_maze(mazes[current_maze])
    pygame.display.flip()

pygame.quit()
sys.exit()
