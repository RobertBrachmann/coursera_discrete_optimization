import random, numpy, math, copy, matplotlib.pyplot as plt
from timeit import default_timer as timer


def tsp_opt(points):

    def length(point1, point2):
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

    cities = points
    n = len(points)
    print("Instance with n={n}".format(n=n))
    tour = random.sample(range(n), n)


    # start timer
    start = timer()

    for temperature in numpy.logspace(0,5,num=100000)[::-1]:
        [i,j] = sorted(random.sample(range(n),2))
        newTour = tour[:i] + tour[j:j+1] + tour[i+1:j] + tour[i:i+1] + tour[j+1:]
        if math.exp((sum([math.sqrt(sum([(cities[tour[(k+1) % n]][d] - cities[tour[k % n]][d])**2 for d in [0,1] ])) for k in [j,j-1,i,i-1]]) - sum([math.sqrt(sum([(cities[newTour[(k+1) % n]][d] - cities[newTour[k % n]][d])**2 for d in [0,1] ])) for k in [j,j-1,i,i-1]])) / temperature) > random.random():
            tour = copy.copy(newTour)
        if timer() - start > 120:
            break

    print("Time elapsed {s} sec.".format(s=timer() - start))
    plt.plot([cities[tour[i % n]][0] for i in range(n+1)], [cities[tour[i % n]][1] for i in range(n+1)], 'xb-')
    plt.show()

    # calculate obj
    obj = 0
    for i, point_id in enumerate(tour):
        if i == len(tour) - 1:
            obj += length(points[point_id], points[0])
        else:
            obj += length(points[point_id], points[tour[i + 1]])

    return obj, 0, tour
