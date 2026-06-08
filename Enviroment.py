
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
