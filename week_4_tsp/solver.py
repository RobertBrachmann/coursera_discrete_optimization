#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from collections import namedtuple
from sklearn.cluster import KMeans

Point = namedtuple("Point", ['i', 'c', 'x', 'y'])


def length(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


def greedy_cluster_heuristic(points):

    obj = 0
    opt = 0
    solution = []

    # cluster point
    cluster = KMeans(n_clusters=math.ceil(len(points)/5)).fit(points).labels_

    # create nodes
    nodes = []
    for i, point in enumerate(points):
        nodes.append(Point(i, cluster[i], point[0], point[1]))
    nodes = sorted(nodes, key=lambda p: cluster[p.i])

    # calculation objective
    for i, node in enumerate(nodes):
        solution.append(node.i)
        if i == len(nodes) - 1:
            obj += length(node, nodes[0])
        else:
            obj += length(node, nodes[i + 1])

    return obj, opt, solution


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

    # calculate the length of the tour
    obj, opt, solution = greedy_cluster_heuristic(points)

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

