"""
Pure Pac-Man movement engine used by both experiments and pygame.

Rules implemented here:
- Pac-Man starts with 3 lives.
- Walls block movement.
- Static ghosts cause one life loss and send Pac-Man back to the start.
- Food is collected when Pac-Man enters the food cell.
- The run succeeds only after all food is collected and Pac-Man reaches the exit.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Iterable

from .mazes import EMPTY, EXIT, FOOD, GHOST, PACMAN, WALL, find_all_symbols, find_symbol, validate_grid

MOVE_DELTAS: dict[str, tuple[int, int]] = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1),
}


@dataclass
class StepRecord:
    step: int
    move: str
    from_position: tuple[int, int]
    to_position: tuple[int, int]
    event: str
    lives_left: int
    foods_left: int


@dataclass
class RunResult:
    success: bool
    reached_exit: bool
    lives_left: int
    lives_lost: int
    foods_total: int
    foods_collected: int
    planned_steps: int
    executed_steps: int
    ghost_collisions: int
    wall_hits: int
    final_position: tuple[int, int]
    events: list[StepRecord] = field(default_factory=list)

    def to_dict(self, include_events: bool = False) -> dict:
        data = asdict(self)
        if not include_events:
            data.pop("events", None)
        return data


class PacmanGame:
    """Small deterministic state machine for replaying a movement sequence."""

    def __init__(self, grid: list[list[str]], lives: int = 3):
        validate_grid(grid)
        self.original_grid = [row[:] for row in grid]
        self.grid = [row[:] for row in grid]
        self.start_position = find_symbol(self.grid, PACMAN)
        self.exit_position = find_symbol(self.grid, EXIT)
        if self.start_position is None or self.exit_position is None:
            raise ValueError("Grid must contain Pac-Man and exit.")

        self.position = self.start_position
        self.lives = lives
        self.initial_lives = lives
        self.ghost_positions = set(find_all_symbols(self.grid, GHOST))
        self.remaining_foods = set(find_all_symbols(self.grid, FOOD))
        self.foods_total = len(self.remaining_foods)
        self.ghost_collisions = 0
        self.wall_hits = 0
        self.executed_steps = 0
        self.events: list[StepRecord] = []

        # Treat the start cell as floor after reading its starting position.
        start_row, start_col = self.start_position
        self.grid[start_row][start_col] = EMPTY

    def in_bounds(self, position: tuple[int, int]) -> bool:
        row, col = position
        return 0 <= row < len(self.grid) and 0 <= col < len(self.grid[0])

    def step(self, move: str) -> StepRecord:
        move = move.upper().strip()
        if move not in MOVE_DELTAS:
            raise ValueError(f"Unknown move '{move}'. Use one of {sorted(MOVE_DELTAS)}")

        if self.is_finished:
            event = "already_finished"
            record = self._make_record(move, self.position, self.position, event)
            self.events.append(record)
            return record

        row_change, col_change = MOVE_DELTAS[move]
        current_row, current_col = self.position
        next_position = (current_row + row_change, current_col + col_change)
        event = "move"

        if not self.in_bounds(next_position):
            self.wall_hits += 1
            event = "blocked_out_of_bounds"
            next_position = self.position
        else:
            next_row, next_col = next_position
            cell = self.grid[next_row][next_col]
            if cell == WALL:
                self.wall_hits += 1
                event = "blocked_wall"
                next_position = self.position
            elif next_position in self.ghost_positions or cell == GHOST:
                self.ghost_collisions += 1
                self.lives -= 1
                event = "ghost_collision"
                next_position = self.start_position if self.lives > 0 else next_position
            else:
                self.position = next_position
                if next_position in self.remaining_foods:
                    self.remaining_foods.remove(next_position)
                    self.grid[next_row][next_col] = EMPTY
                    event = "food_collected"
                elif next_position == self.exit_position:
                    event = "exit_reached" if not self.remaining_foods else "exit_before_all_food"

        if event in {"blocked_out_of_bounds", "blocked_wall"}:
            pass
        elif event == "ghost_collision":
            self.position = next_position
        else:
            self.position = next_position

        self.executed_steps += 1
        record = self._make_record(move, (current_row, current_col), self.position, event)
        self.events.append(record)
        return record

    def _make_record(
        self,
        move: str,
        from_position: tuple[int, int],
        to_position: tuple[int, int],
        event: str,
    ) -> StepRecord:
        return StepRecord(
            step=self.executed_steps,
            move=move,
            from_position=from_position,
            to_position=to_position,
            event=event,
            lives_left=self.lives,
            foods_left=len(self.remaining_foods),
        )

    @property
    def reached_exit(self) -> bool:
        return self.position == self.exit_position

    @property
    def is_success(self) -> bool:
        return self.reached_exit and not self.remaining_foods and self.lives > 0

    @property
    def is_finished(self) -> bool:
        return self.is_success or self.lives <= 0

    def run(self, moves: Iterable[str], stop_when_finished: bool = True) -> RunResult:
        planned_moves = list(moves)
        for move in planned_moves:
            if stop_when_finished and self.is_finished:
                break
            self.step(move)

        return RunResult(
            success=self.is_success,
            reached_exit=self.reached_exit,
            lives_left=self.lives,
            lives_lost=self.initial_lives - self.lives,
            foods_total=self.foods_total,
            foods_collected=self.foods_total - len(self.remaining_foods),
            planned_steps=len(planned_moves),
            executed_steps=self.executed_steps,
            ghost_collisions=self.ghost_collisions,
            wall_hits=self.wall_hits,
            final_position=self.position,
            events=self.events[:],
        )
