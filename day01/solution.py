from collections import Counter

def solve():
    # Read the input file
    with open("input.txt") as file:
        lines = file.readlines()
    
    # Parse the two lists
    left_list = []
    right_list = []
    for line in lines:
        left, right = map(int, line.split())
        left_list.append(left)
        right_list.append(right)
    
    # Count occurrences in the right list
    right_count = Counter(right_list)
    
    # Calculate the similarity score
    similarity_score = 0
    for num in left_list:
        similarity_score += num * right_count.get(num, 0)
    
    # Print the result
    print(f"Similarity score: {similarity_score}")

if __name__ == "__main__":
    solve()


