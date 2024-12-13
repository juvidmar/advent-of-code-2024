import sys
import re

def parse_machine(block):
    """
    Parses a single machine block and returns A_x, A_y, B_x, B_y, P_x, P_y
    """
    lines = block.strip().split('\n')
    A_x = A_y = B_x = B_y = P_x = P_y = None
    for line in lines:
        if line.startswith("Button A:"):
            # Example: "Button A: X+94, Y+34"
            matches = re.findall(r'X\+(\d+), Y\+(\d+)', line)
            if matches:
                A_x, A_y = map(int, matches[0])
        elif line.startswith("Button B:"):
            # Example: "Button B: X+22, Y+67"
            matches = re.findall(r'X\+(\d+), Y\+(\d+)', line)
            if matches:
                B_x, B_y = map(int, matches[0])
        elif line.startswith("Prize:"):
            # Example: "Prize: X=8400, Y=5400"
            matches = re.findall(r'X=(\d+), Y=(\d+)', line)
            if matches:
                P_x, P_y = map(int, matches[0])
    return A_x, A_y, B_x, B_y, P_x, P_y

def find_min_cost(A_x, A_y, B_x, B_y, Q_x, Q_y):
    """
    Finds the minimum token cost to reach (Q_x, Q_y) using buttons A and B.
    Returns the minimum cost if possible, otherwise returns None.
    """
    D = A_x * B_y - A_y * B_x
    if D == 0:
        # Check if the system has infinitely many solutions
        if (Q_x * B_y != Q_y * B_x):
            return None  # No solution
        # Find non-negative integer solutions to A_x * a + B_x * b = Q_x
        # Minimize 3a + b
        # This is equivalent to minimizing a and b such that A_x * a + B_x * b = Q_x
        # To minimize 3a + b, prioritize minimizing 'a' if 3a grows faster
        # Find a particular solution and parameterize
        # Since D == 0 and Q_x * B_y == Q_y * B_x, solutions exist
        # We can express a in terms of b or vice versa
        # Let's iterate over possible a within a feasible range to find the minimal cost
        # Given the large Q_x, we need an efficient method
        # We'll use the Extended Euclidean Algorithm to find a particular solution
        
        # Find gcd(A_x, B_x)
        from math import gcd
        g = gcd(A_x, B_x)
        if Q_x % g != 0:
            return None  # No solution
        
        # Simplify the equation
        A_x_s = A_x // g
        B_x_s = B_x // g
        Q_x_s = Q_x // g
        
        # Find one solution using the Extended Euclidean Algorithm
        def extended_gcd(a, b):
            if b == 0:
                return a, 1, 0
            else:
                g, x, y = extended_gcd(b, a % b)
                return g, y, x - (a // b) * y
        
        _, x0, y0 = extended_gcd(A_x_s, B_x_s)
        a_particular = x0 * Q_x_s
        b_particular = y0 * Q_x_s
        
        # The general solutions are:
        # a = a_particular + k * (B_x_s)
        # b = b_particular - k * (A_x_s)
        # We need a >=0 and b >=0
        # Find the range of k that satisfies these constraints
        k_min = (-a_particular) // B_x_s
        k_max = b_particular // A_x_s
        
        # Adjust k_min and k_max to cover all possible k
        k_min = max(k_min, 0)
        k_max = k_max
        
        if k_min > k_max:
            return None  # No non-negative solutions
        
        # Iterate through possible k values to find the minimal cost
        min_cost = float('inf')
        for k in range(k_min, k_max + 1):
            a = a_particular + k * B_x_s
            b = b_particular - k * A_x_s
            if a < 0 or b < 0:
                continue
            cost = 3 * a + b
            if cost < min_cost:
                min_cost = cost
        return min_cost if min_cost != float('inf') else None
    else:
        a_num = Q_x * B_y - Q_y * B_x
        b_num = A_x * Q_y - A_y * Q_x

        if D < 0:
            a_num = -a_num
            b_num = -b_num
            D = -D

        if a_num % D != 0 or b_num % D != 0:
            return None  # No integer solution

        a = a_num // D
        b = b_num // D

        if a < 0 or b < 0:
            return None  # Negative solutions are invalid

        return 3 * a + b

def main_part_two():
    input_data = sys.stdin.read()
    # Split the input into blocks separated by two or more newlines
    blocks = re.split(r'\n\s*\n', input_data.strip())
    total_tokens = 0
    for block in blocks:
        A_x, A_y, B_x, B_y, P_x, P_y = parse_machine(block)
        if None in [A_x, A_y, B_x, B_y, P_x, P_y]:
            continue  # Skip incomplete machine data
        # Adjust prize positions by adding 10^13 to both X and Y
        Q_x = P_x + 10**13
        Q_y = P_y + 10**13
        min_cost = find_min_cost(A_x, A_y, B_x, B_y, Q_x, Q_y)
        if min_cost is not None:
            total_tokens += min_cost
    print(total_tokens)

if __name__ == "__main__":
    main_part_two()
