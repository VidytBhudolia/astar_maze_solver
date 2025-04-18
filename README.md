# Enhanced A* Maze Solver

A high-performance maze pathfinding solution using A* algorithm with advanced heuristic techniques.

## Overview

This project implements an A* pathfinding algorithm for maze navigation, enhanced with a machine learning-based heuristic system. The enhanced heuristic combines traditional Manhattan distance calculations with K-Nearest Neighbors (KNN) to predict more accurate path distances, resulting in improved pathfinding efficiency.

## Features

- **A* Pathfinding Algorithm**: Efficient directed search algorithm to find optimal paths
- **Enhanced KNN Heuristic**: Machine learning approach that learns from successful paths
- **Adaptive Path Planning**: Dynamically improves pathfinding with experience
- **Obstacle Detection**: Considers wall density and obstacle patterns
- **Performance Optimizations**: Vectorized calculations and caching for speed

## Components

### Enhanced Heuristic System

The core of this system is the `enhanced_heuristic.py` module which provides:

- **KNNHeuristic Class**: Learns from past paths to make better estimations
- **Optimized Distance Calculations**: Using NumPy for vectorized operations
- **Intelligent Caching**: Avoids redundant calculations
- **Obstacle-Aware Estimates**: Considers wall density in path predictions

## Usage

```python
from enhanced_heuristic import train_heuristic, get_optimal_heuristic

# Initialize the maze (0 = open path, 1 = wall)
maze = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
]

start = [0, 0]  # Starting position
goal = [4, 4]   # Target position

# Pre-train the heuristic on the maze
train_heuristic(maze, start, goal)

# Later in your A* algorithm, get the heuristic value:
position = [2, 2]
h_value = get_optimal_heuristic(position, goal, maze)
```

## Technical Details

### KNN Heuristic Implementation

The KNN heuristic uses the K-Nearest Neighbors algorithm to predict distances:

1. Stores successful path positions and their actual distances to the goal
2. When evaluating a new position, finds K most similar positions from training data
3. Uses weighted average of actual distances from similar positions
4. Blends the prediction with traditional Manhattan distance for stability
5. Caches results to improve performance

### Optimization Techniques

- NumPy vectorized operations for fast distance calculations
- Position caching to avoid recalculating common paths
- Efficient neighbor selection using `np.argpartition`
- Pre-training via BFS for initial distance mapping
- Memory-efficient data structures

## Performance

The enhanced heuristic significantly improves A* performance:

- More accurate distance predictions leading to fewer expanded nodes
- Lower memory usage due to more direct paths
- Improved handling of maze patterns and obstacles
- Adaptive learning from previous solutions
- Logarithmic improvement in pathfinding speed as experience grows

## Requirements

- Python 3.6+
- NumPy
- Collections (standard library)

## License

MIT
