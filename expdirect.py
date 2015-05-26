from dgraph import randomDirectedGraph as randDGraph
from dgraph import countTriangles
from dgraph import diameter
g = randDGraph(10, 0.3)

print g
print 'Triangles:', countTriangles(g)
print 'Diameter:', diameter(g)