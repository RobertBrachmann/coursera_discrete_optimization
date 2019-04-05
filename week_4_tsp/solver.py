#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import random
from collections import namedtuple
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from week_4_tsp.gurobi_model import tsp
from week_4_tsp.genetic_algorithm import tsp_gen

Point = namedtuple("Point", ['index','i', 'x', 'y'])


def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)


class Node(object):

    def __init__(self, i, x, y):
        self.i = i
        self.x = x
        self.y = y


def greedy_cluster_heuristic(points):

    # instance size
    n = len(points)
    print("Instance with n={n}".format(n=n))

    # create nodes
    nodes = []
    for i, point in enumerate(points):
        nodes.append(Node(i, point[0], point[1]))

    # sort nodes
    nodes.sort(key=lambda j: (j.x, j.y))
    # create index
    index = []
    for i, node in enumerate(nodes):
       index.append(node.i)

    # create solution
    kn = min(50, n)
    solution = [0]
    while len(index) > 1:

        # get last node
        current_index = solution[len(solution) - 1]

        # get k neighbours
        neighbours = []
        for k in range(0, min(kn, len(index))):
            neighbours.append(random.choice(index))

        # get nearest neighbour
        nearest_neighbour = neighbours[0]
        distance = 1e+9
        for neighbour in neighbours:
            new_distance = length(nodes[current_index], nodes[neighbour])
            if new_distance < distance:
                nearest_neighbour = neighbour

        # add to solution
        index.remove(nearest_neighbour)
        solution.append(nearest_neighbour)

    # calculate solution
    obj = 0
    opt = 0
    solution_nodes = []
    for i, index in enumerate(solution):
        solution_nodes.append(nodes[index].i)
        if i == len(nodes) - 1:
            obj += length(nodes[index], nodes[0])
        else:
            obj += length(nodes[index], nodes[solution[i + 1]])

    plt.plot([points[solution_nodes[i % len(points)]][0] for i in range(len(points)+1)],
             [points[solution_nodes[i % len(points)]][1] for i in range(len(points)+1)], '.b-')
    plt.show()

    return obj, opt, solution_nodes


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    points = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append([float(parts[0]), float(parts[1])])

    n = len(points)
    if n < 100:
        obj, opt, solution = tsp(points, pop_size=25, generation=50)
    elif n < 200:
        obj, opt, solution = tsp(points, pop_size=20, generation=25)
    elif n < 600:
        obj, opt, solution = tsp(points, pop_size=15, generation=20)
    elif n < 2000:
        obj, opt, solution = tsp(points, pop_size=10, generation=10)
    elif n >= 2000:
        obj, opt, solution = tsp(points, pop_size=5, generation=5)

    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


import sys
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')

