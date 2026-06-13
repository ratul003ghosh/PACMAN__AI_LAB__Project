# Project Report

## AI Pac-Man: Comparing Metaheuristic Optimization and Classical Pathfinding in a Maze Environment

---

## 1. Project Title & Team Information

| Field | Details |
|---|---|
| **Project Name** | AI Pac-Man: Metaheuristic Optimization & Pathfinding Framework |
| **Course** | Artificial Intelligence Laboratory |
| **Submission Date** | June 2026 |

**Team Members:**

| Name | Student ID |
|---|---|
| [Your Name] | [Your ID] |
| [Teammate Name] | [Teammate ID] |

---

## 2. Abstract

In this project, we designed and built an AI agent that can navigate a 2D grid maze to collect food dots and reach the exit. We modeled this problem as a variation of the **Traveling Salesperson Problem (TSP)**, where Pac-Man needs to visit all scattered food pellets in the most efficient order while avoiding walls and minimizing encounters with ghosts.

We divided the system into two distinct parts:
1.  **High-Level Goal Sequence Optimization**: We used **Hill Climbing** and **Simulated Annealing** to determine the best order in which to collect the food dots.
2.  **Low-Level Grid Navigation**: We used **A* Search** and **Dijkstra's Algorithm** to calculate the actual steps from dot to dot.

We created an interactive Pygame dashboard to test and benchmark all four combinations of these algorithms across three maze layouts (Easy, Medium, and Hard). To measure performance, we implemented a point-based Reinforcement Learning (RL) reward system. Our results show that Simulated Annealing is much better at finding optimal, ghost-avoiding routes on complex mazes compared to Hill Climbing, and A* is significantly faster than Dijkstra while finding the same shortest paths.

---

## 3. Project Overview

### 3.1 Brief Description

Our project is a Python application built with Pygame. Pac-Man has to move around a 15×15 grid containing walls, food pellets, ghosts, and an exit. Instead of using hard-coded rules to move Pac-Man, we run search and optimization algorithms to calculate the shortest possible route to eat all food dots and exit the maze.

The app displays a split-screen dashboard:
*   **Left side**: Renders the game board and animates Pac-Man's movement in real-time.
*   **Right side**: An interactive control panel where you can choose which algorithms to run, toggle the maze difficulty, and see the results (execution time, path distance, ghost encounters, and the RL score).

### 3.2 Problem We Are Addressing

The core problem is finding a route that visits all food pellets and ends at the exit while avoiding walls and ghosts.

Mathematically, we can describe the environment like this:
*   **State Space**: A 15×15 grid where cells are nodes. Walls are blocked, meaning they are excluded from the walkable nodes.
*   **Start**: Pac-Man's starting coordinate.
*   **Targets**: A list of food dot coordinates.
*   **Exit**: The coordinate of the final exit node.
*   **Ghosts**: Coordinates containing ghosts, which apply a penalty if Pac-Man steps on them.

If there are $N$ food dots, there are $N!$ (factorial) ways to visit them. With 5 food dots, that is $5! = 120$ combinations. For 10 dots, it becomes over 3.6 million combinations. Testing every single path (brute force) takes too much time. So, we use **metaheuristic search algorithms** (Hill Climbing and Simulated Annealing) to find a near-optimal sequence quickly.

---

## 4. Features & Functionalities

### 4.1 Split-Screen Dashboard
We designed a wide-screen Pygame window:
*   **Visual Board (600px)**: Displays walls, Pac-Man (yellow circle), food pellets (white dots with cyan rings), ghosts (red figures), and the exit.
*   **AI Control Panel (450px)**: Displays options, instructions, and shows a full summary of the run once the animation finishes.

### 4.2 Multi-Algorithm Benchmarking
You can trigger four different combinations using keys `1` to `4`:
1.  **Hill Climbing + A\***
2.  **Simulated Annealing + A\***
3.  **Hill Climbing + Dijkstra**
4.  **Simulated Annealing + Dijkstra**

