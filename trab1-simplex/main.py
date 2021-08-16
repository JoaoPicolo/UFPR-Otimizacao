#!/usr/bin/python3

import sys

import numpy as np
from scipy.optimize import linprog

def readInput():
    """ Reads input from stdin
    Inputs:
        n     -- |T|
        l     -- |N|
        h     -- Hi, i = [1..n]
        c     -- Ci, i = [1..l]
        u     -- Ui, i = [1..l]
        total -- Si, i = [1..l]
        task  -- Ti,j where i is a machine and j a task 
    Returns:
        n, l                    -- Same as input
        result[l][n]            -- Matrix indicating which machine
            can realize one task 
        task_h                  -- Necessary time for each task
        machine_data[2][l]      -- Matrix containing on its first row the
            cost for each machine and on its second row the maximum 
            amount of time available for each machine
        costs                   -- Array containing the cost for each
            decision variable
        tasks_machine[l][total] -- Matrix indicating wich tasks will
            be executed by each machine
    """
    stdin = sys.stdin.read().split()
    
    n, l = int(stdin[0]), int(stdin[1])

    result = np.zeros((l,n))
    
    index = 2
    task_h = []
    for i in range(n):
        h = stdin[index]
        index += 1
        task_h.append(h)

    machine_data = [[],[]]
    for i in range(l):
        c, u = stdin[index], stdin[index+1]
        index += 2
        machine_data[0].append(c)
        machine_data[1].append(u)

    costs = []
    machine_tasks = []
    for i in range(l):
        total = int(stdin[index])
        tasks = []
        index += 1
        for j in range(total):
            task = int(stdin[index])
            index += 1
            result[i][task - 1] = 1
            costs.append(machine_data[0][i])
            tasks.append(task)

        machine_tasks.append(tasks)

    return n, l, result, task_h, machine_data, costs, machine_tasks

def proccessTaskMachine(n, l, total, machine_tasks):
    """ Connect task to machine
    Inputs:
        n, l, machine_tasks -- Same as described at readInput()
        total               -- Number of decision variables
    Returns:
        task_machine[n][total] -- Matrix containing on each row
            wheter or not a task n will be executed by a machine
    """
    task_machine = np.zeros((n,total))

    size = 0
    for i in range(l):
        tasks = machine_tasks[i]
        tasks_size = len(tasks)
        for index, value in enumerate(tasks):
            # True if task "value" is will be executed by machine "i"
            task_machine[value - 1][size + index] = 1

        size += tasks_size
    
    return task_machine

def proccessHourMachine(n, l, total, machine_tasks):
    """ Connect machine to hour
    Inputs:
        n, l, machine_tasks -- Same as described at readInput()
        total               -- Number of decision variables
    Returns:
        task_machine[l][total] -- Matrix containing on each row
            wheter or not a machine will execute a given task
    """
    hour_machine = np.zeros((l, total))

    last_index = 0
    for i in range(l):
        tasks = machine_tasks[i]
        for value in tasks:
            # Machine "i" executes task "value"
            hour_machine[i][last_index] = 1
            last_index += 1
    
    return hour_machine

def printResult(n, l, result, optimized, cost):
    """ Prints result to stdout
    Inputs:
        n, l, result     -- Same as described at readInput()
        optimized[total] -- Final value for each decision variable
        cost             -- Final cost of objective function
    """
    opt_index = 0

    for l_index in range(l):
        for n_index in range(n):
            if(result[l_index][n_index]):
                print("{:.1f}".format(optimized[opt_index]), end=" ")
                opt_index += 1
            else:
                print("{:.1f}".format(result[l_index][n_index]), end=" ")

        print()

    print("{:.1f}".format(cost))


def printError(status):
    """ If problem could not be solved
        print default errors to stdout
    """
    if status == 0:
        print("Algorithm proceeding nominally")
    elif status == 1:
        print("Iteration limit reached")
    elif status == 2:
        print("Problem appears to be infeasible")
    elif status == 3:
        print("Problem appears to be unbounded")
    else:
        print("Serious numerical difficulties encountered")

def main(argv):
    n, l, result, task_h, machine_data, costs, machine_tasks = readInput()
    task_machine = proccessTaskMachine(n, l, len(costs), machine_tasks)
    hour_machine = proccessHourMachine(n, l, len(costs), machine_tasks)
    
    solution = linprog(c=costs,
        A_ub=hour_machine, b_ub=machine_data[1],
        A_eq=task_machine, b_eq=task_h, method="simplex")
    
    if(solution.success):
        printResult(n, l, result, solution.x, solution.fun)
    else:
        printError(solution.status)
    

if __name__ == "__main__":
   main(sys.argv[1:])
