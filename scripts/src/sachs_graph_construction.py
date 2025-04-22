import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import copy


# Global memoization dictionary
graph_memo = {}

def v_y_graph(v, y):
    if (v, y) in graph_memo:
        return graph_memo[(v, y)]

    print(v, y)

    if y == 2:
        G = nx.MultiGraph()
        G.add_node(0)
        G.add_node(1)
        for _ in range(v):
            G.add_edge(0, 1)
        graph_memo[(v, y)] = G
        return G

    if v == 2:
        cycle = nx.cycle_graph(y)
        G = nx.MultiGraph(cycle)
        graph_memo[(v, y)] = G
        return G

    G_delta = v_y_graph(v - 1, y)
    G_lambda = v_y_graph(G_delta.number_of_nodes(), y - 1)

    composed_g = replace_nodes_with_graph(G_delta, G_lambda)
    graph_memo[(v, y)] = composed_g
    return composed_g



def draw_multi_graph(G):
    pos = nx.spring_layout(G, seed=42)

    for node, coords in pos.items():
        pos[node] = coords + (0.05 * (node % 2), 0.05 * (node % 3))  # Offset nodes

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=700)

    for i, (u, v, key) in enumerate(G.edges(keys=True)):
        # Apply a small offset to the edge based on its key (to separate parallel edges)
        rad = 0.3 * (i - len(G.edges(u, v)) / 2)  # Adjust the radius of curvature
        edge_path = nx.utils.pairwise([pos[u], pos[v]])
        edge_arc = nx.draw_networkx_edges(
            G,
            pos,
            edgelist=[(u, v)],
            connectionstyle=f'arc3,rad={rad}',
            edge_color="gray",
        )

    # Add labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_color='black')
    plt.show()



def replace_nodes_with_graph(Delta, Lambda):
    G = nx.MultiGraph()

    node_offset = 0
    last_node = None

    unused_nodes_per_copy = []

    edges = len(Lambda.edges())
    nodes_in_order = list(Lambda.nodes())

    for i, node in enumerate(nodes_in_order):
        copy = Delta.copy()
        mapping = {node: node + node_offset for node in copy.nodes()}
        copy_relabeled = nx.relabel_nodes(copy, mapping)
        G = nx.compose(G, copy_relabeled)

        if last_node is not None:
            first_copy_node = min(copy_relabeled.nodes)
            G.add_edge(last_node, first_copy_node)

        if i < len(nodes_in_order) - 1:
            Lambda.remove_edge(nodes_in_order[i], nodes_in_order[i + 1])
        else:
            Lambda.remove_edge(nodes_in_order[i], nodes_in_order[0])

        all_nodes = set(copy_relabeled.nodes())
        min_node = min(all_nodes)
        max_node = max(all_nodes)
        all_nodes.remove(min_node)
        all_nodes.remove(max_node)
        unused_nodes_per_copy.append(all_nodes)

        last_node = max(copy_relabeled.nodes)
        node_offset += len(copy)

    G.add_edge(max(G.nodes), min(G.nodes))


    for edge in Lambda.edges():
        src, dest = edge

        copy1_nodes = unused_nodes_per_copy[src]
        copy2_nodes = unused_nodes_per_copy[dest]

        src_node = copy1_nodes.pop()
        dest_node = copy2_nodes.pop()

        G.add_edge(src_node, dest_node)
    return G

def main():
    v = int(input('v = '))
    y = int(input('y = '))
    G = v_y_graph(v, y)
    # draw_multi_graph(G)
    print(list(G.nodes))
    print(list(G.edges))


if __name__ == '__main__':
    main()

