#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy
import sys
from gurobipy import *
from concurrent.futures import ThreadPoolExecutor, wait, as_completed

from collections import namedtuple
from timeit import default_timer as timer
from week_1_knapsack.gurobi_model import knapsack

Item = namedtuple("Item", ['index', 'value', 'weight', 'ratio'])


class Node(object):

    def __init__(self, v, w, r, e, item_index):
        # node id
        self.id = None
        # accumulated value
        self.v_acc = 0
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
        # take or leave
        self.take = None
        # take item so far
        self.taken_items = []
        # feasible
        self.feasible = True

    def __str__(self):
        return "Node id             {id} \n" \
               "Item id:            {index} \n" \
               "Take node:          {take} \n" \
               "Acc. value:         {acc_val} \n" \
               "Value:              {value} \n" \
               "Weight:             {weight} \n" \
               "Slack:              {slack} \n" \
               "Feasible:           {feasible} \n" \
               "Estimate:           {estimate} \n" \
               "Taken:              {taken} \n".format(
                    id=self.id,
                    index=self.item_index,
                    take=self.take,
                    acc_val=self.v_acc,
                    value=self.v,
                    weight=self.w,
                    slack=self.r,
                    feasible=self.feasible,
                    estimate=self.e,
                    taken=self.taken_items
                )


def gurobi_ip(items, capacity):
    pass


