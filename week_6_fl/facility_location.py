import math
import matplotlib.pyplot as plt
from collections import namedtuple


Point = namedtuple("Point", ['x', 'y'])
Facility = namedtuple("Facility", ['index', 'setup_cost', 'capacity', 'location'])
Customer = namedtuple("Customer", ['index', 'demand', 'location'])


def plot_problem(facilities, customers):

    f_xs = []
    f_ys = []
    c_xs = []
    c_ys = []

    # set style
    plt.style.use('seaborn-darkgrid')

    # set labels
    plt.xlabel("x")
    plt.ylabel("y")

    for facility in facilities:
        f_xs.append(facility.location.x)
        f_ys.append(facility.location.y)

    for customer in customers:
        c_xs.append(customer.location.x)
        c_ys.append(customer.location.y)

    # add facilities
    plt.scatter(f_xs, f_ys, marker='o', color='red')
    # add customers
    plt.scatter(c_xs, c_ys, marker='^', color='orange')

    plt.show()


def plot_solution(facilities, customers, solution):

    # set style
    plt.style.use('seaborn-darkgrid')


    c_xs = []
    c_ys = []

    for f, facility in enumerate(facilities):

        if f in solution:
            # add active facilities
            plt.scatter(facility.location.x, facility.location.y, marker='o', color='red')
        else:
            # add passive facilities
            plt.scatter(facility.location.x, facility.location.y, marker='o', color='royalblue', alpha=0.3)

    for customer in customers:
        c_xs.append(customer.location.x)
        c_ys.append(customer.location.y)

    # add customers
    plt.scatter(c_xs, c_ys, marker='^', color='orange')

    # add edges
    for i, customer in enumerate(customers):

        xs = []
        ys = []
        # add customer
        xs.append(customer.location.x)
        ys.append(customer.location.y)
        # get facility index
        f = solution[i]
        # add facility
        xs.append(facilities[f].location.x)
        ys.append(facilities[f].location.y)

        # add facilities
        plt.plot(xs, ys, '--', color='grey', alpha=0.2)

    plt.show()


def random_nearest_neighbour(facilities, customers):

    # calculates distance between locations
    def length(point1, point2):
        return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

    solution = [-1] * len(customers)



    # calculate the cost of the solution
    used = [0] * len(facilities)
    for facility_index in solution:
        used[facility_index] = 1
    obj = sum([f.setup_cost*used[f.index] for f in facilities])
    for customer in customers:
        obj += length(customer.location, facilities[solution[customer.index]].location)

    return solution