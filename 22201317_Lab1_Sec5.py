import heapq
def load_data(file_path):
    with open(file_path, "r") as file:
        heuristic_map = {}
        graph_map = {}
        for line in file:
            parts = line.strip().split()
            node = parts[0]
            heuristic_map[node] = int(parts[1])
            neighbors = []
            for i in range(2, len(parts) - 1, 2):
                neighbors.append((parts[i], int(parts[i + 1])))
            graph_map[node] = neighbors
    print(graph_map)
    #print(heuristic_map)
    return graph_map, heuristic_map
class PathFinder:
    def __init__(self, graph_map, heuristic_map):
        self.graph = graph_map
        self.heuristic = heuristic_map
        self.visit = {}
    def heuristic_cost(self, node):
        return self.heuristic[node]
    def neighbors(self, node):
        return self.graph[node]
    def a_star(self, start_node, end_node):
        open_set = [(0, start_node)]
        parents_map = {}
        parents_map[start_node] = None
        cost_map = {node: float('inf') for node in self.graph}
        #print(cost_map)
        cost_map[start_node] = 0
        for node in self.graph:
            self.visit[node] = False  
        while open_set:
            current_cost, current_node = heapq.heappop(open_set)
            self.visit[current_node] = True
            if current_node == end_node:
                path = []
                while current_node:
                    path.append(current_node)
                    current_node = parents_map[current_node]
                path.reverse()
                return path, cost_map[end_node]
            for neighbor, travel_cost in self.neighbors(current_node):
                if not self.visit[neighbor]:  
                    new_cost = cost_map[current_node] + travel_cost
                    if new_cost < cost_map[neighbor]:
                        cost_map[neighbor] = new_cost
                        total_cost = new_cost + self.heuristic_cost(neighbor)
                        heapq.heappush(open_set, (total_cost, neighbor))
                        parents_map[neighbor] = current_node
        return None, 0  
def write_output(file_path, path, distance):
    with open(file_path, "w") as output_file:
        if path:
            output_file.write("Path: " + " -> ".join(path) + "\n")
            output_file.write(f"Total distance: {distance} km\n")
        else:
            output_file.write("NO PATH FOUND\n")
graph_data, heuristic_data = load_data("input.txt")
finder = PathFinder(graph_data, heuristic_data)
start = input("Enter start location: ")
goal = input("Enter destination: ")
path_result, total_distance = finder.a_star(start, goal)
write_output("output.txt", path_result, total_distance)