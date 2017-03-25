from knapi.knapsacksolver.KnapsackSolver import KnapsackSolver

data_size = input('Which data? > ')

algo = input('Pick algo (branch and bound|dynamic programming|greedy heuristic|auto) >> ')
solver = KnapsackSolver()
solver.load_data_from_file('data/ks_' + str(data_size) + '.json')
solver.solve(algo)

print solver.knapsack
