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
with open('small.txt') as file:
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

print(f"n={n}, k1={k1}, k2={k2}, C1={C1}, C2={C2}, L={L}")
print(f"demand: {demand}")
print(f"dist[0,5]={dist[0,5]:.3f}")


