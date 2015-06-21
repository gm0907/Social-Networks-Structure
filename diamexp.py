#!/usr/bin/python
from dgraph import randomDirectedGraph as randDGraph
from dgraph import countTriangles as ctD
from lesson1 import countTriangles as ctU
from lesson1 import randomGraph
from dgraph import countEdges as cE
from dgraph import diameter
from dgraph import readGraph


# g = randomGraph(500, 0.5)
# g = {0: [2, 3, 4], 1: [0, 2, 3], 2: [1], 3: [0, 4], 4: [0]}
g = readGraph('wiki-Vote.txt')
print 'Nodes: ', len(g.keys())
print 'Edges: ', cE(g)
print 'Diameter: ', diameter(g)
# print 'Triangles: ', ctD(g)
