import csv
from datetime import timedelta
import networkx as nx


def read_edges_csv(filename):
    edge_list = list()
    csv_reader = csv.reader(open(filename), delimiter=',', quotechar='"')

    next(csv_reader)
    for row in csv_reader:
        edge_list.append((int(row[0]), int(row[1]), int(row[2])))

    return edge_list


def read_nodes_csv(filename):
    node_dict = dict()
    csv_reader = csv.reader(open(filename), delimiter=',', quotechar='"')

    next(csv_reader)
    for idx, row in enumerate(csv_reader):
        # node_list.append(((int(row[0])), row[1]))
        node_dict[idx] = row[1]
    return node_dict


def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


# Window graphs and Graphs in newminingvol2 have the save directory format
def form_graph(c_date, r_type, e_type, path):

    current_day = str(c_date.year) + "-" + str(c_date.month) + "-" + str(c_date.day)
    current_week = str(c_date.isocalendar()[1]) + "-" + str(c_date.isocalendar()[0])
    nodes_dict = read_nodes_csv(path + r_type + "/" + current_week + "/" + current_day
                                + "/" + "politicsNodes" + e_type + ".csv")
    edges_list = read_edges_csv(path + r_type + "/" + current_week + "/" + current_day
                                + "/" + "politicsEdges" + e_type + ".csv")

    # Adding nodes to graph
    c_graph = nx.Graph()
    for key in nodes_dict:
        c_graph.add_node(key, name=nodes_dict[key])
    c_graph.add_weighted_edges_from(edges_list)

    return c_graph
