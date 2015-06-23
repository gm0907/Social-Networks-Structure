#!/usr/bin/python
# dgraph.py >>> Directed graph

import random
import itertools
import copy

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
	fill_incoming(graph)
	return graph

def fill_incoming(graph):
	global incoming
	incoming = dict.fromkeys(graph.keys(), set())
	for u in graph.keys():
		for v in graph[u]:
			incoming[v].add(u)

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


# n is the number of nodes
# r is the radius of each node (a node u is connected with each other node at distance at most r) - strong ties
# k is the number of random edges for each node u - weak ties
def GenWSGridGraph(n, r, k, q=2):
	line = int(math.sqrt(n))
	graph = dict()
	#Initialization
	for i in range(line): #i represents the grid row
		for j in range(line): #j represents the grid coloumn
			graph[i*line+j] = set() #Each node is identified by a number in [0, n - 1]

	#For each node u, we add an edge to each node at distance at most r from u
	for i in range(line):
		for j in range(line):
			for x in range(r+1): # x is the horizontal offset
				for y in range(r+1-x): # y is the vertical offset. The sum of offsets must be at most r
					if x + y > 0: # The sum of offsets must be at least 1
						if i + x < line and j + y < line:
							graph[i*line+j].add((i+x)*line+(j+y))
							graph[(i+x)*line+(j+y)].add(i*line+j)
							# We do not consider(i+x,j-y) (i-x,j+y) and (i-x,j-y) since the edge between these nodes and (i,j) has been already added at previous iterations

			#For each node u, we add a node to k randomly chosen nodes
			for h in range(k):
				xs = random.randint(0, line)
				ys = random.randint(0, line)
				if xs != i and xy != j and random.random() <= euclidian_distance((xs, ys), (i,j))**q:
					graph[i*line+j].add(s)
					# graph[s].add(i*line+j)
	return graph

def euclidian_distance(a, b):
	return ((a[0] - b[0])**2 + (a[1] - b[1])**2)**(0.5)
# s / line + (s - (s/line)*line)
# 2 ; 2
# n is the number of nodes
# r is the radius
# k is the number of random edges
def WS2DGraph(n, r, k):
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
	for i in range(n):
		for j in range(i+1,n):
			dist=math.sqrt((graph[i]["x"]-graph[j]["x"])**2 + (graph[i]["y"]-graph[j]["y"])**2) # Euclidean distance between i and j
			if dist <= r:
				graph[i]["list"].add(j)
				graph[j]["list"].add(i)

		#For each node u, we add a node to k randomly chosen nodes
		for h in range(k):
			s = random.randint(0,n-1)
			if s != i:
				graph[i]["list"].add(s)
				graph[s]["list"].add(s)
	return graph

def Page_Rank(graph, alpha=0.85, max_iter=100, eps=1.0e-8):
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
			# pr[u] = (one_minus_alpha / N) + alpha * sum([(pr_last[v] / len(graph[v])) for v in incoming[u]]) # standard formula
			pr[u] = (one_minus_alpha) * sum([(pr_last[v] / len(graph[v]) ) + alpha_on_N for v in incoming[u]])

		# normalize to 1
		s = float(sum(pr.values()))
		# print s
		pr.update((k, float(v) / s) for k, v in pr.items())

		# CHECK
		err = sum([abs(pr[u] - pr_last[u]) for u in keys])
		if err < eps:
			break
		if i > max_iter:
			raise Exception('Exceeded max number of iterations')
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
		A |= S
		neg_A -= S
		i += 1
		if rounds and i > rounds:
			break

	return A, neg_A, i


def IC_round(graph, adopters, others, recents):
	N = set() # new adopters
	for u in recents: # each node u in S
		for v in graph[u]:
			if v in others:
				deg_v = len(graph[v]) + len(incoming[v])
				if random.random() >= 1.0 / deg_v: # higher degree(v) means that v has to adopt the feature
					N.add(v)
	return N
