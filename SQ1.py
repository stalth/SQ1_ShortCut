import sys
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import itertools
import random
import time

def sq1_experiments(n, k, failure_num, rep, seed, ran_dom):
    if ran_dom:
        for i in range(rep):
            g = create_graphs(n, k, i, seed)
    else:
        g = nx.read_gml("benchmark_graphs/BtEurope.gml")

#Graphen erstellen
def create_graphs(n, k, rep, seed):
    g = nx. random_regular_graph(k,n)
    while nx.edge_connectivity(g) < k: #Konnektivität von k oder größer, sonst neuen Graph erstellen
           g = nx.random_regular_graph(k, n).to_directed()
    g.graph['seed'] = seed
    g.graph['k'] = k
    f = open('results/' + 'SQ1_ShortCut' + str(seed) + '_graph_' + str(n) + '_' + str(rep) + '.txt', 'w')
    f.write('n=' + str(n) + ', k=' + str(k) + ', rep=' + str(rep) + ', seed=' + str(seed)) #!!!!!!!!!!!!!!!!!!!!!!!!!
    f.close() 
    return g 


if __name__ == "__main__":
    start = time.time()

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