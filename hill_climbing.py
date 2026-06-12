# hill_climbing.py
# Author: Ratul Ghosh | ID: 0112410038
# Branch: optimization_0112410038
# Algorithm: Hill Climbing

algorithm_name = 'Hill Climbing'
student_id = '0112410038'

class HillClimbing:                                     # Class for the Hill Climbing algorithm

    # Constructor method
    def __init__(self):
        self.current_state = None                       # Store the current state being evaluated
        self.current_score = None                       # Store the score of the current state
        self.grid = None                                # Store the maze grid to check for walls


    def evaluate_state(self, state):                    # Evaluate the quality of a given state
        return 0                                        # Return 0 as a placeholder (actual scoring logic later)

    def get_neighbors(self, state):                     # Generate neighboring states from the current state
        row, col = state
        neighbors = []
        # Possible movements: Up, Down, Left, Right
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in moves:
            r, c = row + dr, col + dc
            # Check if within bounds and not a wall ('W')
            if 0 <= r < len(self.grid) and 0 <= c < len(self.grid[0]):
                if self.grid[r][c] != 'W':
                    neighbors.append((r, c))
                    
        return neighbors

    def solve(self, state, grid):   # Main Hill Climbing search process
        self.current_state = state
        self.grid = grid

        
        while True:
            # Step 1: Evaluate current state
            self.current_score = self.evaluate_state(self.current_state)

            # Step 2: Generate neighboring states
            neighbors = self.get_neighbors(self.current_state)
            if not neighbors:
                break

            # Step 3: Select best neighbor
            best_neighbor = None         # Store the best neighboring state
            best_score = float('-inf')
            
            for neighbor in neighbors:
                score = self.evaluate_state(neighbor)
                if score > best_score:
                    best_score = score
                    best_neighbor = neighbor

            # Step 4: Move to better neighbor
            # Step 5: Stop if no improvement exists
            if best_score <= self.current_score:
                break  # Reached a peak (local maximum)
                
            self.current_state = best_neighbor
            
        return self.current_state