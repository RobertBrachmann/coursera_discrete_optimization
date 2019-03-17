#!/usr/bin/python
# -*- coding: utf-8 -*-


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
    pass


def solve_it(data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
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

    for node in nodes:

        tmp_node = Node(node)
        for edge in edges:
            if edge[0] == node:
                tmp_node.edges.append(edge[1])

            if edge[1] == node:
                tmp_node.edges.append(edge[0])

        node_objs.append(tmp_node)

    for node in node_objs:
        print(node)

    # build a trivial solution
    # every node has its own color
    solution = range(0, node_count)

    # prepare the solution in the specified output format
    output_data = str(node_count) + ' ' + str(0) + '\n'
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
