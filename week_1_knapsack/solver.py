#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy
from collections import namedtuple
from timeit import default_timer as timer

Item = namedtuple("Item", ['index', 'value', 'weight', 'ratio'])


class Node(object):

    def __init__(self, v, w, r, e, item_index):
        # node id
        self.id = None
        # value
        self.v = v
        # weight
        self.w = w
        # remaining capacity
        self.r = r
        # estimate
        self.e = e
        # item index
        self.item_index = item_index
        # take item so far
        self.taken_item = []

    def __str__(self):
        return "Node id             {id} \n" \
               "Item id:            {index} \n" \
               "Value:              {value} \n" \
               "Weight:             {weight} \n" \
               "Slack:              {slack} \n" \
               "Estimate:           {estimate} \n" \
               "Taken:              {taken} \n".format(
                    id=self.id,
                    index=self.item_index,
                    value=self.v,
                    weight=self.w,
                    slack=self.r,
                    estimate=self.e,
                    taken=self.taken_item
                )


def branch_and_bound(items, capacity, estimation, search_strategy="df", sorted_by_ratio=False):
    """
    Simple branch and bound algorithm with different search strategies
    :param estimation: optimistic constraint from linear relaxation
    :param capacity: capacity constraint
    :param sorted_by_ratio: sort items by value weight ration if True
    :param items: list of items
    :param search_strategy: df: depth first, bf: best first, ld: least discrepancy
    :return:value, weight, taken, opt, elapsed time
    """
    sys.setrecursionlimit(len(items) * len(items))

    # global variable
    global best_value
    global node_id
    best_value = 0
    node_id = 1

    # variables
    traversed_nodes = []

    def get_next_item(list_of_items, current_item_index):
        """
        Returns Node if existis
        :param current_item_index:
        :param list_of_items:
        :return: Node if exists
        """
        # case: current node is start node
        if current_item_index == -1:
            # return first item
            return Node(v=list_of_items[0].value,
                        w=list_of_items[0].weight,
                        r=0,
                        e=0,
                        item_index=list_of_items[0].index)

        else:
            # next item list index
            next_i = None

            # get list index form current item
            for i, item in enumerate(list_of_items):
                if item.index == current_item_index:
                    next_i = i + 1

            # check if exists
            if next_i < len(items):
                return Node(v=list_of_items[next_i].value,
                            w=list_of_items[next_i].weight,
                            r=0,
                            e=0,
                            item_index=list_of_items[next_i].index)
        return None

    # start timer
    start = timer()
    # create start node
    start_node = Node(v=0, w=0, r=capacity, e=estimation, item_index=-1)
    start_node.id = 0

    # sort items by value weight ratio
    if sorted_by_ratio:
        items.sort(key=lambda i: i.value / i.weight, reverse=True)

    # branch and bound algorithms with different strategies
    if search_strategy == "df":
        print("Start branch and bound algorithm depth first... \n")

        # depth first search with recursive function
        def traverse(node, parent=None):
            # reference global variable
            global best_value
            global node_id
            # if start next_node -> branch
            if not parent:
                # add start node to traversed nodes
                traversed_nodes.append(node)
                # get next in items
                next_node = get_next_item(list_of_items=items, current_item_index=node.item_index)
                # branch if next item exists
                if next_node:
                    traverse(node=next_node, parent=node)
            else:

                # branches node_1 = take item, node_0 = leave item
                node_1 = copy.deepcopy(node)
                node_1.id = node_id
                node_id += 1
                node_0 = copy.deepcopy(node)
                node_0.id = node_id
                node_id += 1

                # case: take the item
                # calculate value
                node_1.v += parent.v
                # calculate remaining capacity
                node_1.r = parent.r - node_1.w
                # calculate estimate
                node_1.e = parent.e
                # update taken items
                # TODO: fix taken items, weight accumulation
                node_1.taken_item = copy.deepcopy(parent.taken_item)
                node_1.taken_item.append(node_1.item_index)
                # add to traversed nodes
                traversed_nodes.append(node_1)
                print("Take item")
                print(node_1)
                # check if feasible
                if node_1.r >= 0:

                    # update best value
                    if node_1.v > best_value:
                        best_value = node_1.v

                    # compare best value to estimate -> branch or prune
                    if node_1.e > best_value:
                        # get next in items
                        next_node = get_next_item(items, node_1.item_index)
                        # branch if next item exists
                        if next_node:
                            next_node.id = node_id
                            node_id += 1
                            traverse(next_node, node_1)

                # case: leave the item
                # calculate value
                node_0.v = parent.v
                # calculate remaining capacity
                node_0.r = parent.r
                # calculate estimate
                node_0.e = parent.e - node_0.v
                # update taken items
                # TODO: fix taken items, weight accumulation
                node_0.taken_item = copy.deepcopy(parent.taken_item)
                node_0.taken_item.append(node_0.item_index)
                # add to traversed nodes
                traversed_nodes.append(node_0)
                print("Leave item")
                print(node_0)
                # compare best value to estimate -> branch or prune
                if node_0.e > best_value:
                    # get next in items
                    next_node = get_next_item(items, node_0.item_index)
                    # branch if next item exists
                    if next_node:
                        traverse(node=next_node, parent=node_0)

        # start is own parent
        traverse(node=start_node)

    elif search_strategy == "bf":
        pass
    elif search_strategy == "ld":
        pass

    # end timer
    end = timer()

    # get best solution
    value = best_value
    weight = None
    slack = None
    taken = []
    opt = 1
    time = end - start

    for node in traversed_nodes:
        if node.v == best_value:
            weight = node.w
            slack = node.r
            taken = node.taken_item

    desc = "Value:                 " + str(best_value) + "\n" \
           "Weight:                " + str(weight) + "\n" \
           "Slack:                 " + str(slack) + "\n" \
           "Traversed nodes:       " + str(len(traversed_nodes)) + "\n" \
           "Taken items:           " + str(taken) + "\n"

    print(desc)

    for node in traversed_nodes:
        print(node)
        if node.v == best_value:
            print("Found")

    return value, weight, taken, opt, time, desc


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


def value_weight_heuristic(items, capacity):
    """
    Heuristic based on value-weight-ratio
    :param items: list of items
    :param capacity: constraint
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

    for item in items_w_ratio:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight

    return value, weight, taken, opt


def solve_it(input_instance, instance_location=None):
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
    # value, weight, taken, opt = value_weight_heuristic(items, capacity)

    # estimation by linear relaxation
    estimation = linear_relaxation(items)

    # branch and bound algorithm with depth first
    value, weight, taken, opt, time, desc = branch_and_bound(items=items,
                                                       capacity=capacity,
                                                       estimation=estimation,
                                                       search_strategy="df",
                                                       sorted_by_ratio=True)

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
        print(solve_it(input_data, file_location))
    else:
        print('This test requires an input file.  '
              'Please select one from the data directory. '
              '(i.e. python solver.py ./data/ks_4_0)')


