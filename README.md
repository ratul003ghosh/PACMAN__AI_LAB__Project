# AI Pac-Man: Optimization & Pathfinding Framework

Welcome to the **AI Pac-Man Optimization Project**! This project is a comprehensive Python and Pygame application designed to solve the food-collection problem using various artificial intelligence algorithms. 

By treating the maze like a variation of the **Traveling Salesperson Problem (TSP)**, this framework dynamically calculates the optimal sequence for Pac-Man to eat all the dots and reach the exit using advanced heuristics!

## 🚀 How to Run the Presentation

To start the Interactive Visual Sandbox for your presentation, simply follow these steps in your terminal:

**1. Install Dependencies**
Ensure you have Pygame installed in your Python environment:
```bash
pip install pygame
```

**2. Launch the Application**
Run the main script to open the dashboard:
```bash
python main.py
```

## 🎮 Features & Controls

Once the window opens, you will have access to the **Professional Split-Screen Dashboard**. 
- **The Left Panel** displays the dynamic Pac-Man maze and real-time animations.
- **The Right Panel** is your interactive AI Control Panel.

### Keyboard Controls:
* **Press `M`**: Instantly toggle the map between **Easy**, **Medium**, and **Hard** layouts.
* **Press `1`**: Run **Hill Climbing + A***.
* **Press `2`**: Run **Simulated Annealing + A***.
* **Press `3`**: Run **Hill Climbing + Dijkstra**.
* **Press `4`**: Run **Simulated Annealing + Dijkstra**.
* **Press `ESC`**: Exit the application.

## 🧠 The AI Algorithms

This project combines high-level **Metaheuristic Optimizers** with low-level **Pathfinding Algorithms** to achieve incredible results:

### 1. The Pathfinders (The "How to move")
* **A* (A-Star) Search**: Uses Manhattan distance heuristics to find the absolute shortest path between two points while avoiding walls.
* **Dijkstra's Algorithm**: Exhaustively maps out the shortest path to all reachable nodes without a heuristic bias.

### 2. The Optimizers (The "What order to eat")
Because there are multiple food dots scattered across the map, we must decide the *order* in which to collect them to minimize the total steps taken.
* **Hill Climbing**: An iterative local search algorithm that continuously swaps the order of the food nodes to find a more efficient sequence. It is incredibly fast but can sometimes get stuck in local optima.
* **Simulated Annealing**: A probabilistic technique inspired by metallurgy. It initially accepts "worse" paths to jump out of local optima, gradually "cooling down" to hone in on the absolute best global path sequence!

## 📊 On-Screen Analysis
After the AI finishes "Thinking", Pac-Man will animate his journey. Once he reaches the exit, the dashboard will dynamically print the results:
* **Execution Time:** How fast the AI computed the route.
* **Path Distance:** The exact number of steps Pac-Man took.
* **Food Sequence:** The coordinate order he visited the food.
* **Path Sequence:** Every single step taken from start to finish!
