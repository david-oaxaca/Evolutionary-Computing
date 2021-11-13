#Looking for an optimal tour in the Traveling Salesman problem with a Genetic Algorithm
#Alumno: Oaxaca Pérez David Arturo
#Materia: Evolutionary Computing
#Profesor: Jorge Luis Rosas Trigueros
#Grupo: 3CV11
#Fecha de realización: 08/10/2021

'''
Ciudades que seran recorridas
           Berlin   Cairo   Chicago  Honolulu  London  CDMX   Montreal
Berlin        -     1,795    4,405    7,309      579   6,047   3,729
Cairo       1,795     -      6,129    8,838     2,181  7,688   5,414
Chicago     4,405   6,129      -      4,250     3,950  1,691    744
Honolulu    7,309	  8,838    4,250      -       7,228  3,779	 4,910
London       579	  2,181    3,950    7,228	      -    5,550	 3,282 
CDMX        6,047   7,688    1,691    3,779	    5,550    -     2,318	
Montreal    3,729	  5,414     744     4,910     3,282  2,318     -

'''

import math
import random
import time
import matplotlib.pyplot as plt
import numpy as np
from IPython import display as display
from functools import cmp_to_key

#Table of cities' distances
cities_distances = [ [None, 1795, 4405, 7309, 579, 6047, 3729],
                     [1795, None, 6129, 8838, 2181, 7688, 5414],
                     [4405, 6129, None, 4250, 3950, 1691, 744],
                     [7309,	8838, 4250, None, 7228, 3779, 4910],
                     [579, 2181, 3950, 7228, None, 5550, 3282],
                     [6047, 7688, 1691, 3779, 5550, None, 2318],
                     [3729, 5414, 744, 4910, 3282, 2318, None]]


#Chromosomes are 4 bits long
L_chromosome= len(cities_distances)
N_chains=2**L_chromosome
#Number of chromosomes
N_chromosomes=7
#Probability of mutation
prob_m=0.75
#Initial population
F0=[]
#Fitness values array
fitness_values=[]
#Points for the crossover
#(Since it's a cycle crossover these wont be used)
#crossover_start=2
#crossover_end=4
#Sum of all chromosomes 
suma=float(N_chromosomes*(N_chromosomes+1))/2.
#Wheel fractions
Lwheel=N_chromosomes*10

def random_chromosome():
    chromosome=random.sample(range(1,len(cities_distances)+1),len(cities_distances))
    return chromosome

def chromosome_creation():
  for i in range(0,N_chromosomes):
      F0.append(random_chromosome())
      
      fitness_values.append(0)

def decode_chromosome(chromosome):
  global L_chromosome

  # Distances between cities
  distances = []
  i,j = 0, 1
  while j < len(chromosome):
    #We advance with the counters adding the distances between cities in the tour
    city_1,city_2 = chromosome[i], chromosome[j]
    distances.append(cities_distances[city_1-1][city_2-1])
    i+=1
    j+=1

  #We add the distance of the last city to the first one to have a complete tour
  distances.append(cities_distances[chromosome[0]-1][chromosome[i]-1])

  return distances

def fitness_function(distances):
  #Retornamos la suma de todas las distancias
  return sum(distances)

    
def evaluate_chromosomes():
    global F0

    for p in range(N_chromosomes):
        distances=decode_chromosome(F0[p])
        fitness_values[p]=fitness_function(distances)

def compare_chromosomes(chromosome1,chromosome2):
    distance_chromosome1=decode_chromosome(chromosome1)
    distance_chromosome2=decode_chromosome(chromosome2)
    fitness_evaluation1=fitness_function(distance_chromosome1)
    fitness_evaluation2=fitness_function(distance_chromosome2)
    # if fitness_evaluation1 > fitness_evaluation2:
    if fitness_evaluation1 > fitness_evaluation2:
        return 1
    elif fitness_evaluation1 == fitness_evaluation2:
        return 0
    else: #fitness_evaluation1 < fitness_evaluation2
        return -1


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
        
