def turn_right(direction):
    # directions are (dr, dc)
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    i = directions.index(direction)
    return directions[(i + 1) % 4]

def read_map(filename):
    with open(filename, 'r') as f:
        grid = [list(line.rstrip('\n')) for line in f]
    return grid

def find_guard(grid):
    # Find guard symbol and direction
    dir_map = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] in dir_map:
                return (r, c, dir_map[grid[r][c]])
    return None

def is_inside(grid, r, c):
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])

def simulate(grid, extra_obstacle=None):
    # Find the guard initial position and direction
    start_r, start_c, direction = find_guard(grid)
    # Replace the guard symbol with '.' to simulate movement
    grid[start_r][start_c] = '.'

    # Set initial state
    r, c = start_r, start_c
    visited_states = set()
    state = (r, c, direction)
    visited_states.add(state)

    while True:
        # Next cell in front
        fr, fc = r + direction[0], c + direction[1]

        # Check if out of bounds => guard leaves map
        if not is_inside(grid, fr, fc):
            # Guard leaves the map
            return 'exit'

        # Within bounds, check if blocked
        if (fr, fc) == extra_obstacle:
            # This cell is blocked because we placed a new obstruction here
            blocked = True
        else:
            cell = grid[fr][fc]
            # '#' is an obstacle
            # '.' is free
            # We have already replaced the guard symbol, so no '^','v','<','>' in the grid now
            blocked = (cell == '#')

        if blocked:
            # turn right if blocked
            direction = turn_right(direction)
        else:
            # move forward
            r, c = fr, fc

        state = (r, c, direction)
        if state in visited_states:
            # Loop detected
            return 'loop'
        visited_states.add(state)

def main():
    grid = read_map("input.txt")

    start_r, start_c, start_dir = find_guard(grid)

    # For part two:
    # We want to know how many positions (currently '.') can become an obstruction to cause a loop.
    loop_count = 0
    rows = len(grid)
    cols = len(grid[0])

    # We'll copy the grid for each test since we modify it by replacing the guard symbol
    from copy import deepcopy

    # Find guard and direction once (for resetting between attempts)
    original_grid = deepcopy(grid)
    sr, sc, sdir = find_guard(original_grid)

    for r in range(rows):
        for c in range(cols):
            if (r, c) != (sr, sc) and original_grid[r][c] == '.':
                # Try placing an obstacle here
                # Make a fresh copy and simulate
                test_grid = deepcopy(original_grid)
                result = simulate(test_grid, extra_obstacle=(r, c))
                if result == 'loop':
                    loop_count += 1

    print(loop_count)

if __name__ == "__main__":
    main()
