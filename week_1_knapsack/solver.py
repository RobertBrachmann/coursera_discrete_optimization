#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight', 'ratio'])


def value_weight_heuristic(items, capacity):
    """
    Heuristic based on value-weight-ratio
    :param items:
    :param capacity:
    :return:
    """

    # variables
    value = 0
    weight = 0
    taken = [0] * len(items)
    opt = 0
    items_w_ratio = []

    # calculate ratio
    for item in items:
        items_w_ratio.append(Item(
            index=item.index,
            value=item.value,
            weight=item.weight,
            ratio=item.value / item.weight
        ))

    # sort items by ratio
    items_w_ratio.sort(key=lambda i: i.ratio, reverse=True)

    print(capacity, items_w_ratio)

    for item in items_w_ratio:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight

    return value, weight, taken, opt


def linear_relaxation(items):
    """
    Relaxes capacity constraint and calculates optimistic estimation
    :param items: list of items
    :return: optimistic estimation
    """

    # optimistic estimation
    estimation = 0

    # sum all values
    for item in items:
        estimation += item.value

    return estimation




def solve_it(input_instance):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_instance.split('\n')

    first_line = lines[0].split()
    item_count = int(first_line[0])
    capacity = int(first_line[1])

    # get data
    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1]), 0.0))

    # first greedy heuristics
    value, weight, taken, opt = value_weight_heuristic(items, capacity)

    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(opt) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        print(sys.argv)
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  '
              'Please select one from the data directory. '
              '(i.e. python solver.py ./data/ks_4_0)')


