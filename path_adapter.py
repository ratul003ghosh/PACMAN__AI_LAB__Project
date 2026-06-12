"""
Adapter between this experiment branch and teammate pathfinding files.

The teammate pathfinding branch exposes a_star.solve(grid, ...).  This adapter
keeps the experiment runner stable even if the project is not merged yet:
1. It tries to call a_star.solve.
2. If that module is not present, it uses a small internal BFS fallback so the
   experiment and pygame files still run for testing.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from importlib import import_module
from typing import Callable

from .mazes import EXIT, FOOD, GHOST, PACMAN, WALL, find_all_symbols, find_symbol


@dataclass
class PlanResult:
    solver: str
    path_cost: float
    food_sequence: list[tuple[int, int]]
    movements: list[str]
    full_path: list[tuple[int, int]]
    used_fallback: bool = False
    error: str | None = None


def _path_to_movements(path: list[tuple[int, int]]) -> list[str]:
    moves: list[str] = []
    for index in range(1, len(path)):
        previous_row, previous_col = path[index - 1]
        current_row, current_col = path[index]
        row_change = current_row - previous_row
        col_change = current_col - previous_col
        if row_change == -1 and col_change == 0:
            moves.append("UP")
        elif row_change == 1 and col_change == 0:
            moves.append("DOWN")
        elif row_change == 0 and col_change == -1:
            moves.append("LEFT")
        elif row_change == 0 and col_change == 1:
            moves.append("RIGHT")
        else:
            raise ValueError(f"Non-adjacent path jump: {path[index - 1]} -> {path[index]}")
    return moves


def _neighbors(grid: list[list[str]], position: tuple[int, int], avoid_ghosts: bool) -> list[tuple[int, int]]:
    row, col = position
    candidates = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
    valid: list[tuple[int, int]] = []
    for next_row, next_col in candidates:
        if not (0 <= next_row < len(grid) and 0 <= next_col < len(grid[0])):
            continue
        cell = grid[next_row][next_col]
        if cell == WALL:
            continue
        if avoid_ghosts and cell == GHOST:
            continue
        valid.append((next_row, next_col))
    return valid


def _bfs_path(
    grid: list[list[str]],
    start: tuple[int, int],
    goal: tuple[int, int],
    avoid_ghosts: bool = True,
) -> tuple[list[tuple[int, int]] | None, float]:
    if start == goal:
        return [start], 0

    queue = deque([start])
    previous: dict[tuple[int, int], tuple[int, int]] = {}
    visited = {start}

    while queue:
        current = queue.popleft()
        for neighbor in _neighbors(grid, current, avoid_ghosts):
            if neighbor in visited:
                continue
            visited.add(neighbor)
            previous[neighbor] = current
            if neighbor == goal:
                path = [goal]
                while path[-1] != start:
                    path.append(previous[path[-1]])
                path.reverse()
                return path, len(path) - 1
            queue.append(neighbor)

    return None, float("inf")


def _fallback_greedy_solver(grid: list[list[str]], avoid_ghosts: bool = True) -> PlanResult:
    """Nearest-food BFS fallback used only when teammate A* cannot be imported."""

    start = find_symbol(grid, PACMAN)
    exit_position = find_symbol(grid, EXIT)
    foods = find_all_symbols(grid, FOOD)
    if start is None or exit_position is None:
        return PlanResult("fallback_bfs_greedy", float("inf"), [], [], [], True, "Missing P or E")

    current = start
    remaining = set(foods)
    food_sequence: list[tuple[int, int]] = []
    full_path: list[tuple[int, int]] = [start]
    total_cost = 0.0

    while remaining:
        best_food = None
        best_path = None
        best_cost = float("inf")
        for food in sorted(remaining):
            path, cost = _bfs_path(grid, current, food, avoid_ghosts=avoid_ghosts)
            if path is not None and cost < best_cost:
                best_food = food
                best_path = path
                best_cost = cost

        if best_food is None or best_path is None:
            return PlanResult("fallback_bfs_greedy", float("inf"), food_sequence, [], full_path, True, "Food unreachable")

        food_sequence.append(best_food)
        full_path.extend(best_path[1:])
        total_cost += best_cost
        current = best_food
        remaining.remove(best_food)

    exit_path, exit_cost = _bfs_path(grid, current, exit_position, avoid_ghosts=avoid_ghosts)
    if exit_path is None:
        return PlanResult("fallback_bfs_greedy", float("inf"), food_sequence, [], full_path, True, "Exit unreachable")

    full_path.extend(exit_path[1:])
    total_cost += exit_cost
    return PlanResult(
        solver="fallback_bfs_greedy",
        path_cost=total_cost,
        food_sequence=food_sequence,
        movements=_path_to_movements(full_path),
        full_path=full_path,
        used_fallback=True,
    )


def _import_teammate_solver() -> Callable | None:
    """Return a_star.solve when it is available on PYTHONPATH."""

    try:
        module = import_module("a_star")
    except Exception:
        return None

    return getattr(module, "solve", None)


def plan_route(
    grid: list[list[str]],
    avoid_ghosts: bool = True,
    danger_penalty: int = 0,
    exact_limit: int = 8,
    prefer_teammate_a_star: bool = True,
) -> PlanResult:
    """Plan a full route that collects all food and reaches the exit."""

    if prefer_teammate_a_star:
        teammate_solve = _import_teammate_solver()
        if teammate_solve is not None:
            try:
                result = teammate_solve(
                    grid,
                    heuristic_map=None,
                    avoid_ghosts=avoid_ghosts,
                    danger_penalty=danger_penalty,
                    exact_limit=exact_limit,
                )
                if len(result) == 4:
                    path_cost, food_sequence, movements, full_path = result
                elif len(result) == 3:
                    path_cost, food_sequence, movements = result
                    full_path = []
                else:
                    raise ValueError(f"Unexpected a_star.solve return value: {result!r}")

                return PlanResult(
                    solver="teammate_a_star",
                    path_cost=path_cost,
                    food_sequence=list(food_sequence),
                    movements=list(movements),
                    full_path=list(full_path),
                    used_fallback=False,
                )
            except Exception as exc:  # keep experiments running, but record the error
                fallback = _fallback_greedy_solver(grid, avoid_ghosts=avoid_ghosts)
                fallback.error = f"a_star.solve failed; fallback used: {exc}"
                return fallback

    return _fallback_greedy_solver(grid, avoid_ghosts=avoid_ghosts)
