def read_map(filename):
    """Reads the map from input.txt and returns it as a list of lists."""
    with open(filename, "r") as file:
        return [list(line.strip()) for line in file.readlines()]

def find_guard_position_and_direction(lab_map):
    """Finds the initial position and direction of the guard."""
    directions = {"^": (0, -1), ">": (1, 0), "v": (0, 1), "<": (-1, 0)}
    for y, row in enumerate(lab_map):
        for x, cell in enumerate(row):
            if cell in directions:
                return (x, y), directions[cell]
    raise ValueError("Guard not found on the map.")

def turn_right(direction):
    """Turns the direction 90 degrees to the right."""
    right_turns = {
        (0, -1): (1, 0),  # Up to Right
        (1, 0): (0, 1),   # Right to Down
        (0, 1): (-1, 0),  # Down to Left
        (-1, 0): (0, -1)  # Left to Up
    }
    return right_turns[direction]

def simulate_patrol(lab_map):
    """Simulates the guard's patrol and returns the number of distinct visited positions."""
    width, height = len(lab_map[0]), len(lab_map)
    visited = set()

    # Find initial guard position and direction
    guard_pos, direction = find_guard_position_and_direction(lab_map)
    visited.add(guard_pos)

    while True:
        x, y = guard_pos
        dx, dy = direction
        next_pos = (x + dx, y + dy)

        # Check if the guard will leave the map
        if not (0 <= next_pos[0] < width and 0 <= next_pos[1] < height):
            break

        # Check if the next position is an obstacle
        if lab_map[next_pos[1]][next_pos[0]] == "#":
            # Turn right
            direction = turn_right(direction)
        else:
            # Move forward
            guard_pos = next_pos
            visited.add(guard_pos)

    return len(visited)

def solve():
    # Read the lab map from input.txt
    lab_map = read_map("input.txt")

    # Simulate the guard's patrol
    result = simulate_patrol(lab_map)

    # Print the result
    print(f"Number of distinct positions visited: {result}")

if __name__ == "__main__":
    solve()
