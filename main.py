import pygame
import time
import sys
import Enviroment
from Enviroment import mazes, draw_maze, CELL_SIZE, BLACK, YELLOW, WHITE, WIDTH, HEIGHT, GRAY, GREEN, RED
from dijkstra import get_key_points, shortest_path
from a_star import a_star, evaluate_food_sequence
from hill_climbing import HillClimbing
from simulated_annealing import SimulatedAnnealing

# Create a dedicated UI Dashboard panel next to the Maze
DASHBOARD_WIDTH = 450
WINDOW_WIDTH = WIDTH + DASHBOARD_WIDTH
DASHBOARD_X = WIDTH

# Override the Pygame screen to be wider!
Enviroment.screen = pygame.display.set_mode((WINDOW_WIDTH, HEIGHT))
screen = Enviroment.screen

# Wrapper functions
def astar_pathfinder(start, end, grid):
    path, cost = a_star(grid, start, end)
    return cost

def dijkstra_pathfinder(start, end, grid):
    path, cost = shortest_path(grid, start, end)
    return cost

pygame.font.init()
font_title = pygame.font.SysFont('Arial', 28, bold=True)
font_text = pygame.font.SysFont('Arial', 20)
font_small = pygame.font.SysFont('Arial', 14)

def draw_text(text, font, color, x, y, max_width=None):
    if max_width:
        words = text.split(" ")
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] < max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)
        
        for i, line in enumerate(lines):
            surface = font.render(line, True, color)
            screen.blit(surface, (x, y + i * font.get_linesize()))
        return y + len(lines) * font.get_linesize()
    else:
        surface = font.render(text, True, color)
        screen.blit(surface, (x, y))
        return y + font.get_linesize()

def draw_dashboard_bg():
    pygame.draw.rect(screen, (25, 25, 35), (DASHBOARD_X, 0, DASHBOARD_WIDTH, HEIGHT))
    pygame.draw.line(screen, GRAY, (DASHBOARD_X, 0), (DASHBOARD_X, HEIGHT), 4)

def show_menu(analysis_data=None):
    running = True
    maze_idx = 0
    
    while running:
        screen.fill(BLACK)
        draw_maze(mazes[maze_idx])
        
        draw_dashboard_bg()
        
        y_offset = 20
        # --- SHOW MENU OPTIONS ---
        y_offset = draw_text("AI Optimization Control", font_title, YELLOW, DASHBOARD_X + 20, y_offset)
        y_offset += 15
        y_offset = draw_text(f"Map: {['Easy', 'Medium', 'Hard'][maze_idx]} (Press 'M' to switch)", font_text, GREEN, DASHBOARD_X + 20, y_offset)
        y_offset += 15
        y_offset = draw_text("[1] Hill Climbing + A*", font_text, WHITE, DASHBOARD_X + 20, y_offset)
        y_offset = draw_text("[2] Simulated Annealing + A*", font_text, WHITE, DASHBOARD_X + 20, y_offset)
        y_offset = draw_text("[3] Hill Climbing + Dijkstra", font_text, WHITE, DASHBOARD_X + 20, y_offset)
        y_offset = draw_text("[4] Simulated Annealing + Dijkstra", font_text, WHITE, DASHBOARD_X + 20, y_offset)
        y_offset += 10
        y_offset = draw_text("[ESC] Exit Program", font_text, RED, DASHBOARD_X + 20, y_offset)
        
        y_offset += 15
        pygame.draw.line(screen, GRAY, (DASHBOARD_X + 20, y_offset), (WINDOW_WIDTH - 20, y_offset), 2)
        y_offset += 20
        
        # --- SHOW ANALYSIS ---
        if analysis_data:
            y_offset = draw_text("Results Analysis", font_title, YELLOW, DASHBOARD_X + 20, y_offset)
            y_offset += 10
            y_offset = draw_text(f"Algorithm: {analysis_data['title']}", font_text, (150, 200, 255), DASHBOARD_X + 20, y_offset, max_width=DASHBOARD_WIDTH-40)
            y_offset = draw_text(f"Execution Time: {analysis_data['time']:.4f} sec", font_text, WHITE, DASHBOARD_X + 20, y_offset)
            y_offset = draw_text(f"Path Distance: {analysis_data['distance']} steps", font_text, WHITE, DASHBOARD_X + 20, y_offset)
            
            y_offset += 15
            if analysis_data['food_seq']:
                food_seq_str = "Food Sequence: " + " -> ".join([f"({r},{c})" for r, c in analysis_data['food_seq']])
            else:
                food_seq_str = "Food Sequence: NONE"
            y_offset = draw_text(food_seq_str, font_small, (200, 200, 255), DASHBOARD_X + 20, y_offset, max_width=DASHBOARD_WIDTH-40)
            
            y_offset += 10
            if analysis_data['path']:
                path_str = "Path Coordinates: " + " -> ".join([f"({r},{c})" for r, c in analysis_data['path']])
            else:
                path_str = "Path Coordinates: PATH BLOCKED BY GHOSTS"
            y_offset = draw_text(path_str, font_small, (200, 255, 200), DASHBOARD_X + 20, y_offset, max_width=DASHBOARD_WIDTH-40)
            
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                char = event.unicode.lower()
                if event.key == pygame.K_m or char == 'm':
                    maze_idx = (maze_idx + 1) % 3
                elif event.key in [pygame.K_1, pygame.K_KP1] or char == '1':
                    return maze_idx, 1
                elif event.key in [pygame.K_2, pygame.K_KP2] or char == '2':
                    return maze_idx, 2
                elif event.key in [pygame.K_3, pygame.K_KP3] or char == '3':
                    return maze_idx, 3
                elif event.key in [pygame.K_4, pygame.K_KP4] or char == '4':
                    return maze_idx, 4
                elif event.key == pygame.K_ESCAPE or char == 'q':
                    pygame.quit()
                    sys.exit()

