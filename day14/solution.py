import re

def parse_input(file_path):
    """
    Parses the input file and extracts robot positions and velocities.

    Args:
        file_path (str): Path to the input file.

    Returns:
        list of tuples: Each tuple contains (x, y, vx, vy) for a robot.
    """
    robots = []
    # Regular expression to extract integers from the input lines
    pattern = re.compile(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")
    with open(file_path, 'r') as f:
        for line in f:
            match = pattern.search(line)
            if match:
                x, y, vx, vy = map(int, match.groups())
                robots.append((x, y, vx, vy))
    return robots

def compute_position(robot, t, width, height):
    """
    Computes the new position of a robot after t seconds with wrapping.

    Args:
        robot (tuple): A tuple containing (x, y, vx, vy) of the robot.
        t (int): Time in seconds.
        width (int): Width of the grid (for wrapping).
        height (int): Height of the grid (for wrapping).

    Returns:
        tuple: New position (new_x, new_y) of the robot.
    """
    x, y, vx, vy = robot
    new_x = (x + vx * t) % width
    new_y = (y + vy * t) % height
    return (new_x, new_y)

def determine_quadrant(pos, center_x, center_y):
    """
    Determines which quadrant a position belongs to.

    Args:
        pos (tuple): A tuple containing (x, y) position of the robot.
        center_x (int): The x-coordinate of the central vertical line.
        center_y (int): The y-coordinate of the central horizontal line.

    Returns:
        int: Quadrant number (1, 2, 3, 4) or 0 if excluded.
    """
    x, y = pos
    if x < center_x and y < center_y:
        return 1  # Q1
    elif x > center_x and y < center_y:
        return 2  # Q2
    elif x < center_x and y > center_y:
        return 3  # Q3
    elif x > center_x and y > center_y:
        return 4  # Q4
    else:
        return 0  # Excluded (on central lines)

def calculate_safety_factor(robots, t, width, height):
    """
    Calculates the safety factor after t seconds.

    Args:
        robots (list of tuples): List containing (x, y, vx, vy) for each robot.
        t (int): Time in seconds.
        width (int): Width of the grid (for wrapping).
        height (int): Height of the grid (for wrapping).

    Returns:
        int: The safety factor.
    """
    center_x = width // 2
    center_y = height // 2
    quadrant_counts = {1:0, 2:0, 3:0, 4:0}

    for robot in robots:
        pos = compute_position(robot, t, width, height)
        quadrant = determine_quadrant(pos, center_x, center_y)
        if quadrant != 0:
            quadrant_counts[quadrant] += 1

    # Calculate safety factor by multiplying quadrant counts
    safety_factor = 1
    for q in range(1,5):
        safety_factor *= quadrant_counts[q]

    return safety_factor

def main():
    # Define grid size based on problem statement
    width = 101   # x ranges from 0 to 100
    height = 103  # y ranges from 0 to 102

    # Time after which to calculate safety factor
    t = 100

    # Parse the input file
    robots = parse_input('input.txt')

    if not robots:
        print("No robots found in the input.")
        return

    # Calculate the safety factor
    safety_factor = calculate_safety_factor(robots, t, width, height)

    # Output the result
    print(safety_factor)

if __name__ == "__main__":
    main()
