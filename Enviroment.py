
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