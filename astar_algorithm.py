import heapq
import time
from heuristic.manhattan_heuristic import manhattan_distance
from heuristic.knn_heuristic import get_optimal_heuristic, train_heuristic
from heuristic.decision_tree_heuristic import dt_heuristic, setup_decision_tree

def astar_solve(maze, start, end, heuristic_type='knn'):
    """algorithm for maze solving
    Enhanced A* algorithm for maze solving with different heuristic functions
    
    Args:
        maze: 2D grid representing the maze (0=path, 1=wall)
        start: Starting position [x, y]
        end: Goal position [x, y]
        heuristic_type: Type of heuristic to use ('manhattan', 'knn', 'decision_tree')
        
    Returns:
        tuple: (solved_maze, execution_time)
    """
    start_time = time.time()
    
    # Set up the appropriate heuristic function
    if heuristic_type == 'knn':
        # Pre-train the KNN heuristic for better initial estimates
        train_heuristic(maze, start, end)
        heuristic_func = lambda pos, goal, m: get_optimal_heuristic(pos, goal, m)
    elif heuristic_type == 'decision_tree':
        # Set up the decision tree model
        setup_decision_tree(maze, start, end)
        heuristic_func = lambda pos, goal, m: dt_heuristic(pos, goal, m)
    else:  # Default to manhattan distance
        heuristic_func = lambda pos, goal, m: manhattan_distance(pos, goal)
    
    # Define directions (up, right, down, left)
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    
    # Create a copy of the maze to mark the solution path
    maze_copy = [row.copy() for row in maze]
    
    # Initialize the open list (priority queue)
    open_list = []
    # Format: (f_score, g_score, position)
    initial_h = heuristic_func(start, end, maze)
    heapq.heappush(open_list, (initial_h, 0, start))
    
    # Initialize closed set and parent dictionary
    closed_set = set()
    parent = {}
    
    # Track best path for training
    actual_distances = {}
    
    while open_list:
        # Get position with lowest f_score
        _, g_score, current = heapq.heappop(open_list)
        
        # Convert to tuple for set operations
        current_tuple = tuple(current)
        
        # Skip if already processed
        if current_tuple in closed_set:
            continue
            
        # Mark as visited
        closed_set.add(current_tuple)
        actual_distances[current_tuple] = g_score
        
        # Check if we reached the end
        if current == end:
            # Reconstruct path
            path = []
            while tuple(current) in parent:
                path.append(current)
                current = parent[tuple(current)]
            path.append(start)
            
            # Mark path on maze copy (with 2s)
            for x, y in path:
                maze_copy[x][y] = 2
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            return maze_copy, execution_time
            
        # Check neighbors
        for dx, dy in directions:
            nx, ny = current[0] + dx, current[1] + dy
            neighbor = [nx, ny]
            neighbor_tuple = tuple(neighbor)
            
            # Check if valid neighbor (within bounds and not a wall)
            if (0 <= nx < len(maze) and 
                0 <= ny < len(maze[0]) and 
                maze[nx][ny] == 0 and 
                neighbor_tuple not in closed_set):
                
                # Calculate scores
                tentative_g = g_score + 1
                
                # Use the selected heuristic
                h_score = heuristic_func(neighbor, end, maze)
                f_score = tentative_g + h_score
                
                # Add to open list
                heapq.heappush(open_list, (f_score, tentative_g, neighbor))
                
                # Only update parent if this is a new path or a better path
                if neighbor_tuple not in parent or tentative_g < actual_distances.get(neighbor_tuple, float('inf')):
                    parent[neighbor_tuple] = current
    
    # No path found
    end_time = time.time()
    execution_time = end_time - start_time
    return maze_copy, execution_time
