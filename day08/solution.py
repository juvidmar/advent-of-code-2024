from math import gcd

def main():
    # Read the input
    with open("input.txt", "r") as f:
        grid = [line.rstrip("\n") for line in f]

    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Collect antenna positions by frequency
    antenna_positions = {}
    for y in range(rows):
        for x in range(cols):
            c = grid[y][x]
            if c != '.':
                if c not in antenna_positions:
                    antenna_positions[c] = []
                antenna_positions[c].append((y, x))

    # We need to find all points that are collinear with at least two antennas
    # of the same frequency. The updated model states:
    # "an antinode occurs at any grid position exactly in line with at least
    # two antennas of the same frequency, regardless of distance."
    #
    # This means:
    # 1) For each frequency, consider all pairs of antennas.
    # 2) Each pair of antennas defines a line. Every integer point in the grid 
    #    that lies on this line is an antinode for this frequency.
    #
    # To find points on the line defined by (y1, x1) and (y2, x2):
    # Let's form the line in standard form: A*x + B*y + C = 0
    # Given two points:
    #   A = y2 - y1
    #   B = x1 - x2
    #   C = x2*y1 - x1*y2
    # We do not need to worry about uniqueness because we will store all found points in a set.
    #
    # After generating all lines, we will check all points in the grid if they satisfy A*x + B*y + C = 0.
    # That would be O((R*C)*number_of_pairs), potentially large.
    #
    # But there's a potentially huge complexity problem if the grid is large.
    # Since the problem context is from a puzzle setting, let's assume the input is manageable.
    #
    # Optimization:
    # Instead of checking every grid cell against every line (which could be huge),
    # we can generate all points on the line by stepping from one antenna to the edges of the grid.
    #
    # Actually, we can do this:
    # A line passing through (y1, x1) and (y2, x2) can be represented by a direction vector (dy, dx) = (y2-y1, x2-x1).
    # Reduce (dy, dx) by their gcd to get the step: (sdy, sdx)
    # From one of the antennas, say (y1, x1), we move in both directions along (sdy, sdx) and (−sdy, -sdx)
    # until we go out of bounds. We add all points encountered.
    #
    # This way, we do not check the entire grid. We just walk along the line in both directions until we leave the grid.
    #
    # Steps:
    # For each frequency:
    #   For each pair of antennas:
    #       Compute sdy, sdx = direction vector reduced by gcd.
    #       From antenna A:
    #         Move forward in direction (sdy, sdx) until out of bounds. Add all points.
    #         Move backward in direction (-sdy, -sdx) until out of bounds. Add all points.
    #   All these points form antinodes for that frequency.
    # Then combine antinodes from all frequencies.
    #
    # This avoids O(R*C) checks and should be efficient enough.

    antinode_set = set()
    for freq, positions in antenna_positions.items():
        if len(positions) < 2:
            # No lines from a single antenna
            continue

        # For each pair of antennas in this frequency
        n = len(positions)
        for i in range(n):
            for j in range(i+1, n):
                y1, x1 = positions[i]
                y2, x2 = positions[j]

                dy = y2 - y1
                dx = x2 - x1
                g = gcd(dy, dx)
                dy //= g
                dx //= g

                # Move along the line starting from antenna 1 (y1,x1)
                # Forward direction
                yy, xx = y1, x1
                while 0 <= yy < rows and 0 <= xx < cols:
                    antinode_set.add((yy, xx))
                    yy += dy
                    xx += dx
                # Backward direction
                yy, xx = y1, x1
                while 0 <= yy < rows and 0 <= xx < cols:
                    antinode_set.add((yy, xx))
                    yy -= dy
                    xx -= dx

                # Move along the line starting from antenna 2 (y2,x2), since the line might not be fully covered yet.
                # However, note that we already covered the whole line in both directions from (y1, x1).
                # Starting from both antennas would cause double coverage. 
                # Actually, not needed, because from one antenna we already went forward and backward to cover everything.
                # No point on the line is left out since we covered it fully in both directions.
                #
                # If we wanted to be absolutely sure, we could omit this step because the line is infinite and we've already
                # covered it fully (the entire grid line is covered when we go both ways from one point on that line).

    # Now antinode_set contains all antinodes from all frequencies
    print(len(antinode_set))

if __name__ == "__main__":
    main()
