import matplotlib.pyplot as plt
import networkx as nx

def plot_network(G):
    plt.figure(figsize=(10,8))
    nx.draw_networkx(G, with_labels=True, node_size=500, font_size=8)
    plt.axis("off")
    return plt.gca()
