import os
import networkx as nx
import time
import csv

def read_adjacency_list(filename):
    graph = {}
    with open(filename) as f:
        for line in f:
            if ':' not in line:
                continue
            node, neighbors = line.strip().split(':')
            node = int(node)
            # Ensure nodes start at 1
            if node < 1:
                node = 1
            neighbors = list(map(int, neighbors.strip().split()))
            graph[node] = neighbors
    return graph

""" sufficient conditions for general graphs """
def satisfies_dirac(graph):
    n = len(graph)
    if n < 3:
        return False
    threshold = n // 2
    for(node, neighbors) in graph.items():
        if len(neighbors) < threshold:
            return False
    return True

def satisfies_ore(graph):
    n = len(graph)
    if n < 3:
        return False
    for u in graph:
        for v in graph:
            if u != v and v not in graph[u]:
                deg_u = len(graph[u])
                deg_v = len(graph[v])
                if deg_u + deg_v < n:
                    return False
    return True

""" sufficient conditions for regular 2-connected graphs """

def is_regular(graph):
    degree = len(next(iter(graph.values())))
    for neighbors in graph.values():
        if len(neighbors) != degree:
            return False
    return True

def is_2_connected(graph):
    G = nx.Graph()
    for u, neighbours in graph.items():
        for v in neighbours:
            G.add_edge(u, v)
    return len(list(nx.articulation_points(G))) == 0

def satisfies_erdos_hobbs(graph):
    num_vertices = len(graph)
    if not is_regular(graph):
        return False
    if not is_2_connected(graph):
        return False

    degree = len(next(iter(graph.values())))

    if num_vertices % 2 == 0:
        n = num_vertices // 2
        k = n - degree
        return n >= k ** 2 + k + 1

    else:
        n = (num_vertices - 1) // 2
        k = n - degree
        return n >= 2 * k ** 2 - 3 * k + 3

def satisfies_jackson(graph):
    if not is_regular(graph):
        return False
    if not is_2_connected(graph):
        return False

    degree = len(next(iter(graph.values())))
    num_vertices = len(graph)

    return num_vertices <= 3 * degree



def test_conditions(graph):
    return {
        "Dirac": satisfies_dirac(graph),
        "Ore": satisfies_ore(graph),
        "Erdos_Hobbs": satisfies_erdos_hobbs(graph),
        "Jackson": satisfies_jackson(graph)
    }


if __name__ == '__main__':
    start = time.time()

    graph_folder = '/Users/jakubsmihula/Documents/Matfyz/BC thesis/Graphs/Record'
    csv_path = 'resultsREC.csv'
    txt_path = 'resultsREC.txt'

    with open(txt_path, mode='w') as txtfile:

        header = f"{'Graph Name':<22} {'Dirac':<10} {'Ore':<10} {'Erdos_Hobbs':<13} {'Jackson':<10}\n"
        txtfile.write(header)
        txtfile.write("-" * len(header) + "\n")

        for filename in sorted(os.listdir(graph_folder)):
            if filename.endswith('.lst'):
                print(f"Processing {filename}...")
                path = os.path.join(graph_folder, filename)
                graph = read_adjacency_list(path)
                result = test_conditions(graph)

                dirac = "YES" if result["Dirac"] else "NO"
                ore = "YES" if result["Ore"] else "NO"
                erdos = "YES" if result["Erdos_Hobbs"] else "NO"
                jackson = "YES" if result["Jackson"] else "NO"

                line = f"{filename:<22} {dirac:<10} {ore:<10} {erdos:<13} {jackson:<10}\n"
                txtfile.write(line)

    print("Execution time:", time.time() - start)
    print(f"Results saved to:\n - {csv_path}\n - {txt_path}")
