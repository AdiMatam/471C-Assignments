"""
Plot BER vs 1/N0 (dB) from results.txt.

results.txt format, one "N0_dB, BER" pair per line:
    -10, 4e-6
    -8, 0.000177
    ...

Signal power is held at 1, so SNR (dB) = -N0 (dB). We plot BER (log scale,
y-axis) against 1/N0 (dB) = -N0_dB (linear scale, x-axis).
"""

import matplotlib.pyplot as plt

RESULTS_FILE = "results.txt"


def load_results(path):
    x_vals = []
    ber_vals = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            n0_db_str, ber_str = line.split(",")
            n0_db = float(n0_db_str.strip())
            ber = float(ber_str.strip())
            x_vals.append(-n0_db)  # 1/N0 in dB = -N0 in dB
            ber_vals.append(ber)
    return x_vals, ber_vals


def main():
    x_vals, ber_vals = load_results(RESULTS_FILE)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x_vals, ber_vals, "o-", color="tab:red", markersize=7)

    ax.set_yscale("log")
    ax.set_xlabel(r"$1/N_0$ (dB)")
    ax.set_ylabel("BER")
    ax.set_title(r"BER vs $1/N_0$")
    ax.grid(True, which="both", alpha=0.5)

    fig.tight_layout()
    fig.savefig("ber_plot.png", dpi=200)
    plt.show()


if __name__ == "__main__":
    main()
