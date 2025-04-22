"""Simple Travelling Salesperson Problem (TSP) between cities."""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def parse_graph(filename):
    """Parses the adjacency list and creates a distance matrix."""
    # Read graph
    graph = {}
    with open(filename, "r") as f:
        for line in f:
            parts = line.strip().split(":")
            node = int(parts[0]) # Convert to 0-based index
            neighbors = list(map(lambda x: int(x), parts[1].split()))
            graph[node] = neighbors

    size = len(graph)
    distance_matrix = [[100000] * size for _ in range(size)]

    for i in range(size):
        distance_matrix[i][i] = 0  # Distance to self is 0
        for j in graph[i]:
            distance_matrix[i][j] = 1  # Distance to neighbor is 1

    return distance_matrix


def create_data_model(filename):
    """Stores the data for the problem."""
    data = {}
    data["distance_matrix"] = parse_graph(filename)
    data["num_vehicles"] = 1
    data["depot"] = 0
    return data


def print_solution(manager, routing, solution):
    """Prints solution on console."""
    print(f"Objective: {solution.ObjectiveValue()} miles")
    index = routing.Start(0)
    plan_output = "Route for vehicle 0:\n"
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += f" {manager.IndexToNode(index)} ->"
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += f" {manager.IndexToNode(index)}\n"
    plan_output += f"Route distance: {route_distance}miles\n"
    print(plan_output)


def main():
    """Entry point of the program."""
    # Instantiate the data problem.
    filename = "/Users/jakubsmihula/PycharmProjects/hamiltonicity-of-cages/Graphs/Record/3 - 18.lst"
    data = create_data_model(filename)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]), data["num_vehicles"], data["depot"]
    )

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data["distance_matrix"][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.seconds = 100000
    search_parameters.log_search = True

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(manager, routing, solution)


if __name__ == "__main__":
    main()