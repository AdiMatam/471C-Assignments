import numpy as np
import matplotlib.pyplot as plt

N = 5000

constellation = np.array([
    1+1j,
    1-1j,
   -1+1j,
   -1-1j
])

a = np.random.choice(constellation,N)

alpha = 0.5

r = a.copy()

r[1:] = a[1:] + alpha*a[:-1]

plt.figure(figsize=(6,6))

plt.scatter(
    r.real,
    r.imag,
    s=5,
    alpha=0.3
)

plt.grid(True)
plt.axis('equal')
plt.title(
    f'QPSK with ISI (alpha={alpha})'
)

plt.show()