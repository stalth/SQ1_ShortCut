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


#SQ1 experiments
def sq1_experiments(n, k, failure_num, rep, seed, ran_dom, fail_random):
    #hops_array = np.array([[1,4,7,3,4,3,4,3]])
    #hopsS_array = np.array([[1,4,7,3,4,3,4,3]])
    hops_list_rep = []
    hops_list_shortcut_rep = []
    if ran_dom:        
        for i in range(rep):
            start_rep = time.time()
            g = create_graphs(n, k, i, seed)
            nodes = list(g.nodes())
            edges = list(g.edges())
            for i in nodes:
                source = i
                for j in nodes:
                    destination = j
                    if source == destination:
                        pass
                    else:                        
            #source = random.choice(nodes)
            #destination = random.choice(nodes)
            #while destination == source:
            #    destination = random.choice(nodes)
                        disjoint_path_list = get_disjoint_path(g, destination)
                        disjoint_path_list_shortcut = disjoint_path_list
                        fails_list = get_fails_list(g, source, destination, disjoint_path_list, fail_random, failure_num)

                        hop_list = []
                        hop_list_shortcut = []
                        dis_joint_path = disjoint_path_list_shortcut[source][destination]
                        dis_joint_path_shortcut = dis_joint_path

                        for j in range(0, len(fails_list)):
                            fails_sublist = fails_list[:j]
                            [_, hops, _, detour, _]= routingSQ1(dis_joint_path, source, destination, n, fails_sublist, sc_bool= False)
                            [_, hopsS, _, detourS, dis_joint_path_shortcut] = routingSQ1(dis_joint_path_shortcut, source, destination, n, fails_sublist, sc_bool= True) 
                            hop_list.append(hops)
                            hop_list_shortcut.append(hopsS)
                            #hop_list_shortcut.append(len(disjoint_path_list_shortcut[source][destination][j])-1)
                        #hops_array = np.append(hops_array,[hop_list],axis=0)
                        #hopsS_array = np.append(hopsS_array,[hop_list_shortcut],axis=0)
                        hops_list_rep.append(hop_list)
                        hops_list_shortcut_rep.append(hop_list_shortcut)
                        #array2 = np.append(array,[liste], axis=0)
            end_rep = time.time()
            print(time.asctime( time.localtime(start_rep)))
            print(time.asctime( time.localtime(end_rep)))        
    else:
        g = nx.read_gml("benchmark_graphs/BtEurope.gml")

#Create a graph
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

#Create a list of edge-disjoint paths to destination, source nodes vary
def get_disjoint_path(g, destination):
    SQ1 = {}
    H = build_auxiliary_edge_connectivity(g)
    R = build_residual_network(H, 'capacity')
    SQ1 = {n: {} for n in g}
    for u in g.nodes():
        if (u != destination):
            k = sorted(list(nx.edge_disjoint_paths(
                g, u, destination, auxiliary=H, residual=R)), key=len)
            SQ1[u][destination] = k
    return SQ1

#Check for fails in edge-disjoint paths
def doesntContainFail(path, fails):
    zipped = list(zip(path, path[1:]))
    return all(fail not in zipped for fail in fails)

#Routing
def routingSQ1(SQ1, source, destination, n, fails, sc_bool):
    if sc_bool:
        newList = [path for path in SQ1 if doesntContainFail(path, fails)]
        return (False, len(newList[0]-1), 2, None, newList)
    else:
        curRoute = SQ1[0]
        k = len(SQ1)
        detour_edges = []
        index = 1
        hops = 0
        switches = 0
        curNode = source  # current node
        #n = len(T[0].nodes())
        while (curNode != destination):
            nxt = curRoute[index]
            if (nxt, curNode) in fails or (curNode, nxt) in fails:
                for i in range(2, index+1):
                    detour_edges.append((curNode, curRoute[index-i]))
                    curNode = curRoute[index-i]
                switches += 1
                curNode = source
                hops += (index-1)
                curRoute = SQ1[switches % k]
                index = 1
            else:
                if switches > 0:
                    detour_edges.append((curNode, nxt))
                curNode = nxt
                index += 1
                hops += 1
            if hops > 3*n or switches > k*n:
                print("cycle square one")
                return (True, hops, switches, detour_edges, SQ1)
        return (False, hops, switches, detour_edges, SQ1)

#Create a list of fails, either random or specifically on edge-disjoint paths
def get_fails_list(g, source, destination, disjoint_path_list, fail_random, failure_num):
    edge_list = list(g.edges())
    pathList = disjoint_path_list[source][destination]
    num_edgedesjointpaths = len(pathList)
    fails_list = []
    if fail_random:
        for i in range(failure_num):
            random_fail = random.choice(edge_list)
            while random_fail in fails_list:
                random_fail = random.choice(edge_list)
            fails_list.append(random_fail)
    else:
        for i in range(num_edgedesjointpaths):
            nodeindex_in_path = random.randint(0, len(pathList[i])-2)
            fails_list.append((pathList[i][nodeindex_in_path], pathList[i][nodeindex_in_path+1]))
    return fails_list

#Initialize parameters for experiments, take runtime, start experiments
if __name__ == "__main__":
    start = time.time()
    # favorite_color = pickle.load( open( "./save.p", "rb" ) )
    #parameters
    seed = 1
    n = 40
    rep = 2
    k = 8
    failure_num = 200
    ran_dom = True
    fail_random = False
    #G = nx.Graph()
    #G.add_edges_from([(1, 4), (4, 5), (1, 2), (2,3), (3,5), (3,6), (6,5), (2,4)])
    
    sq1_experiments(n, k, failure_num, rep, seed, ran_dom, fail_random)
 
    end = time.time()
    print(end-start)
    print(time.asctime( time.localtime(start)))
    print(time.asctime( time.localtime(end)))