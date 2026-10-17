import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

N = 100000

bits = np.random.randint(0,2,N)

symbols = 2*bits - 1

fig, (ax1,ax2) = plt.subplots(
    1,2,
    figsize=(12,5)
)

plt.subplots_adjust(bottom=0.25)

def simulate(alpha):

    r = symbols.copy().astype(float)

    r[1:] += alpha*symbols[:-1]

    decisions = np.sign(r)

    ber = np.mean(decisions != symbols)

    return r, ber

alpha = 0

r, ber = simulate(alpha)

scatter = ax1.scatter(
    r[:2000],
    np.zeros(2000),
    alpha=0.3
)

ax1.set_xlim([-3,3])
ax1.set_ylim([-1,1])
ax1.grid()

ber_text = ax2.text(
    0.1,
    0.7,
    f"BER = {ber:.5f}",
    fontsize=18
)

ax2.axis('off')

slider_ax = plt.axes([0.2,0.1,0.6,0.03])

slider = Slider(
    slider_ax,
    'ISI',
    0,
    1,
    valinit=0
)

def update(val):

    alpha = slider.val

    r, ber = simulate(alpha)

    scatter.set_offsets(
        np.c_[r[:2000],np.zeros(2000)]
    )

    ber_text.set_text(
        f"BER = {ber:.5f}"
    )

    fig.canvas.draw_idle()

slider.on_changed(update)

plt.show()