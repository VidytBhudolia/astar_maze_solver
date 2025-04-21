import random
import colorama
from colorama import Fore, Back, Style

# Initialize colorama
colorama.init(autoreset=True)

def generate_maze(n, m, multiple_paths=True, wall_removal_probability=0.25):
    """Generate a maze with walls (1), paths (0)
    
    Args:
        n: Height of the maze
        m: Width of the maze
        multiple_paths: If True, creates multiple possible paths by randomly removing walls
        wall_removal_probability: Probability (0-1) of removing a wall to create alternative paths
    """
    # Create initial grid with all walls
    maze = [[1 for _ in range(m)] for _ in range(n)]
    
    # Carve paths using recursive backtracking
    _carve_passages(maze, 1, 1)
    
    # Ensure start and end are open
    maze[1][1] = 0  # Start point
    maze[n-2][m-2] = 0  # End point
    
    # Randomly remove additional walls to create multiple paths
    if multiple_paths:
        # First pass: Remove walls that connect path segments
        for i in range(2, n-2):
            for j in range(2, m-2):
                if maze[i][j] == 1:  # If it's a wall
                    # Check if it has path cells on opposite sides (horizontally or vertically)
                    horizontal_path = (maze[i][j-1] == 0 and maze[i][j+1] == 0)
                    vertical_path = (maze[i-1][j] == 0 and maze[i+1][j] == 0)
                    diagonal_path = (maze[i-1][j-1] == 0 and maze[i+1][j+1] == 0) or (maze[i-1][j+1] == 0 and maze[i+1][j-1] == 0)
                    
                    # Higher chance of removal if it would connect existing paths
                    if horizontal_path or vertical_path:
                        if random.random() < wall_removal_probability * 1.5:  # Higher probability for good candidates
                            maze[i][j] = 0  # Remove wall
                    # Consider diagonal path connections with lower probability
                    elif diagonal_path and random.random() < wall_removal_probability * 0.7:
                        maze[i][j] = 0
                    # Sometimes remove random walls to create diverse path options
                    elif random.random() < wall_removal_probability * 0.4:
                        maze[i][j] = 0
        
        # Second pass: Create some wider corridors by removing adjacent walls
        for i in range(2, n-2):
            for j in range(2, m-2):
                if maze[i][j] == 0:  # If it's a path
                    # Randomly widen corridors by removing adjacent walls
                    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        nx, ny = i + dx, j + dy
                        if (0 < nx < n-1 and 0 < ny < m-1 and 
                            maze[nx][ny] == 1 and random.random() < wall_removal_probability * 0.3):
                            maze[nx][ny] = 0  # Remove additional adjacent wall
    
    return maze

def _carve_passages(maze, cx, cy):
    """Recursively carve passages through the maze"""
    directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
    random.shuffle(directions)
    
    for dx, dy in directions:
        nx, ny = cx + dx, cy + dy
        if 0 < nx < len(maze)-1 and 0 < ny < len(maze[0])-1 and maze[nx][ny] == 1:
            maze[nx][ny] = 0
            maze[cx + dx//2][cy + dy//2] = 0
            _carve_passages(maze, nx, ny)

def print_maze(maze):
    """
    Print the maze with colored formatting:
    - White for walls
    - Blue for path
    - Green for start
    - Red for end
    """
    start_pos = (1, 1)
    end_pos = (len(maze)-2, len(maze[0])-2)
    
    for i, row in enumerate(maze):
        line = ""
        for j, cell in enumerate(row):
            if (i, j) == start_pos:
                line += Back.GREEN + '  ' + Style.RESET_ALL
            elif (i, j) == end_pos:
                line += Back.RED + '  ' + Style.RESET_ALL
            elif cell == 1:
                line += Back.WHITE + '  ' + Style.RESET_ALL
            elif cell == 2:
                line += Back.BLUE + '  ' + Style.RESET_ALL
            else:
                line += '  '
        print(line)

if __name__ == "__main__":
    # Example usage
    maze = generate_maze(15, 15)
    print_maze(maze)
