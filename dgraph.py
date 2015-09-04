#!/usr/bin/python
# dgraph.py >>> Directed graph

from __future__ import division
import random
import itertools
import copy
import math


incoming = {}

def readGraph(filename):
    graph = {}
    with open(filename) as fp:
        for line in fp:
            if '#' not in line:
                u, v = line.split()
                if u not in graph:
                    graph[u] = set()
                graph[u].add(v)
                if v not in graph:
                    graph[v] = set()
    return graph

def fill_incoming(graph):
    global incoming
    incoming = {k: set() for k, _ in graph.items()}
    for u, nbrs in graph.items():
        for v in nbrs:
            if u not in incoming[v]:
                incoming[v].add(u)

def standardize(ws2dgraph):
    return {k: v['list'] for k,v in ws2dgraph.items()}

def toUndirect(directGraph):
    dcopy = copy.deepcopy(directGraph)
    if type(dcopy.values()[0]) is set:
        ugraph = dcopy
    elif type(dcopy.values()[0]) is list:
        ugraph = {k:set(v) for k, v in dcopy.items()}

    for u in ugraph.keys():
        for v in ugraph[u]:
            if v not in ugraph:
                ugraph[v] = set()
            if u not in ugraph[v]:
                ugraph[v].add(u)
    return ugraph

def randomDirectGraph(n, p):
    graph = {}
    for i in xrange(n): #we represent a graph as a list of adjacency lists
        graph[i] = []
    for i in xrange(n):
        for j in xrange(n):
            if i == j:
                continue
            r = random.random()
            if r <= p:
                graph[i].append(j) #graph is directed, thus we don't need to add the other edge (j, i)
    return graph

def randomDirectBalancedGraph(n, p, edges):
    graph = {i: [] for i in xrange(n)}
    while edges > 0:
            while True:
                v1 = random.randint(0, n-1)
                v2 = random.randint(0, n-1)
                if (v1 != v2) and v2 not in graph[v1]:
                    break
            # random graph property
            r = random.random()
            if r <= p:
                graph[v1].append(v2)
                edges -= 1
    return graph

def countTriangles(graph):
    triangles = 0
    for c in itertools.combinations(graph.keys(), 3):
        for x in itertools.permutations(c):
            if x[1] in graph[x[0]] and x[2] in graph[x[1]] and x[2] in graph[x[0]]:
                triangles += 1
                break
    return triangles

def countEdges(graph):
    edges = 0
    for k in graph.keys():
        edges += len(graph[k])
    return edges

def diameter(graph):
    n = len(graph)
    diameter = -1
    for i in graph.keys(): #check the max distance for every node i
        visited = [] #keep a list of visited nodes to check if the graph is connected
        max_distance = 0 #keep the max distance from i
        ###BFS###
        queue = [i]
        distance = dict()
        for j in graph.keys():
            distance[j] = -1
        distance[i] = 0
        while queue != []:
            s = queue.pop(0)
            visited.append(s)
            for j in graph[s]:
                if distance[j] < 0:
                    queue.append(j)
                    distance[j] = distance[s] + 1
                    if distance[j] > max_distance:
                        max_distance = distance[j]
        ###END###
        if len(visited) < n: #graph is not connected
            break
        elif max_distance > diameter:
            diameter = max_distance
    return diameter


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
                        if i + x < line and j + y < line and (i+x)*line+(j+y) not in graph[i*line+j]:
                            graph[i*line+j].add((i+x)*line+(j+y))
                            m -= 1
                            if m == 0:
                                return graph
                            # We do not consider(i+x,j-y) (i-x,j+y) and (i-x,j-y) since the edge between these nodes and (i,j) has been already added at previous iterations

            #For each node u, we add a node to k randomly chosen nodes
            weak_ties = random.choice(k)
            while weak_ties > 0:
                xt = random.randint(0, line-1)
                yt = random.randint(0, line-1)
                if xt*line+yt > n-1:
                    continue
                if xt != i and yt != j and random.random() <= (1/(euclidean_distance((xt, yt), (i,j))**q)):
                    #break
                    graph[i*line+j].add(xt*line+yt)
                    m -= 1
                    weak_ties -= 1
                    if m == 0:
                        return graph
    return graph

def euclidean_distance(a, b):
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2)**(0.5)

def WS2DGraph(n, m, r, k):
    '''
    @param n: number of nodes
    @param m: number of edges
    @param r: radius
    @param k: number of random edges [list] e.g. [0, 5, 10]
    '''
    line = int(math.sqrt(n))
    graph = dict()
    #Initialization
    for i in range(n):
        x = random.random()
        y = random.random()
        graph[i] = dict()
        graph[i]["x"] = x*line
        graph[i]["y"] = y*line
        graph[i]["list"] = set()


    #For each node u, we add an edge to each node at distance at most r from u
    while m > 0:
        i = random.randint(0, n-1)
        if not graph[i]['list']:
            for j in range(n):
                dist = math.sqrt((graph[i]["x"]-graph[j]["x"])**2 + (graph[i]["y"]-graph[j]["y"])**2) # Euclidean distance between i and j

                if dist <= r and i != j and j not in graph[i]["list"]:
                    graph[i]["list"].add(j)
                    m -= 1
                    if m == 0:
                        break

            #For each node u, we add a node to k randomly chosen nodes
            weak_ties = random.choice(k)
            while weak_ties > 0:
                s = random.randint(0,n-1)
                if s == i or s in graph[i]["list"]:
                    continue
                graph[i]["list"].add(s)
                m -= 1
                weak_ties -= 1
                if m == 0:
                    break

    return graph

def Page_Rank(graph, alpha=0.85, max_iter=150, eps=1.0e-5):
    # INIT
    keys = graph.keys()
    N = len(keys)
    alpha_on_N = alpha / N
    one_minus_alpha = 1.0 - alpha
    pr = dict.fromkeys(keys, 1.0/N)

    # ITERATE PAGE RANK
    i = 0
    while True:
        pr_last = copy.deepcopy(pr)
        
        for u in keys:
            # Calculate u's Page Rank
            pr[u] = (one_minus_alpha) * sum([(pr_last[v] / len(graph[v]) ) + alpha_on_N for v in incoming[u]])

        # Max value
        s = max(pr.values())
              
        # normalize to 1
        pr.update((k, float(v) / s) for k, v in pr.items())
        
        # Summation of differences: new - previous
        err = sum([abs(pr[u] - pr_last[u]) for u in keys])
        
        if err < eps:
            break
        if i > max_iter:
            raise Exception('Exceeded max number of iterations. Last error margin: %f' % err)
        i += 1

    return pr, i+1, err

def Independent_Cascade(graph, seeds, rounds=0):
    # INIT
    A = set(seeds) # adopters
    neg_A = set(graph.keys()) - A # not influenced indivuduals set
    S = A # recent adopters
    i = 1 # iterations

    # DIFFUSE
    while True:
        S = IC_round(graph, A, neg_A, S)
        if not S:
            break
        A |= S # A = A U S
        neg_A -= S
        i += 1
        if rounds and i > rounds:
            break

    return A, neg_A, i


def IC_round(graph, adopters, others, recents):
    N = set() # new adopters
    for u in recents: # each node u in S
        for v in graph[u]: # tries to influence each neighbor v in neg_A
            if v in others:
                deg_v = len(graph[v]) + len(incoming[v])
                if random.random() <= 1.0 / deg_v: # higher degree(v) means that v has to adopt the feature
                    N.add(v)
    return N
