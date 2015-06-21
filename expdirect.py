#!/usr/bin/python
import operator
from dgraph import randomDirectGraph as randDGraph
from dgraph import countTriangles as ctD
from lesson4 import topk
from lesson4 import betweenness
from mylesson5 import eigenvector_centrality as ec
from dgraph import diameter
from dgraph import readGraph
from dgraph import Page_Rank as pr
from dgraph import fill_incoming as fi

g = randDGraph(500, 0.1)
# g = {0: [2, 3, 4], 1: [0, 2, 3], 2: [1], 3: [0, 4], 4: [0]}
fi(g) # a :D
# g = readGraph('wiki-Vote.txt')
print 'Nodes: ', len(g.keys())
print 'Diameter: ', diameter(g)
print 'Page Rank execution...'
# print 'Triangles: ', ctD(g)
pagerank, iterations, err = pr(g, 1.0e-6)
print iterations, ' iterations.'
print 'Error: ', err
print 'Page Rank:', sorted(pagerank.items(), key=operator.itemgetter(1), reverse=True)[:10]
print 'Eigenvector Centrality'
cscores, diffsum = ec(g)
print topk(cscores, 10)
bet = betweenness(g)
print 'Betweennes centrality: ', topk(bet, 10)