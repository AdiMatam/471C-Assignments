"""
Plot BER vs 1/N0 (dB) for BPSK and QPSK from results.txt.

results.txt format, one "N0_dB, BER_BPSK, BER_QPSK" row per line (header row
skipped):
    -10, 0.000034, 0.002184
    -8, 0.000728, 0.012288
    ...

Signal power is held at 1, so SNR (dB) = -N0 (dB). We plot BER (log scale,
y-axis) against 1/N0 (dB) = -N0_dB (linear scale, x-axis). Packet length =
500 bits, BER averaged over 1000 iterations per point.
"""

import matplotlib.pyplot as plt

RESULTS_FILE = "results.txt"


def load_results(path):
    x_vals = []
    bpsk_vals = []
    qpsk_vals = []
    with open(path) as f:
        next(f)  # skip header
        for line in f:
            line = line.strip()
            if not line:
                continue
            n0_db_str, bpsk_str, qpsk_str = line.split(",")
            n0_db = float(n0_db_str.strip())
            x_vals.append(-n0_db)  # 1/N0 in dB = -N0 in dB
            bpsk_vals.append(float(bpsk_str.strip()))
            qpsk_vals.append(float(qpsk_str.strip()))
    return x_vals, bpsk_vals, qpsk_vals


def main():
    x_vals, bpsk_vals, qpsk_vals = load_results(RESULTS_FILE)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(x_vals, bpsk_vals, "o-", color="tab:red", markersize=7, label="BPSK")
    ax.plot(x_vals, qpsk_vals, "s-", color="tab:blue", markersize=7, label="QPSK")

    ax.set_yscale("log")
    ax.set_xlabel(r"$1/N_0$ (dB)")
    ax.set_ylabel("BER")
    ax.set_title(r"BER vs $1/N_0$ — BPSK vs QPSK")
    ax.grid(True, which="both", alpha=0.5)
    ax.legend()

    fig.tight_layout()
    fig.savefig("ber_plot.png", dpi=200)
    plt.show()


if __name__ == "__main__":
    main()
