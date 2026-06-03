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