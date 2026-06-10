
import pygame
import sys

pygame.init()

CELL_SIZE = 40

ROWS = 15
COLS = 15

WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Pac-Man Maze Environment")

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (70, 70, 70)


# Maze 1 (Easy)
maze1 = [
list("WWWWWWWWWWWWWWW"),
list("WP   F      G W"),
list("W WWW WWWWWWW W"),
list("W             W"),
list("W   F         W"),
list("W WWWWWWWWWWW W"),
list("W             W"),
list("W G           W"),
list("W      F      W"),
list("W WWWWWWWWWWW W"),
list("W             W"),
list("W             W"),
list("W         E   W"),
list("W             W"),
list("WWWWWWWWWWWWWWW")
]
# Maze 2 (Medium)
maze2 = [
list("WWWWWWWWWWWWWWW"),
list("WP W      F   W"),
list("W  W WWWWWWW  W"),
list("W  W     G W  W"),
list("W  WWWWWWW W  W"),
list("W      F   W  W"),
list("WWWWWWW WWWW  W"),
list("W            GW"),
list("W WWWWWWWWWW  W"),
list("W      F      W"),
list("W WWWWWWWWWW  W"),
list("W             W"),
list("W      E      W"),
list("W             W"),
list("WWWWWWWWWWWWWWW")
]

# Maze 3 (Hard)
maze3 = [
list("WWWWWWWWWWWWWWW"),
list("WP     W     FW"),
list("W WWWW W WWWW W"),
list("W W        W  W"),
list("W W WWWWWW W GW"),
list("W W      W W  W"),
list("W WWWWWW W W  W"),
list("W      W W W  W"),
list("WWWWW W W W  FW"),
list("W     W W W   W"),
list("W WWWWW W WWWWW"),
list("W     G W     W"),
list("W WWWWWWWWWW  W"),
list("W       E     W"),
list("WWWWWWWWWWWWWWW")
]
# =========================
# STORE ALL MAZES
# =========================
mazes = [maze1, maze2, maze3]
current_maze = 0


# =========================
# DRAW MAZE FUNCTION
# =========================
def draw_maze(grid):

    # LOOP THROUGH ROWS & COLUMNS
    for row in range(len(grid)):
        for col in range(len(grid[row])):

            # CALCULATE CELL POSITION
            x = col * CELL_SIZE
            y = row * CELL_SIZE

            # GET CURRENT CELL
            cell = grid[row][col]

            # DRAW BACKGROUND
            pygame.draw.rect(
                screen,
                BLACK,
                (x, y, CELL_SIZE, CELL_SIZE)
            )

            # DRAW WALL
            if cell == "W":
                pygame.draw.rect(
                    screen,
                    BLUE,
                    (x, y, CELL_SIZE, CELL_SIZE)
                )

            # DRAW PACMAN
            elif cell == "P":
                pygame.draw.circle(
                    screen,
                    YELLOW,
                    (x + CELL_SIZE // 2,
                     y + CELL_SIZE // 2),
                    CELL_SIZE // 3
                )

            # DRAW FOOD
            elif cell == "F":
                pygame.draw.circle(
                    screen,
                    WHITE,
                    (x + CELL_SIZE // 2,
                     y + CELL_SIZE // 2),
                    6
                )

            # DRAW GHOST
            elif cell == "G":
                pygame.draw.rect(
                    screen,
                    RED,
                    (x + 8, y + 8,
                     CELL_SIZE - 16,
                     CELL_SIZE - 16)
                )

            # DRAW EXIT
            elif cell == "E":
                pygame.draw.rect(
                    screen,
                    GREEN,
                    (x + 5, y + 5,
                     CELL_SIZE - 10,
                     CELL_SIZE - 10)
                )

            # DRAW GRID BORDER
            pygame.draw.rect(
                screen,
                GRAY,
                (x, y, CELL_SIZE, CELL_SIZE),
                1
            )

# =========================
# MAIN GAME LOOP
# =========================
running = True

while running:

    # HANDLE EVENTS
    for event in pygame.event.get():

        # CLOSE WINDOW
        if event.type == pygame.QUIT:
            running = False

        # KEYBOARD INPUT
        if event.type == pygame.KEYDOWN:

            # SWITCH TO MAZE 1
            if event.key == pygame.K_1:
                current_maze = 0

            # SWITCH TO MAZE 2
            elif event.key == pygame.K_2:
                current_maze = 1

            # SWITCH TO MAZE 3
            elif event.key == pygame.K_3:
                current_maze = 2

    # CLEAR SCREEN
    screen.fill(BLACK)

    # DRAW CURRENT MAZE
    draw_maze(mazes[current_maze])

    # UPDATE DISPLAY
    pygame.display.flip()


# =========================
# EXIT GAME
# =========================
pygame.quit()
sys.exit()
