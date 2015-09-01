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
import networkx as nx

# g = randDGraph(500, 0.1)
g = readGraph('wiki-Vote.txt')

#G = nx.from_dict_of_lists(g)
#print 'NetworkX Page Rank'
#print [a for a,b in topk(nx.pagerank(G, alpha=1.0e-6, tol=1.0e-10), 10)]
# print [a for a,b in topk(nx.eigenvector_centrality(G), 10)]
# g = {0: [2, 3, 4], 1: [0, 2, 3], 2: [1], 3: [0, 4], 4: [0]}
fi(g) # a :D
print 'Incoming edges stored'
# print 'Nodes: ', len(g.keys())
# print 'Diameter: ', diameter(g)
print 'Page Rank execution...'
# print 'Triangles: ', ctD(g)
pagerank, iterations, err = pr(g, alpha=1.0e-5, eps=1.0e-8) # alpha = 0.00001
print iterations, ' iterations. Error:', err
print 'Page Rank'
print [a for a,b in topk(pagerank, 10)]
# print 'Eigenvector Centrality'
# cscores, diffsum = ec(g)
# print [a for a, b in topk(cscores, 10)]
# bet = betweenness(g)
# print 'Betweennes centrality'
# print [a for a, b in topk(bet, 10)]