def manhattan_distance(a, b):
    """
    Calculate Manhattan distance between two points
    
    Args:
        a: First position [x, y]
        b: Second position [x, y]
        
    Returns:
        Manhattan distance (sum of absolute differences)
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
