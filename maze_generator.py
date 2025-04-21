import random
import colorama
from colorama import Fore, Back, Style

# Initialize colorama
colorama.init(autoreset=True)

def generate_maze(n, m):
    """Generate a maze with walls (1), paths (0)"""
    # Create initial grid with all walls
    maze = [[1 for _ in range(m)] for _ in range(n)]
    
    # Carve paths using recursive backtracking
    _carve_passages(maze, 1, 1)
    
    # Ensure start and end are open
    maze[1][1] = 0  # Start point
    maze[n-2][m-2] = 0  # End point
    
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
