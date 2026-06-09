
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
