from multiprocessing import Pool, cpu_count
from itertools import product
import time


def parse_graph_from_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    adj_list = {}
    all_nodes = set()

    for line in lines:
        if ':' in line:
            parts = line.strip().split(':')
            node = int(parts[0])
            neighbors = list(map(int, parts[1].strip().split()))
            adj_list[node] = neighbors
            all_nodes.add(node)
            all_nodes.update(neighbors)

    sorted_nodes = sorted(all_nodes)
    index_map = {node: i for i, node in enumerate(sorted_nodes)}
    n = len(sorted_nodes)

    graph = [[0 for _ in range(n)] for _ in range(n)]
    for u in adj_list:
        for v in adj_list[u]:
            i, j = index_map[u], index_map[v]
            graph[i][j] = 1
            graph[j][i] = 1

    return graph, sorted_nodes


def is_safe(graph, path, pos, v):
    if graph[path[pos - 1]][v] == 0:
        return False
    if v in path:
        return False
    return True


def hamiltonian_util(graph, path, pos):
    if pos == len(graph):
        return graph[path[pos - 1]][path[0]] == 1

    for v in range(len(graph)):
        if is_safe(graph, path, pos, v):
            path[pos] = v
            if hamiltonian_util(graph, path, pos + 1):
                return True
            path[pos] = -1
    return False


def generate_initial_paths(graph, depth=2):
    n = len(graph)
    paths = []

    def dfs(path, visited, current_depth):
        if current_depth == depth:
            paths.append(list(path))
            return
        u = path[-1]
        for v in range(n):
            if graph[u][v] == 1 and v not in visited:
                path.append(v)
                visited.add(v)
                dfs(path, visited, current_depth + 1)
                path.pop()
                visited.remove(v)

    dfs([0], {0}, 1)
    return paths


def try_backtrack(args):
    graph, start_path = args
    n = len(graph)
    path = [-1] * n
    for i, node in enumerate(start_path):
        path[i] = node

    if hamiltonian_util(graph, path, len(start_path)):
        return path
    return None


def find_hamiltonian_cycle_parallel(graph):
    initial_paths = generate_initial_paths(graph, depth=4)
    args_list = [(graph, path) for path in initial_paths]

    with Pool(processes=cpu_count()) as pool:
        for result in pool.imap_unordered(try_backtrack, args_list):
            if result:
                pool.terminate()
                pool.join()
                return result
    return None


if __name__ == '__main__':
    start_time =  time.time()
    graph, node_labels = parse_graph_from_file('/Users/jakubsmihula/PycharmProjects/hamiltonicity-of-cages/Graphs/Cages/3 - 6.lst')
    result = find_hamiltonian_cycle_parallel(graph)

    if result:
        cycle = [node_labels[i] for i in result] + [node_labels[result[0]]]
        print("Hamiltonian Cycle found:", cycle)
    else:
        print("No Hamiltonian Cycle found.")

    print("Execution time:", time.time() - start_time)
