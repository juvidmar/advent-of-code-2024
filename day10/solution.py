from functools import lru_cache

def read_grid(filename):
    """
    Reads the topographic map from the given filename.
    Each line in the file represents a row in the grid.
    Each character in the line represents the height at that position.
    """
    with open(filename, 'r') as f:
        grid = [list(map(int, line.strip())) for line in f if line.strip()]
    return grid

def find_trailheads_and_nines(grid):
    """
    Identifies all trailheads (positions with height 0) and nines (positions with height 9).
    Returns two lists: trailheads and nines.
    """
    trailheads = []
    nines = set()
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == 0:
                trailheads.append((r, c))
            if val == 9:
                nines.add((r, c))
    return trailheads, nines

def compute_trailhead_ratings(grid):
    """
    Computes the sum of ratings for all trailheads.
    A trailhead's rating is the number of distinct hiking trails starting from it.
    """
    trailheads, nines = find_trailheads_and_nines(grid)
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    directions = [(-1,0), (1,0), (0,-1), (0,1)]  # up, down, left, right

    @lru_cache(maxsize=None)
    def count_paths(r, c):
        """
        Returns the number of distinct paths from position (r, c) to any position with height 9.
        Utilizes memoization to cache results for efficiency.
        """
        current_height = grid[r][c]
        
        # Base case: if current position is height 9, there's exactly one path (the trail itself)
        if current_height == 9:
            return 1
        
        total = 0
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            # Check if neighbor is within bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbor_height = grid[nr][nc]
                # Move only to positions with height exactly 1 greater
                if neighbor_height == current_height + 1:
                    total += count_paths(nr, nc)
        return total

    total_rating = 0
    for trailhead in trailheads:
        r, c = trailhead
        paths = count_paths(r, c)
        total_rating += paths

    return total_rating

def main():
    """
    Main function to execute the program.
    Reads the grid, computes the sum of trailhead ratings, and prints the result.
    """
    grid = read_grid('input.txt')
    total_rating = compute_trailhead_ratings(grid)
    print(total_rating)

if __name__ == "__main__":
    main()
