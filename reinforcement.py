import numpy as np

# Q-table: 3 states, 2 actions
Q = np.zeros((3, 2))

# Parameters
alpha = 0.1   # Learning rate
gamma = 0.9   # Discount factor
epsilon = 1.0 # Exploration rate

# Training
for episode in range(100):
    state = 0

    for step in range(50):  # Max 50 steps per episode
        
        # Epsilon-greedy action selection
        if np.random.rand() < epsilon:
            action = np.random.randint(2)      # Explore
        else:
            action = np.argmax(Q[state])       # Exploit

        # Environment
        if action == 1:
            next_state = state + 1
            reward = 1
        else:
            next_state = state
            reward = 0

        # Q-learning update
        Q[state, action] = Q[state, action] + alpha * (
            reward + gamma * np.max(Q[next_state]) - Q[state, action]
        )

        state = next_state

        # Stop if reached terminal state
        if state >= 2:
            break

    # Decay epsilon
    epsilon = max(0.1, epsilon * 0.99)

# Results
print("Q-Table:")
print(Q)
print("\nBest Actions:")
for s in range(2):
    best = np.argmax(Q[s])
    print(f"  State {s} → Action {best} ({'Move Forward' if best == 1 else 'Stay'})")
