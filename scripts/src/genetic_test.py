import random
import numpy as np


# Fitness function: calculates the length of the Hamiltonian cycle
def fitness(individual, graph):
    total_cost = 0
    for i in range(len(individual) - 1):
        total_cost += graph[individual[i]][individual[i + 1]]
    total_cost += graph[individual[-1]][individual[0]]  # Return to the start
    return total_cost


# Create a random individual (Hamiltonian cycle) as a permutation of nodes
def create_individual(num_nodes):
    return random.sample(range(num_nodes), num_nodes)


# Crossover function (Ordered Crossover)
def crossover(parent1, parent2):
    size = len(parent1)
    child = [-1] * size
    start, end = sorted([random.randint(0, size - 1) for _ in range(2)])

    # Copy the slice from parent1
    for i in range(start, end + 1):
        child[i] = parent1[i]

    # Fill in the rest from parent2
    current_pos = 0
    for i in range(size):
        if child[i] == -1:
            while parent2[current_pos] in child:
                current_pos += 1
            child[i] = parent2[current_pos]
    return child


# Mutation function (Swap Mutation)
def mutate(individual):
    size = len(individual)
    i, j = random.sample(range(size), 2)
    individual[i], individual[j] = individual[j], individual[i]
    return individual


# Selection function (Tournament Selection)
def select(population, fitness_values):
    tournament_size = 5
    selected = random.sample(list(zip(population, fitness_values)), tournament_size)
    selected.sort(key=lambda x: x[1])  # Sort by fitness value (lower is better)
    return selected[0][0]


# Read graph from file and convert it to an adjacency matrix
def read_graph_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    num_nodes = len(lines)
    graph = np.zeros((num_nodes, num_nodes), dtype=int)

    for line in lines:
        line = line.strip()  # Remove any leading/trailing whitespace or newlines
        if not line:
            continue  # Skip empty lines

        # Split the line into node and neighbors part
        try:
            parts = line.split(":")
            node = int(parts[0].strip()) - 1  # Convert to 0-based index

            neighbors = parts[1].strip()
            if neighbors:
                neighbors = list(map(int, neighbors.split()))
                for neighbor in neighbors:
                    graph[node][neighbor - 1] = 1  # 1 represents an edge between nodes
        except ValueError as e:
            print(f"Error processing line: {line}. Skipping this line.")
            continue  # Skip lines that cannot be parsed correctly

    return graph


# Check if a cycle is valid: Each node should appear exactly once, and consecutive nodes must be connected
def is_valid_hamiltonian_cycle(cycle, graph):
    for i in range(len(cycle) - 1):
        if graph[cycle[i]][cycle[i + 1]] == 0:
            return False  # No edge between consecutive nodes
    if graph[cycle[-1]][cycle[0]] == 0:
        return False  # No edge between the last and first node
    return len(set(cycle)) == len(cycle)  # Ensure no duplicate nodes


# Main Genetic Algorithm for Hamiltonian Cycle
def genetic_algorithm(graph, population_size=100, generations=500, mutation_rate=0.1):
    num_nodes = len(graph)
    population = [create_individual(num_nodes) for _ in range(population_size)]

    for generation in range(generations):
        # Evaluate fitness for the entire population
        fitness_values = [fitness(individual, graph) for individual in population]

        # Check if we have found a valid Hamiltonian cycle
        min_fitness = min(fitness_values)
        if min_fitness == 0:
            best_individual = population[fitness_values.index(min_fitness)]
            if is_valid_hamiltonian_cycle(best_individual, graph):
                return best_individual, min_fitness

        # Select the best individuals to form the new population
        new_population = []
        for _ in range(population_size // 2):
            parent1 = select(population, fitness_values)
            parent2 = select(population, fitness_values)

            # Perform crossover
            child1 = crossover(parent1, parent2)
            child2 = crossover(parent2, parent1)

            # Apply mutation
            if random.random() < mutation_rate:
                child1 = mutate(child1)
            if random.random() < mutation_rate:
                child2 = mutate(child2)

            new_population.extend([child1, child2])

        population = new_population

    # If no solution found, return a message
    return None, None  # No valid Hamiltonian cycle found


# Example usage:
if __name__ == "__main__":
    # Read graph from file
    filename = '/Users/jakubsmihula/PycharmProjects/hamiltonicity-of-cages/Graphs/Cages/3 - 4.lst'  # Replace with your input file
    graph = read_graph_from_file(filename)

    solution, cost = genetic_algorithm(graph)
    if solution is None:
        print("No Hamiltonian cycle found.")
    else:
        print("Best Hamiltonian Cycle:", solution)
        print("Cost of the cycle:", cost)
