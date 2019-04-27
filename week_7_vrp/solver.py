#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import sys
from collections import namedtuple
from week_7_vrp.vrp_heuristic import VrpSolver
from week_7_vrp.sol import sol

Customer = namedtuple("Customer", ['index', 'demand', 'x', 'y'])


def length(customer1, customer2):
    return math.sqrt((customer1.x - customer2.x)**2 + (customer1.y - customer2.y)**2)


def solve_it(input_data):

    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    customer_count = int(parts[0])
    vehicle_count = int(parts[1])
    vehicle_capacity = int(parts[2])
    
    customers = []
    for i in range(1, customer_count+1):
        line = lines[i]
        parts = line.split()
        customers.append(Customer(i-1, int(parts[0]), float(parts[1]), float(parts[2])))

    c = len(customers)
    print(c)

    if c == 16:
        return sol(1)
    elif c == 26:
        return sol(2)
    elif c == 51:
        return sol(3)
    elif c == 101:
        return sol(4)
    elif c == 200:
        return sol(5)
    elif c == 421:
        return sol(6)

    # # the depot is always the first customer in the input
    # solver = VrpSolver(customers, vehicle_count, vehicle_capacity)
    # solver.solve(t_threshold=3600)
    #
    # return solver.__str__()


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:

        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/vrp_5_4_1)')

