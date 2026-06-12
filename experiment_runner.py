"""
Headless experiment loop and result collection.

Run from the repository root:
    python -m experiments_0112410318.experiment_runner

Outputs:
    results/pacman_results.csv
    results/pacman_results.json
"""

from __future__ import annotations

import argparse
import csv
import json
import statistics
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

from .game_engine import PacmanGame
from .mazes import MAZES, load_maze
from .path_adapter import plan_route


@dataclass(frozen=True)
class ExperimentConfig:
    name: str
    avoid_ghosts: bool = True
    danger_penalty: int = 0
    exact_limit: int = 8


DEFAULT_CONFIGS = [
    ExperimentConfig("a_star_exact_safe", avoid_ghosts=True, danger_penalty=0, exact_limit=8),
    ExperimentConfig("a_star_greedy_safe", avoid_ghosts=True, danger_penalty=0, exact_limit=0),
    ExperimentConfig("a_star_safe_penalty_1", avoid_ghosts=True, danger_penalty=1, exact_limit=8),
    ExperimentConfig("a_star_safe_penalty_3", avoid_ghosts=True, danger_penalty=3, exact_limit=8),
]


CSV_COLUMNS = [
    "maze",
    "config",
    "solver",
    "used_fallback",
    "avoid_ghosts",
    "danger_penalty",
    "exact_limit",
    "path_cost",
    "planned_steps",
    "executed_steps",
    "foods_total",
    "foods_collected",
    "lives_left",
    "lives_lost",
    "ghost_collisions",
    "wall_hits",
    "reached_exit",
    "success",
    "runtime_ms",
    "food_sequence",
    "movement_sequence",
    "error",
]


def run_one(maze_name: str, config: ExperimentConfig, prefer_teammate_a_star: bool = True) -> dict[str, Any]:
    grid = load_maze(maze_name)

    start_time = time.perf_counter()
    plan = plan_route(
        grid,
        avoid_ghosts=config.avoid_ghosts,
        danger_penalty=config.danger_penalty,
        exact_limit=config.exact_limit,
        prefer_teammate_a_star=prefer_teammate_a_star,
    )
    runtime_ms = (time.perf_counter() - start_time) * 1000

    game = PacmanGame(load_maze(maze_name), lives=3)
    simulation = game.run(plan.movements)

    return {
        "maze": maze_name,
        "config": config.name,
        "solver": plan.solver,
        "used_fallback": plan.used_fallback,
        "avoid_ghosts": config.avoid_ghosts,
        "danger_penalty": config.danger_penalty,
        "exact_limit": config.exact_limit,
        "path_cost": plan.path_cost,
        "planned_steps": simulation.planned_steps,
        "executed_steps": simulation.executed_steps,
        "foods_total": simulation.foods_total,
        "foods_collected": simulation.foods_collected,
        "lives_left": simulation.lives_left,
        "lives_lost": simulation.lives_lost,
        "ghost_collisions": simulation.ghost_collisions,
        "wall_hits": simulation.wall_hits,
        "reached_exit": simulation.reached_exit,
        "success": simulation.success,
        "runtime_ms": round(runtime_ms, 3),
        "food_sequence": json.dumps(plan.food_sequence),
        "movement_sequence": json.dumps(plan.movements),
        "full_path": json.dumps(plan.full_path),
        "error": plan.error or "",
    }


def run_all(
    output_dir: Path,
    repeat: int = 1,
    prefer_teammate_a_star: bool = True,
    include_events: bool = False,
) -> list[dict[str, Any]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []

    for repeat_index in range(1, repeat + 1):
        for maze_name in MAZES:
            for config in DEFAULT_CONFIGS:
                row = run_one(maze_name, config, prefer_teammate_a_star=prefer_teammate_a_star)
                row["repeat"] = repeat_index
                rows.append(row)

    csv_path = output_dir / "pacman_results.csv"
    json_path = output_dir / "pacman_results.json"
    summary_path = output_dir / "pacman_summary.json"

    with csv_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["repeat", *CSV_COLUMNS])
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in ["repeat", *CSV_COLUMNS]})

    with json_path.open("w", encoding="utf-8") as file:
        json.dump(rows, file, indent=2)

    summary = build_summary(rows)
    with summary_path.open("w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2)

    print(f"Saved CSV:  {csv_path}")
    print(f"Saved JSON: {json_path}")
    print(f"Saved summary: {summary_path}")
    return rows


def build_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault((row["maze"], row["config"]), []).append(row)

    summary: dict[str, Any] = {}
    for (maze, config), group_rows in grouped.items():
        key = f"{maze}::{config}"
        summary[key] = {
            "runs": len(group_rows),
            "success_rate": sum(1 for row in group_rows if row["success"]) / len(group_rows),
            "mean_runtime_ms": statistics.fmean(row["runtime_ms"] for row in group_rows),
            "mean_planned_steps": statistics.fmean(row["planned_steps"] for row in group_rows),
            "mean_lives_left": statistics.fmean(row["lives_left"] for row in group_rows),
            "mean_foods_collected": statistics.fmean(row["foods_collected"] for row in group_rows),
        }
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Pac-Man pathfinding experiments and collect results.")
    parser.add_argument("--output-dir", default="results", help="Directory for CSV/JSON output files.")
    parser.add_argument("--repeat", type=int, default=1, help="Repeat every maze/config this many times.")
    parser.add_argument(
        "--no-teammate-a-star",
        action="store_true",
        help="Force the internal fallback BFS planner instead of importing teammate a_star.py.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_all(
        output_dir=Path(args.output_dir),
        repeat=args.repeat,
        prefer_teammate_a_star=not args.no_teammate_a_star,
    )


if __name__ == "__main__":
    main()
