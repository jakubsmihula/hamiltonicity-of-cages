import os


TSP_FILE_FOLDER = "/home/jakub/Plocha/Bachelor thesis/Graphs/Input for TSP/"
RECORD_FOLDER = "/home/jakub/Plocha/Bachelor thesis/Graphs/Record/"
CAGES_FOLDER = "/home/jakub/Plocha/Bachelor thesis/Graphs/Cages/"

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



if __name__ == "__main__":
    file_path = CAGES_FOLDER + "3 - 7.lst"
    # exoo_adjacency_list_transformation(file_path)
    convert_adj_list_to_tsp(file_path, TSP_FILE_FOLDER)
    # convert_adj_list_to_tsp("/Users/jakubsmihula/Documents/Matfyz/BC thesis/Graphs/Cages/3 - 5.lst", TSP_FILE_FOLDER)