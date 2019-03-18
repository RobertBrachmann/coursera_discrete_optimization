#!/usr/bin/python
# -*- coding: utf-8 -*-

# from week_2_graph_coloring.gurobi_model import graph_coloring
from week_2_graph_coloring.greedy_networkx import greedy_networkx

class Node(object):

    def __init__(self, node_id):
        self.id = node_id
        self.edges = []
        self.color = None

    def __str__(self):
        return "Node:   {node} \n" \
               "Edges:  {edges} \n" \
               "Color:  {color} \n".format(
                    node=self.id,
                    edges=self.edges,
                    color=self.color
                )


def heuristic(node_objs):
    """
    Simple heuristic for graph coloring problem
    :param node_objs: list
    :return: objective value, optimality (0), solution
    """

    # colors
    colors = [0]

    # sort by density
    node_objs.sort(key=lambda n: len(n.edges))

    # assign each node
    for node in node_objs:
        # check color of neighbours
        for color in colors:
            neighbour_colors = [neighbour.color if neighbour.id in node.edges else None for neighbour in node_objs]
            if color not in neighbour_colors:
                # assign color if no neighbour has color
                node.color = color
                break
            else:
                # create new color
                new_color = max(colors) + 1
                node.color = new_color
                colors.append(new_color)
                break

    objective_value = len(colors)
    optimality = 0

    # sort nodes by id
    node_objs.sort(key=lambda n: n.id)
    solution = [node.color for node in node_objs]

    # for node in node_objs:
    #     print(node)

    return objective_value, optimality, solution


def solve_it(data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = data.split('\n')

    first_line = lines[0].split()
    edge_count = int(first_line[1])

    edges = []
    nodes = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        nodes.append(int(parts[0]))
        nodes.append(int(parts[1]))
        edges.append((int(parts[0]), int(parts[1])))

    # remove duplicates
    nodes = list(set(nodes))
    node_objs = []

    # create list of node objects
    for node in nodes:
        tmp_node = Node(node)
        for edge in edges:
            if edge[0] == node:
                tmp_node.edges.append(edge[1])
            if edge[1] == node:
                tmp_node.edges.append(edge[0])
        node_objs.append(tmp_node)

    # run heuristic
    # objective_value, optimality, solution = heuristic(node_objs)

    # greedy networkx
    objective_value, optimality, solution = greedy_networkx(len(nodes), edges)

    # run gurobi model
    # objective_value, optimality, solution = graph_coloring(nodes, edges)

    # prepare the solution in the specified output format
    output_data = str(objective_value) + ' ' + str(optimality) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  '
              'Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')
