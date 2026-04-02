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
with open('xxxl.txt') as file:
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

# This function takes in a cluster and computes the demand location that mimimizes weighted distance to
# each other demand location in the cluster
def compute_center(cluster):
    best = None
    best_cost = float('inf')
    for v in cluster:
        cost = sum(demand[i] * dist[v, i] for i in cluster)
        if cost < best_cost:
            best_cost = cost
            best = v
    return best

# Cluster function to determine local/regional clusters
def cluster(items, item_demand, k, capacity):
    clusters = {i: [i] for i in items} # each item (demand location/local FC) begins as its own cluster
    cluster_demand = {i: item_demand[i] for i in items}
    incompatible = set()

    while len(clusters) > k:
        # find the two closest clusters by center
        best_pair = None
        best_dist = float('inf')
        for a in clusters:
            for b in clusters:
                if a >= b:
                    continue
                if (a, b) in incompatible:
                    continue
                center_a = compute_center(clusters[a])
                center_b = compute_center(clusters[b])
                d = dist[center_a, center_b]
                if d < best_dist:
                    best_dist = d
                    best_pair = (a, b)

        if best_pair is None:
            break

        a, b = best_pair
        if cluster_demand[a] + cluster_demand[b] <= capacity:
            clusters[a] += clusters[b]
            cluster_demand[a] += cluster_demand[b]
            del clusters[b]
            del cluster_demand[b]
        else:
            incompatible.add((a, b))

    return clusters

it1 = tm.time()

# Phase 1
city_demand = {i: demand[i] for i in nodes} # add the demand of each demand location into a dictionary
local_clusters = cluster(nodes, city_demand, k1, C1) # run the clustering algorithm for phase 1
local_fcs = [compute_center(members) for members in local_clusters.values()] # with the final clusters from phase 1, compute the centers (local FCs)

# Phase 2:

# this basically takes each local FC and sums the demand values of each of the demand locations in the cluster
fc_demand = {fc: sum(demand[i] for i in members) # zip just connects them. so the pair looks like (local FC i, demand locations served by that local FC)
             for fc, members in zip(local_fcs, local_clusters.values())}
regional_clusters = cluster(local_fcs, fc_demand, k2, C2)
regional_fcs = [compute_center(members) for members in regional_clusters.values()]

# compute serving cost (local to demand location)
serving_cost = 0
for fc, members in zip(local_fcs, local_clusters.values()):
    for i in members:
        serving_cost += demand[i] * dist[fc, i]

# compute link cost (regional to local)
link_cost = 0
for regional, locals in regional_clusters.items():
    for v in locals:
        link_cost += L * dist[regional, v]

total_cost = serving_cost + link_cost
it2 = tm.time()

print(f"Time taken: {it2-it1}")
print(f"Heuristic cost: {total_cost}")
print(f"Local FCs: {sorted(local_fcs)}")
print(f"Regional FCs: {sorted(regional_fcs)}")

print(f"\nLocal clusters: {local_clusters}")
print(f"\nRegional clusters: {regional_clusters}")
