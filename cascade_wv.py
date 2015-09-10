
# coding: utf-8

# # Wiki Vote Direct Graph

# In[1]:

# get_ipython().magic('matplotlib inline')
import sys
import random
import copy
# import matplotlib.pyplot as plt
from dgraph import readGraph
from lesson1 import averageClustering as ac
from dgraph import countEdges
from lesson4 import topk
from lesson4 import betweenness
from lesson5 import eigenvector_centrality as ec
from dgraph import randomDirectBalancedGraph as rdbg
from dgraph import Page_Rank as pr
from dgraph import fill_incoming as fi
from dgraph import Independent_Cascade as ic
from dgraph import toUndirect as und


# In[2]:

def independent_cascade(graph, seed, centrality):
    adopters, haters, steps = ic(g, seed)
    # print 'Independent Cascade Model: TOP %d %s' % (len(seed), centrality)
    # print '\tFinal Adopters:\t', len(adopters)
    # print '\tFinal Haters:\t', len(haters)
    # print '\t# Iterations:\t', steps
    return len(adopters)


# ## Set Parameters

# In[3]:



# ##Read the wiki-vote graph

# In[4]:

g = readGraph('wiki-Vote.txt')
nodes = len(g.keys())

print '# Cascade Expansion Wiki-Vote.txt'
print '# Edges = %d\tAverage Clustering = %f'% (countEdges(g), ac(und(g)))
fi(g) # Fill incoming edges dictionary


sys.stdout.flush()

# ## Execute centrality measures

# In[8]:

print '# Page Rank execution...'
pagerank, iterations, err = pr(g, alpha=1.0e-5, eps=1.0e-3)
print '#',iterations, ' iterations. Error:', err
top_pr = [a for a,b in topk(pagerank, nodes)]


# In[9]:

print '# Eigenvector Centrality...',
cscores, diffsum = ec(g)
top_eigenc = [a for a, b in topk(cscores, nodes)]
print '# Done'


# In[10]:

print '# Betweennes centrality...',
bet = betweenness(g)
top_bet = [a for a, b in topk(bet, nodes)]
print '# Done'

sys.stdout.flush()

# ## Execute Independent Cascade Model

seed = [i for i in xrange(200, nodes - 100, 200)]

print '# Page Rank\tEigenvector\tBetweenness'
i = 0
while True:
    max_pr_ad = independent_cascade(g, top_pr[:seed[i]], 'Page Rank')
    max_eigenc_ad = independent_cascade(g, top_eigenc[:seed[i]], 'Eigenvector')
    max_bet_ad = independent_cascade(g, top_bet[:seed[i]], 'Betweenness')

    # In[28]:
    print '%d %d\t%d %d\t%d %d' % (seed[i], max_pr_ad, seed[i], max_eigenc_ad, seed[i], max_bet_ad)
    sys.stdout.flush()

    if i == len(seed)-1 or max_pr_ad >= nodes or max_eigenc_ad >= nodes or max_bet_ad >= nodes:
        break

    i += 1