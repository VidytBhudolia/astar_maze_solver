import time
import matplotlib.pyplot as plt
import numpy as np
from maze_generator import generate_maze, print_maze
from astar_algorithm import astar_solve

def main():
    # Create maze dimensions
    m = 41
    n = 41
    
    print("Generating maze...")
    # Generate maze and start/end points
    maze = generate_maze(n, m)
    start = [1, 1]
    end = [m-2, n-2]
    
    # Compare different heuristics
    compare_heuristics(maze, start, end)

def compare_heuristics(maze, start, end):
    """
    Compare different heuristic functions for A* algorithm
    
    Args:
        maze: The maze grid
        start: Starting position [x, y]
        end: Goal position [x, y]
    """
    heuristic_types = ['manhattan', 'knn', 'decision_tree']
    results = {}
    
    print("\nComparing different heuristic functions:")
    print("----------------------------------------")
    
    for heuristic_type in heuristic_types:
        print(f"\nSolving maze with A* algorithm using {heuristic_type} heuristic...")
        
        # Solve the maze with the specified heuristic
        solved_maze, execution_time = astar_solve(maze, start, end, heuristic_type)
        
        # Store result
        results[heuristic_type] = {
            'time': execution_time,
            'solved_maze': solved_maze
        }
        
        # Print result
        print(f"Execution time with {heuristic_type}: {execution_time:.6f} seconds")
        
    # Identify the fastest heuristic
    fastest = min(results.items(), key=lambda x: x[1]['time'])
    print(f"\nFastest heuristic: {fastest[0]} ({fastest[1]['time']:.6f} seconds)")
    
    # Print the solution from the fastest heuristic
    print("\nSolution using the fastest heuristic:")
    print_maze(fastest[1]['solved_maze'])
    
    # Plot comparison
    plot_comparison(results)

def plot_comparison(results):
    """
    Plot the execution time comparison between different heuristics
    
    Args:
        results: Dictionary with heuristic results
    """
    heuristics = list(results.keys())
    times = [results[h]['time'] for h in heuristics]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(heuristics, times, color=['blue', 'green', 'red'])
    
    # Add labels and title
    plt.xlabel('Heuristic Function')
    plt.ylabel('Execution Time (seconds)')
    plt.title('A* Algorithm: Execution Time by Heuristic Function')
    
    # Add the time values on top of the bars
    for bar, time_val in zip(bars, times):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001,
                f'{time_val:.4f}s', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('heuristic_comparison.png')
    plt.show()

if __name__ == "__main__":
    main()