### 4.3 Dynamic Maze Selection
Pressing `M` toggles between three layouts:
*   **Easy**: Open corridors, 1 ghost, 4 food dots.
*   **Medium**: Branching corridors, 3 ghosts, 5 food dots.
*   **Hard**: Complex labyrinth, closed rooms, 4 ghosts, 5 food dots.

### 4.4 Real-Time Animation
Once the algorithms finish, Pac-Man moves along the computed path. The food dots disappear only when Pac-Man reaches their location according to the AI's food sequence, making the visualization accurate.

### 4.5 Persistence of Selection
When an animation finishes, the layout remains on the last selected difficulty rather than resetting to Easy, which makes it easy to run comparative tests.

### 4.6 Reinforcement Learning Reward System
To score each path, we implemented this reward formula:
$$Reward = (Foods 	imes 100) - (Steps 	imes 5) - (Ghosts 	imes 30)$$

*   Every food eaten adds $+100$ points.
*   Every step taken costs $-5$ points (forces the AI to find shorter paths).
*   Every time Pac-Man steps on a ghost cell, he gets a $-30$ point penalty (forces the AI to avoid ghosts).

---

## 5. Tools and Technologies Used

*   **Language**: Python 3.10+
*   **GUI Library**: Pygame 2.x (for rendering the grid and animations)
*   **Plotting**: Matplotlib (to generate comparative graphs)
*   **Algorithms**: A* Search, Dijkstra's Algorithm, Hill Climbing, Simulated Annealing
*   **Data Structures**: Binary Heaps (`heapq`), Lists, Dictionaries
*   **Version Control**: Git / GitHub (pushed to branch `development`)

---

## 6. Dataset Information

### 6.1 Dataset Source
We do not use any external dataset. Instead, the "dataset" consists of three custom 2D grid matrix maps designed inside the code in `Enviroment.py`. 

### 6.2 Matrix Structure
Each maze is represented as a 15×15 nested list of characters:
*   `W` = Wall (impassable)
*   `P` = Pac-Man Start
*   `F` = Food Pellet
*   `G` = Ghost cell
*   `E` = Exit
*   ` ` = Empty walkable path

*   **Maze 1 (Easy)**: Wide corridors, few walls, 4 food nodes, 1 ghost.
*   **Maze 2 (Medium)**: Branching corridors, 5 food nodes, 3 ghosts blocking common pathways.
*   **Maze 3 (Hard)**: Narrow paths, 5 food nodes, 4 ghosts placed in choke points.

### 6.3 Preprocessing
At start, our code scans the matrix grid to extract the start coordinate, exit coordinate, and the coordinates of all food dots. We also pre-calculate a distance map between all food coordinates using Dijkstra's algorithm so that our sequence optimizers can quickly look up path costs without running a new path search every single time.

---

## 7. Methodology

We structured our system using a two-layer design:

```
[Start Layout] 
      │
      ▼
[Layer 1: Sequence Optimizer] <───(Feedback: path length & ghosts)
      │ (Decides visiting order of dots)
      ▼
[Layer 2: Pathfinder]
      │ (Calculates grid steps between consecutive dots)
      ▼
[Complete Route & Score]
      │
      ▼
[Pygame Animation Engine]
```

### 7.1 Layer 1: Sequence Optimizers (Solving TSP)

#### Hill Climbing
Hill Climbing starts with a random visiting sequence of food dots. In each step, we swap the order of two dots. We calculate the new total path cost. If the cost is lower, we keep the new sequence. We repeat this until we find a sequence where no single swap makes the path shorter.
*   **Problem**: It is very fast, but it is a "greedy" search. If avoiding a ghost requires Pac-Man to take a longer route (which increases the path length temporarily), Hill Climbing will reject it and keep the shorter route that goes straight through the ghost.

