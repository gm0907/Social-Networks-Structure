
# coding: utf-8

# # Watts-Strogatz direct graph on the 2-dimensional space

# In[1]:
import sys
# get_ipython().magic('matplotlib inline')
import random
# import matplotlib.pyplot as plt
from dgraph import readGraph
from dgraph import standardize
from dgraph import Page_Rank as pr
from dgraph import fill_incoming as fi
from dgraph import Independent_Cascade as ic
from dgraph import GenWSGridGraph as genWS
from dgraph import WS2DGraph as WS2D
from lesson4 import topk
from lesson5 import eigenvector_centrality as ec
from lesson4 import betweenness
from lesson1 import averageClustering as ac
from dgraph import countEdges
from dgraph import toUndirect as und


# In[2]:

def independent_cascade(graph, seed, centrality):
    adopters, haters, steps = ic(g, seed)
    # print 'Independent Cascade Model: TOP %d %s' % (len(seed), centrality)
    # print '\tFinal Adopters:\t', len(adopters)
    # print '\tFinal Haters:\t', len(haters)
    # print '\t# Iterations:\t', steps
    return len(adopters), len(haters)

print '# Cascade Expansion Watts-Strogatz Graphs'

NODES = 7115
edges = random.randint(75000, 125000)
radius = 2
weak_ties = [i*5 for i in xrange(0, 4)]
seed = 100


# ##Create a Watts-Strogatz 2D direct graph

# In[4]:

g = standardize(WS2D(NODES, edges, radius, weak_ties))
print '# Edges %d\tAverage Clustering = %f' % (countEdges(g)*2,ac(und(g)))
fi(g) # Fill incoming edges

sys.stdout.flush()


# ## Execute centrality measures

# In[5]:

print '# Page Rank execution...'
pagerank, iterations, err = pr(g, alpha=1.0e-5, eps=1.0e-3)
print '#',iterations, ' iterations. Error:', err
top_pr = [a for a,b in topk(pagerank, NODES)]


# In[6]:

print '# Eigenvector Centrality...',
cscores, diffsum = ec(g)
top_eigenc = [a for a, b in topk(cscores, NODES)]
print '# Done'


# In[7]:

print '# Betweennes centrality...',
bet = betweenness(g)
top_bet = [a for a, b in topk(bet, NODES)]
print '# Done'

sys.stdout.flush()
# In[3]:
# ## Execute Independent Cascade Model

seed = [i for i in xrange(200, 7001, 200)]

print '# Page Rank\tEigenvector\tBetweenness'
i = 0
while True:
    max_pr_ad, pr_haters = independent_cascade(g, top_pr[:seed[i]], 'Page Rank')
    max_eigenc_ad, eigenc_haters = independent_cascade(g, top_eigenc[:seed[i]], 'Eigenvector')
    max_bet_ad, bet_haters = independent_cascade(g, top_bet[:seed[i]], 'Betweenness')

    # In[28]:
    print '#Haters: %d %d %d' % (pr_haters, eigenc_haters, bet_haters)
    print '%d %d\t%d %d\t%d %d' % (seed[i], max_pr_ad, seed[i], max_eigenc_ad, seed[i], max_bet_ad)
    sys.stdout.flush()

    if i == len(seed)-1 or max_pr_ad >= nodes or max_eigenc_ad >= nodes or max_bet_ad >= nodes:
        break

    i += 1