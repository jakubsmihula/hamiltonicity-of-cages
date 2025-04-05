import os
import pandas as pd
import numpy as np


TSP_FILE_FOLDER = "/Users/jakubsmihula/PycharmProjects/hamiltonicity-of-cages/Graphs/Input for TSP"
RECORD_FOLDER = "/Users/jakubsmihula/Documents/Matfyz/BC thesis/Graphs/Record/"
CAGES_FOLDER = "/Users/jakubsmihula/PycharmProjects/hamiltonicity-of-cages/Graphs/Cages/"

SAVE_FOR_IMAGE_FOLDER = "/Users/jakubsmihula/Documents/Matfyz/BC thesis/Graphs/GraphImagesInput"


def exoo_adjacency_list_transformation(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    modified_lines = []
    for i, line in enumerate(lines):
        if line.find(':') == -1:
            modified_lines.append(f"{i}: {line.strip()}\n")
        else:
            modified_lines.append(f"{line.strip()}\n")

    with open(file_path, 'w') as file:
        file.writelines(modified_lines)


def convert_adj_list_to_tsp(input_file, output_folder) :
    adj_dict = {}
    vertex_set = set()

    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or ':' not in line:
                continue  # Skip empty or malformed lines
            vertex_part, neighbors_part = line.split(':', 1)
            vertex = int(vertex_part.strip())
            vertex_set.add(vertex)
            if neighbors_part.strip():
                neighbors = [int(x) for x in neighbors_part.split()]
                vertex_set.update(neighbors)
            else:
                neighbors = []
            adj_dict[vertex] = neighbors

    sorted_vertices = sorted(vertex_set)
    mapping = {orig: idx for idx, orig in enumerate(sorted_vertices)}
    n = len(sorted_vertices)

    INF = 10000000000
    matrix = [[0 if i == j else INF for j in range(n)] for i in range(n)]

    for orig_vertex, neighbors in adj_dict.items():
        i = mapping[orig_vertex]
        for neigh in neighbors:
            j = mapping[neigh]
            matrix[i][j] = 1
            matrix[j][i] = 1

    base_name = os.path.splitext(os.path.basename(input_file))[0]
    tsp_name = f"{base_name}_TSP"

    tsp_lines = [
        f"NAME: {tsp_name}",
        "TYPE: TSP",
        "COMMENT: Converted from adjacency list to TSP instance",
        f"DIMENSION: {n}",
        "EDGE_WEIGHT_TYPE: EXPLICIT",
        "EDGE_WEIGHT_FORMAT: FULL_MATRIX",
        "EDGE_WEIGHT_SECTION"
    ]

    for row in matrix:
        row_str = " ".join(str(x) for x in row)
        tsp_lines.append(row_str)

    tsp_lines.append("EOF")
    output_file_name = f"{base_name} - TSP.tsp"
    output_file_path = os.path.join(output_folder, output_file_name)

    with open(output_file_path, "w") as f_out:
        f_out.write("\n".join(tsp_lines))

    print(f"Converted TSP file saved to: {output_file_path}")


def adj_list_to_graph_editor(input_file, output_folder):
    base_name = os.path.splitext(os.path.basename(input_file))[0]

    adj_dict = {}
    vertex_set = set()

    # Read the adjacency list
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or ':' not in line:
                continue
            vertex_part, neighbors_part = line.split(':', 1)
            vertex = int(vertex_part.strip())
            vertex_set.add(vertex)
            neighbors = [int(x) for x in neighbors_part.split() if x.strip()]
            vertex_set.update(neighbors)
            adj_dict[vertex] = neighbors

    # Create the vertices DataFrame
    vertices_df = pd.DataFrame({'id': list(vertex_set), 'label': list(vertex_set)})

    # Create the edges DataFrame efficiently
    edges = set()
    edges_data = []

    for orig_vertex, neighbors in adj_dict.items():
        for neigh in neighbors:
            if (orig_vertex, neigh) not in edges and (neigh, orig_vertex) not in edges:
                edges_data.append({'Source': orig_vertex, 'Target': neigh, 'Weight': 1})
                edges.add((orig_vertex, neigh))

    edges_df = pd.DataFrame(edges_data, columns=['Source', 'Target', 'Weight'])

    # Save to Excel
    vertices_filename = os.path.join(output_folder, f"{base_name}_vertices.xlsx")
    edges_filename = os.path.join(output_folder, f"{base_name}_edges.xlsx")

    vertices_df.to_csv(vertices_filename.replace(".xlsx", ".csv"), index=False)
    edges_df.to_csv(edges_filename.replace(".xlsx", ".csv"), index=False)

    print(f"Files created successfully:")
    print(f"- Vertices: {vertices_filename}")
    print(f"- Edges: {edges_filename}")


def convert_adj_list_to_tsp(input_file, output_folder):
    adj_dict = {}
    vertex_index = {}
    index_counter = 0

    # Read and process file efficiently
    with open(input_file, 'r') as f:
        for line in f:
            if ':' not in line:
                continue  # Skip invalid lines

            vertex_part, neighbors_part = line.split(':', 1)
            vertex = int(vertex_part.strip())

            # Assign an index to the vertex if it's new
            if vertex not in vertex_index:
                vertex_index[vertex] = index_counter
                index_counter += 1

            if neighbors_part.strip():
                neighbors = [int(x) for x in neighbors_part.split()]
                for neighbor in neighbors:
                    if neighbor not in vertex_index:
                        vertex_index[neighbor] = index_counter
                        index_counter += 1
                adj_dict[vertex] = neighbors
            else:
                adj_dict[vertex] = []

    n = len(vertex_index)  # Number of unique vertices
    INF = 10000000000

    # Use NumPy array for better performance
    matrix = np.full((n, n), INF, dtype=np.int32)
    np.fill_diagonal(matrix, 0)  # Set diagonal to 0

    # Populate matrix using dictionary lookup
    for vertex, neighbors in adj_dict.items():
        i = vertex_index[vertex]
        for neighbor in neighbors:
            j = vertex_index[neighbor]
            matrix[i, j] = 1
            matrix[j, i] = 1  # Since the graph is undirected

    # Prepare TSP format
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    tsp_name = f"{base_name}_TSP"

    tsp_lines = [
        f"NAME: {tsp_name}",
        "TYPE: TSP",
        "COMMENT: Converted from adjacency list to TSP instance",
        f"DIMENSION: {n}",
        "EDGE_WEIGHT_TYPE: EXPLICIT",
        "EDGE_WEIGHT_FORMAT: FULL_MATRIX",
        "EDGE_WEIGHT_SECTION"
    ]

    # Convert matrix to string format efficiently
    tsp_lines.extend(" ".join(map(str, row)) for row in matrix)

    tsp_lines.append("EOF")

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    output_file_path = os.path.join(output_folder, f"{base_name} - TSP.tsp")

    # Write to file efficiently
    with open(output_file_path, "w") as f_out:
        f_out.write("\n".join(tsp_lines))

    print(f"Converted TSP file saved to: {output_file_path}")
if __name__ == "__main__":
    file_path = RECORD_FOLDER + "3 - 30.lst"
    exoo_adjacency_list_transformation(file_path)
    adj_list_to_graph_editor(file_path, SAVE_FOR_IMAGE_FOLDER)
    # convert_adj_list_to_tsp("/Users/jakubsmihula/Documents/Matfyz/BC thesis/Graphs/Cages/3 - 5.lst", TSP_FILE_FOLDER)