#!/usr/bin/python

import sys
from lesson1 import randomGraph, averageClustering, countTriangles
from lesson2 import countEdges
from lesson3 import readGraph, count2Paths, diameter

graph = readGraph(sys.argv[1])
print diameter(graph)
