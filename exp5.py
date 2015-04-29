#!/usr/bin/python

import sys
from lesson1 import randomGraph
from lesson4 import betweenness
from lesson5 import eigenvector_centrality

# nodes = int(sys.argv[1]) #number of nodes
# sep = float(sys.argv[2]) #experiments for p = sep, 2sep, 3sep, ..., 1
# graph = randomGraph(nodes,sep)

simple_graph = {}
simple_graph[0] = {1}
simple_graph[1] = {0, 2}
simple_graph[2] = {1, 3}
simple_graph[3] = {2, 4}
simple_graph[4] = {3}
print betweenness(simple_graph)
print eigenvector_centrality(simple_graph)