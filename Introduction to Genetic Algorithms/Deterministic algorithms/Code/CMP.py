# Dynamic Programming of Coin Change Problem

import numpy as np

d = [1, 2, 4]
N = 6

N_den = len(d)

m = np.zeros((N_den, N+1))

for col in range(N+1):
  m[0][col] = col

for row in range(1,N_den):
  for col in range(1, N+1):
    if d[row] > col:
      m[row][col] = m[row-1][col]
    else:
      m[row][col] = min( m[row-1,col], m[row][col-d[row]]+1)


coins_taken = []
amount = m[N_den-1][N]
total_value = N

for i in range(N_den-1, -1, -1):
  if (amount != m[i-1][total_value]) and (d[i] <= total_value):
    coins_per_den = [d[i], total_value//d[i]]
    coins_taken.append(coins_per_den)
    amount = m[i-1][total_value]
    total_value = total_value%d[i]

print('Tabla generada de solución Bottom Up:\n', m)
print(f'Las denominaciones de monedas y su respectiva cantidad de monedas tomadas: {coins_taken}')  