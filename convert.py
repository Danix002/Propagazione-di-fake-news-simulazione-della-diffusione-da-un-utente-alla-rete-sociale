import networkx as nx
import json
from networkx.readwrite import json_graph

G = nx.barabasi_albert_graph(100, 3)
data = json_graph.node_link_data(G)
#write json
with open('force.json', 'w') as outfile:
    json.dump(data, outfile)



