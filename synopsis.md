# ENHANCED A* MAZE SOLVER

## DESCRIPTION
The Enhanced A* Maze Solver is a project designed to solve mazes efficiently using an improved A* algorithm. The algorithm incorporates a KNN-based heuristic to enhance the pathfinding process. Mazes are represented as 2D grids, where the solver identifies the shortest path from a start point to an endpoint. The solution path is marked on the maze for visualization.

This project demonstrates the integration of machine learning techniques with traditional pathfinding algorithms, making it suitable for solving complex mazes. The enhanced heuristic improves the algorithm's efficiency by providing better initial estimates for pathfinding.

## ALGORITHM TO BE USED
The project uses an enhanced version of the A* algorithm, which is a popular pathfinding and graph traversal algorithm. The key steps of the algorithm are as follows:

1. **Pre-training the Heuristic**: The heuristic function is pre-trained using the `train_heuristic` function. This step ensures that the heuristic provides optimal initial estimates for the shortest path, leveraging a KNN-based approach.

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

This enhanced A* algorithm combines the strengths of traditional pathfinding with machine learning techniques to improve efficiency and accuracy.

## EXPECTED OUTPUT OF THE PROJECT
The expected output of this project is a maze-solving algorithm that efficiently finds the shortest path in a given maze. The solution path is marked on the maze grid using a distinct value (e.g., `2`). The enhanced heuristic ensures faster and more accurate pathfinding. The project can be used in applications requiring efficient navigation, such as robotics, game development, and AI simulations.