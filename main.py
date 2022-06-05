import matplotlib.pyplot as plt
import numpy as np
import math
import random
from random import shuffle


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "Point(" + str(self.x) + ", " + str(self.y) + ")"


# calculeaza distanta dintre doua puncte
def distance(point1, point2):
    return math.sqrt(((point2.x - point1.x) * (point2.x - point1.x)) + ((point2.y - point1.y) * (point2.y - point1.y)))


random.seed(10)

points = []
for point_number in range(100):
    points.append(Point(random.randint(0, 5000), random.randint(0, 5000)))

random.seed()

"""
for point in points:
  plt.plot(point.x, point.y, marker="o", color="black")
"""

distances_between_each_two_points = {}
for point1 in points:
    for point2 in points:
        if point1 is not point2:
            distances_between_each_two_points.update({frozenset((point1, point2)): int(distance(point1, point2))})

# SUBPUNCT 1
"""
for key in distances_between_each_two_points.keys():
  frozenset_to_list = list(key)
  print(frozenset_to_list[0], "," ,frozenset_to_list[1] , ": ", distances_between_each_two_points[key])
"""


# functie de evaluare a unui individ, calculeaza distanta totala a unui ciclu
# path - lista de puncte (permutare) corecta
def evaluate_path(path):
    total_distance = 0
    for i in range(0, len(path) - 1):
        total_distance += distances_between_each_two_points[frozenset([path[i], path[i + 1]])]
    total_distance += distances_between_each_two_points[frozenset([path[len(path) - 1], path[0]])]
    return total_distance


def compare_paths(path1, path2):
    return evaluate_path(path1) < evaluate_path(path2)


def edge_recombination(parent1, parent2):
    aux_parent2 = parent2.copy()
    child = []

    # copy the first half of a random parent
    for i in range(0, len(parent1) // 2):
        child.append(parent1[i])
        aux_parent2.remove(parent1[i])

    for point in aux_parent2:
        child.append(point)

    return child


def print_path(path):
    for point in path:
        print(point, end=" ")
    print()


def mutate(path):
    random_index1 = random.randint(0, 99)
    random_index2 = random.randint(0, 99)
    path[random_index1], path[random_index2] = path[random_index2], path[random_index1]
    return path


def handlungsreisendenproblem():
    best_in_each_generation = []
    generation = 0

    # initial population (list of 15 random paths)
    population = []
    for i in range(0, 15):

        list1 = [i for i in range(0, 100)]
        shuffle(list1)

        individ = []
        for index in list1:
            individ.append(points[index])

        population.append(individ)

    population.sort(key=evaluate_path)
    best_so_far = population[0]
    best_in_each_generation.append(population[0])

    while generation <= 2000:

        childs = []
        for i in range(0, 40):

            # wahle gleichverteilt zufallig erstes Elter aus Population
            firstParent = population[random.randint(0, 14)]

            # zufallszahl u aus (0, 10)
            if ((random.randint(0, 10) * i) // 2000 < 4):
                # wahle gleichverteild zufallig zweites Elter aus Population
                secondParent = population[random.randint(0, 14)]

                firstParent = edge_recombination(firstParent, secondParent)

            firstParent = mutate(firstParent)
            childs.append(firstParent)

        all_candidates = []
        for parent in population:
            all_candidates.append(parent)
        for child in childs:
            all_candidates.append(child)

        generation += 1
        all_candidates.sort(key=evaluate_path)

        # 15 best candidates are the new generation
        population = []
        for i in range(0, 15):
            population.append(all_candidates[i])
        best_in_each_generation.append(population[0])
        if compare_paths(population[0], best_so_far):
            best_so_far = population[0]

    return best_in_each_generation, best_so_far


bests, best_so_far = handlungsreisendenproblem()
for i in range(len(bests)):
    if i % 500 == 0:
        print("Total distance: ", evaluate_path(bests[i]))
        x = []
        y = []
        for point in bests[i]:
            x.append(point.x)
            y.append(point.y)
        x.append(bests[i][0].x)
        y.append(bests[i][0].y)
        plt.plot(np.array(x), np.array(y), color="red")
        plt.show()
        plt.clf()

print("Grafic (cel mai eficient din fiecare generatie): ")
evaluations = []
for el in bests:
    evaluations.append(evaluate_path(el))
plt.plot(evaluations, color="red")
plt.show()
plt.clf()

print("Cel mai eficient gasit: ", evaluate_path(best_so_far))
x = []
y = []
for point in best_so_far:
    x.append(point.x)
    y.append(point.y)
x.append(best_so_far[0].x)
y.append(best_so_far[0].y)
plt.plot(np.array(x), np.array(y), color="red")
plt.show()