def branch_and_bound(items, capacity, estimation, search_strategy="df", sort_strategy=None, time_limit=30):
    """
    Simple branch and bound algorithm with different search strategies
    :param sort_strategy: rd (sort items by value weight ration descending),
                            ra (sort items by value weight ration ascending),
                            gd (sort items greedy by value descending)
                            ga (sort items greedy by value ascending)
    :param estimation: optimistic constraint from linear relaxation
    :param capacity: capacity constraint
    :param items: list of items
    :param search_strategy: df: depth first, bf: best first, ld: least discrepancy
    :return:value, weight, taken, opt, elapsed time
    """
    sys.setrecursionlimit(len(items) * len(items))

    # global variable
    global node_id

    # global result variables
    global best_value
    global best_slack
    global best_knapsack_weight
    global best_node_id
    global best_taken_items

    node_id = 1
    best_value = 0
    best_slack = None
    best_knapsack_weight = None
    best_node_id = None
    best_taken_items = []

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
    start_node.v_acc = 0

    check_items = copy.deepcopy(items)

    # sort items
    if sort_strategy == "rd":
        items.sort(key=lambda i: i.value / i.weight, reverse=True)
    elif sort_strategy == "ra":
        items.sort(key=lambda i: i.value / i.weight, reverse=False)
    elif sort_strategy == "gd":
        items.sort(key=lambda i: i.value, reverse=True)
    elif sort_strategy == "ga":
        items.sort(key=lambda i: i.value, reverse=False)

    # branch and bound algorithms with different strategies
    if search_strategy == "df":

        # depth first search with recursive function
        def traverse(node, start_time, time_limit, parent=None):
            # reference global variable
            global node_id
            # result variables
            global best_value
            global best_slack
            global best_knapsack_weight
            global best_node_id
            global best_taken_items

            # if start next_node -> branch
            if not parent:

                # add start node to traversed nodes
                traversed_nodes.append(node)

                # get next in items
                next_node = get_next_item(list_of_items=items, current_item_index=node.item_index)

                # branch if next item exists
                if next_node:
                    traverse(node=next_node, parent=node, start_time=start_time, time_limit=time_limit)
            else:
                elapsed = timer() - start_time
                if elapsed > time_limit:

                    # get best solution
                    r_opt = 0
                    r_solution = []
                    r_check_value = 0
                    r_check_weight = 0
                    # sort items by index
                    best_taken_items.sort()
                    items.sort(key=lambda i: i.index)
                    for r_item in check_items:
                        if r_item.index in best_taken_items:
                            r_solution.append(1)
                            r_check_value = r_check_value + r_item.value
                            r_check_weight = r_check_weight + r_item.weight
                        else:
                            r_solution.append(0)
                    # check if solution is correct and feasible
                    if (r_check_value != best_value) and (r_check_weight > capacity):
                        raise ArithmeticError("Solution infeasible")

                    desc = "Branch and Bound: algorithm depth first, search {s}... \n".format(s=sort_strategy) + "\n" \
                           "Value:                 " + str(r_check_value) + "\n" \
                           "Solution:              " + str(r_solution) + "\n" \
                           "Knapsack weight:       " + str(r_check_weight) + "\n" \
                           "Capacity constraint:   " + str(capacity) + "\n" \
                           "Slack:                 " + str(best_slack) + "\n" \
                           "Traversed nodes:       " + str(len(traversed_nodes)) + "\n" \
                           "Taken items:           " + str(best_taken_items) + "\n" \
                           "Time elapsed (sec.):   " + str(elapsed) + "\n" \
                           "BB Node id:            " + str(best_node_id) + "\n"

                    return best_value, best_knapsack_weight, r_solution, r_opt, elapsed, desc

                # branches node_1 = take item, node_0 = leave item
                node_1 = copy.deepcopy(node)
                node_1.id = node_id
                node_1.take = True
                node_id += 1
                node_0 = copy.deepcopy(node)
                node_0.id = node_id
                node_0.take = False
                node_id += 1

                # case: take the item
                # set v_acc from parent
                node_1.v_acc = parent.v_acc

                # calculate remaining capacity
                node_1.r = parent.r - node_1.w

                # calculate estimate
                node_1.e = parent.e

                # add to traversed nodes
                traversed_nodes.append(node_1)

                # check if feasible
                if node_1.r >= 0:

                    # calculate new v_acc
                    node_1.v_acc = node_1.v_acc + node_1.v

                    # update taken items
                    node_1.taken_items = copy.deepcopy(parent.taken_items)
                    node_1.taken_items.append(node_1.item_index)

                    # update best solution
                    if node_1.v_acc > best_value:
                        best_value = node_1.v_acc
                        best_taken_items = node_1.taken_items
                        best_slack = node_1.r
                        best_knapsack_weight = capacity - best_slack
                        best_node_id = node_1.id

                    # compare best value to estimate -> branch or prune
                    if node_1.e > best_value:

                        # get next in items
                        next_node = get_next_item(items, node_1.item_index)

                        # branch if next item exists
                        if next_node:
                            traverse(node=next_node, parent=node_1, start_time=start_time, time_limit=time_limit)

                # case: leave the item
                # calculate value
                node_0.v = parent.v

                # calculate remaining capacity
                node_0.r = parent.r

                # calculate estimate
                node_0.e = parent.e - node_0.v

                # add to traversed nodes
                traversed_nodes.append(node_0)

                # compare best value to estimate -> branch or prune
                if node_0.e > best_value:

                    # get next in items
                    next_node = get_next_item(items, node_0.item_index)

                    # branch if next item exists
                    if next_node:
                        traverse(node=next_node, parent=node_0, start_time=start_time, time_limit=time_limit)

        # start is own parent
        traverse(node=start_node, start_time=start, time_limit=time_limit)

    elif search_strategy == "bf":
        pass
    elif search_strategy == "ld":
        pass

    # end timer
    end = timer()

    # get best solution
    opt = 0
    solution = []
    time = end - start
    check_value = 0
    check_weight = 0
    # sort items by id
    best_taken_items.sort()
    items.sort(key=lambda i: i.index)
    for item in items:
        if item.index in best_taken_items:
            solution.append(1)
            check_value = check_value + item.value
            check_weight = check_weight + item.weight
        else:
            solution.append(0)
    # check if solution is correct and feasible
    if (check_value != best_value) and (check_weight > capacity):
        raise ArithmeticError("Solution infeasible")

    desc = "Branch and Bound: algorithm depth first, search {s}... \n".format(s=sort_strategy) + "\n" \
           "Value:                 " + str(check_value) + "\n" \
           "Solution:              " + str(solution) + "\n" \
           "Knapsack weight:       " + str(check_weight) + "\n" \
           "Capacity constraint:   " + str(capacity) + "\n" \
           "Slack:                 " + str(best_slack) + "\n" \
           "Traversed nodes:       " + str(len(traversed_nodes)) + "\n" \
           "Taken items:           " + str(best_taken_items) + "\n" \
           "Time elapsed (sec.):   " + str(time) + "\n" \
           "BB Node id:            " + str(best_node_id) + "\n"

    return best_value, best_knapsack_weight, solution, opt, time, desc


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
    check_value = 0
    weight = 0
    check_weight = 0
    taken = []
    opt = 0
    solution = []

    # start timer
    start = timer()

    # sort items by ratio
    check_items = copy.deepcopy(items)
    items.sort(key=lambda i: i.value / i.weight, reverse=True)

    for item in items:
        if weight + item.weight <= capacity:
            taken.append(item.index)
            value += item.value
            weight += item.weight

    end = timer()
    items.sort(key=lambda i: i.index)
    taken.sort()
    for item in check_items:
        if item.index in taken:
            solution.append(1)
            check_value = check_value + item.value
            check_weight = check_weight + item.weight
        else:
            solution.append(0)

    # check if solution is correct and feasible
    if (check_value != value) and (check_weight > capacity):
        raise ArithmeticError("Heuristic solution infeasible")

    desc = "Start value_weight_heuristic \n\n" \
           "Value:                 " + str(value) + "\n" \
           "Solution:              " + str(solution) + "\n" \
           "Taken:                 " + str(taken) + "\n" \
           "Knapsack weight:       " + str(weight) + "\n" \
           "Capacity constraint:   " + str(capacity) + "\n"\
           "Slack:                 " + str(capacity - weight) + "\n" \
           "Time elapsed (sec.):   " + str(end - start) + "\n"

    return value, weight, solution, opt, end - start, desc


def solve_it(input_instance, instance_location=None):

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

    solution = []

    # first greedy heuristics
    value, weight, taken, opt, time, desc = value_weight_heuristic(items, capacity)
    print(desc)
    solution.append([value, taken, opt])

    # gurobi model
    value, opt, taken = knapsack(items=items, capacity=capacity)
    solution.append([value, taken, opt])

    # sort solutions by value
    solution.sort(key=lambda sol: sol[0], reverse=True)

    # prepare the solution in the specified output format
    output_data = str(solution[0][0]) + ' ' + str(solution[0][2]) + '\n'
    output_data += ' '.join(map(str, solution[0][1]))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data, sys.argv))
    else:
        print('This test requires an input file.  '
              'Please select one from the data directory. '
              '(i.e. python solver.py ./data/ks_4_0)')