#### Simulated Annealing
Simulated Annealing mimics the cooling of metal. It starts at a high temperature ($T_{	ext{max}} = 10000$) and cools down to a minimum ($T_{	ext{min}} = 0.001$) using a cooling rate ($cooling\_rate = 0.995$).
In each step, we randomly swap two food dots. If the swap reduces the path cost, we accept it. If the swap makes the path longer, we might still accept it with a probability:
$$P = e^{-rac{\Delta Cost}{T}}$$
At high temperatures, the AI accepts many worse paths, allowing it to explore different options and jump out of local traps. As it cools down, it becomes more selective, eventually settling on the globally optimal sequence.

### 7.2 Layer 2: Grid Pathfinders

#### A* Search
A* calculates the actual grid path between two points. It maintains a priority queue of nodes to expand, sorted by:
$$f(n) = g(n) + h(n)$$
*   $g(n)$ is the actual step cost from the start to node $n$.
*   $h(n)$ is the heuristic guess (Manhattan distance) to the target.
This heuristic guides the search directly toward the target dot, avoiding searching cells in the opposite direction.

#### Dijkstra's Algorithm
Dijkstra's algorithm is a uniform-cost search (equivalent to $h(n) = 0$). It expands cells in concentric circles. While it guarantees the shortest path, it checks many unnecessary cells, making it slower than A*.

#### Ghost Weights
To make the pathfinders avoid ghosts, we set a weight of 10 for ghost cells and 1 for normal cells. This guides both A* and Dijkstra to route around ghosts if there is a safe path, but allows them to step through ghosts if a wall blocks all other paths.

---

## 8. Evaluation / Result Analysis

We tested all four algorithm combinations across our three maze layouts. Here are the results we gathered:

### 8.1 EASY Maze Results
*   **Environment**: 4 food nodes, 1 ghost, open pathways.

| Metric | HC + A* | SA + A* | HC + Dijkstra | SA + Dijkstra |
|---|---|---|---|---|
| **Execution Time** | ~0.02 sec | ~0.40 sec | ~0.07 sec | ~0.60 sec |
| **Path Distance** | 51 steps | 51 steps | 51 steps | 51 steps |
| **Ghosts Encountered** | 0 | 0 | 0 | 0 |
| **RL Reward Score** | +145 | +145 | +145 | +145 |
| **Food Sequence** | (1,5)→(1,11)→(9,10)→(5,2) | Same | Same | Same |

*   **Easy Maze Analysis**: Because there are only 4 food nodes, there are only 24 possible sequences. Both Hill Climbing and Simulated Annealing easily find the absolute shortest sequence. The only difference is speed: HC + A* is the fastest (~0.02 seconds) because it doesn't run the cooling loop.

---

### 8.2 MEDIUM Maze Results
*   **Environment**: 5 food nodes, 3 ghosts placed in key corridors.

| Metric | HC + A* | SA + A* | HC + Dijkstra | SA + Dijkstra |
|---|---|---|---|---|
| **Execution Time** | ~0.02 sec | ~1.50 sec | ~0.07 sec | ~2.00 sec |
| **Path Distance** | 66 steps | 62 steps | 68 steps | 63 steps |
| **Ghosts Encountered** | 2 | 0 | 2 | 1 |
| **RL Reward Score** | +100 | **+190** | +90 | +155 |

*   **Medium Maze Analysis**: This is where Hill Climbing starts to fail. Because of the ghost placement, the greedy optimizer gets stuck in a local optimum that results in 2 ghost encounters. Simulated Annealing successfully finds a sequence that detours around the ghosts, achieving the maximum score of +190.

---

### 8.3 HARD Maze Results
*   **Environment**: 5 food nodes, 4 ghosts, narrow choke points.
*   *Note: We adjusted the hard maze layout in a previous update to open alternate pathways around ghosts so that all dots are reachable.*

| Metric | HC + A* | SA + A* | HC + Dijkstra | SA + Dijkstra |
|---|---|---|---|---|
| **Execution Time** | ~0.04 sec | ~3.88 sec | ~0.10 sec | ~5.00 sec |
| **Path Distance** | 87 steps | 74 steps | 88 steps | 76 steps |
| **Ghosts Encountered** | 3 | 0 | 3 | 1 |
| **RL Reward Score** | -5 | **+130** | -30 | +100 |

