import sys
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import itertools
from networkx.algorithms.connectivity import build_auxiliary_edge_connectivity
from networkx.algorithms.flow import build_residual_network
import random
import pickle
import time



def sq1_experiments(n, k, failure_num, rep, seed, ran_dom):
    if ran_dom:
        for i in range(rep):
            g = create_graphs(n, k, i, seed)
            nodes = list(g.nodes())
            source = random.choice(nodes)
            destination = random.choice(nodes)
            while destination == source:
                destination = random.choice(nodes)
            disjoint_path_list = get_disjoint_path(g, destination)
    else:
        g = nx.read_gml("benchmark_graphs/BtEurope.gml")

#Graphen erstellen
def create_graphs(n, k, rep, seed):
    g = nx.random_regular_graph(k,n)
    while nx.edge_connectivity(g) < k: #Konnektivität von k oder größer, sonst neuen Graph erstellen
           g = nx.random_regular_graph(k, n).to_directed()
    g.graph['seed'] = seed
    # pickle.dump(g,  open( "./save.p", "wb" ))
    g.graph['k'] = k
    with open('results/' + 'SQ1_ShortCut' + str(seed) + '_graph_' + str(n) + '_' + str(rep) + '.txt', 'w') as file:
        # file.write('n=' + str(n) + ', k=' + str(k) + ', rep=' + str(rep) + ', seed=' + str(seed)) 
        file.write(f"{n=}, {k=}, {rep=}, {seed=}") 
    return g 

def get_disjoint_path(g, d):
    SQ1 = {}
    H = build_auxiliary_edge_connectivity(g)
    R = build_residual_network(H, 'capacity')
    SQ1 = {n: {} for n in g}
    for u in g.nodes():
        if (u != d):
            k = sorted(list(nx.edge_disjoint_paths(
                g, u, d, auxiliary=H, residual=R)), key=len)
            SQ1[u][d] = k
    return SQ1

if __name__ == "__main__":
    start = time.time()
    # favorite_color = pickle.load( open( "./save.p", "rb" ) )
    #parameters
    seed = 1
    n = 100
    rep = 2
    k = 8
    failure_num = 40
    ran_dom = True
    #G = nx.Graph()
    #G.add_edges_from([(1, 4), (4, 5), (1, 2), (2,3), (3,5), (3,6), (6,5), (2,4)])
    
    sq1_experiments(n, k, failure_num, rep, seed, ran_dom)
 
    end = time.time()
    print(end-start)
    print(time.asctime( time.localtime(start)))
    print(time.asctime( time.localtime(end)))