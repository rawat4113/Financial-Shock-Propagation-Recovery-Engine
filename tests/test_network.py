from src.network.correlation_network import build_correlation_network
import pandas as pd

def test_network():
    x=pd.DataFrame({'A':[1,2,3],'B':[1,2,4]})
    G,c=build_correlation_network(x,0.5)
    assert len(G.nodes)==2
