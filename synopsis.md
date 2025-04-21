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