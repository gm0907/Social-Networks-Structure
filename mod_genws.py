#!/usr/bin/python
from __future__ import division
import random
import itertools
import copy
import math
from lesson1 import averageClustering as ac
from dgraph import countEdges
from dgraph import toUndirect as und
from dgraph import euclidean_distance

def GenWSGridGraph(n, m, r, k, q=2):
    '''
    @param n: number of nodes
    @param m: number of edges
    @param r : radius of each node (a node u is connected with each other node at distance at most r) - strong ties
    @param k : number of random edges for each node u - weak ties [list] e.g. [0, 5, 10]
    '''
    line = int(math.sqrt(n))
    #Initialization
    graph = {k : set() for k in xrange(n)}

    while m > 0:
        i = random.randint(0, line-1)
        #j = random.randint(0, line-1)
        #For each node u, we add an edge to each node at distance at most r from u
        for j in xrange(line):
            for x in xrange(r+1): # x is the horizontal offset
                for y in xrange(r+1-x): # y is the vertical offset. The sum of offsets must be at most r
                    if x + y > 0: # The sum of offsets must be at least 1
                        if i + x < line:
                            if j + y < line and (i+x)*line+(j+y) not in graph[i*line+j]:
                                graph[i*line+j].add((i+x)*line+(j+y))
                                m -= 1
                                if m == 0:
                                    return graph
                            if j - y >= 0 and (i+x)*line+(j-y) not in graph[i*line+j]:
                                graph[i*line+j].add((i+x)*line+(j-y))
                                m -= 1
                                if m == 0:
                                    return graph
                        if i - x >= 0:
                            if j + y < line and (i-x)*line+(j+y) not in graph[i*line+j]:
                                graph[i*line+j].add((i-x)*line+(j+y))
                                m -= 1
                                if m == 0:
                                    return graph
                            if j - y >= 0 and (i-x)*line+(j-y) not in graph[i*line+j]:
                                graph[i*line+j].add((i-x)*line+(j-y))
                                m -= 1
                                if m == 0:
                                    return graph

            #For each node u, we add a node to k randomly chosen nodes
            weak_ties = random.choice(k)
            while weak_ties > 0:
                xt = random.randint(0, line-1)
                yt = random.randint(0, line-1)
                if xt*line+yt > n-1:
                    continue
                if xt != i and yt != j and xt*line+yt not in graph[i*line+j] and random.random() <= (1/(euclidean_distance((xt, yt), (i,j))**q)):
                    graph[i*line+j].add(xt*line+yt)
                    m -= 1
                    weak_ties -= 1
                    if m == 0:
                        return graph
    return graph


if __name__ == '__main__':
    EXECUTIONS = 3
    NODES = 7056
    # edges = random.randint(75000, 125000)
    edges = [75000, 100000, 125000]
    radius = 2
    weak_ties = [i*5 for i in xrange(0, 3)]
    seed = 100
    for i in xrange(EXECUTIONS):
        g = GenWSGridGraph(NODES, edges[i], radius, weak_ties)
        print 'Edges %d\tAverage Clustering = %f' % (countEdges(g),ac(und(g)))