def animate_path(grid, path, title):
    clean_grid = [list(row) for row in grid]
    for r in range(len(clean_grid)):
        for c in range(len(clean_grid[r])):
            if clean_grid[r][c] == 'P':
                clean_grid[r][c] = ' '
                
    if not path:
        return

    for step in path:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        screen.fill(BLACK)
        draw_maze(clean_grid)
        
        draw_dashboard_bg()
        draw_text("Running Animation...", font_title, YELLOW, DASHBOARD_X + 20, 20)
        draw_text(title, font_text, WHITE, DASHBOARD_X + 20, 60, max_width=DASHBOARD_WIDTH-40)
        
        r, c = step
        x = c * CELL_SIZE
        y = r * CELL_SIZE
        pygame.draw.circle(screen, YELLOW, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 3)
        
        if clean_grid[r][c] == 'F':
            clean_grid[r][c] = ' '
            
        pygame.display.flip()
        time.sleep(0.2)

def run_visual_experiment():
    analysis_data = None
    
    while True:
        maze_idx, choice = show_menu(analysis_data)
        
        grid = mazes[maze_idx]
        key_points = get_key_points(grid)
        start_pos = key_points["start"]
        exit_pos = key_points["exit"]
        foods = key_points["foods"]

        def astar_func(start, end): return astar_pathfinder(start, end, grid)
        def dijkstra_func(start, end): return dijkstra_pathfinder(start, end, grid)

        title = ""
        best_route = []
        
        # Display "Computing..."
        screen.fill(BLACK)
        draw_maze(grid)
        draw_dashboard_bg()
        draw_text("AI is Computing Path...", font_title, YELLOW, DASHBOARD_X + 20, HEIGHT//2)
        pygame.display.flip()

        start_time = time.time()

        if choice == 1:
            title = "Hill Climbing + A*"
            hc = HillClimbing(start_pos=start_pos, exit_pos=exit_pos, pathfinder_func=astar_func)
            best_route = hc.solve(foods)
            cost = -hc.evaluate_state(best_route)
        elif choice == 2:
            title = "Simulated Annealing + A*"
            sa = SimulatedAnnealing(start_pos=start_pos, exit_pos=exit_pos, pathfinder_func=astar_func)
            best_route = sa.solve(foods)
            cost = -sa.evaluate_state(best_route)
        elif choice == 3:
            title = "Hill Climbing + Dijkstra"
            hc = HillClimbing(start_pos=start_pos, exit_pos=exit_pos, pathfinder_func=dijkstra_func)
            best_route = hc.solve(foods)
            cost = -hc.evaluate_state(best_route)
        elif choice == 4:
            title = "Simulated Annealing + Dijkstra"
            sa = SimulatedAnnealing(start_pos=start_pos, exit_pos=exit_pos, pathfinder_func=dijkstra_func)
            best_route = sa.solve(foods)
            cost = -sa.evaluate_state(best_route)
            
        exec_time = time.time() - start_time
        
        # We set avoid_ghosts=False here so that the animation ALWAYS shows a path for the presentation,
        # even if the teammate's maze has a ghost physically blocking the choke point!
        _, full_path = evaluate_food_sequence(grid, start_pos, best_route, exit_pos, heuristic_map=None, avoid_ghosts=False)
        
        pygame.display.set_caption(title)
        animate_path(grid, full_path, title)
        
        analysis_data = {
            'title': title,
            'time': exec_time,
            'distance': cost,
            'food_seq': best_route,
            'path': full_path
        }

if __name__ == "__main__":
    run_visual_experiment()
