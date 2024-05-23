import networkx as nx

# Leggi il file edgelist e crea un grafo NetworkX
G = nx.read_weighted_edgelist("higgs-retweet_network_copy.edgelist")

# Salva il grafo in formato GraphML
# nx.write_graphml(G, "higgs-retweet_network_copy.graphml")

connected_components = nx.connected_components(G)

# Trova la giant component
giant_component = max(connected_components, key=len)

# Crea un sottografo contenente solo la giant component
giant_component_subgraph = G.subgraph(giant_component)

# Ora puoi fare quello che vuoi con la giant component, ad esempio salvarla in un nuovo file
nx.write_graphml(giant_component_subgraph, "higgs-retweet_network_giant_component.graphml")
