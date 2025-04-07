import time
from generate_maze import generate_maze
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
    
    print("Solving maze with A* algorithm ...")
    # Solve maze with A*
    start_time = time.time()
    solved_maze = astar_solve(maze, start, end)
    elapsed_time = time.time() - start_time
    
    # Print results
    print("Execution time: %s seconds" % elapsed_time)
    print_maze(solved_maze)

def print_maze(maze):
    # ANSI color codes
    RESET = "\033[0m"
    WALL = "\033[47m  " + RESET      # White background
    PATH = "\033[0m  "               # Default/transparent background
    SOLUTION = "\033[44m  " + RESET  # Blue background
    START = "\033[42;1m  " + RESET   # Green background
    END = "\033[41;1m  " + RESET     # Red background
    
    # Find start and end points (typically [1,1] and [len(maze)-2, len(maze[0])-2])
    start = [1, 1]
    end = [len(maze)-2, len(maze[0])-2]
    
    # Check if terminal supports ANSI colors
    try:
        # Create fancy border with double-line characters
        border_top = "╔" + "══" * len(maze[0]) + "╗"
        border_bottom = "╚" + "══" * len(maze[0]) + "╝"
        
        print("\n" + border_top)
        
        for i, row in enumerate(maze):
            print("║", end="")
            for j, cell in enumerate(row):
                if [i, j] == start:
                    print(START, end="")
                elif [i, j] == end:
                    print(END, end="")
                elif cell == 1:
                    print(WALL, end="")
                elif cell == 2:
                    print(SOLUTION, end="")
                else:
                    print(PATH, end="")
            print("║")
            
        print(border_bottom + "\n")
        
        # Add legend
        print(" Legend:")
        print(" " + START + " Start point")
        print(" " + END + " End point")
        print(" " + SOLUTION + " Solution path")
        print(" " + PATH + " Open path (unvisited)")
        print(" " + WALL + " Wall\n")
        
    except:
        # Fallback if terminal doesn't support ANSI colors
        print("\n+" + "-" * (len(maze[0]) * 2) + "+")
        
        for i, row in enumerate(maze):
            print("|", end="")
            for j, cell in enumerate(row):
                if [i, j] == start:
                    print("SS", end="")
                elif [i, j] == end:
                    print("EE", end="")
                elif cell == 1:
                    print("░░", end="")  # Light shade for walls
                elif cell == 2:
                    print("··", end="")  # Dots for solution path
                else:
                    print("  ", end="")  # Empty for open paths
            print("|")
            
        print("+" + "-" * (len(maze[0]) * 2) + "+\n")
        
        # Add legend for non-ANSI terminals
        print(" Legend:")
        print(" SS - Start point")
        print(" EE - End point")
        print(" ·· - Solution path")
        print(" ░░ - Wall")
        print("    - Open path (unvisited)\n")

if __name__ == "__main__":
    main()
