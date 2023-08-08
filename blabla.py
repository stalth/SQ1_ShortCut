import sys
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import itertools
import random
import pickle
import time

G = nx.Graph()
G.add_edges_from([(1, 4), (4, 5), (1, 2), (2,3), (3,5), (3,6), (6,5), (2,4)])
source = 1
destination = 6

pos = nx.spring_layout(G, k=0.65)  # Adjust k to increase spacing
nx.draw(G, pos, with_labels=True)
plt.show()
path_list = list(nx.edge_disjoint_paths(G,source,destination))
print(path_list)