import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc

snr_db = np.linspace(0,12,100)

snr = 10**(snr_db/10)

ber = 0.5*erfc(np.sqrt(snr))

plt.figure(figsize=(8,5))

plt.semilogy(
    snr_db,
    ber,
    linewidth=3
)

plt.grid(True,which='both')

plt.xlabel('Eb/N0 (dB)')
plt.ylabel('BER')

plt.title('BPSK BER Curve')

plt.show()