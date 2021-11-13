# Paisaje usando fractales
# Alumno: Oaxaca Pérez David Arturo
# Materia: Evolutionary Computing
# Profesor: Dr. Jorge Luis Rosas Trigueros
# Lab Session 06: Particle Swarm Optmization
# Basado en el codigo del Dr. Jorge Luis Rosas Trigueros visto en clase
# Grupo: 3CV11
# Fecha de realización: 15/10/2021

#Original File: pso_wikipedia.ipynb
#Example of PSO based on the wikipedia entry

import matplotlib.pyplot as plt
import numpy as np


lower_limit=-5
upper_limit=5

n_particles=10
n_dimensions=2

# Función a evaluar con el algoritmo
def ackley_function(x, y):
  return -20.0 * np.exp(-0.2 * np.sqrt(0.5 * (x**2 + y**2))) - \
  np.exp(0.5 * (np.cos(2 * np.pi * x)+np.cos(2 * np.pi * y))) + np.e + 20 


# Initialize the particle positions and their velocities
#Bias the initial population
X = lower_limit + 0.25*(upper_limit - lower_limit) * np.random.rand(n_particles, n_dimensions) 
assert X.shape == (n_particles, n_dimensions)
# V = np.zeros(X.shape)
V = -(upper_limit - lower_limit) + 2*(upper_limit - lower_limit)*np.random.rand(n_particles, n_dimensions)
 
# Initialize the global and local fitness to the worst possible
fitness_gbest = np.inf
fitness_lbest = fitness_gbest * np.ones(n_particles)

X_lbest = 1*X
X_gbest = 1*X_lbest[0]

fitness_X = np.zeros(X.shape)

for i in range(0, n_particles):
    if ackley_function(X_lbest[i][0], X_lbest[i][1]) < ackley_function(X_gbest[0], X_gbest[1]):
        X_gbest = 1*X_lbest[i]


count=0

def iteration():
    global count
    global X,X_lbest,X_gbest,V

    # Loop until convergence, in this example a finite number of iterations chosen
    weight=0.7 # Inercia
    C1=0.2 # Historia personal

    C2=0.1 # Seguir la tendencia que va marcando el lider

    count+=1

    if count%100 == 0:
      print (f"Generation {count}: Best particle in: {X_gbest} \ngbest: {ackley_function(X_gbest[0], X_gbest[1])}\n")

    # Update the particle velocity and position
    for I in range(0, n_particles):
        for J in range(0, n_dimensions):
          R1 = np.random.rand()#uniform_random_number()
          R2 = np.random.rand()#uniform_random_number()
          V[I][J] = (weight*V[I][J]
                    + C1*R1*(X_lbest[I][J] - X[I][J]) 
                    + C2*R2*(X_gbest[J] - X[I][J]))
          X[I][J] = X[I][J] + V[I][J]
        if ackley_function(X[I][0], X[I][1]) < ackley_function(X_lbest[I][0], X_lbest[I][1]):
            X_lbest[I]=1*X[I]
            if ackley_function(X_lbest[I][0], X_lbest[I][1]) < ackley_function(X_gbest[0], X_gbest[1]):
                X_gbest=1*X_lbest[I]
          


for i in range(2500):
  iteration()
