# Dynamic programming of Longest Common Subsequence

import numpy as np

L1 = 'EAVAOALAUACAIAOANA'
L2 = 'EVOLUCION'

x = len(L1)
y = len(L2)

m = np.zeros( (y+1, x+1) )

for row in range(1, y+1):
  for col in range(1, x+1):
    if L1[col-1] != L2[row-1]:
      m[row][col] = max(m[row-1][col], m[row][col-1])
    else:
      m[row][col] = m[row-1][col-1] + 1

LCS = ""
res = m[y][x]
i = y
j = x

while i > 0 and j > 0:

  if L1[j-1] == L2[i-1]:
    LCS = L1[j-1] + LCS
    i -= 1
    j -= 1
    res -= 1
  elif m[i][j-1] > m[i-1][j-1]:
    j -= 1
  else:
    i -= 1

  

print('Tabla generada de la solución Bottom-up: \n', m)
print(f'La subsecuencia mas larga de caracteres es de {m[y][x]}')
print(f'La subsecuencia mas larga de caracteres es {LCS}')
