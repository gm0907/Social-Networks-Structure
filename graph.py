import random
import itertools

# ASSIGNMENT
# fare proc per indice di clustering
# 50 run
# 	- medie e grafico con indice di clustering
# 	- n = 100, p = [0.1, .., 1] +0.15

class Graph:
	nodes = []

	def add_edge(self, i, j):
		self.nodes[i].add_neighb(self.nodes[j])
		self.nodes[j].add_neighb(self.nodes[i])

	def random_graph(self, n, p):
		for x in xrange(n):
			self.nodes.append(Node(x))

		pairs = list(itertools.combinations(xrange(n), 2))
		for pair in pairs:
			r = random.random()
			if r >= p:
				self.add_edge(pair[0], pair[1])
		return self

	def count_triangles(self):
		triangles = 0
		n = len(self.nodes)
		for x in xrange(n):
			for y in xrange(x+1, n):
				for z in xrange(y+1, n):
					if (self.nodes[x] in self.nodes[y].neighbors) and (self.nodes[y] in self.nodes[z].neighbors) and (self.nodes[z] in self.nodes[x].neighbors):
						triangles += 1
		return triangles

	def average_clustering(self):
		n = len(self.nodes)
		total = 0
		for i in self.nodes:
			triangles = 0
			neigh_pairs = (len(i.neighbors)*(len(i.neighbors)-1))/2 #number of pairs of neighbors of node i
			for j in i.neighbors:
				for k in i.neighbors:
					if k in j.neighbors:
						triangles += 1 #number of pairs of neighbors of node i that are adjacent
			if neigh_pairs > 0:
				total += triangles/neigh_pairs # triangles/neighbors is the individual clustering of node i
		return total/n #the average clustering is the average of individual clusterings

	def diameter(self):
		n = len(self.nodes)
		diameter = -1

		for i in self.nodes: #check the max distance for every node i
			visited = [] #keep a list of visited nodes to check if the graph is connected
			max_distance = 0 #keep the max distance from i
			###BFS###
			queue = [i]
			distance = {}
			for j in self.nodes:
				distance[j] = 0
			while queue != []:
				s = queue.pop()
				visited.append(s)
				for j in s.neighbors:
					if distance[j] <= 0:
						queue.append(j)
						distance[j] = distance[s] + 1
						if distance[j] > max_distance:
								max_distance = distance[j]
			###END###
			if len(visited) < n: #graph is not connected
				break
			else:
				diameter = max_distance
		return diameter

	def print_graph(self):
		for n in self.nodes:
			print 'Node ',n.value,': ', [x.value for x in n.neighbors]

class Node:
	def __init__(self, v):
		self.value = v
		self.neighbors = []

	def add_neighb(self, node):
		self.neighbors.append(node)

	def print_neighbors(self):
		for n in self.neighbors:
			print n.value


#############################################################################
n = 25
p = 0.3

g = Graph().random_graph(n, p)
# g.print_graph()
print 'Triangles: ', g.count_triangles()
print 'Diameter: ', g.diameter()
print 'Average Clustering: ', g.average_clustering()
