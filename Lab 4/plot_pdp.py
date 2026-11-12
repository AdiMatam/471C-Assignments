"""
Lab 4 Sec 3.2: power-delay profile of the wideband link (T = 0.2 us, channel estimate length 6).

Per-packet values are hardcoded normalized |h^[n]|^2 in dB; the average at each tap is the mean
in LINEAR power over the packets listed for that tap.

Run:  MPLBACKEND=Agg python3 plot_pdp.py     -> Lab4_PDP.png
"""
import os
import numpy as np
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))

delay_us = np.array([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])

# Per-packet normalized power |h^[n]|^2 (dB) at each tap (one list per tap)
packets_db = [
    [-0.5, -3.0],
    [-4.0, -7.5, -9.5, -15.1, -19.4],
    [-8.0, -10.4, -12.6, -16.0, -19.5],
    [-14.2, -14.5, -18.2, -19.8, -30.9],
    [-17.3, -20.4, -21.1, -22.5, -25.4],
    [-23.7, -24.2, -29.6, -29.9, -36.1],
]

# Average PDP: mean of LINEAR power over the packets at each tap, then back to dB
avg_db = np.array([10 * np.log10(np.mean(10 ** (np.array(v) / 10))) for v in packets_db])

ORANGE, BLACK, INK, MUTED = "#eb6834", "#000000", "#2b2b29", "#8a8a85"
plt.rcParams.update({"axes.spines.top": False, "axes.spines.right": False, "font.size": 10,
                     "axes.edgecolor": MUTED})

fig, ax = plt.subplots(figsize=(7.5, 4.4))
FLOOR = -40
ax.vlines(delay_us, FLOOR, avg_db, color=ORANGE, lw=2)
for i, (x, vals) in enumerate(zip(delay_us, packets_db)):
    ax.scatter([x] * len(vals), vals, s=18, color=BLACK, alpha=0.8, linewidths=0, zorder=3,
               label="individual packets" if i == 0 else None)
ax.scatter(delay_us, avg_db, s=50, color=ORANGE, zorder=4, label="average over packets")
for x, v in zip(delay_us, avg_db):
    ax.annotate(f"{v:.1f} dB", (x, v), textcoords="offset points", xytext=(10, 2), fontsize=8, color=INK)

ax.set(xlabel="Delay τ = n·T (µs),  T = 0.2 µs", ylabel="Normalized pwr (dB)",
       ylim=(FLOOR, 3), xlim=(-0.08, 1.12), xticks=delay_us,
       title="Power-delay profile, wideband link (5 MSym/s)")
ax.grid(alpha=0.5)
ax.legend(frameon=False, fontsize=9, loc="upper right")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "Lab4_PDP.png"), dpi=200)

print("Average PDP (dB):", np.round(avg_db, 2))
