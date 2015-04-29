#!/usr/bin/python

import sys
from lesson3 import readGraph, count2Paths, diameter
from lesson4 import betweenness, cb_max, topk

simple_graph = {}
simple_graph[0] = {1}
simple_graph[1] = {0, 2}
simple_graph[2] = {1, 3}
simple_graph[3] = {2, 4}
simple_graph[4] = {3}
cb = betweenness(simple_graph, True)

# graph = readGraph(sys.argv[1])
# cb = betweenness(graph)

k = 10
print 'Top ', k, '=>', topk(cb, k)
