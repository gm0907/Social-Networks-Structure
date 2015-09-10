
# coding: utf-8

# # Generalized Watts-Strogatz direct graph on grid with clustering exponent *q* = 2

# In[1]:
import sys
# get_ipython().magic('matplotlib inline')
import random
# import matplotlib.pyplot as plt
from dgraph import standardize
from lesson1 import averageClustering as ac
from dgraph import countEdges
from lesson4 import topk
from lesson4 import betweenness
from lesson5 import eigenvector_centrality as ec
from mod_genws import GenWSGridGraph
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




# In[5]:
print '# Cascade Expansion on Generalized Watts-Strogatz Graphs'
NODES = 7056
edges = random.randint(75000, 125000)
radius = 2
weak_ties = [i*5 for i in xrange(0, 3)]



# ##Create a generalized Watts-Strogatz direct graph on grid with clustering exponent *q* = 2

# In[6]:

g = GenWSGridGraph(NODES, edges, radius, weak_ties)
print '# Edges %d\tAverage Clustering = %f' % (countEdges(g)*2,ac(und(g)))
fi(g) # Fill incoming edges dictionary


# ## Execute centrality measures

# In[12]:

print '# Page Rank execution...'
pagerank, iterations, err = pr(g, alpha=1.0e-5, eps=1.0e-3)
print '#',iterations, ' iterations. Error:', err
top_pr = [a for a,b in topk(pagerank, NODES)]


# In[13]:

print '# Eigenvector Centrality...',
ecscores, _ = ec(g)
top_eigenc = [a for a, b in topk(ecscores, NODES)]
print '# Done'


# In[14]:

print '# Betweennes centrality...',
bet = betweenness(g)
top_bet = [a for a, b in topk(bet, NODES)]
print '# Done'

# ## Execute Independent Cascade Model

seed = [i for i in xrange(200, 7001, 200)]

print '# Page Rank\tEigenvector\tBetweenness'
i = 0
while True:
    max_pr_ad = independent_cascade(g, top_pr[:seed[i]], 'Page Rank')
    max_eigenc_ad = independent_cascade(g, top_eigenc[:seed[i]], 'Eigenvector')
    max_bet_ad = independent_cascade(g, top_bet[:seed[i]], 'Betweenness')

    # In[28]:
    print '%d %d\t%d %d\t%d %d' % (seed[i], max_pr_ad, seed[i], max_eigenc_ad, seed[i], max_bet_ad)
    sys.stdout.flush()

    if i == len(seed)-1 or max_pr_ad >= NODES or max_eigenc_ad >= NODES or max_bet_ad >= NODES:
        break

    i += 1