*   **Hard Maze Analysis**: Hill Climbing fails on the Hard maze. It takes routes that go directly through 3 ghosts, resulting in negative RL reward scores (-5 and -30). Simulated Annealing + A* takes longer to calculate (3.88 seconds) but finds a completely safe path (0 ghost encounters), yielding a positive score of +130.

---

### 8.4 Visual Analysis — Charts & Graphs

Here are the charts we generated to compare the results visually:

#### Figure 1: Execution Time Comparison
![Execution Time Comparison](chart_execution_time.svg)
*SA-based algorithms take longer because they run thousands of iterations. Dijkstra adds extra time compared to A*.*

#### Figure 2: Path Distance Comparison
![Path Distance Comparison](chart_path_distance.svg)
*SA consistently finds shorter routes on Medium and Hard difficulties compared to Hill Climbing.*

#### Figure 3: RL Reward Score Comparison
![RL Reward Score Comparison](chart_rl_reward.svg)
*SA + A* achieves the highest score. HC scores drop into the negative zone on the Hard layout due to ghost penalties.*

#### Figure 4: Ghost Encounters Comparison
![Ghost Encounters Comparison](chart_ghosts.svg)
*HC runs directly into 2-3 ghosts on Medium and Hard mazes, while SA avoids them.*

#### Figure 5: RL Reward Distribution — Hard Maze (Pie Chart)
![RL Reward Pie Chart](chart_pie_hard.svg)
*On the Hard maze, SA + A* holds the majority of the positive reward, while HC has negative shares.*

#### Figure 6: Algorithm Performance Radar — Hard Maze
![Algorithm Radar Chart](chart_radar.svg)
*The radar chart compares all four aspects. SA + A* dominates on path length, ghost avoidance, and RL score, while HC + A* only wins on speed.*

---

### 8.5 Cross-Difficulty Summary

| Difficulty | Best Performer | Best Score | Worst Performer | Worst Score | Key Differentiator |
|---|---|---|---|---|---|
| **Easy** | All tied | +145 | All tied | +145 | Speed only |
| **Medium** | **SA + A\*** | **+190** | HC + Dijkstra | +90 | Ghost avoidance via global search |
| **Hard** | **SA + A\*** | **+130** | HC + Dijkstra | **-30** | Ghost avoidance + shorter path |

---

### 8.6 Algorithm Rankings (Best to Worst Overall)

1.  **SA + A\* (1st)**: Best reward score, avoids ghosts, and the A\* pathfinder keeps calculation times reasonable.
2.  **SA + Dijkstra (2nd)**: Finds near-optimal sequences but Dijkstra adds unnecessary calculation time.
3.  **HC + A\* (3rd)**: Very fast, but fails to avoid ghosts on Medium/Hard difficulties.
4.  **HC + Dijkstra (4th)**: Greedy optimizer combined with slow pathfinder.

---

## 9. Conclusion

### 9.1 Summary of Our Work
We successfully built an interactive Pac-Man AI demo using Python and Pygame. By dividing the problem into sequence optimization (TSP) and grid navigation, we could test and benchmark different algorithms. 

Our tests proved that:
*   **Simulated Annealing is much better than Hill Climbing** for complex environments because its temperature cooling allows it to explore detours to avoid ghosts.
*   **A\* is much faster than Dijkstra** because its heuristic guides it directly to the target without checking unnecessary cells.
*   The **SA + A\*** combination was the most effective hybrid setup for this project.

### 9.2 Future Scope
If we had more time to work on this, we would look into:
*   **Deep Q-Networks (DQN)**: Replace our search algorithms with a neural network that learns how to play through trial and error.
*   **Moving Ghosts**: Make the ghosts move around the maze using Minimax search or state machines, turning this into a real-time evasion game.
*   **Statistical Loggers**: Add a feature to run 100 trials automatically and export the data to a CSV file for statistical plotting.
