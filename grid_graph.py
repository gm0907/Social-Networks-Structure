#!/usr/bin/python

import sys
import random
import math

# n is the number of nodes
# r is the radius
# k is the number of random edges (weak ties)

def WSGridGraph(n, r, k):
	#initialization
	graph = dict()
	for i in range(n):
		for j in range(n):
			graph[i*n+j] = set()

	#for each node, i add an edge to each node at distance at most r
	for i in range(n):
		for j in range(n):
			for x in range(r+1): #horizontal offset
				for y in range(r+1-x): #vertical offset
					if x != 0 or y != 0:
						if i+x<n and j+y<n:
							graph[i*n+j].add((i+x)*n+(j+y))
							graph[(i+x)*n+(j+y)].add(i*n+j)
						if i+x<n and j-y>=0:
							graph[i*n+j].add((i+x)*n+(j-y))
							graph[(i+x)*n+(j-y)].add(i*n+j)

	#for each node, choose k nodes at random and add an edge
	for i in range(n):
		for j in range(n):
			for h in range(k):
				s = random.randint(0,n*n-1)
				if s not in graph[i*n+j]:
					graph[i*n+j].add(s)
					graph[s].add(i*n+j)

	return graph


n = int(sys.argv[1])
r = int(sys.argv[2])
k = int(sys.argv[3])
print(WSGridGraph(n,r,k))