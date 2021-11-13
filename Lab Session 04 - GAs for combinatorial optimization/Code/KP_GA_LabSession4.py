#Solving the KP with a Genetic Algorithm
#Alumno: Oaxaca Pérez David Arturo
#Materia: Evolutionary Computing
#Profesor: Jorge Luis Rosas Trigueros
#Grupo: 3CV11
#Fecha de realización: 08/10/2021

import math
import random
import time
import matplotlib.pyplot as plt
import numpy as np
from IPython import display as display
from functools import cmp_to_key

#Other tests
#v = (10,6,12)
#w = (2,1,3)
#W=5

#w = ( 2, 4, 5, 5, 7 ) 
#v = ( 2, 3, 4, 5, 6 ) 
#W=9

#w = [832, 913, 693, 156, 247, 51, 928, 885, 890, 126, 232, 864, 495, 830, 325, 613, 775, 501, 766, 60]
#v = [73, 22, 26, 91, 99, 52, 100, 61, 87, 64, 73, 58, 59, 11, 54, 98, 85, 39, 15, 88] 
#W= 1000


#Random creation of 20 values an weights for the items
v = [random.randint(1, 100) for _ in range(20)] 
w = [round(random.random(), 3) for _ in range(20)]
W = 1

#Chromosomes are 4 bits long
L_chromosome= len(v)
N_chains=2**L_chromosome
#Number of chromosomes
N_chromosomes=40
#probability of mutation
prob_m=0.8

#Penalty value to punish solutions that surpass the maximum weight
penalty_value = 100000

#POint at which two chromosome parents will be combined to create an offspring
crossover_point=int(L_chromosome/2)


def random_chromosome():
    chromosome=[]
    for i in range(0,L_chromosome):
        if random.random()<0.5:
            chromosome.append(0)
        else:
            chromosome.append(1)

    return chromosome


F0=[]
fitness_values=[]

for i in range(0,N_chromosomes):
    F0.append(random_chromosome())
    fitness_values.append(0)

def decode_chromosome(chromosome):
  global L_chromosome,v,w

  Total_weight=sum([w_i*c_i for w_i,c_i in zip(w,chromosome)])
  Total_value=sum([v_i*c_i for v_i,c_i in zip(v,chromosome)])

  return Total_value,Total_weight


def fitness_function(x):
  global W
  Total_value,Total_weight=x
  excess = Total_weight-W
  return Total_value if excess <= 0 else (Total_value - (excess + penalty_value)) 


        
def evaluate_chromosomes():
    global F0

    for p in range(N_chromosomes):
        v=decode_chromosome(F0[p])
        fitness_values[p]=fitness_function(v)

def compare_chromosomes(chromosome1,chromosome2):
    vc1=decode_chromosome(chromosome1)
    vc2=decode_chromosome(chromosome2)
    fvc1=fitness_function(vc1)
    fvc2=fitness_function(vc2)
    # if fvc1 > fvc2:
    if fvc1 < fvc2:
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
    if acc==0:
      return [0]*Lwheel
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
n=0

def print_solution(F0, fitness_values, n):
    print(f'Poblacion: {F0}')
    print(f'Valores fitness: {fitness_values}\n')
    print( "Best solution so far:")
    print( f'Generacion {n}, Cromosoma mas apto: {F0[0]}')
    print(f'f( {decode_chromosome(F0[0])} )= {fitness_function(decode_chromosome(F0[0]))}\n' )
                
def crossover(chromosme1,chromosome2):
    #Two descendants are generated
    new_chromosme1=chromosme1[0:crossover_point]
    new_chromosme1.extend(chromosome2[crossover_point:L_chromosome])
    new_chromosme2=chromosome2[0:crossover_point]
    new_chromosme2.extend(chromosme1[crossover_point:L_chromosome])

    return new_chromosme1, new_chromosme2

def mutation(chromosome1):
    #Each descendant is mutated with probability prob_m
    if random.random() < prob_m:
      chromosome1[int(round(random.random()*(L_chromosome-1)))]^=1

    return chromosome1

def next_generation():
    global n
    F0.sort(key=cmp_to_key(compare_chromosomes) )
    evaluate_chromosomes()
    
    n+=1
    if n%500 == 0: 
      print_solution(F0, fitness_values, n)                                             
    #elitism, the two best chromosomes go directly to the next generation
    F1[0]=F0[0]
    F1[1]=F0[1]
    #Creation of the wheel with fraction determined by the aptitudes
    roulette=create_wheel()
    for i in range(0,int((N_chromosomes-2)/2)):  
        #Crossover
        #Two parents are selected
        p1=random.choice(roulette)
        p2=random.choice(roulette)
        #Call to the crossover function
        o1,o2 = crossover(F0[p1],F0[p2])

        #Mutation
        #Call to the mutation function
        o1 = mutation(o1)
        o2 = mutation(o2)
        #The descendants are added to F1
        F1[2+2*i]=o1
        F1[3+2*i]=o2

    #The generation replaces the old one
    F0[:]=F1[:]
    evaluate_chromosomes()


F0.sort(  key=cmp_to_key(compare_chromosomes))
evaluate_chromosomes()

print(f'Values: {v} \nWeights: {w}\n')
for i in range(0, 10000):
  next_generation()