#Creación de cromosomas
chromosome_creation()
F1=F0[:]
n=0

def print_solution(F0, fitness_values, n):
    print( "Best solution so far:")
    print(f'Poblacion: {F0}')
    print(f'Valores fitness: {fitness_values}\n')
    print( "Best solution so far:")
    print( f'Generacion {n}, Cromosoma mas apto: {F0[0]}')
    string_distances = [str(int) for int in decode_chromosome(F0[0])]
    display_distances = ', '.join(string_distances)
    print( f'f({display_distances})=  {fitness_function(decode_chromosome(F0[0]))}\n' )          

# Genetic operators

# Cycle crossover (CX)
def crossover(Chromosome1, Chromosome2):
  global L_chromosome
  offspring = [None for _ in range(L_chromosome)]
  free_elems = Chromosome1[:]

  #Initialization of the offspring withe the first city of the first chromosome
  offspring[0] = Chromosome1[0]
  free_elems.remove(offspring[0])
  leap = L_chromosome-1

  #If all the cities have been added to the offspring we end up the crossover
  while None in offspring:
    #If we come across to elements already added to the offspring we look for the next null
    while not (Chromosome2[leap] in offspring and Chromosome1[leap] in offspring):
      #We check wich element of the parents will be added given the leap
      if not (Chromosome2[leap] in offspring):
        #If the element of the second chromosome is not in the offspring, we take it
        offspring[leap] = Chromosome2[leap]
        free_elems.remove(offspring[leap])
        leap = Chromosome1.index(Chromosome2[leap])
      elif not (Chromosome1[leap] in offspring):
        #If the element of the first chromosome is not in the offspring, we take it
        offspring[leap] = Chromosome1[leap]
        free_elems.remove(offspring[leap])
        leap = Chromosome2.index(Chromosome1[leap])
    else:
      # We look for the next null value on the offspring tour 
      if Chromosome2[leap] in offspring and Chromosome1[leap] in offspring and offspring[leap] == None:
        #If we look at both options and none of them are elegible
        #we take the next city avaible on the first chromosome
        offspring[leap] = free_elems[0]
        free_elems.remove(offspring[leap])
      elif None in offspring:
        leap = offspring.index(None)  

    
  if len(set(offspring)) != len(offspring):
    print("REPETIDO!!!")

  #Return the offspring of the two chromosomes
  return offspring


# Exchange Mutation (EM)
def mutation(Chromosome):
  
  change_1, change_2 = random.sample(range(0,len(cities_distances)),2)
  Chromosome[change_1], Chromosome[change_2] = Chromosome[change_2], Chromosome[change_1]
  
  return Chromosome


def next_generation():
    global n
    F0.sort(key=cmp_to_key(compare_chromosomes) )
    evaluate_chromosomes()
    n+=1
    print_solution(F0, fitness_values, n)                                                      
    #elitism, the two best chromosomes go directly to the next generation
    F1[0]=F0[0]
    F1[1]=F0[1]
    roulette=create_wheel()
    for i in range(0,int((N_chromosomes-2)/2)):  

        #Crossover
        #Two parents are selected
        p1=random.choice(roulette)
        p2=random.choice(roulette)
        #Two descendants are generated
        o1 = crossover(F0[p1], F0[p2])
        o2 = crossover(F0[p2], F0[p1])

        #Mutation
        #Each descendant is mutated with probability prob_m
        if random.random() < prob_m:
            o1 = mutation(o1)
        if random.random() < prob_m:
            o2 = mutation(o2)
        #The descendants are added to F1
        F1[2+2*i]=o1
        F1[3+2*i]=o2

    #The generation replaces the old one
    F0[:]=F1[:]
    evaluate_chromosomes()


F0.sort(  key=cmp_to_key(compare_chromosomes))
evaluate_chromosomes()


for i in range(0, 200):
  next_generation()
