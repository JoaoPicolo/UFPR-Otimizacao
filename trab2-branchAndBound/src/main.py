#!/usr/bin/python3

import sys
import datetime as time

alternative_bound = False
groups = set({})
actors = list([])
n_roles = 0

best_X = []
best_cost = float("inf")
current_X = []
n_nodes = 0


def readInput():
    global groups, actors, n_roles

    stdin = sys.stdin.read().split()
    l, m, n = int(stdin[0]), int(stdin[1]), int(stdin[2])
    c_idx = 3

    n_roles = n

    for i in range(l):
        groups.add(i + 1)

    for i in range(m):
        actors.append({"value": int(stdin[c_idx]), "groups": set({})})
        
        n_subgroups = int(stdin[c_idx + 1])
        c_idx += 2
        
        subgroups = set({})
        for j in range(n_subgroups):
            subgroups.add(int(stdin[c_idx + j]))
        actors[i]["groups"] = subgroups
        c_idx += j + 1
        

def isFeasible(l, current_X):
    global actors, groups, n_roles
    
    selected_groups = set({})
    undecided_groups = set({})

    n_selected = sum(current_X[:l])
    n_undecided = len(current_X) - l
    if (n_undecided < (n_roles - n_selected)) or (n_selected > n_roles):
        return False

    for i, item in enumerate(current_X):
        if item:
            selected_groups = selected_groups.union(actors[i]["groups"])
        else:
            if i >= l:
                undecided_groups = undecided_groups.union(actors[i]["groups"])

    missing_groups = groups.difference(selected_groups)
    subset = missing_groups.issubset(undecided_groups)

    return subset


def currentCost(current_X):
    global actors
    cost = 0
    for i, item in enumerate(current_X):
        cost += item * actors[i]["value"]

    return cost


def stricterBound(l, current_X):
    global actors, n_roles

    cost = currentCost(current_X)
    costs = []
    size = len(current_X)

    for i in range(l, size):
        costs.append(actors[i]["value"])

    n_selected = sum(current_X[:l])
    costs.sort()
    cost += sum(costs[:(n_roles - n_selected)])
    return cost


def simpleBound(l, current_X):
    global actors
    cost = 0
    for i, item in enumerate(current_X):
        cost += item * actors[i]["value"]

    return cost


def computeLowerBound(l, current_X):
    global alternative_bound

    if alternative_bound:
        return simpleBound(l, current_X)
    else:
        return stricterBound(l, current_X)


def branchAndBound(l, current_X):
    global actors, best_cost, best_X, n_nodes

    nextbound = []
    nextchoice = []
    n_nodes += 1

    if not isFeasible(l, current_X):
        return

    if l == len(actors):
        currentC = currentCost(current_X)

        if currentC < best_cost:
            best_cost = currentC
            best_X = current_X
    else:
        choiceSet = set({0, 1})
        for item in choiceSet:
            current_X[l] = item
            nextbound.append(computeLowerBound(l + 1, current_X))
            nextchoice.append(item)

        nextbound, nextchoice = (list(t) for t in zip(*sorted(zip(nextbound, nextchoice))))

    for i, item in enumerate(nextchoice):
        if nextbound[i] >= best_cost:
            return
        copy_X = current_X[:] # Pass by value and not by reference
        copy_X[l] = item
        branchAndBound(l + 1, copy_X)


def printResult(final_t):
    global best_X, best_cost, n_nodes

    if len(best_X) == 0:
        print("Inviável")
    else:
        for i, item in enumerate(best_X):
            if item:
                print(i + 1, end=" ")
        print(f"\n{best_cost}")

    print(f"Nós visitados: {n_nodes}\nTempo de execução: {final_t}", file=sys.stderr)


def main(argv):
    global actors, n_nodes, alternative_bound

    if "-a" in argv:
        alternative_bound = True
    readInput()

    start_t = time.datetime.now()
    current_X = [0] * len(actors)
    branchAndBound(0, current_X)
    end_t = time.datetime.now()

    final_t = end_t - start_t
    printResult(final_t)
    

if __name__ == "__main__":
    main(sys.argv[1:])
