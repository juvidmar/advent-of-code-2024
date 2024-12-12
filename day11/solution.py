from collections import Counter

def read_initial_stones(filename):
    """
    Reads the initial arrangement of stones from the given filename.
    Assumes that numbers are separated by whitespace.
    """
    with open(filename, 'r') as file:
        content = file.read()
        # Split by any whitespace and convert to integers
        stones = list(map(int, content.split()))
    return stones

def split_number(n):
    """
    Splits a number with an even number of digits into two halves.
    Leading zeros in the second half are removed by converting to int.
    """
    s = str(n)
    mid = len(s) // 2
    left = int(s[:mid]) if s[:mid] else 0
    right = int(s[mid:]) if s[mid:] else 0
    return left, right

def simulate_blinks(initial_stones, total_blinks):
    """
    Simulates the transformation of stones over a given number of blinks.
    Uses a Counter to efficiently track the frequency of each unique stone number.
    """
    # Initialize the Counter with the initial stones
    stone_counts = Counter(initial_stones)
    
    for blink in range(1, total_blinks + 1):
        new_stone_counts = Counter()
        for stone, count in stone_counts.items():
            if stone == 0:
                # Rule 1: Replace 0 with 1
                new_stone_counts[1] += count
            elif len(str(stone)) % 2 == 0:
                # Rule 2: Split the number into two halves
                left, right = split_number(stone)
                new_stone_counts[left] += count
                new_stone_counts[right] += count
            else:
                # Rule 3: Multiply the number by 2024
                multiplied = stone * 2024
                new_stone_counts[multiplied] += count
        stone_counts = new_stone_counts
        # Optional: Uncomment the following line to monitor progress
        # print(f"After blink {blink}: {sum(stone_counts.values())} stones")
    
    return sum(stone_counts.values())

def main():
    """
    Main function to execute the program.
    Reads the grid, computes the sum of trailhead ratings, and prints the result.
    """
    initial_stones = read_initial_stones('input.txt')
    total_blinks = 75
    final_stone_count = simulate_blinks(initial_stones, total_blinks)
    print(final_stone_count)

if __name__ == "__main__":
    main()
