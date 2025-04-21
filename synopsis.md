# ENHANCED A* MAZE SOLVER

## DESCRIPTION
The Enhanced A* Maze Solver is a project designed to solve mazes efficiently using an improved A* algorithm. The algorithm incorporates multiple heuristic functions including Manhattan distance, KNN-based, and decision tree approaches to enhance the pathfinding process. Mazes are represented as 2D grids, where the solver identifies the shortest path from a start point to an endpoint. The solution path is marked on the maze for visualization.

This project demonstrates the integration of machine learning techniques with traditional pathfinding algorithms, making it suitable for solving complex mazes. The enhanced heuristics improve the algorithm's efficiency by providing better initial estimates for pathfinding.

## MAZE GENERATION
The project includes a maze generator that creates random mazes using a depth-first search algorithm with backtracking. The generator ensures that there's always a valid path from the start point to the endpoint. The maze is represented as a 2D grid where:
- `0` represents an open path
- `1` represents a wall
- `2` represents the solution path (after the A* algorithm has found it)

The generated mazes provide a challenging environment for testing different heuristic functions in the A* algorithm.

## ALGORITHM TO BE USED
The project uses an enhanced version of the A* algorithm, which is a popular pathfinding and graph traversal algorithm. The key steps of the algorithm are as follows:

1. **Pre-training the Heuristic**: Multiple heuristic functions are available:
   - Manhattan distance: Traditional distance calculation
   - KNN-based heuristic: Leverages K-Nearest Neighbors approach for better path estimation
   - Decision tree heuristic: Uses decision trees for pathfinding decisions

2. **Initialization**:
   - The maze is represented as a 2D grid, where `0` indicates open paths, and `1` indicates walls.
   - A priority queue (open list) is initialized to store nodes to be explored, prioritized by their `f_score` (sum of the cost to reach the node and the heuristic estimate to the goal).
   - A closed set is used to track visited nodes, and a parent dictionary is maintained to reconstruct the path.

3. **Exploration**:
   - Nodes are explored in order of their `f_score`. For each node, its neighbors are evaluated.
   - Valid neighbors are those within the maze bounds, not walls, and not already visited.
   - For each valid neighbor, the algorithm calculates:
     - `g_score`: The cost to reach the neighbor from the start.
     - `h_score`: The heuristic estimate of the cost to reach the goal from the neighbor.
     - `f_score`: The sum of `g_score` and `h_score`.

4. **Path Reconstruction**:
   - If the endpoint is reached, the algorithm reconstructs the path by backtracking through the parent dictionary.
   - The solution path is marked on the maze grid using a distinct value (e.g., `2`).

5. **No Path Found**:
   - If the open list is exhausted and the endpoint is not reached, the algorithm returns the maze with no solution path.

## HEURISTIC FUNCTIONS IN DETAIL
The success and efficiency of the A* algorithm heavily depend on the chosen heuristic function. This project implements and compares three different heuristic approaches:

### 1. Manhattan Distance Heuristic
- **Definition**: The Manhattan distance (also known as taxicab or city block distance) is calculated as the sum of the absolute differences between the coordinates of two points.
- **Formula**: h(n) = |x₁ - x₂| + |y₁ - y₂|, where (x₁, y₁) is the current position and (x₂, y₂) is the goal position.
- **Properties**: This heuristic is admissible (never overestimates the distance) and consistent (satisfies the triangle inequality), ensuring optimal solutions.
- **Advantages**: Simple to compute, efficient, and works well for grid-based environments where movement is restricted to four directions.
- **Limitations**: Does not account for obstacles or maze structure; only considers raw distance.
- **Example**: If current position is (3, 4) and goal is at (7, 9), Manhattan distance = |7 - 3| + |9 - 4| = 4 + 5 = 9.

### 2. KNN-Based Heuristic
- **Definition**: This heuristic leverages the K-Nearest Neighbors algorithm to estimate distances based on patterns observed from previously solved similar maze configurations.
- **Implementation**:
  1. For training, the algorithm collects data points consisting of (state, actual_distance_to_goal) pairs from previously solved mazes.
  2. For inference, given a new state, it identifies K most similar states from the training data.
  3. The heuristic estimate is calculated as the weighted average of the actual distances from the K nearest neighbors.
