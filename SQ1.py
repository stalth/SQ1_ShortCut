import sys
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import itertools
import random
import time

def sq1_experiments(n, k, failure_num, rep, seed):
    a = 2

if __name__ == "__main__":
    start = time.time()

    #parameters
    seed = 1
    n = 100
    rep = 2
    k = 8
    failure_num = 40
    #G = nx.Graph()
    #G.add_edges_from([(1, 4), (4, 5), (1, 2), (2,3), (3,5), (3,6), (6,5), (2,4)])

    #G = nx.read_gml("benchmark_graphs/BtEurope.gml")
    sq1_experiments(n, k, failure_num, rep, seed)
    end = time.time()
    print(end-start)
    print(time.asctime( time.localtime(start)))
    print(time.asctime( time.localtime(end)))