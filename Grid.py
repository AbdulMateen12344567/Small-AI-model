import pandas as pd
import datetime
import heapq  # Using heapq for priority queue functionality

# Load the Excel files
file_path_1 = 'data.xlsx'
file_path_2 = 'emergencySiteData.xlsx'

data_1 = pd.read_excel(file_path_1)
data_2 = pd.read_excel(file_path_2)

# Select the required columns for roads
columns_1 = ['Road Segment Start', 'Road Segment End', 'Status', 'Current Speed (km/h)', 'Time']
selected_data_1 = data_1[columns_1]
data_list_1 = selected_data_1.values.tolist()

# Select the required columns for emergency sites
columns_2 = ['Emergency Site', 'Coordinates', 'Time']
selected_data_2 = data_2[columns_2]
data_list_2 = selected_data_2.values.tolist()

# Function to get valid neighbors for a given current node and time
def get_neighbors(current_node, time, data_list):
    neighbors = []
    for road in data_list:
        start, end, status, speed, road_time = road
        if start == current_node:
            if isinstance(road_time, datetime.time):
                # Check if the road is open at the given time
                if road_time == time and status == 'Open':
                    neighbors.append((end, speed))
        elif end == current_node:
            if isinstance(road_time, datetime.time):
                # Check if the road is open at the given time
                if road_time == time and status == 'Open':
                    neighbors.append((start, speed))
    return neighbors
# Dijkstra's algorithm to find the shortest path using priority queue
def dijkstra(start, target, time, data_list):
    # Min-heap for the priority queue: stores (cumulative_time, current_node)
    frontier = []
    heapq.heappush(frontier, (datetime.timedelta(0), start))  # Start with 0 time and the initial node
    explored = set()
    times = {start: datetime.timedelta(0)}  # Starting time is 0
    paths = {start: [start]}  # Path taken to reach each node
    
    while frontier:
        current_time, current_node = heapq.heappop(frontier)
        if current_node == target:
            return current_time, paths[current_node]

        neighbors = get_neighbors(current_node, time, data_list)
        for neighbor, speed in neighbors:
            if neighbor not in explored:
                travel_time = datetime.timedelta(hours=1) / speed  # Time taken to travel 1 km
                new_time = current_time + travel_time
                
                if neighbor not in times or new_time < times[neighbor]:
                    times[neighbor] = new_time
                    paths[neighbor] = paths[current_node] + [neighbor]
                    heapq.heappush(frontier, (new_time, neighbor))  # Push to the frontier
                explored.add(current_node)
    return None, None  # Return None if no path found
# Function to find the optimal path from both fire stations to the emergency site
def findPath(data_list, emergency_site):
    start1 = '(1, 1)'
    start2 = '(10, 10)'
    target = emergency_site[1]
    time = emergency_site[2]

    print(f"Starting search for paths from {start1} and {start2} to {target} at {time}")
    
    # Find the path from the first fire station (1, 1) to the emergency site
    time_from_start1, path_from_start1 = dijkstra(start1, target, time, data_list)
    # Find the path from the second fire station (10, 10) to the emergency site
    time_from_start2, path_from_start2 = dijkstra(start2, target, time, data_list)
    print("the time from (1,1) is", time_from_start1)
    print("the time from (10,10) is", time_from_start2)
    # Determine the shortest path and time
    if time_from_start1 and time_from_start2:
        if time_from_start1 < time_from_start2:
            return time_from_start1, path_from_start1
        else:
            return time_from_start2, path_from_start2
    elif time_from_start1:
        return time_from_start1, path_from_start1
    elif time_from_start2:
        return time_from_start2, path_from_start2
    else:
        return "No path available", None

# Test the function with the first emergency site
print("|----------The emergency Sites-----------|")
i=0
for site,Coordinate,time in data_list_2:
    print(f"{i}: Emergency site: {site}, Coordinates: {Coordinate}, Time: {time}")
    i=i+1
E_site=int(input("Enter the emergency site: "))
emergency_site = data_list_2[E_site]
result = findPath(data_list_1, emergency_site)

if result != "No path available":
    time_taken, path = result
    print(f"Shortest time: {time_taken}, Path: {path}")
else:
    print("No path available")
