# hill_climbing.py
# Author: Ratul Ghosh | ID: 0112410038
# Branch: optimization_0112410038
# Algorithm: Hill Climbing

algorithm_name = 'Hill Climbing'
student_id = '0112410038'

class HillClimbing:                                     # Class for the Hill Climbing algorithm

    # Constructor method
    def __init__(self, start_pos=None, exit_pos=None, pathfinder_func=None):
        self.current_state = None                       # Store the current state (order of foods)
        self.current_score = None                       # Store the score of the current state
        self.start_pos = start_pos                      # Pacman's starting position
        self.exit_pos = exit_pos                        # The exit position
        self.pathfinder_func = pathfinder_func          # Teammate's A* or Dijkstra function

    def evaluate_state(self, state):                    # Evaluate the quality of a given state (food order)
        if not state or not self.start_pos:
            return float('-inf')

        total_distance = 0
        current_pos = self.start_pos

        # Calculate the total path distance for visiting the foods in this specific order
        for food in state:
            if self.pathfinder_func:
                # Use Dijkstra or A* to get the exact path distance
                total_distance += self.pathfinder_func(current_pos, food)
            else:
                # Fallback: Manhattan distance if no pathfinder is provided yet
                total_distance += abs(current_pos[0] - food[0]) + abs(current_pos[1] - food[1])
            current_pos = food

        # Finally, add the distance from the last food to the exit
        if self.exit_pos:
            if self.pathfinder_func:
                total_distance += self.pathfinder_func(current_pos, self.exit_pos)
            else:
                total_distance += abs(current_pos[0] - self.exit_pos[0]) + abs(current_pos[1] - self.exit_pos[1])

        # Return negative distance because Hill Climbing maximizes the score (shorter distance = higher score)
        return -total_distance

    def get_neighbors(self, state):                     # Generate neighboring states by swapping foods
        neighbors = []
        # Generate new routes by swapping the order of any two food items
        for i in range(len(state)):
            for j in range(i + 1, len(state)):
                neighbor = state.copy()
                # Swap the items
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                neighbors.append(neighbor)
        return neighbors

    def solve(self, environment_foods):   # Main Hill Climbing search process
        # environment_foods is the initial list of food coordinates: e.g., [(1,1), (3,4), (5,5)]
        self.current_state = environment_foods.copy()
        
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