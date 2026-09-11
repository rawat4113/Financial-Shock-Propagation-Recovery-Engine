import networkx as nx

def add_sector_edges(G, mapping):
    for ticker, sector in mapping.items():
        if ticker not in G: G.add_node(ticker)
        sector_node=f"SECTOR:{sector}"
        G.add_node(sector_node, node_type="sector")
        G.add_edge(ticker, sector_node, relationship="sector")
    return G
