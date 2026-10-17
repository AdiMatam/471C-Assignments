"""
Plot timing error statistic eps(N) vs RX oversample factor N for the Max Energy
and Early-Late gate symbol timing recovery methods.

results.txt format, one "algorithm, rx_oversample, error_statistic,
symbol_duration_us" row per line. Lines starting with '#' are comments.
    maxenergy, 4, 0.008900, 7.2
    elgate, 4, 0.008637, 7.2

Only rows with symbol duration >= 7.0 us are plotted (the 7.2 us sweep, plus
N = 14 at 7.28 us because 7.2 us has no valid sample-rate pair for N = 14).
The 1 us runs are ignored. If a point has repeated runs, the median is drawn
and the min-max spread is shown as an error bar.

Settings: tau_d = 0.34*Ts, h = 0.75*exp(j*pi/4), noise = -inf dB, 200
iterations per run. Log scale for eps (y), linear scale for N (x). A value of
exactly 0 cannot be drawn on a log axis, so it is drawn at ZERO_FLOOR.
"""

import statistics
from collections import defaultdict

import matplotlib.pyplot as plt

RESULTS_FILE = "results.txt"
OUTPUT_FILE = "../Lab3_timing_error.png"
MIN_DURATION_US = 7.0
ZERO_FLOOR = 1e-6


def load_results(path):
    runs = defaultdict(lambda: defaultdict(list))  # algorithm -> N -> [eps]
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            algo, n, eps, duration = [p.strip() for p in line.split(",")]
            if float(duration) < MIN_DURATION_US:
                continue
            runs[algo][int(n)].append(max(float(eps), ZERO_FLOOR))
    return runs


def summarize(by_n):
    n_vals = sorted(by_n)
    med = [statistics.median(by_n[n]) for n in n_vals]
    lo = [m - min(by_n[n]) for m, n in zip(med, n_vals)]
    hi = [max(by_n[n]) - m for m, n in zip(med, n_vals)]
    return n_vals, med, [lo, hi]


def main():
    runs = load_results(RESULTS_FILE)

    fig, ax = plt.subplots(figsize=(8, 6))
    for algo, label, fmt, color in (
        ("maxenergy", "Max Energy", "o-", "tab:blue"),
        ("elgate", "Early-Late Gate", "s--", "tab:orange"),
    ):
        n_vals, med, err = summarize(runs[algo])
        ax.errorbar(n_vals, med, yerr=err, fmt=fmt, color=color, markersize=7,
                    capsize=4, label=label)

    ax.set_yscale("log")
    ax.set_xticks(range(2, 21, 2))
    ax.set_xlabel("RX oversample factor $N$")
    ax.set_ylabel(r"Timing error $\varepsilon(N)$")
    ax.set_title(r"Timing error vs RX oversample factor ($\tau_d = 0.34\,T_s$)")
    ax.grid(True, which="both", alpha=0.5)
    ax.legend()

    fig.tight_layout()
    fig.savefig(OUTPUT_FILE, dpi=200)


if __name__ == "__main__":
    main()
