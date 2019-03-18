from gurobipy import *
from week_2_graph_coloring.greedy_networkx import greedy_networkx


def graph_coloring(nodes, edges, greedy_start=True):

    try:

        m = Model("graph_coloring")

        node_count = len(nodes)
        init_objective_value, init_optimality, init_solution = greedy_networkx(node_count, edges)

        colors = m.addVars(init_objective_value, vtype=GRB.BINARY, name="colors")
        nodes = m.addVars(node_count, init_objective_value, vtype=GRB.BINARY, name="assignments")

        if greedy_start:
            for i in range(init_objective_value):
                colors[i].setAttr("Start", 0)
                for j in range(node_count):
                    nodes[(j, i)].setAttr("Start", 0)

            for i, j in enumerate(init_solution):
                colors[j].setAttr("Start", 1)
                nodes[(i, j)].setAttr("Start", 1)

        m.setObjective(quicksum(colors), GRB.MINIMIZE)

        # each node has only one color
        m.addConstrs((nodes.sum(i, "*") == 1 for i in range(node_count)), name="eq1")

        # only color in use can be assigned ot nodes
        m.addConstrs((nodes[(i, k)] - colors[k] <= 0
                      for i in range(node_count)
                      for k in range(init_objective_value)),
                     name="ieq2")

        # vertices sharing one edge have different colors
        m.addConstrs((nodes[(edge[0], k)] + nodes[(edge[1], k)] <= 1
                      for edge in edges
                      for k in range(init_objective_value)),
                     name="ieq3")

        # color index should be as low as possible
        m.addConstrs((colors[i] - colors[i + 1] >= 0
                      for i in range(init_objective_value - 1)),
                     name="ieq4")

        m.update()
        m.optimize()

        # prepare solution
        sol = [int(var.x) for var in m.getVars()]
        objective_value = sum(sol[:init_objective_value])
        solution = [j for i in range(node_count) for j in range(init_objective_value)
                    if sol[init_objective_value + init_objective_value * i + j] == 1]

        if m.status == 1:
            optimality = 1
        else:
            optimality = 0

        return objective_value, optimality, solution

    except GurobiError as e:
        print('Error code ' + str(e.errno) + ": " + str(e))

    except AttributeError:
        print('Encountered an attribute error')
