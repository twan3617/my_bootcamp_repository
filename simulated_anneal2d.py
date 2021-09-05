import numpy as np
from numpy import asarray, exp 
from numpy.random import randn, rand, seed

### Simulated Annealing, from scratch.
### A stochastic gradient-style optimisation algorithm, simulated annealing does not require the computation of gradients
### and can more efficiently explore and find global optima of a non-linear functions. 
### Well-known gradient-dependent deterministic algorithms are often unable to compute global optima due to their 
### intrinsic local nature, while also being inefficient due to requiring multiple gradient (and hence matrix) computations.
### Simulated annealing is a form of genetic algorithm. The idea is, given a starting point, randomly select a direction to move in. 
### In general, we expect to keep moving in directions which improve the criteria, but randomly, we may choose to take directions which 
### decrease the criteria. The probability of doing so is based on the "temperature" of the system, which decays as we use more iterations.
'''Algorithm
Generate and evaluate initial point
Run the algorithm: 
1. Take a normally distributed random sized step 
2. Evaluate candidate point
3. If it's the best solution, replace best 
4. Check whether to keep or replace current point using the metropolis criterion:
    if diff < 0 or rand() < metropolis
    replace 
    (i.e. if it's a better point or if a randomly sampled point < metropolis)
    temperature: temp / float(1 + i)
    metropolis criterion: exp(-diff / temp)
'''

a = 1
b = 100 
step_size = 0.05 #Hyperparameters to alter 
eps = 10e-4
error = 1
temp = 10
n_iter = 1000

# Define the 2D - Rosenbrock objective function
# Make this dimension-agnostic
def objective(x): #x should be a tuple
    return (a - x[0])**2 + b * (x[1] - x[0]**2)**2

bounds = asarray([[-5.0, 5.0], 
            [-5, 5]])

initial = bounds[:,0] + rand(len(bounds)) * (bounds[:,1] - bounds[:,0])
initial_eval = objective(initial)

best, best_eval = initial, initial_eval
current, current_eval = initial, initial_eval
    
for n in range(n_iter):
    candidate = current + randn(len(bounds)) * step_size
    candidate_eval = objective(candidate)

    if candidate_eval < best_eval:
        best, best_eval = candidate, candidate_eval
    
    t = temp/(n + 1)
    diff =  candidate_eval - current_eval
    metro = exp(- diff / t)

    ### Replace current with candidate 
    if rand() < metro or diff < 0:
        current, current_eval = candidate, candidate_eval
    print(f"Best: {best} Value: {best_eval}")






