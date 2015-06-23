#!/usr/bin/python
import sys
from lesson4 import topk, lastk
from dgraph import readGraph
from dgraph import Page_Rank as pr
from dgraph import Independent_Cascade as ic

seed = int(sys.argv[1])

g = readGraph('wiki-Vote.txt')

pagerank, iterations, err = pr(g, alpha=1.0e-5, eps=1.0e-6) # alpha = 0.00001
# print pagerank
print 'Page Rank. %s iterations. %s accuracy' % (iterations, err)
top = [a for a,b in topk(pagerank, seed)]
last = [a for a,b in lastk(pagerank, seed)]
print 'Top', seed
print [(u, pagerank[u]) for u in top]
print 'Last', seed
print [(u, pagerank[u]) for u in last]
adopters, haters, steps = ic(g, top)
print 'Independent Cascade Model: TOP', seed
print 'Final Adopters:', len(adopters)
print 'Final Haters:', len(haters)
print '# Iterations:', steps
adopters, haters, steps = ic(g, last)
print 'Independent Cascade Model: LAST', seed
print 'Final Adopters:', len(adopters)
print 'Final Haters:', len(haters)
print '# Iterations:', steps