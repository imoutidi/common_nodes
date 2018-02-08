from datetime import date
import networkx as nx
from tools import graph_tools


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


# returns the number of common neighbors between two nodes
# def common_neighbors():




def jaccard_similarity(alpha_graph, beta_graph):
    commons_ids = common_nodes(alpha_graph, beta_graph)
    com_ids_score = list()
    # for c_id in commons_ids:



if __name__ == "__main__":
    a_date = date(2018, 2, 2)
    b_date = date(2018, 2, 3)
    c_date = date(2018, 2, 4)
    a_graph = graph_tools.form_graph(a_date, "Sentence", "P")
    b_graph = graph_tools.form_graph(b_date, "Sentence", "P")
    c_graph = graph_tools.form_graph(c_date, "Sentence", "P")
    common_nodes(a_graph, b_graph)
