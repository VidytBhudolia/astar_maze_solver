import numpy as np
from collections import deque
from .manhattan_heuristic import manhattan_distance

class KNNHeuristic:
    """
    K-Nearest Neighbors based heuristic calculation to improve A* pathfinding.
    This helps identify more promising paths by learning from previously successful paths.
    """
    def __init__(self):
        self.training_positions = []  # Store positions
        self.training_distances = []  # Store actual distances
        self.k = 3  # Number of neighbors to consider
        self.max_samples = 1000  # Limit samples for performance
        self.cache = {}  # Cache for position-to-distance lookups
    
    def add_sample(self, position, actual_distance):
        """Add a position and its actual distance to the goal to the training data"""
        # Convert to tuple for consistency
        position_tuple = tuple(position)
        self.training_positions.append(position_tuple)
        self.training_distances.append(actual_distance)
        self.cache[position_tuple] = actual_distance
        
        # Keep the training set manageable
        if len(self.training_positions) > self.max_samples:
            removed_pos = self.training_positions.pop(0)
            self.training_distances.pop(0)
            if removed_pos in self.cache:
                del self.cache[removed_pos]
    
    def predict_distance(self, position, default_heuristic):
        """Predict distance using KNN if possible, otherwise use default heuristic"""
        position_tuple = tuple(position)
        
        # Check cache first for exact matches
        if position_tuple in self.cache:
            return self.cache[position_tuple]
        
        if len(self.training_positions) < self.k:
            return default_heuristic
        
        # Convert to numpy arrays for vectorized operations if not already
        if not isinstance(self.training_positions, np.ndarray):
            positions_array = np.array(self.training_positions)
        else:
            positions_array = self.training_positions
            
        # Vectorized Manhattan distance calculation
        diffs = np.abs(positions_array - np.array(position))
        feature_dists = np.sum(diffs, axis=1)
        
        # Get indices of k nearest neighbors
        if len(feature_dists) <= self.k:
            nearest_indices = np.arange(len(feature_dists))
        else:
            nearest_indices = np.argpartition(feature_dists, self.k)[:self.k]
        
        # Get distances and actuals for k nearest neighbors
        nearest_dists = feature_dists[nearest_indices]
        nearest_actuals = np.array(self.training_distances)[nearest_indices]
        
        # Calculate weights (inverse distance)
        weights = np.where(nearest_dists > 0, 1.0 / nearest_dists, 1.0)
        sum_weights = np.sum(weights)
        
        # Calculate weighted average
        if sum_weights > 0:
            prediction = np.sum(weights * nearest_actuals) / sum_weights
            # Blend with the default heuristic for stability
            result = 0.7 * prediction + 0.3 * default_heuristic
            # Cache the result
            self.cache[position_tuple] = result
            return result
        else:
            return default_heuristic

# Initialize a global instance for use across the application
knn_heuristic = KNNHeuristic()

def get_optimal_heuristic(position, goal, maze=None):
    """
    Get the best heuristic estimate using KNN
    
    Args:
        position: Current position [x, y]
        goal: Goal position [x, y]
        maze: The maze grid (optional)
    
    Returns:
        Heuristic distance estimate
    """
    # Calculate basic Manhattan distance
    base_heuristic = manhattan_distance(position, goal)
    
    # Use KNN to potentially improve the estimate
    enhanced_estimate = knn_heuristic.predict_distance(position, base_heuristic)
    
    # If maze is provided, we can do additional analysis
    if maze is not None:
        # Quick check for immediate obstacles - increases heuristic if surrounded by walls
        obstacles = 0
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        for dx, dy in directions:
            nx, ny = position[0] + dx, position[1] + dy
            if (0 <= nx < len(maze) and 
                0 <= ny < len(maze[0]) and 
                maze[nx][ny] == 1):  # If it's a wall
                obstacles += 1
        
        # Penalize positions surrounded by walls
        obstacle_factor = 1 + (obstacles / 8)  # Small penalty based on obstacles
        enhanced_estimate *= obstacle_factor
    
    return enhanced_estimate

def train_heuristic(maze, start, goal):
    """
    Pre-train the KNN heuristic by running a quick BFS to get actual distances
    This helps the A* algorithm make better decisions from the start
    """
    maze_height = len(maze)
    maze_width = len(maze[0]) if maze else 0
    
    # Initialize distance map
    distances = {}
    visited = set()
    queue = deque([(goal, 0)])  # Start from goal, working backwards
    visited.add(tuple(goal))
    
    # Pre-calculate valid directions once
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    
    # BFS to calculate actual distances from all points to goal
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
    
    # Batch add samples to our KNN model
    for pos, dist in distances.items():
        knn_heuristic.add_sample(list(pos), dist)
    
    return distances.get(tuple(start), None)  # Return distance from start to goal if found
