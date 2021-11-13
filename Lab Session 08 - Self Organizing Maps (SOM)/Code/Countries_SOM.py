# Countries SOM using wellbeing indicators
# Alumno: Oaxaca Pérez David Arturo
# Materia: Evolutionary Computing

import numpy as np
import SOM

print( "Initialization...")
a = SOM.SOM(16,16,10,1,False,0.07)


training_set = []
test_set = []
countries = []
coordinates = []


f = open('countries.txt','r')
cont = 0
for line in f:
    muestra=[]
    line_split = line.split(',')
    countries.append(line_split[0])
    line_split = line_split[1:]

    for x in line_split:
        muestra.append(float(x))

    training_set.append([muestra,[cont]])
    cont+=1

f.close()

test_set = training_set[:] 

print( "Training for the countries function..." )
a.train(2850,training_set)

print( "\nPredictions for some countries..." )

for i in range(40):
  prediccion = a.predict(test_set[i][0], True)
  coordinates.append([prediccion[1],prediccion[2],countries[i]])
  #print(coordinates[i])
  print( f"Prediction para el pais de indice {i} ({countries[i]}):" \
  f"{round(prediccion[0][0],7)} | {round(prediccion[0][0])} | {prediccion[1], prediccion[2]}")
  
print( "\n")
map2D = []
for y in range(16):
    row=[]
    for x in range(16):
        row.append(round(a.nodes[(x)*a.width+y].PV[0]))
    map2D.append(row)

for coord in coordinates:
  map2D[coord[0]][coord[1]] = coord[2]

for row in map2D:
  for val in row:
    print(str(val).center(5, ' '), end="")
  print("")