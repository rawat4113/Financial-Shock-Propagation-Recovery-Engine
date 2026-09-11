import pandas as pd
import networkx as nx

def build_correlation_network(returns, threshold=0.60):
    corr=returns.corr()
    G=nx.Graph()
    for a in corr.columns:
        G.add_node(a)
    for i,a in enumerate(corr.columns):
        for b in corr.columns[i+1:]:
            w=corr.loc[a,b]
            if pd.notna(w) and abs(w)>=threshold:
                G.add_edge(a,b,weight=float(w))
    return G, corr
