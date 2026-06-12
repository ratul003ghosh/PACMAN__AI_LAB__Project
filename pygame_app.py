"""
Pygame implementation for visual Pac-Man route execution.

Controls:
- 1 / 2 / 3: switch maze
- SPACE: plan route and start animation
- R: reset current maze
- ESC or window close: quit

Run from repository root:
    python -m experiments_0112410318.pygame_app
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .game_engine import MOVE_DELTAS, PacmanGame
from .mazes import EMPTY, EXIT, FOOD, GHOST, MAZES, PACMAN, WALL, load_maze
from .path_adapter import plan_route

CELL_SIZE = 40
FPS = 60
MOVE_DELAY_MS = 160

BLACK = (10, 10, 10)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 60, 60)
GREEN = (0, 255, 100)
GRAY = (50, 50, 50)
TEXT = (230, 230, 230)
CYAN = (100, 200, 255)


def draw_maze(pygame, screen, font, game: PacmanGame, maze_name: str, status: str) -> None:
    grid = game.grid
    rows = len(grid)
    cols = len(grid[0])

    for row in range(rows):
        for col in range(cols):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            position = (row, col)
            original_cell = game.original_grid[row][col]
            cell = grid[row][col]

            pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE))

            if original_cell == WALL:
                pygame.draw.rect(screen, (20, 20, 180), (x, y, CELL_SIZE, CELL_SIZE), border_radius=8)
                pygame.draw.rect(screen, CYAN, (x + 4, y + 4, CELL_SIZE - 8, CELL_SIZE - 8), 2, border_radius=6)
            elif position in game.ghost_positions:
                pygame.draw.circle(screen, RED, (x + CELL_SIZE // 2, y + 15), 12)
                pygame.draw.rect(screen, RED, (x + 8, y + 15, CELL_SIZE - 16, CELL_SIZE - 12))
                pygame.draw.circle(screen, WHITE, (x + 14, y + 18), 4)
                pygame.draw.circle(screen, WHITE, (x + 26, y + 18), 4)
                pygame.draw.circle(screen, BLUE, (x + 15, y + 19), 2)
                pygame.draw.circle(screen, BLUE, (x + 27, y + 19), 2)
            elif position in game.remaining_foods:
                pygame.draw.circle(screen, WHITE, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), 5)
                pygame.draw.circle(screen, CYAN, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), 10, 1)
            elif original_cell == EXIT:
                pygame.draw.rect(screen, GREEN, (x + 5, y + 5, CELL_SIZE - 10, CELL_SIZE - 10), border_radius=5)

            pygame.draw.rect(screen, GRAY, (x, y, CELL_SIZE, CELL_SIZE), 1)

    pacman_row, pacman_col = game.position
    pacman_x = pacman_col * CELL_SIZE + CELL_SIZE // 2
    pacman_y = pacman_row * CELL_SIZE + CELL_SIZE // 2
    pygame.draw.circle(screen, YELLOW, (pacman_x, pacman_y), CELL_SIZE // 3)

    info_y = rows * CELL_SIZE + 8
    info_lines = [
        f"Maze: {maze_name} | Lives: {game.lives} | Food left: {len(game.remaining_foods)} | Steps: {game.executed_steps}",
        f"Status: {status}",
        "Controls: 1/2/3 switch maze, SPACE solve/animate, R reset, ESC quit",
    ]
    for index, line in enumerate(info_lines):
        text_surface = font.render(line, True, TEXT)
        screen.blit(text_surface, (10, info_y + index * 22))


def save_run_result(output_dir: Path, maze_name: str, plan, result) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "maze": maze_name,
        "solver": plan.solver,
        "path_cost": plan.path_cost,
        "used_fallback": plan.used_fallback,
        "food_sequence": plan.food_sequence,
        "movement_sequence": plan.movements,
        "result": result.to_dict(include_events=True),
        "error": plan.error,
    }
    output_path = output_dir / f"pygame_run_{maze_name}.json"
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2)


def run_pygame(start_maze_index: int = 0, output_dir: Path = Path("results")) -> None:
    try:
        import pygame
    except ImportError as exc:
        raise SystemExit("pygame is not installed. Run: pip install pygame") from exc

    pygame.init()
    maze_names = list(MAZES.keys())
    current_index = max(0, min(start_maze_index, len(maze_names) - 1))
    maze_name = maze_names[current_index]
    game = PacmanGame(load_maze(maze_name), lives=3)

    rows = len(game.grid)
    cols = len(game.grid[0])
    screen = pygame.display.set_mode((cols * CELL_SIZE, rows * CELL_SIZE + 82))
    pygame.display.set_caption("AI Pac-Man Experiments - 0112410318")
    font = pygame.font.SysFont("arial", 16)
    clock = pygame.time.Clock()

    moves_queue: list[str] = []
    active_plan = None
    last_move_time = 0
    status = "Press SPACE to solve and animate."

    running = True
    while running:
        now = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    new_index = int(event.unicode) - 1
                    if 0 <= new_index < len(maze_names):
                        current_index = new_index
                        maze_name = maze_names[current_index]
                        game = PacmanGame(load_maze(maze_name), lives=3)
                        moves_queue = []
                        active_plan = None
                        status = "Maze changed. Press SPACE to solve and animate."
                elif event.key == pygame.K_r:
                    game = PacmanGame(load_maze(maze_name), lives=3)
                    moves_queue = []
                    active_plan = None
                    status = "Reset complete. Press SPACE to solve and animate."
                elif event.key == pygame.K_SPACE:
                    game = PacmanGame(load_maze(maze_name), lives=3)
                    active_plan = plan_route(load_maze(maze_name))
                    moves_queue = active_plan.movements[:]
                    status = f"Animating {active_plan.solver}; planned steps: {len(moves_queue)}"
                    if active_plan.error:
                        status += f" | {active_plan.error}"

        if moves_queue and now - last_move_time >= MOVE_DELAY_MS:
            move = moves_queue.pop(0)
            record = game.step(move)
            last_move_time = now
            status = f"Last move: {move} -> {record.event}"
            if game.is_finished or not moves_queue:
                result = game.run([])
                status = "SUCCESS: all food collected and exit reached." if result.success else "Finished without success."
                if active_plan is not None:
                    save_run_result(output_dir, maze_name, active_plan, result)
                moves_queue = []

        screen.fill(BLACK)
        draw_maze(pygame, screen, font, game, maze_name, status)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Visualize Pac-Man pathfinding with pygame.")
    parser.add_argument("--maze", type=int, default=1, choices=[1, 2, 3], help="Starting maze number.")
    parser.add_argument("--output-dir", default="results", help="Directory for pygame run JSON output.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_pygame(start_maze_index=args.maze - 1, output_dir=Path(args.output_dir))


if __name__ == "__main__":
    main()
