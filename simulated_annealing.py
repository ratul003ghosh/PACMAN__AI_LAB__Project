# simulated_annealing.py
# Author: Ratul Ghosh | ID: 0112410038
# Branch: optimization_0112410038
# Algorithm: Simulated Annealing

algorithm_name = 'Simulated Annealing'
student_id = '0112410038'
initial_temperature = 100.0
cooling_rate = 0.99

class SimulatedAnnealing:      # class for the Simulated Annealing algorithm

    # Constructor method
    def __init__(self, start_pos=None, exit_pos=None, pathfinder_func=None):
        self.temperature = initial_temperature          # Initial temperature for exploration
        self.cooling_rate = cooling_rate                # Cooling rate to decrease the temperature after each iteration 
        self.current_state = None                       # Store the current state (order of foods)
        self.current_score = None                       # Store the score of the current state
        self.start_pos = start_pos                      # Pacman's starting position
        self.exit_pos = exit_pos                        # The exit position
        self.pathfinder_func = pathfinder_func          # Teammate's A* or Dijkstra function
    
    def cool_down(self):            # Reduce the temperature after each iteration
        self.temperature *= self.cooling_rate

    def evaluate_state(self, state):                    # Evaluate the quality of a given state (food order)
        if not state or not self.start_pos:
            return float('-inf')

        total_distance = 0
        current_pos = self.start_pos

        # Calculate the total path distance for visiting the foods in this specific order
        for food in state:
            if self.pathfinder_func:
                total_distance += self.pathfinder_func(current_pos, food)
            else:
                total_distance += abs(current_pos[0] - food[0]) + abs(current_pos[1] - food[1])
            current_pos = food

        # Finally, add the distance from the last food to the exit
        if self.exit_pos:
            if self.pathfinder_func:
                total_distance += self.pathfinder_func(current_pos, self.exit_pos)
            else:
                total_distance += abs(current_pos[0] - self.exit_pos[0]) + abs(current_pos[1] - self.exit_pos[1])

        # Return negative distance because Simulated Annealing maximizes the score
        return -total_distance

    def get_neighbors(self, state):                     # Generate neighboring states from the current state
        return []                                       # Return an empty list as a placeholder (actual logic later)

    def solve(self, state):   # Main Simulated Annealing search process
        # Step 1: Evaluate current state

        # Step 2: Generate neighboring states

        # Step 3: Select random neighbor

        # Step 4: Calculate energy difference & decide acceptance

        # Step 5: Cool down temperature

        # Step 6: Stop when temperature is very low

        pass