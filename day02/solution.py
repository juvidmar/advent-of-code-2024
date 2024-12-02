from collections import Counter

def is_safe(report):
    # Calculate differences between adjacent levels
    differences = [report[i + 1] - report[i] for i in range(len(report) - 1)]
    
    # Check if all differences are positive (increasing) and within [1, 3]
    is_increasing = all(1 <= diff <= 3 for diff in differences)
    
    # Check if all differences are negative (decreasing) and within [-3, -1]
    is_decreasing = all(-3 <= diff <= -1 for diff in differences)
    
    # Return True if either increasing or decreasing
    return is_increasing or is_decreasing

def can_be_safe_with_removal(report):
    # If already safe, no need to remove anything
    if is_safe(report):
        return True
    
    # Try removing one level at a time
    for i in range(len(report)):
        modified_report = report[:i] + report[i+1:]
        if is_safe(modified_report):
            return True
    
    # If no single removal makes it safe, return False
    return False

def solve():
    # Read input from file
    with open("input.txt") as file:
        reports = [list(map(int, line.split())) for line in file.readlines()]
    
    # Count the number of safe reports (with or without the Problem Dampener)
    safe_count = sum(1 for report in reports if can_be_safe_with_removal(report))
    
    # Print the result
    print(f"Number of safe reports with Problem Dampener: {safe_count}")

if __name__ == "__main__":
    solve()

