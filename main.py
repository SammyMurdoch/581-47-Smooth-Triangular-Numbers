from math import prod
from sympy import primefactors
from itertools import chain, combinations
from sympy.solvers.diophantine.diophantine import diop_DN
from time import time


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)+1))


def get_additional_solutions(f, n, c):
    x_1, y_1 = f[0], f[1]
    x_k, y_k = x_1, y_1

    solution_list = []

    for k in range(c):
        x_k, y_k = x_1 * x_k + n * y_1 * y_k, x_1 * y_k + y_1 * x_k
        solution_list.append((x_k, y_k))

    return solution_list


is_smooth_cache = {}


def is_smooth(p, n):
    if n > (10**15)/15:
        return False

    if n == 1:
        return True

    if primefactors(n)[-1] > p:
        return False

    return True


def verify_pair_smoothness(p):
    if is_smooth(primes[-1], p[0]) and is_smooth(primes[-1], p[1]):
        return True

    return False


total_time = time()

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
print(primes)

powerset_time = time()

product_list = [1] + [prod(s) for s in powerset(primes)][1:]

print(time()-powerset_time)

solutions_required = int(max(3, (primes[-1] + 1) / 2))  # Clearly

smooth_numbers = []


for q in product_list:
    smooth_time = time()
    solutions = list(diop_DN(2*q, 1))

    solutions += get_additional_solutions(solutions[0], 2*q, solutions_required-1)

    #print('{0} solutions'.format(len(solutions)))
    for solution in solutions:
        pair = ((solution[0]-1)/2, (solution[0]+1)/2)

        if verify_pair_smoothness(pair):
            smooth_numbers.append(pair[0])

    #print('{0} seconds'.format(time()-smooth_time))

print(smooth_numbers)
print(len(smooth_numbers))
print(sum(smooth_numbers))

print(time()-total_time)