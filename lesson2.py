#!/usr/bin/python

def countEdges(graph):
	edges = 0
	for k in graph:
		edges += len(graph[k])
	return edges/2