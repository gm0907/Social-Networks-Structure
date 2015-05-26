#!/usr/bin/python
# dgraph.py >>> Directed graph
import random

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
	for i in graph.keys():
		for j in graph[i]:
			for k in graph[j]:
				if k in graph[i]:
					triangles += 1
	return int(triangles/6)

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