- **Properties**: This heuristic is learning-based and can potentially provide more accurate estimates than pure geometric approaches.
- **Advantages**: Can capture maze-specific patterns, potentially more accurate when trained on similar mazes, adapts to the structure of the problem.
- **Limitations**: Requires training data, may not generalize well to dramatically different maze structures, computationally more expensive than simpler heuristics.
- **Example**: If similar positions in past mazes required 12, 14, and 11 steps to reach the goal, the KNN heuristic might estimate around 12.3 steps for a new similar position.

### 3. Decision Tree Heuristic
- **Definition**: This heuristic uses a decision tree model to predict the distance to the goal based on various features of the current state.
- **Implementation**:
  1. Features are extracted from the maze state, such as local wall patterns, distance metrics, and relative position features.
  2. The decision tree model, trained on prior maze-solving experiences, predicts the estimated distance to the goal.
  3. The prediction is used as the heuristic value in the A* algorithm.
- **Properties**: Can capture complex non-linear relationships between maze features and actual distances.
- **Advantages**: Can identify complex patterns that simple distance metrics miss, takes into account the structure of the maze, can learn from experience.
- **Limitations**: Requires significant training data for accuracy, may overfit to specific maze types, more complex to implement and tune.
- **Example**: The decision tree might learn that when there's a wall to the right and an open path ahead with the goal in the northeast direction, an optimal estimate is typically 15% longer than the Manhattan distance.

Each heuristic has its strengths and weaknesses, and their performance can vary significantly depending on the specific characteristics of the maze. The comparative analysis implemented in this project helps identify which heuristic performs best under different conditions.

## HEURISTIC COMPARISON
The project features a comprehensive heuristic comparison functionality that:

1. Solves the same maze using different heuristic functions
2. Measures and compares execution time for each heuristic
3. Identifies the fastest heuristic for pathfinding
4. Visualizes the performance comparison using:
   - Interactive charts in the web interface
   - Matplotlib for data analysis and reporting
5. Displays the solution path for each heuristic
6. Saves visualization as image files for future reference

This comparison helps identify which heuristic performs best under different maze configurations and sizes.

## WEB INTERFACE
The project includes a web-based interface that allows users to:

1. Generate mazes of different sizes
2. Visualize the generated maze with clear start and end points
3. Solve the maze using multiple heuristic functions
4. Compare the performance of different heuristics
5. View the solution path for each heuristic
6. See visualization of time comparisons through interactive charts
7. Highlight the fastest solution path for quick identification

The interface provides an intuitive way to interact with the maze solver and visualize results.

## EXPECTED OUTPUT OF THE PROJECT
The expected output of this project is:

1. A maze-solving algorithm that efficiently finds the shortest path in a given maze
2. Visual representation of the solution path marked on the maze grid
3. Performance metrics of different heuristic functions
4. Bar chart visualization comparing execution times of different heuristics
5. Identification of the most efficient heuristic for the given maze
6. Interactive web interface for user engagement and result visualization
7. Exportable visualization reports for documentation purposes

The enhanced heuristic ensures faster and more accurate pathfinding. The project can be used in applications requiring efficient navigation, such as robotics, game development, and AI simulations.

## TECHNICAL IMPLEMENTATION
The project is implemented using:

1. Backend: Python with Flask for API endpoints
2. Frontend: HTML, CSS, and JavaScript for the web interface
3. Visualization: 
   - Chart.js for interactive performance comparison charts
   - Matplotlib for advanced data visualization and export
4. Algorithm: Custom implementation of A* with enhanced heuristics
5. Machine Learning: Implementation of KNN and Decision Tree heuristics
6. Data Processing: NumPy and Pandas for efficient data handling

The modular architecture allows for easy extension to include additional heuristic functions or maze generation algorithms.