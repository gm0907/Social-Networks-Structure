#!/usr/bin/python

import random
import math

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
				graph[v].add(u)
	return graph

def count2Paths(graph):
	twopaths = 0
	for i in graph.keys():
		for j in graph[i]:
			for k in graph[j]:
				if k != i:
					twopaths += 1
	return int(twopaths/2)

def diameter(graph):
  n = len(graph)
  diameter = 0
  nodes = 0
  edges = 0
  for i in graph.keys(): #check the max distance for every node i
    visited = [] #keep a list of visited nodes to check if the graph is connected
    max_distance = 0 #keep the max distance from i
    tmp_edges = 0
    ###BFS###
    queue = [i]
    distance = dict()
    for j in graph.keys():
      distance[j] = -1
    distance[i] = 0
    while queue != []:
      s = queue.pop(0)
      visited.append(s)
      tmp_edges += len(graph[s])
      for j in graph[s]:
        if distance[j] < 0:
          queue.append(j)
          distance[j] = distance[s] + 1
          if distance[j] > max_distance:
            max_distance = distance[j]
    ###END###
    if len(visited) > nodes: #graph is not connected
    	nodes = len(visited)
    	edges = tmp_edges / 2
    if max_distance > diameter:
      diameter = max_distance
  return nodes, edges, diameter