# Read the grid from 'input.txt'
with open('input.txt', 'r') as file:
    grid_str = [line.strip() for line in file if line.strip()]

# Convert the grid into a 2D list
grid = [list(row) for row in grid_str]
n = len(grid)
m = len(grid[0]) if n > 0 else 0

# Initialize the count of X-MAS patterns
count = 0

# Define the valid patterns for diagonals
valid_patterns = [('M', 'A', 'S'), ('S', 'A', 'M')]

# Iterate over the grid, excluding the borders to prevent index errors
for i in range(1, n - 1):
    for j in range(1, m - 1):
        # Check if the center is 'A'
        if grid[i][j] == 'A':
            # Check Diagonal 1 (top-left to bottom-right)
            diag1 = (grid[i - 1][j - 1], grid[i][j], grid[i + 1][j + 1])
            diag1_rev = diag1[::-1]
            diag1_ok = diag1 in valid_patterns or diag1_rev in valid_patterns

            # Check Diagonal 2 (top-right to bottom-left)
            diag2 = (grid[i - 1][j + 1], grid[i][j], grid[i + 1][j - 1])
            diag2_rev = diag2[::-1]
            diag2_ok = diag2 in valid_patterns or diag2_rev in valid_patterns

            # If both diagonals are valid, increment the count
            if diag1_ok and diag2_ok:
                count += 1

# Output the result
print("Number of X-MAS patterns:", count)
