#!/usr/bin/python
import sys
from lesson4 import topk
from dgraph import readGraph
from dgraph import Page_Rank as pr
from dgraph import Independent_Cascade as ic

seed = int(sys.argv[1])

g = readGraph('wiki-Vote.txt')

pagerank, iterations, err = pr(g, alpha=1.0e-6, eps=1.0e-14) # alpha = 0.000001
print 'Page Rank. %s iterations. %s accuracy' % (iterations, err)
top = [a for a,b in topk(pagerank, seed)]
print 'Top', seed
print top
adopters, haters, steps = ic(g, top)
print 'Independent Cascade Model'
print 'Final Adopters:', len(adopters)
print 'Final Haters:', len(haters)
print 'Iterations needed:', steps