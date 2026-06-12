"""
Shared maze definitions for the experiment branch.

This file intentionally does not import pygame.  It can be used by both the
headless experiment runner and the pygame visualizer.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Iterable

WALL = "W"
GHOST = "G"
FOOD = "F"
PACMAN = "P"
EXIT = "E"
EMPTY = " "


# Maze 1 in the environment branch had a few short rows.  The normalize_grid()
# helper pads short rows with walls so Dijkstra/A* code that uses len(grid[0])
# cannot index outside shorter rows.
MAZE_1 = [
    "WWWWWWWWWWWWWWW",
    "WP   F     F  W",
    "W WWW   WWWW W",
    "W   G        W",
    "W WWWWW WWWW W",
    "W F       G  W",
    "W WWW WWWWW W",
    "W     W      W",
    "W WWW W WWWW W",
    "W   G     F  W",
    "W WWWWWWWWWW W",
    "W            W",
    "W   F    E   W",
    "W            W",
    "WWWWWWWWWWWWWWW",
]

MAZE_2 = [
    "WWWWWWWWWWWWWWW",
    "WP W   F   W  W",
    "W W WWWWW W W W",
    "W   G   W   F W",
    "WWWWW W WWWWW W",
    "W   W     G   W",
    "W W WWWWW W W W",
    "W F W   W   W W",
    "W WWWWW W WWW W",
    "W   G   F   W W",
    "W W WWWWWWW W W",
    "W   W     W   W",
    "W WWWW W WWWW W",
    "W    E        W",
    "WWWWWWWWWWWWWWW",
]

MAZE_3 = [
    "WWWWWWWWWWWWWWW",
    "WP W   F   W  W",
    "W W W WWW W W W",
    "W G W   W   W W",
    "W WWWWW W WWWWW",
    "W   W   G   W W",
    "WW W WWWWW W WW",
    "W  F W   W F  W",
    "W WWWW W WWWW W",
    "W   G   W   W W",
    "WWW W WWW W WWW",
    "W   W   G   W W",
    "W W WWWWWWW W W",
    "W   F   E     W",
    "WWWWWWWWWWWWWWW",
]

MAZES: dict[str, list[str]] = {
    "maze1_easy": MAZE_1,
    "maze2_medium": MAZE_2,
    "maze3_hard": MAZE_3,
}


class MazeValidationError(ValueError):
    """Raised when a maze is missing required symbols or is malformed."""


def normalize_grid(rows: Iterable[str | list[str]], pad: str = WALL) -> list[list[str]]:
    """Return a rectangular list-of-lists grid.

    Shorter rows are padded with walls.  This keeps the maze boundary safe and
    prevents teammate pathfinding functions from reading beyond a row.
    """

    row_strings = ["".join(row) if isinstance(row, list) else str(row) for row in rows]
    if not row_strings:
        raise MazeValidationError("Maze cannot be empty.")

    width = max(len(row) for row in row_strings)
    if width == 0:
        raise MazeValidationError("Maze rows cannot be empty.")

    return [list(row.ljust(width, pad)) for row in row_strings]


def copy_grid(rows: Iterable[str | list[str]]) -> list[list[str]]:
    """Deep-copy a maze into mutable list-of-lists form."""

    return deepcopy(normalize_grid(rows))


def grid_to_strings(grid: Iterable[Iterable[str]]) -> list[str]:
    """Convert a list-of-lists grid into printable strings."""

    return ["".join(row) for row in grid]


def find_symbol(grid: list[list[str]], symbol: str) -> tuple[int, int] | None:
    for row_index, row in enumerate(grid):
        for col_index, cell in enumerate(row):
            if cell == symbol:
                return row_index, col_index
    return None


def find_all_symbols(grid: list[list[str]], symbol: str) -> list[tuple[int, int]]:
    positions: list[tuple[int, int]] = []
    for row_index, row in enumerate(grid):
        for col_index, cell in enumerate(row):
            if cell == symbol:
                positions.append((row_index, col_index))
    return positions


def validate_grid(grid: list[list[str]]) -> None:
    """Validate grid shape and required Pac-Man symbols."""

    if not grid:
        raise MazeValidationError("Maze cannot be empty.")

    width = len(grid[0])
    if width == 0:
        raise MazeValidationError("Maze rows cannot be empty.")

    for row in grid:
        if len(row) != width:
            raise MazeValidationError("Maze must be rectangular after normalization.")

    allowed = {WALL, GHOST, FOOD, PACMAN, EXIT, EMPTY}
    invalid_cells = sorted({cell for row in grid for cell in row if cell not in allowed})
    if invalid_cells:
        raise MazeValidationError(f"Invalid maze symbols: {invalid_cells}")

    pacman_positions = find_all_symbols(grid, PACMAN)
    exit_positions = find_all_symbols(grid, EXIT)
    if len(pacman_positions) != 1:
        raise MazeValidationError("Maze must contain exactly one Pac-Man start 'P'.")
    if len(exit_positions) != 1:
        raise MazeValidationError("Maze must contain exactly one exit 'E'.")


def load_maze(name: str) -> list[list[str]]:
    """Load a named maze as a validated mutable grid."""

    if name not in MAZES:
        valid_names = ", ".join(MAZES)
        raise KeyError(f"Unknown maze '{name}'. Valid names: {valid_names}")
    grid = copy_grid(MAZES[name])
    validate_grid(grid)
    return grid
