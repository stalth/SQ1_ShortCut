import pickle
from obj_class_pickle import DataGraphs

for i in range(100):
    result = DataGraphs.load("C:/Repositories/SQ1_ShortCut/results/50nodes/SQ1_ShortCut_1_graph_True_50_200_0_False.pickle") 
    print(result)
    print(str(len(result.e)))