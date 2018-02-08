import networkx as nx
from tools import graph_tools
from datetime import date

if __name__ == "__main__":
    a_date = date(2018, 2, 2)
    gg = graph_tools.form_graph(a_date, "Sentence", "P")
    a = nx.get_node_attributes(gg, 'name')
    print(a)
    print(gg.degree())
    print(nx.degree(gg, nbunch=None, weight='weight'))
    print(gg.nodes[10]['name'])

