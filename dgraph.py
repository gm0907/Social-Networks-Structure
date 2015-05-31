#!/usr/bin/python
# dgraph.py >>> Directed graph
import random
import itertools

def randomDirectedGraph(n, p):
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

# def countTriangles(graph):
# 	triangles = {}
# 	for i in graph.keys():
# 		for j in graph[i]:
# 			for k in graph[j]:
# 				if k in graph[i]:
# 					vert = ''.join(sorted([str(i), str(j), str(k)]))
# 					try:
# 						triangles[vert]
# 					except KeyError:
# 						triangles[vert] = None
# 	return len(triangles.keys())

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