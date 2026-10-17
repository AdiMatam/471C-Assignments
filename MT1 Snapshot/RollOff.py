import numpy as np
import matplotlib.pyplot as plt

alphas = [0,0.25,0.5,1.0]

f = np.linspace(-1.5,1.5,2000)

plt.figure(figsize=(8,4))

for alpha in alphas:

    H = np.zeros_like(f)

    if alpha == 0:
        H[np.abs(f) <= 0.5] = 1

    else:
        f1 = (1-alpha)/2
        f2 = (1+alpha)/2

        H[np.abs(f)<=f1] = 1

        idx = (np.abs(f)>f1) & (np.abs(f)<f2)

        H[idx] = 0.5*(1+
                      np.cos(np.pi/alpha*
                      (np.abs(f[idx])-f1)))

    plt.plot(f,H,label=f"alpha={alpha}")

plt.legend()
plt.grid()
plt.title("Raised Cosine Spectrum")
plt.show()