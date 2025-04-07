import random

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
    """Print the maze in a readable format"""
    for row in maze:
        print("".join(["#" if cell == 1 else " " for cell in row]))

if __name__ == "__main__":
    # Example usage
    maze = generate_maze(15, 15)
    print_maze(maze)
