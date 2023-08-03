import networkx as nx
import matplotlib.pyplot as plt
import random


G = nx.Graph()
G.add_edges_from([(1, 4), (4, 5), (1, 2), (2,3), (3,5), (3,6), (6,5), (2,4)])

#G = nx.read_gml("benchmark_graphs/BtEurope.gml")