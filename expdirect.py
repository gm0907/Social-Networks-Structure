#!/usr/bin/python
from dgraph import randomDirectedGraph as randDGraph
from dgraph import countTriangles as ctD
from lesson1 import countTriangles as ctU
from lesson1 import randomGraph
from dgraph import diameter


g = randomGraph(500, 0.5)
# g = {0: [2, 3, 4], 1: [0, 2, 3], 2: [1], 3: [0, 4], 4: [0]}
# print g
# ctu_start = time.time()
tr = ctU(g)
print 'Triangles:', tr
# print 'Time Undirected:', time.time() - ctu_start
#print 'Diameter:', diameter(g)
# ctd_start = time.time()
tr = ctD(g)
print 'Triangles:', tr
# print 'Time Directed:', time.time() - ctd_start