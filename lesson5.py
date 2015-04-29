def eigenvector_centrality(graph, epsilon = 0.001):
	cscores = list()
	diff_sum = 0xFFFFFFFF

	for node in graph:
		cscores.append(1)

	while (diff_sum >= epsilon):

		old_cscores_summation = sum(cscores)
		# print 'old_cscores_summation', old_cscores_summation
		tmp = dict()
		for node in graph:
			tmp[node] = cscores[node]

			for neigh in graph[node]:
				tmp[node] += cscores[neigh]


		max_neigh_cscore = max(tmp.values())
		# print tmp, max_neigh_cscore
		for node in graph:
			cscores[node] = float(tmp[node]) / float(max_neigh_cscore)

		diff_sum = abs(sum(cscores) - old_cscores_summation)

	return cscores, diff_sum