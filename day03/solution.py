import re

def solve():
    # Read input from file
    with open("input.txt") as file:
        memory = file.read().strip()
    
    # Define regex patterns
    mul_pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    do_pattern = r"do\(\)"
    dont_pattern = r"don't\(\)"
    
    # Combine patterns to extract all instructions in order
    combined_pattern = f"{mul_pattern}|{do_pattern}|{dont_pattern}"
    
    # Find all matches
    matches = re.finditer(combined_pattern, memory)
    
    # Track whether mul instructions are enabled
    enabled = True
    total = 0
    
    # Process each match
    for match in matches:
        if match.group(1) and match.group(2):  # This is a mul(X,Y) instruction
            x, y = int(match.group(1)), int(match.group(2))
            if enabled:
                total += x * y
        elif match.group(0) == "do()":  # This is a do() instruction
            enabled = True
        elif match.group(0) == "don't()":  # This is a don't() instruction
            enabled = False
    
    # Print the result
    print(f"Total sum of enabled multiplications: {total}")

if __name__ == "__main__":
    solve()
