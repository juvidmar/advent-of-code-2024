# Function for topological sort with preference
def topological_sort_with_preference(nodes, edges, preference_order):
    from collections import defaultdict

    # Build adjacency list and in-degree dictionary
    adj = defaultdict(list)
    in_degree = {node: 0 for node in nodes}

    for src, dst in edges:
        adj[src].append(dst)
        in_degree[dst] += 1

    # Map node to its position in the original order
    preference = {node: idx for idx, node in enumerate(preference_order)}

    # Nodes with zero in-degree, sorted by preference
    zero_in_degree = [node for node in nodes if in_degree[node] == 0]
    zero_in_degree.sort(key=lambda x: preference.get(x, float('inf')))

    sorted_list = []
    while zero_in_degree:
        node = zero_in_degree.pop(0)
        sorted_list.append(node)
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                zero_in_degree.append(neighbor)
                zero_in_degree.sort(key=lambda x: preference.get(x, float('inf')))
    if len(sorted_list) != len(nodes):
        # Cycle detected
        raise ValueError("Cycle detected in the graph")
    return sorted_list

# Main code
# Read the input from 'input.txt'
with open('input.txt', 'r') as f:
    lines = [line.strip() for line in f]

# Split the input into rules and updates
rules = []
updates = []
i = 0

# Read rules until an empty line is found
while i < len(lines) and lines[i]:
    rules.append(lines[i])
    i += 1

# Skip empty lines
while i < len(lines) and not lines[i]:
    i += 1

# Read updates
while i < len(lines):
    if lines[i]:
        updates.append(lines[i])
    i += 1

# Parse the rules into a list of tuples
ordering_rules = []
for rule in rules:
    x_str, y_str = rule.strip().split('|')
    x = int(x_str)
    y = int(y_str)
    ordering_rules.append((x, y))

# Parse the updates into lists of integers
update_sequences = []
for update in updates:
    pages = [int(page) for page in update.strip().split(',')]
    update_sequences.append(pages)

valid_updates = []
invalid_updates = []

# Identify valid and invalid updates
for pages in update_sequences:
    pages_in_update = set(pages)
    # Extract relevant ordering rules
    relevant_rules = [(x, y) for (x, y) in ordering_rules if x in pages_in_update and y in pages_in_update]
    # Create a mapping from page to its index in the sequence
    page_to_index = {page: idx for idx, page in enumerate(pages)}
    # Check if all relevant ordering rules are satisfied
    valid = True
    for (x, y) in relevant_rules:
        if page_to_index[x] >= page_to_index[y]:
            valid = False
            break
    if valid:
        # Update is correctly ordered
        valid_updates.append(pages)
    else:
        # Update is incorrectly ordered
        invalid_updates.append(pages)

# Process invalid updates
total = 0  # Sum of middle page numbers after reordering invalid updates

for pages in invalid_updates:
    pages_in_update = set(pages)
    # Extract relevant ordering rules
    relevant_rules = [(x, y) for (x, y) in ordering_rules if x in pages_in_update and y in pages_in_update]
    # Build the dependency graph
    nodes = pages_in_update
    edges = relevant_rules

    # Perform topological sort with preference
    try:
        sorted_pages = topological_sort_with_preference(nodes, edges, pages)
    except ValueError as e:
        print(f"Cycle detected in update with pages: {pages}")
        continue  # Skip this update if there's a cycle

    # Find the middle page
    mid_index = len(sorted_pages) // 2  # Integer division
    middle_page = sorted_pages[mid_index]
    total += middle_page

# Output the result
print(total)

