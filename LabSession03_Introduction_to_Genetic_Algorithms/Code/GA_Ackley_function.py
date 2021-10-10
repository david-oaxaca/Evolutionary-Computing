# Ackley function f(x,y)
# Alumno: Oaxaca Pérez David Arturo
# Materia: Evolutionary Computing

#Functions and tools import
import math
import random
import time
import matplotlib.pyplot as plt
import numpy as np

from IPython import display as display
from functools import cmp_to_key
'''
Chromosomes are 4 bits long but are composed of two strings to 
represent a point in R^2
'''
L_chromosome=8
N_chains=2**L_chromosome
#Lower and upper limits of search space
a=-5
b=5
crossover_point=int(L_chromosome/2)

#Number of chromosomes
N_chromosomes=10
#probability of mutation
prob_m=0.5

# Función a evaluar con el algoritmo
def ackley_function(x, y):
  return -20.0 * np.exp(-0.2 * np.sqrt(0.5 * (x**2 + y**2))) - \
  np.exp(0.5 * (np.cos(2 * np.pi * x)+np.cos(2 * np.pi * y))) + np.e + 20 


# Función para crear un cromosoma random

def random_chromosome():
    chromosome=[[],[]]
    for i in range(0,L_chromosome):
        if random.random()<0.5:
            chromosome[0].append(0)
        else:
            chromosome[0].append(1)

    for i in range(0,L_chromosome):
        if random.random()<0.5:
            chromosome[1].append(0)
        else:
            chromosome[1].append(1)

    return chromosome

#binary codification
def decode_chromosome(chromosome):
    global L_chromosome,N_chains,a,b
    value1=0
    value2=0
    for p in range(L_chromosome):
        # Traducimos a decimal el cromosoma
        value1+=(2**p)*chromosome[0][-1-p]
        value2+=(2**p)*chromosome[1][-1-p]


    #Conversión a un punto en el intervalo de busqueda
    return a+(b-a)*float(value1)/(N_chains-1), a+(b-a)*float(value2)/(N_chains-1)

#F0 es la primera población
F0=[]
fitness_values=[]

#Creación de los diez cromosomas utilizados para la función
for i in range(0,N_chromosomes):
    F0.append(random_chromosome())
    fitness_values.append(0)

#print(F0)

def evaluate_chromosomes():
    global F0

    for p in range(N_chromosomes):
        #Valor del punto dado por el cromosoma
        v1,v2=decode_chromosome(F0[p])
        #Evaluamos el punto en la función y lo metemos en los valores de aptitud
        fitness_values[p] = ackley_function(v1,v2)
        

def compare_chromosomes(chromosome1,chromosome2):
    vc1_str1, vc1_str2=decode_chromosome(chromosome1)
    vc2_str1, vc2_str2=decode_chromosome(chromosome2)
    #print(vc1_str1, vc1_str2)
    fvc1=ackley_function(vc1_str1, vc1_str2)
    fvc2=ackley_function(vc2_str1, vc2_str2)
    if fvc1 > fvc2:
        return 1
    elif fvc1 == fvc2:
        return 0
    else: #fvg1<fvg2
        return -1

suma=float(N_chromosomes*(N_chromosomes+1))/2.

Lwheel=N_chromosomes*10

def create_wheel():
    global F0,fitness_values

    maxv=max(fitness_values)
    acc=0
    for p in range(N_chromosomes):
        acc+=maxv-fitness_values[p]
        #print(acc)
    fraction=[]
    for p in range(N_chromosomes):
        fraction.append( float(maxv-fitness_values[p])/acc)
        if fraction[-1]<=1.0/Lwheel:
            fraction[-1]=1.0/Lwheel
##    print fraction
    fraction[0]-=(sum(fraction)-1.0)/2
    fraction[1]-=(sum(fraction)-1.0)/2
##    print fraction

    wheel=[]

    pc=0

    for f in fraction:
        Np=int(f*Lwheel)
        for i in range(Np):
            wheel.append(pc)
        pc+=1

    return wheel
        
F1=F0[:]


def nextgeneration():
    F0.sort(key=cmp_to_key(compare_chromosomes) )
    print( "Best solution so far:")
    decode_value1, decode_value2 = decode_chromosome(F0[0])
    print(f'f({decode_value1}, {decode_value2}) = {ackley_function(decode_value1, decode_value2)}')
                                                                    
    #elitism, the two best chromosomes go directly to the next generation
    F1[0]=F0[0]
    F1[1]=F0[1]
    roulette=create_wheel()
    for i in range(0,int((N_chromosomes-2)/2)):
        
        #Two parents are selected
        p1=random.choice(roulette)
        p2=random.choice(roulette)


        #Two descendants are generated
        o1=[F0[p1][0][0:crossover_point], F0[p1][1][0:crossover_point]]
        o1[0].extend(F0[p2][0][crossover_point:L_chromosome])
        o1[1].extend(F0[p2][1][crossover_point:L_chromosome])
        
        o2=[F0[p2][0][0:crossover_point], F0[p2][1][0:crossover_point]]
        o2[0].extend(F0[p1][0][crossover_point:L_chromosome])
        o2[1].extend(F0[p1][1][crossover_point:L_chromosome])


        #Each descendant is mutated with probability prob_m
        if random.random() < prob_m:
            o1[0][int(round(random.random()*(L_chromosome-1)))]^=1
            o1[1][int(round(random.random()*(L_chromosome-1)))]^=1
        if random.random() < prob_m:
            o2[0][int(round(random.random()*(L_chromosome-1)))]^=1
            o2[1][int(round(random.random()*(L_chromosome-1)))]^=1
        #The descendants are added to F1
        F1[2+2*i]=o1
        F1[3+2*i]=o2

    #The generation replaces the old one
    F0[:]=F1[:]

F0.sort(  key=cmp_to_key(compare_chromosomes))
evaluate_chromosomes()

for i in range(0, 100):
  print(f"\nGeneracion {i}:")
  nextgeneration()