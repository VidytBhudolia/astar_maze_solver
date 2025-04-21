import numpy as np
from collections import deque
from sklearn.tree import DecisionTreeRegressor
from .manhattan_heuristic import manhattan_distance

# Global Decision Tree model
dt_model = None

def setup_decision_tree(maze, start, goal):
    """
    Pre-train the Decision Tree heuristic by running a quick BFS
    to get actual distances and training a decision tree model
    """
    global dt_model
    
    # Get distances using BFS
    maze_height = len(maze)
    maze_width = len(maze[0]) if maze else 0
    
    # Initialize distance map
    distances = {}
    visited = set()
    queue = deque([(goal, 0)])  # Start from goal, working backwards
    visited.add(tuple(goal))
    
    # BFS to calculate actual distances
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    
    while queue:
        current, dist = queue.popleft()
        current_tuple = tuple(current)
        distances[current_tuple] = dist
        
        # Check all four directions
        for dx, dy in directions:
            nx, ny = current[0] + dx, current[1] + dy
            
            if (0 <= nx < maze_height and 
                0 <= ny < maze_width and 
                maze[nx][ny] == 0):  # If it's a path
                
                neighbor = (nx, ny)
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(([nx, ny], dist + 1))
    
    # Prepare data for Decision Tree training
    X = []  # Features (position, relative to goal, wall density)
    y = []  # Target (actual distance)
    
    for pos, dist in distances.items():
        # Extract x, y coordinates
        x, y_pos = pos
        
        # Calculate relative position to goal
        rel_x = x - goal[0]
        rel_y = y_pos - goal[1]
        
        # Calculate Manhattan distance
        man_dist = abs(rel_x) + abs(rel_y)
        
        # Calculate wall density around position (in 3x3 grid)
        walls = 0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = x + dx, y_pos + dy
                if 0 <= nx < maze_height and 0 <= ny < maze_width and maze[nx][ny] == 1:
                    walls += 1
        
        # Features: position, relative position, manhattan distance, wall density
        X.append([x, y_pos, rel_x, rel_y, man_dist, walls])
        y.append(dist)
    
    # Train the decision tree
    if X and y:
        dt_model = DecisionTreeRegressor(max_depth=10)
        dt_model.fit(np.array(X), np.array(y))
    else:
        dt_model = None
    
    return distances.get(tuple(start), None)

def dt_heuristic(position, goal, maze=None):
    """
    Decision Tree based heuristic
    
    Args:
        position: Current position [x, y]
        goal: Goal position [x, y]
        maze: The maze grid (optional)
    
    Returns:
        Heuristic distance estimate
    """
    global dt_model
    
    # Calculate Manhattan distance as fallback
    base_heuristic = manhattan_distance(position, goal)
    
    # If model isn't trained or maze isn't available, use Manhattan distance
    if dt_model is None or maze is None:
        return base_heuristic
    
    # Extract features as in setup_decision_tree
    x, y_pos = position
    rel_x = x - goal[0]
    rel_y = y_pos - goal[1]
    man_dist = abs(rel_x) + abs(rel_y)
    
    # Calculate wall density
    walls = 0
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            nx, ny = x + dx, y_pos + dy
            if (0 <= nx < len(maze) and 
                0 <= ny < len(maze[0]) and 
                maze[nx][ny] == 1):
                walls += 1
    
    # Prepare feature vector
    features = np.array([[x, y_pos, rel_x, rel_y, man_dist, walls]])
    
    # Predict using the decision tree
    try:
        prediction = dt_model.predict(features)[0]
        # Ensure prediction is positive (sometimes models can predict negative values)
        return max(1.0, prediction)
    except:
        # Fallback to Manhattan distance if prediction fails
        return base_heuristic
