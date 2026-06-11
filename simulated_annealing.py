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
    def __init__(self):
        self.temperature = initial_temperature          # Initial temperature for exploration
        self.cooling_rate = cooling_rate                   # Cooling rate to decrease the temperature after each iteration 
    
    def cool_down(self):            # Reduce the temperature after each iteration
        self.temperature *= self.cooling_rate

    def evaluate_state(self, state):                    # Evaluate the quality of a given state
        return 0                                        # Return 0 as a placeholder (actual scoring logic later)

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