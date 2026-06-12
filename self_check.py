"""Quick verification script for the experiment branch."""

from __future__ import annotations

from pathlib import Path

from .experiment_runner import run_all
from .mazes import MAZES, load_maze


def main() -> None:
    for maze_name in MAZES:
        grid = load_maze(maze_name)
        print(f"OK maze loaded: {maze_name} ({len(grid)}x{len(grid[0])})")

    output_dir = Path("results/self_check")
    rows = run_all(output_dir=output_dir, repeat=1, prefer_teammate_a_star=False)
    if len(rows) != len(MAZES) * 4:
        raise SystemExit(f"Expected {len(MAZES) * 4} rows, got {len(rows)}")

    print(f"OK experiment rows generated: {len(rows)}")
    print("Self-check completed.")


if __name__ == "__main__":
    main()
