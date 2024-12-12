from collections import defaultdict, deque

def read_input(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def get_neighbors(x, y, rows, cols):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols:
            yield nx, ny

def bfs(map_data, visited, x, y):
    plant_type = map_data[x][y]
    rows, cols = len(map_data), len(map_data[0])
    queue = deque([(x, y)])
    visited.add((x, y))

    area = 0
    perimeter = 0

    while queue:
        cx, cy = queue.popleft()
        area += 1
        local_perimeter = 4

        for nx, ny in get_neighbors(cx, cy, rows, cols):
            if map_data[nx][ny] == plant_type:
                local_perimeter -= 1
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny))

        perimeter += local_perimeter

    return area, perimeter

def calculate_total_price(map_data):
    visited = set()
    total_price = 0

    for x in range(len(map_data)):
        for y in range(len(map_data[0])):
            if (x, y) not in visited:
                area, perimeter = bfs(map_data, visited, x, y)
                total_price += area * perimeter

    return total_price

if __name__ == "__main__":
    input_file = "input.txt"
    map_data = read_input(input_file)
    total_price = calculate_total_price(map_data)
    print(f"Total price of fencing all regions: {total_price}")
