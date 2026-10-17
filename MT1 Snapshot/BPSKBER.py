import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from scipy.special import erfc

N = 50000

bits = np.random.randint(0,2,N)

symbols = 2*bits - 1

fig = plt.figure(figsize=(11,5))

ax1 = plt.subplot(121)
ax2 = plt.subplot(122)

plt.subplots_adjust(bottom=0.25)

snr_db = 8

def compute_ber(snr_db):

    snr = 10**(snr_db/10)

    sigma = np.sqrt(1/(2*snr))

    noise = sigma*np.random.randn(N)

    rx = symbols + noise

    decisions = np.sign(rx)

    ber_sim = np.mean(decisions != symbols)

    ber_theory = 0.5*erfc(np.sqrt(snr))

    return rx, ber_sim, ber_theory

rx, ber_sim, ber_theory = compute_ber(snr_db)

scatter = ax1.scatter(
    rx[:2000],
    np.zeros(2000),
    alpha=0.25
)

ax1.set_xlim([-4,4])
ax1.set_ylim([-1,1])
ax1.grid(True)
ax1.set_title("Received BPSK Symbols")

snr_range = np.linspace(0,12,50)

ber_theory_curve = 0.5*erfc(np.sqrt(10**(snr_range/10)))

line_theory, = ax2.semilogy(
    snr_range,
    ber_theory_curve,
    label='Theory'
)

point_sim, = ax2.semilogy(
    snr_db,
    ber_sim,
    'ro',
    markersize=8,
    label='Simulation'
)

ax2.grid(True,which='both')
ax2.set_xlabel('SNR (dB)')
ax2.set_ylabel('BER')
ax2.legend()

slider_ax = plt.axes([0.2,0.1,0.6,0.03])

slider = Slider(
    slider_ax,
    'SNR(dB)',
    0,
    12,
    valinit=snr_db
)

def update(val):

    snr_db = slider.val

    rx, ber_sim, ber_theory = compute_ber(snr_db)

    scatter.set_offsets(
        np.c_[rx[:2000], np.zeros(2000)]
    )

    point_sim.set_data(
        [snr_db],
        [ber_sim]
    )

    fig.canvas.draw_idle()

slider.on_changed(update)

plt.show()