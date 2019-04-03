import sys
import math
import random
import itertools
from gurobipy import *


def tsp(points):

    # Callback - use lazy constraints to eliminate sub-tours
    def sub_tour_elim(model, where):
        if where == GRB.Callback.MIPSOL:
            # make a list of edges selected in the solution
            vals = model.cbGetSolution(model._vars)
            selected = tuplelist((i, j) for i, j in model._vars.keys() if vals[i, j] > 0.5)
            # find the shortest cycle in the selected edge list
            tour = sub_tour(selected)
            if len(tour) < n:
                # add sub_tour elimination constraint for every pair of cities in tour
                model.cbLazy(quicksum(model._vars[i, j]
                                      for i, j in itertools.combinations(tour, 2))
                             <= len(tour) - 1)

    def sub_tour(edges):
        unvisited = list(range(n))
        cycle = range(n + 1)  # initial length has 1 more city
        while unvisited:  # true if list is non-empty
            thiscycle = []
            neighbors = unvisited
            while neighbors:
                current = neighbors[0]
                thiscycle.append(current)
                unvisited.remove(current)
                neighbors = [j for i, j in edges.select(current, '*') if j in unvisited]
            if len(cycle) > len(thiscycle):
                cycle = thiscycle
        return cycle

    n = len(points)
    dist = {(i, j):
            math.sqrt(sum((points[i][k]-points[j][k])**2 for k in range(2)))
            for i in range(n) for j in range(i)
            }

    m = Model()
    m.setParam("TimeLimit", 180.0)
    # Create variables
    vars = m.addVars(dist.keys(), obj=dist, vtype=GRB.BINARY, name='e')
    for i, j in vars.keys():
        vars[j, i] = vars[i, j]  # edge in opposite direction

    # Add degree-2 constraint
    m.addConstrs(vars.sum(i, '*') == 2 for i in range(n))

    # Optimize model
    m._vars = vars
    m.Params.lazyConstraints = 1
    m.optimize(sub_tour_elim)

    vals = m.getAttr('x', vars)
    selected = tuplelist((i, j) for i, j in vals.keys() if vals[i, j] > 0.5)

    tour = sub_tour(selected)
    print(tour)

    print('')
    print('Optimal tour: %s' % str(tour))
    print('Optimal cost: %g' % m.objVal)
    if m.status == 2:
        opt = 1
    else:
        opt = 0

    return m.objVal, opt, tour
