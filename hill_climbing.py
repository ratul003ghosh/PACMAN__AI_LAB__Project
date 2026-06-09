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

    def evaluate_state(self, state):                    # Evaluate the quality of a given state
        return 0                                        # Return 0 as a placeholder (actual scoring logic later)

    def get_neighbors(self, state):                     # Generate neighboring states from the current state
        return []                                       # Return an empty list as a placeholder (actual logic later)