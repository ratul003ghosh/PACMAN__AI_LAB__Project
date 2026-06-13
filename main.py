import time
from Enviroment import mazes
from dijkstra import get_key_points, shortest_path
from a_star import a_star
from hill_climbing import HillClimbing
from simulated_annealing import SimulatedAnnealing

def run_experiment(maze_index=0):
    grid = mazes[maze_index]
    key_points = get_key_points(grid)
    start_pos = key_points["start"]
    exit_pos = key_points["exit"]
    foods = key_points["foods"]

    print(f"--- Running Experiment on Maze {maze_index + 1} ---")
    print(f"Total Foods to collect: {len(foods)}")

    # Wrapper functions for pathfinders to match the optimizer interface (start -> end distance)
    def dijkstra_pathfinder(start, end):
        _, cost = shortest_path(grid, start, end)
        return cost

    def astar_pathfinder(start, end):
        _, cost = a_star(grid, start, end)
        return cost

    # --- HILL CLIMBING EXPERIMENT ---
    print("\n[1] Hill Climbing + A*")
    hc_astar = HillClimbing(start_pos=start_pos, exit_pos=exit_pos, pathfinder_func=astar_pathfinder)
    start_time = time.time()
    best_route_hc = hc_astar.solve(foods)
    exec_time_hc = time.time() - start_time
    # Score is negative distance, so we flip it for displaying positive distance
    distance_hc = -hc_astar.evaluate_state(best_route_hc)
    
    print(f"Execution Time: {exec_time_hc:.4f} seconds")
    print(f"Optimized Path Distance: {distance_hc}")

    # --- SIMULATED ANNEALING EXPERIMENT ---
    print("\n[2] Simulated Annealing + A*")
    sa_astar = SimulatedAnnealing(start_pos=start_pos, exit_pos=exit_pos, pathfinder_func=astar_pathfinder)
    start_time = time.time()
    best_route_sa = sa_astar.solve(foods)
    exec_time_sa = time.time() - start_time
    distance_sa = -sa_astar.evaluate_state(best_route_sa)
    
    print(f"Execution Time: {exec_time_sa:.4f} seconds")
    print(f"Optimized Path Distance: {distance_sa}")

if __name__ == "__main__":
    # Run the experiment on Maze 1 (index 0)
    run_experiment(0)
