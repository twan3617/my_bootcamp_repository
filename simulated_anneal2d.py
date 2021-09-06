import numpy as np
from numpy import asarray, exp 
from numpy.random import randn, rand, seed
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import *
from matplotlib import cm

### Simulated Annealing, from scratch. Source: https://machinelearningmastery.com/simulated-annealing-from-scratch-in-python/
### A stochastic gradient-style optimisation algorithm, simulated annealing does not require the computation of gradients
### and can more efficiently explore and find global optima of a non-linear functions. 
### Well-known gradient-dependent deterministic algorithms are often unable to compute global optima due to their 
### intrinsic local nature, while also being inefficient due to requiring multiple gradient (and hence matrix) computations.
### Simulated annealing is a form of genetic algorithm. The idea is, given a starting point, randomly select a direction to move in. 
### In general, we expect to keep moving in directions which improve the criteria, but randomly, we may choose to take directions which 
### decrease the criteria. The probability of doing so is based on the "temperature" of the system, which decays as we use more iterations.

### Some new things to add: OOP-ify this code? 
### Make this dimension-agnostic
### Make the 3D plot a function

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

class anneal_class():  
    def __init__(self, a, b, step_size, bounds, temp = 10, n_iter = 2000, eps = 0):
    ###a, b are rosenbrock parameters, step_size is the size of each step, eps is the error tolerance, n_iter is the number of iterations.
    ###Either specify n_iter or eps
        self.params = np.zeros((2,))
        self.params[0] = a
        self.params[1] = b
        self.step_size = step_size
        self.n_iter = n_iter
        self.eps = eps
        self.bounds = bounds
        self.temp = temp
    
    def objective(self, x): 
        return (self.params[0] - x[0])**2 + self.params[1]*(x[1] - x[0]**2)**2

    def anneal(self): ### Pass initial random point init. 
        initial = self.bounds[:,0] + rand(len(self.bounds)) * (self.bounds[:,1] - self.bounds[:,0])
        initial_eval = self.objective(initial)

        ### Set best and current values to the initial value.
        best, best_eval = initial, initial_eval
        current, current_eval = initial, initial_eval
            
        # Repeadly take random steps and evaluate based on objective function and metropolis criterion.
        best_history = asarray([best[0], best[1], best_eval]).reshape((1,3))
        for n in range(self.n_iter):

            candidate = current + randn(len(self.bounds)) * self.step_size
            candidate_eval = self.objective(candidate)

            ### If newly found candidate is better, replace best
            if candidate_eval < best_eval:
                print(f"New best found: {best} Value: {best_eval}")
                best, best_eval = candidate, candidate_eval
                best_history = np.vstack((best_history,np.hstack((best[0], best[1], best_eval))))

            ### Compute temperature, diff and the metropolis criterion
            t = self.temp/(n + 1)
            diff =  candidate_eval - current_eval
            metro = exp(- diff / t)

            ### Replace current with candidate 
            if rand() < metro or diff < 0:
                current, current_eval = candidate, candidate_eval
        return best, best_eval, best_history

    def plot(self, best_history):
        ### plotting code
        fig = plt.figure()
        ax = fig.gca(projection='3d')               # to work in 3d

        theCM = cm.get_cmap()
        theCM._init()
        alphas = np.abs(np.linspace(-1.0, 1.0, theCM.N))
        theCM._lut[:-3,-1] = alphas

        x_surf=np.arange(self.bounds[0,:], 0.01)                # generate a mesh
        y_surf=np.arange(self.bounds[0,:], 0.01)
        x_surf, y_surf = np.meshgrid(x_surf, y_surf)
        z_surf = self.objective((x_surf,y_surf))           # ex. function, which depends on x and y
        ax.plot_surface(x_surf, y_surf, z_surf, cmap=theCM);    # plot a 3d surface plot

        ax.scatter(best_history[:,0], best_history[:,1], best_history[:,2])
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.set_xlim(self.bounds[0,:])
        ax.set_ylim(self.bounds[1,:])

        plt.show()



        return 



def main():
    a = 1
    b = 100 
    step_size = 0.075 #Hyperparameters to alter 
    eps = 10e-4
    error = 1
    temp = 10
    n_iter = 2000
    bounds = asarray([[-5.0, 5.0], 
            [-5.0, 5.0]])
    init = bounds[:,0] + rand(len(bounds)) * (bounds[:,1] - bounds[:,0])
    sim = anneal_class(a, b, step_size, bounds, temp, n_iter)
    best, best_eval, best_history = sim.anneal()
    #sim.plot(best_history)
    x_surf=np.arange(bounds[0,:], 0.01)
    return 

if __name__ == "__main__": 
    main()
    