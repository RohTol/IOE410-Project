from gurobipy import *
from itertools import product
import random
import time as tm
import math

cities = {}
coordinates = {}
demand = {}

# Here we read our input file. First line of the file contains the number of locations, k1, k2, C1, C2, and L.
# There are n = number of locations lines after the first.
# These have the location index, coordinates, and demand of each location.
with open('large.txt') as file:
    first = next(file).split()
    n, k1, k2, C1, C2, L = int(first[0]), int(first[1]), int(first[2]), int(first[3]), int(first[4]), float(first[5])

    for _ in range(n):
        line = next(file).split()
        i = int(line[0])
        coordinates[i] = (float(line[1]), float(line[2]))
        demand[i] = int(line[3])

nodes = range(n)

# Here we compute the Euclidean distance between each location and put it into a distance matrix.
# We define a function to compute Euclidean distance below
def euclidean(i, j):
    xi, yi = coordinates[i]
    xj, yj = coordinates[j]
    return math.sqrt((xi - xj)**2 + (yi - yj)**2)

dist = {}
for i in nodes:
    for j in nodes:
        dist[i, j] = euclidean(i, j)



# Now, we build the actual model
it1 = tm.time()
IPmod = Model("fulfillment centers")

# We first define all of our decision variables
x = IPmod.addVars(nodes, vtype=GRB.BINARY, name="x")
y = IPmod.addVars(nodes, vtype=GRB.BINARY, name="y")
z = IPmod.addVars(nodes, nodes, vtype=GRB.BINARY, name="z")
w = IPmod.addVars(nodes, nodes, vtype=GRB.BINARY, name="w")
q = IPmod.addVars(nodes, nodes, nodes, vtype=GRB.BINARY, name="q")

# Next, we set out objective function
IPmod.setObjective(
    quicksum(L * dist[u,v] * z[u,v] for u in nodes for v in nodes) +
    quicksum(demand[i] * dist[v, i] * w[v, i] for v in nodes for i in nodes),
    GRB.MINIMIZE
)

# Next, we list our constraints:
# 1. Each local FC v must be connected to exactly 1 regional FC if open, and 0 if closed
for v in nodes:
    IPmod.addConstr(quicksum(z[u, v] for u in nodes) == x[v])

# 2. Each demand location i must be connected to exactly 1 local FC
for i in nodes:
    IPmod.addConstr(quicksum(w[v, i] for v in nodes) == 1)

# 3. A demand location i can only be assigned to a local FC v if v is open
for v in nodes:
    for i in nodes:
        IPmod.addConstr(w[v, i] <= x[v])

# 4. A local FC v can only be assigned to a regional FC u if u is open
for u in nodes:
    for v in nodes:
        IPmod.addConstr(z[u, v] <= y[u])

# 5. A maximum of k1 local FCs can be opened
IPmod.addConstr(quicksum(x[v] for v in nodes) <= k1)

# 6. A maximum of k2 regional FCs can be opened
IPmod.addConstr(quicksum(y[u] for u in nodes) <= k2)

# 7. The sum of the items processed by local FC v is less than C1
for v in nodes:
    IPmod.addConstr(quicksum(demand[i] * w[v, i] for i in nodes) <= C1)

# 8. The sum of the items processed by regional FC u is less than C2
for u in nodes:
    IPmod.addConstr(quicksum(demand[i] * q[u, v, i] for i in nodes for v in nodes) <= C2)

# 8a, 8b: If at least 1 of w(v, i) or z(u, v) is 0, then q(u, v, i) = 0
# 8c: If both w(v, i) = 1 and z(u, v) = 1, then q(u, v, i) = 1
for u in nodes:
    for v in nodes:
        for i in nodes:
            IPmod.addConstr(q[u, v, i] <= w[v, i]) #8a
            IPmod.addConstr(q[u, v, i] <= z[u, v]) #8b
            IPmod.addConstr(q[u, v, i] >= w[v, i] + z[u, v] - 1) #8c

IPmod.optimize()
it2 = tm.time()

# Finally, we print the output:
print(f"Minimum cost: {IPmod.objVal}")
print(f"Time taken: {it2-it1}")

# Let's figure out which local/regional FCs are open
print(f"Local FCs open: {[v for v in nodes if x[v].x == 1]}")
print(f"Regional FCs open: {[u for u in nodes if y[u].x == 1]}")

# Lastly, let's figure out the assignments:
print("Demand location to Local FC assignments: ")
for i in nodes:
    for v in nodes:
        if w[v, i].x == 1:
            print(f" Demand location {i} --> Local FC {v}")
print("Local FC to Regional FC assignments: ")
for v in nodes:
    for u in nodes:
        if z[u, v].x == 1:
            print(f" Local FC {v} --> Regional FC {u}")








