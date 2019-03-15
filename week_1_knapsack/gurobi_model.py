#!/usr/bin/python

# Copyright 2018, Gurobi Optimization, LLC

# This example formulates and solves the following simple MIP model:
#  maximize
#        x +   y + 2 z
#  subject to
#        x + 2 y + 3 z <= 4
#        x +   y       >= 1
#  x, y, z binary

from gurobipy import *


def knapsack(items, capacity):

    try:

        # Create a new model
        m = Model("knapsack ip")

        # Create variables
        x = m.addVars(len(items), vtype=GRB.BINARY, name="X")

        # Set objective
        m.setObjective(sum(x[i] * items[i].value for i in x), GRB.MAXIMIZE)

        # Add constraints
        m.addConstr(sum(x[i] * items[i].weight for i in x) <= capacity)

        m.optimize()

        solution = []
        obj_value = int(m.objVal)
        status = 0

        if m.status == GRB.Status.OPTIMAL:
            status = 1

        for v in m.getVars():
            if v.x == 1.0:
                solution.append(1)
            else:
                solution.append(0)

        return obj_value, status, solution

    except GurobiError as e:
        print('Error code ' + str(e.errno) + ": " + str(e))

    except AttributeError:
        print('Encountered an attribute error')
