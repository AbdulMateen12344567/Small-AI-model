Emergency Response Pathfinding with Dijkstra's Algorithm

This project aims to determine the optimal path for sending help from two fire stations to an emergency site in a city grid layout, where paths may be open or blocked over time. The solution uses Dijkstra's Algorithm, which finds the shortest path considering open roads and varying speeds at specific times.
Project Overview

The city grid is composed of sites linked in a grid format, with multiple emergency sites and two fire stations. At any given time, some paths between sites may be blocked or open, and emergency sites need immediate help. The task is to find the shortest path from the fire stations to the emergency site based on available paths and their statuses.
Data Files

The project uses two Excel files for data input:

    data.xlsx: Contains road segments, their current status (open/closed), speed, and time intervals. The road data represents connectivity between nodes, and the status determines if the road is passable at any given time.

    emergencySiteData.xlsx: Contains information about emergency sites, including their coordinates and the time at which help is required.

Requirements

    Python 3.x
    pandas
    datetime
    heapq (for priority queue functionality)

Installation

    Clone this repository or download the files.

    Install the required dependencies using pip:

    pip install pandas

    Download or place the data.xlsx and emergencySiteData.xlsx files in the project directory.

Approach
Step 1: Data Observation

The first step is to observe the structure of the Excel sheets. In the emergencySiteData.xlsx, the data is straightforward. However, in the data.xlsx file, the road segments are listed with only one direction (from a,b to x,y). The reverse path (from x,y to a,b) is not present, so the algorithm must account for this.
Step 2: Retrieving and Storing Data

The data from the Excel files is loaded and stored in Python lists. This enables efficient processing during the algorithm's execution.

import pandas as pd
import datetime
import heapq

file_path_1 = 'data.xlsx'
file_path_2 = 'emergencySiteData.xlsx'

data_1 = pd.read_excel(file_path_1)
data_2 = pd.read_excel(file_path_2)

columns_1 = ['Road Segment Start', 'Road Segment End', 'Status', 'Current Speed (km/h)', 'Time']
selected_data_1 = data_1[columns_1]
data_list_1 = selected_data_1.values.tolist()

columns_2 = ['Emergency Site', 'Coordinates', 'Time']
selected_data_2 = data_2[columns_2]
data_list_2 = selected_data_2.values.tolist()

Step 3: Algorithm Implementation
3.1: Pathfinding (Neighbors)

We define a function get_neighbors() that returns the open neighboring sites at a given time. It checks if the road is open and accessible at the specified time.

def get_neighbors(current_node, time, data_list):
    neighbors = []
    for road in data_list:
        start, end, status, speed, road_time = road
        if start == current_node:
            if isinstance(road_time, datetime.time):
                if road_time == time and status == 'Open':
                    neighbors.append((end, speed))
        elif end == current_node:
            if isinstance(road_time, datetime.time):
                if road_time == time and status == 'Open':
                    neighbors.append((start, speed))
    return neighbors

3.2: Dijkstra's Algorithm

The dijkstra() function implements the core of the algorithm. It finds the shortest path from a start point (fire station) to the target (emergency site) while considering road statuses and times.

def dijkstra(start, target, time, data_list):
    frontier = []
    heapq.heappush(frontier, (datetime.timedelta(0), start))
    explored = set()
    times = {start: datetime.timedelta(0)}
    paths = {start: [start]}
    
    while frontier:
        current_time, current_node = heapq.heappop(frontier)
        if current_node == target:
            return current_time, paths[current_node]

        neighbors = get_neighbors(current_node, time, data_list)
        for neighbor, speed in neighbors:
            if neighbor not in explored:
                travel_time = datetime.timedelta(hours=1) / speed
                new_time = current_time + travel_time
                
                if neighbor not in times or new_time < times[neighbor]:
                    times[neighbor] = new_time
                    paths[neighbor] = paths[current_node] + [neighbor]
                    heapq.heappush(frontier, (new_time, neighbor))
                explored.add(current_node)
    return None, None

3.3: Comparing Paths from Both Fire Stations

The findPath() function determines the shortest path to the emergency site from both fire stations. It compares the times and returns the optimal path.

def findPath(data_list, emergency_site):
    start1 = '(1, 1)'
    start2 = '(10, 10)'
    target = emergency_site[1]
    time = emergency_site[2]

    print(f"Starting search for paths from {start1} and {start2} to {target} at {time}")
    
    time_from_start1, path_from_start1 = dijkstra(start1, target, time, data_list)
    time_from_start2, path_from_start2 = dijkstra(start2, target, time, data_list)
    print("the time from (1,1) is", time_from_start1)
    print("the time from (10,10) is", time_from_start2)
    
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

Step 4: Output

The output will show the optimal path from either of the fire stations to the emergency site, including the travel time.
Example

When you call findPath() with the data list and emergency site information, the system will calculate and print the shortest path from both fire stations to the emergency site and return the optimal path along with the time taken.

findPath(data_list_1, emergency_site_data)

Conclusion

This algorithm helps optimize response times by calculating the shortest paths considering road status and time. It provides an efficient way for emergency teams to reach critical locations in a city grid layout.
