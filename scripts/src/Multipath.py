import networkx as nx
import multiprocessing
from copy import deepcopy
import time


def is_hamiltonian_cycle(path, graph):
    return len(path) == len(graph.nodes) and path[0] in graph.neighbors(path[-1])

def is_valid_graph(G):
    return nx.is_connected(G)

def extend_segment(G, segment, w):
    new_segment = segment + [w]
    G_prime = deepcopy(G)
    S_prime = []

    for i in range(len(new_segment) - 1):
        if G_prime.has_edge(new_segment[i], new_segment[i + 1]):
            G_prime.remove_edge(new_segment[i], new_segment[i + 1])

    S_prime.append(new_segment)

    return new_segment, S_prime, G_prime

def multipath(G, segments, visited, result_queue, stop_event):
    if stop_event.is_set():
        return

    for segment in segments:
        u = segment[-1]
        for w in G.neighbors(u):
            if w in segment:
                continue

            new_segment, new_segments, G_prime = extend_segment(G, segment, w)

            if len(set(new_segment)) == len(G.nodes) and new_segment[0] in G.neighbors(w):
                result_queue.put(new_segment + [new_segment[0]])
                stop_event.set()
                return

            if is_valid_graph(G_prime):
                multipath(G_prime, new_segments, visited | {w}, result_queue, stop_event)
                if stop_event.is_set():
                    return

def parallel_multipath_solver(G, start_node=1):
    manager = multiprocessing.Manager()
    result_queue = manager.Queue()
    stop_event = manager.Event()
    processes = []

    for neighbor in G.neighbors(start_node):
        segment = [start_node, neighbor]
        G_prime = deepcopy(G)
        if G_prime.has_edge(start_node, neighbor):
            G_prime.remove_edge(start_node, neighbor)

        p = multiprocessing.Process(
            target=multipath,
            args=(G_prime, [segment], set(segment), result_queue, stop_event)
        )
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    if not result_queue.empty():
        return result_queue.get()
    else:
        return None


def load_graph_from_file(filepath):
    G = nx.Graph()
    with open(filepath, 'r') as f:
        for line in f:
            if ':' not in line:
                continue
            node_str, neighbors_str = line.strip().split(':')
            node = int(node_str)
            neighbors = map(int, neighbors_str.strip().split())
            for neighbor in neighbors:
                G.add_edge(node, neighbor)
    return G

if __name__ == "__main__":
    graph = load_graph_from_file("/Users/jakubsmihula/PycharmProjects/hamiltonicity-of-cages/Graphs/Cages/3 - 6.lst")
    start = time.time()
    cycle = parallel_multipath_solver(graph, start_node=1)
    end = time.time()

    if cycle:
        print("Hamiltonian cycle found:", cycle)
    else:
        print("No Hamiltonian cycle found.")

    print("Time taken:", round(end - start, 2), "seconds")

