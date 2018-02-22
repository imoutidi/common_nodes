from datetime import date
import networkx as nx
from tools import graph_tools
import math


# Here we will calculate a number of common node
# similarities for two consecutive graphs
def common_nodes(alpha_graph, beta_graph):
    common_nodes_ids = list()
    alpha_dict = nx.get_node_attributes(alpha_graph, 'name')
    beta_dict = nx.get_node_attributes(beta_graph, 'name')
    alpha_entities = list(alpha_dict.values())
    beta_entities = list(beta_dict.values())

    # Using sets to efficiently detect the common nodes of the graphs
    common_entities = list(set(alpha_entities).intersection(beta_entities))
    reverse_ad = dict((y, x) for x, y in alpha_dict.items())
    reverse_bd = dict((y, x) for x, y in beta_dict.items())
    for c_node in common_entities:
        common_nodes_ids.append((reverse_ad[c_node], reverse_bd[c_node]))
    return common_nodes_ids


# Returns the number of common neighbors between all
# common nodes of two graphs
# |Γ(u) τομή Γ(v)|
def common_neighbors(alpha_graph, beta_graph):
    commons_ids = common_nodes(alpha_graph, beta_graph)
    alpha_dict = nx.get_node_attributes(alpha_graph, 'name')
    beta_dict = nx.get_node_attributes(beta_graph, 'name')
    # reverse dictionaries are for debugging
    reverse_ad = dict((y, x) for x, y in alpha_dict.items())
    reverse_bd = dict((y, x) for x, y in beta_dict.items())

    com_ids_score = list()
    alpha_n_names = list()
    beta_n_names = list()
    for c_id in commons_ids:
        alpha_neighbors = alpha_graph.neighbors(c_id[0])
        beta_neighbors = beta_graph.neighbors(c_id[1])
        for a_n in alpha_neighbors:
            alpha_n_names.append(alpha_dict[a_n])
        for b_n in beta_neighbors:
            beta_n_names.append(beta_dict[b_n])

        common_neighbors_names = set(alpha_n_names).intersection(beta_n_names)
        com_ids_score.append((c_id[0], c_id[1], len(common_neighbors_names)))
        alpha_n_names.clear()
        beta_n_names.clear()
    return com_ids_score


# Returns a set with the union of the neighbors of two common nodes
# |Γ(u) ένωση Γ(v)|
def union_neighbors(alpha_graph, beta_graph):
    commons_ids = common_nodes(alpha_graph, beta_graph)
    alpha_dict = nx.get_node_attributes(alpha_graph, 'name')
    beta_dict = nx.get_node_attributes(beta_graph, 'name')
    # reverse dictionaries are for debugging
    reverse_ad = dict((y, x) for x, y in alpha_dict.items())
    reverse_bd = dict((y, x) for x, y in beta_dict.items())

    alpha_n_names = list()
    beta_n_names = list()
    ids_union_size = list()

    for c_id in commons_ids:
        alpha_neighbors = alpha_graph.neighbors(c_id[0])
        beta_neighbors = beta_graph.neighbors(c_id[1])
        for a_n in alpha_neighbors:
            alpha_n_names.append(alpha_dict[a_n])
        for b_n in beta_neighbors:
            beta_n_names.append(beta_dict[b_n])

        all_neighbors = set(alpha_n_names).union(beta_n_names)
        # print(alpha_dict[c_id[0]], beta_dict[c_id[1]], all_neighbors)
        ids_union_size.append((c_id[0], c_id[1], len(all_neighbors)))
        alpha_n_names.clear()
        beta_n_names.clear()
    return ids_union_size


# Returns the Jaccard similarity of two common nodes
# If both nodes don't have any neighbors in both graphs
# then the Jaccard similarity is 1 because
# both nodes do not have any neighbors so that
# is something similar between them.
def jaccard_similarity(alpha_graph, beta_graph):
    intersec_score = common_neighbors(alpha_graph, beta_graph)
    union_score = union_neighbors(alpha_graph, beta_graph)

    ids_jaccard_score = list()
    for idx, score in enumerate(intersec_score):
        if score[2] == 0 and union_score[idx][2] == 0:
            ids_jaccard_score.append((score[0], score[1], 1))
        elif score[2] == 0:
            ids_jaccard_score.append((score[0], score[1], 0))
        else:
            ids_jaccard_score.append((score[0], score[1], score[2] / union_score[idx][2]))
    return ids_jaccard_score


# Calculating the sorenson similarity of the common nodes
# of the graphs
def sorenson_similarity(alpha_graph, beta_graph):
    intersec_score = common_neighbors(alpha_graph, beta_graph)

    ids_sorenson_score = list()
    for score in intersec_score:
        degree_sum = alpha_graph.degree(score[0]) + beta_graph.degree(score[1])

        if degree_sum == 0:
            ids_sorenson_score.append((score[0], score[1], 1))
        elif score[2] == 0:
            ids_sorenson_score.append((score[0], score[1], 0))
        else:
            ids_sorenson_score.append((score[0], score[1], (2 * score[2]) / degree_sum))
    return ids_sorenson_score


# Calculating the sorenson similarity of the common nodes
# of the graphs
def salton_similarity(alpha_graph, beta_graph):
    intersec_score = common_neighbors(alpha_graph, beta_graph)

    ids_salton_score = list()
    for score in intersec_score:
        a_degree = alpha_graph.degree(score[0])
        b_degree = beta_graph.degree(score[1])
        root_of_degree_product = math.sqrt(a_degree * b_degree)

        if a_degree == 0 and b_degree == 0:
            ids_salton_score.append((score[0], score[1], 1))
        elif score[2] == 0:
            ids_salton_score.append((score[0], score[1], 0))
        else:
            ids_salton_score.append((score[0], score[1], score[2] / root_of_degree_product))
    return ids_salton_score


def preferential_attachment(alpha_graph, beta_graph):
    commons_ids = common_nodes(alpha_graph, beta_graph)

    ids_attachment_score = list()
    for c_id in commons_ids:
        alpha_neighbors = alpha_graph.neighbors(c_id[0])
        beta_neighbors = beta_graph.neighbors(c_id[1])
        num_of_a_n = sum(1 for _ in alpha_neighbors)
        num_of_b_n = sum(1 for _ in beta_neighbors)
        ids_attachment_score.append((c_id[0], c_id[1], num_of_a_n * num_of_b_n))
    return ids_attachment_score


if __name__ == "__main__":
    file_path = "/home/iraklis/PycharmProjects/newsMiningVol2/Graphs/"
    a_date = date(2018, 2, 2)
    b_date = date(2018, 2, 3)
    c_date = date(2018, 2, 4)
    a_graph = graph_tools.form_graph(a_date, "Sentence", "P", file_path)
    b_graph = graph_tools.form_graph(b_date, "Sentence", "P", file_path)
    c_graph = graph_tools.form_graph(c_date, "Sentence", "P", file_path)
    p = salton_similarity(a_graph, b_graph)
    print(p)


