#!/usr/bin/python

def eigenvector_centrality(graph, epsilon = 0.001):
	cscores = dict.fromkeys(graph.keys(), 1)
	diff_sum = 0xFFFFFFFF
	keys = graph.keys()
	i = 0
	while (diff_sum >= epsilon):
		# print i, '. eigenvector_centrality: current error = ', diff_sum
		old_cscores_summation = sum(cscores.values())
		# print 'old_cscores_summation', old_cscores_summation
		tmp = {}
		for node in keys:
			tmp[node] = cscores[node]

			for neigh in graph[node]:
				tmp[node] += cscores[neigh]


		max_neigh_cscore = max(tmp.values())
		# print tmp, max_neigh_cscore
		for node in keys:
			cscores[node] = float(tmp[node]) / float(max_neigh_cscore)

		diff_sum = abs(sum(cscores.values()) - old_cscores_summation)
		i += 1

	return cscores, diff_sum