#Dynamic programming of Knapsack 0-1 problem

import numpy as np

v = (6, 10, 12)
w = (1, 2, 3)
W = 5
N = len(v)

m = np.zeros( (N+1, W+1) )

for row in range(1,N+1):
  for col in range(1, W+1):
    if w[row-1] > col:
      m[row][col] = m[row-1][col]
    else:
      m[row][col] = max( m[row-1][col], m[row-1][col-w[row-1]]+v[row-1])


items_taken = []
weight = W
res = m[N][W]

for i in range(N, 0, -1):
  if res <= 0:
    break
  if res == m[i-1][weight]:
    continue
  else:
    items_taken.append(w[i-1])
    res = res - v[i-1]
    weight = weight - w[i-1]



print('Tabla generada de solución Bottom Up:\n', m)

print(f'Lista de los indices de los elementos tomados: {items_taken}')