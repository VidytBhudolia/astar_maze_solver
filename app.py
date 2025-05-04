from flask import Flask, render_template, request, jsonify
import sys
import os

# Add the path to your existing A* code
sys.path.append('e:/tensor_learn/astar_maze_solver')

from maze_generator import generate_maze
from astar_algorithm import astar_solve

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_maze', methods=['POST'])
def generate_maze_endpoint():
    data = request.get_json()
    size = int(data.get('size', 15))
    multiple_paths = data.get('multiple_paths', True)  # Default to True for multiple paths
    wall_removal_probability = data.get('wall_removal_probability', 0.20)  # Increased probability
    
    # Generate maze using modified function with multiple paths
    maze = generate_maze(size, size, multiple_paths, wall_removal_probability)
    
    return jsonify({
        'maze': maze,
        'start': [1, 1],
        'end': [size-2, size-2]
    })

@app.route('/solve_maze', methods=['POST'])
def solve_maze_endpoint():
    data = request.get_json()
    maze = data.get('maze')
    start = data.get('start', [1, 1])
    end = data.get('end', [len(maze)-2, len(maze[0])-2])
    
    # Solve maze with different heuristics
    results = {}
    heuristic_types = ['manhattan', 'KNN', 'decision_tree']
    
    # Define display order
    display_order = {
        'manhattan': 1,
        'KNN': 2,
        'decision_tree': 3
    }
    
    for heuristic_type in heuristic_types:
        solved_maze, execution_time = astar_solve(maze, start, end, heuristic_type)
        results[heuristic_type] = {
            'time': execution_time,
            'solved_maze': solved_maze,
            'display_order': display_order[heuristic_type]  # Add display order
        }
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
