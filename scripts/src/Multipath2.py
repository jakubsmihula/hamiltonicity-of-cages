from mpi4py import MPI
import networkx as nx
from multiprocessing import Pool, cpu_count
import random
import sys
import time
import sys
sys.setrecursionlimit(10000)

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def is_valid(vertex, pos, path, graph):
    if not graph[path[pos - 1]][vertex]:
        return False
    if vertex in path:
        return False
    return True

def hamilton_cycle_util(graph, path, pos):
    n = len(graph)
    while pos < n:
        found = False
        for vertex in range(n):
            if is_valid(vertex, pos, path, graph):
                path[pos] = vertex
                if hamilton_cycle_util(graph, path, pos + 1):
                    return True
                path[pos] = -1
        return False
    return graph[path[pos - 1]][path[0]] == 1


def try_vertex(args):
    graph, start_vertex = args
    n = len(graph)
    path = [-1] * n
    path[0] = 0
    path[1] = start_vertex
    if graph[0][start_vertex] == 0:
        return None
    if hamilton_cycle_util(graph, path, 2):
        return path
    return None



def read_graph(filepath, nodes):
    G = [[0]*nodes for _ in range(nodes)]
    with open(filepath, 'r') as f:
        for line in f:
            if ':' not in line:
                continue
            node_str, neighbors_str = line.strip().split(':')
            node = int(node_str) - 1
            neighbors = map(int, neighbors_str.strip().split())
            for neighbor in neighbors:
                G[node][neighbor - 1] = 1
    return G


def main():
    print(f"Using up to {cpu_count()} CPU cores...")
    start_time = time.time()

    n_vertices = 70
    graph = read_graph("/Users/jakubsmihula/PycharmProjects/hamiltonicity-of-cages/Graphs/Cages/3 - 10 - 1.lst", n_vertices)

    candidates = [(graph, v) for v in range(1, n_vertices)]

    with Pool() as pool:
        results = pool.map(try_vertex, candidates)

    for res in results:
        if res:
            print("Hamiltonian cycle found!")
            print(res, "...")
            break
    else:
        print("No Hamiltonian cycle found.")

    print("Total time:", time.time() - start_time)


if __name__ == "__main__":
    main()
