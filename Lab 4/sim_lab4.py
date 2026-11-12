"""
Lab 4 pre-lab reference simulation (NOT hardware data).

Models the Lab 4 link at the symbol rate:
  QPSK, root-raised-cosine TX/RX (alpha = 0.5 assumed) -> composite pulse = raised cosine,
  44-symbol training (4 x Barker-11), 500-bit packets (250 QPSK symbols), AWGN.
The same indoor multipath channel h(tau) is seen through
  - the narrowband system (Sec 3.1): T = 10 us   (100 kSym/s)
  - the wideband system   (Sec 3.2): T = 0.2 us  (5 MSym/s)
Receiver: LS channel estimate (L+1 = 6 taps) and direct LS equalizer (Eq. 14) with delay search.

Run:  MPLBACKEND=Agg python3 sim_lab4.py      (writes PNGs + sim_results.txt next to this file)
"""
import os
import numpy as np
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(471)
out_lines = []


def log(s=""):
    print(s)
    out_lines.append(s)


BLUE, ORANGE, AQUA, INK, MUTED = "#2a78d6", "#eb6834", "#1baf7a", "#2b2b29", "#8a8a85"
plt.rcParams.update({"axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": INK,
                     "ytick.color": INK, "axes.spines.top": False, "axes.spines.right": False,
                     "font.size": 10})

ALPHA = 0.5                      # RRC roll-off (assumed default, same as Lab 3)
BARKER11 = np.array([1, 1, 1, -1, -1, -1, 1, -1, -1, 1, -1], dtype=complex)
TRAIN = np.tile(BARKER11, 4)     # 44 symbols; direct equalizer uses first half (Nt = 22)
N_DATA = 250                     # 500 bits / 2 bits per QPSK symbol
N_ZEROS = 30                     # trailing zeros the framework appends (illustrative)

# ---- physical indoor multipath channel h(tau): LOS + decaying reflections -------------
DELAYS = np.array([0, 20, 45, 90, 150, 250, 400, 600]) * 1e-9          # seconds
POW_DB = np.array([0, -4, -6, -9, -12, -16, -20, -25], dtype=float)
PHASES = rng.uniform(0, 2 * np.pi, DELAYS.size)
GAINS = 10 ** (POW_DB / 20) * np.exp(1j * PHASES)
GAINS /= np.sqrt(np.sum(np.abs(GAINS) ** 2))                            # unit total power


def raised_cosine(t, T):
    x = t / T
    den = 1 - (2 * ALPHA * x) ** 2
    sing = np.abs(den) < 1e-10
    val = np.sinc(x) * np.cos(np.pi * ALPHA * x) / np.where(sing, 1, den)
    return np.where(sing, np.pi / 4 * np.sinc(1 / (2 * ALPHA)), val)


def discrete_channel(T, gains, eps, n):
    """h[n] = sum_k g_k p(nT + eps - tau_k): composite TX pulse * channel * RX matched filter."""
    return np.array([np.sum(gains * raised_cosine(k * T + eps - DELAYS, T)) for k in n])


def qpsk(nsym):
    bits = rng.integers(0, 2, 2 * nsym)
    sym = ((1 - 2 * bits[0::2]) + 1j * (1 - 2 * bits[1::2])) / np.sqrt(2)
    return bits, sym


def qpsk_demod(r):
    b = np.empty(2 * r.size, dtype=int)
    b[0::2] = (r.real < 0)
    b[1::2] = (r.imag < 0)
    return b


def through_channel(s, h, n0, snr_db):
    """y[n] = sum_m h[m] s[n-m] + v[n]; h is indexed starting at m = n0 (n0 <= 0 allows precursors)."""
    full = np.convolve(s, h)
    y = full[-n0: -n0 + s.size]
    nvar = 10 ** (-snr_db / 10) * np.sum(np.abs(h) ** 2)                 # received SNR (Es = 1)
    return y + np.sqrt(nvar / 2) * (rng.standard_normal(y.size) + 1j * rng.standard_normal(y.size))


def toeplitz(col, row):
    m, n = len(col), len(row)
    return np.array([[col[i - j] if i >= j else row[j - i] for j in range(n)] for i in range(m)])


def ls_channel_estimate(y, t, L):
    """Sec 1.2: rows n = L..Nt-1 of [t[n] ... t[n-L]] a = y[n]."""
    Tm = toeplitz(t[L:], t[L::-1])
    a, *_ = np.linalg.lstsq(Tm, y[L:t.size], rcond=None)
    return a


def direct_equalizer(y, t, Lf, nd):
    """Eq. (13)-(14): rows n = 0..Nt-1 of [y[n+nd] ... y[n+nd-Lf]] f = t[n]; y[<0] taken as 0."""
    ypad = np.concatenate([np.zeros(Lf), y])
    Y = np.array([[ypad[Lf + n + nd - l] for l in range(Lf + 1)] for n in range(t.size)])
    f, *_ = np.linalg.lstsq(Y, t, rcond=None)
    J = np.sum(np.abs(Y @ f - t) ** 2)
    return f, J


def equalize(y, f, nd):
    Lf = f.size - 1
    ypad = np.concatenate([np.zeros(Lf), y, np.zeros(nd + 1)])
    return np.array([np.sum(f * ypad[Lf + n + nd - np.arange(Lf + 1)]) for n in range(y.size)])


def receive(y, Lf):
    """Direct equalizer with delay search over nd = 0..Lf (the framework's equalizer.vi loop)."""
    t = TRAIN[:TRAIN.size // 2]
    best = min((direct_equalizer(y, t, Lf, nd) + (nd,) for nd in range(Lf + 1)), key=lambda z: z[1])
    f, J, nd = best
    return equalize(y, f, nd), f, nd, J


# =========================================================================================
# Directions Q3 / 3(c): tap counts for support [0, 2.5 us)
# =========================================================================================
T_NB, T_WB = 1 / 100e3, 1 / 5e6
log("=== Symbol rates / bandwidths (alpha = %.2f assumed) ===" % ALPHA)
for name, Rs in [("Narrowband (3.1)", 100e3), ("Wideband   (3.2)", 5e6)]:
    log(f"{name}: Rs = {Rs/1e3:.0f} kSym/s, T = {1e6/Rs:.1f} us, "
        f"passband BW = (1+a)Rs = {(1+ALPHA)*Rs/1e3:.0f} kHz, Nyquist-min = {Rs/1e3:.0f} kHz")
support = 2.5e-6
for name, T in [("narrowband", T_NB), ("wideband", T_WB)]:
    taps = int(np.ceil(support / T - 1e-12))
    log(f"Taps in [0, 2.5 us) for {name}: {taps}  (n = 0..{taps-1})")
log()

# =========================================================================================
# How much ISI the same physical channel causes in each system
# =========================================================================================
n_axis = np.arange(-3, 12)
for name, T in [("narrowband", T_NB), ("wideband", T_WB)]:
    h = discrete_channel(T, GAINS, 0.0, n_axis)
    main = np.argmax(np.abs(h))
    sir = np.abs(h[main]) ** 2 / (np.sum(np.abs(h) ** 2) - np.abs(h[main]) ** 2)
    log(f"{name}: |h[main]|^2 = {abs(h[main])**2:.3f}, signal-to-ISI ratio = {10*np.log10(sir):.1f} dB")
rms = np.sqrt(np.sum(np.abs(GAINS) ** 2 * DELAYS ** 2) - np.sum(np.abs(GAINS) ** 2 * DELAYS) ** 2)
log(f"Model channel RMS delay spread = {rms*1e9:.0f} ns, max excess delay = {DELAYS.max()*1e9:.0f} ns")
log()

# =========================================================================================
# Sec 3.1: narrowband constellation before / after 1-tap equalization
# =========================================================================================
SNR_NB = 20
RX_SCALE = 0.04            # arbitrary USRP amplitude -> why the manual says to auto-scale
CFO_RES = 15.0             # Hz residual carrier offset (illustrative)
h_nb = RX_SCALE * discrete_channel(T_NB, GAINS, 0.0, np.arange(-1, 2))
bits_nb, data_nb = qpsk(N_DATA)
s_nb = np.concatenate([TRAIN, data_nb, np.zeros(N_ZEROS)])
y_nb = RX_SCALE * through_channel(s_nb, h_nb / RX_SCALE, -1, SNR_NB)   # scale after AWGN keeps SNR
y_nb = y_nb * np.exp(1j * 2 * np.pi * CFO_RES * T_NB * np.arange(s_nb.size))
r_nb, f_nb, nd_nb, _ = receive(y_nb, Lf=0)
ber_nb = np.mean(qpsk_demod(r_nb[TRAIN.size:TRAIN.size + N_DATA]) != bits_nb)
log("=== Sec 3.1 narrowband ===")
log(f"h_nb[-1,0,1] (x1/RX_SCALE) = " + ", ".join(f"{v/RX_SCALE:.3f}" for v in h_nb))
log(f"|h_nb[0]| = {abs(h_nb[1]):.4f}, angle = {np.degrees(np.angle(h_nb[1])):.1f} deg; "
    f"1-tap equalizer f = {abs(f_nb[0]):.1f} at {np.degrees(np.angle(f_nb[0])):.1f} deg; BER = {ber_nb:.4f}")
log(f"Residual CFO {CFO_RES:.0f} Hz rotates the constellation "
    f"{360*CFO_RES*T_NB*s_nb.size:.1f} deg over one packet")
log()

fig, ax = plt.subplots(1, 2, figsize=(10, 4.6))
seg = [(slice(0, TRAIN.size), MUTED, "training (BPSK Barker)"),
       (slice(TRAIN.size, TRAIN.size + N_DATA), BLUE, "QPSK data"),
       (slice(TRAIN.size + N_DATA, None), ORANGE, "trailing zeros")]
for sl, c, lab in seg:
    ax[0].scatter(y_nb[sl].real, y_nb[sl].imag, s=9, color=c, label=lab, alpha=0.8, linewidths=0)
lim = 1.4 * np.max(np.abs(y_nb))
ax[0].set(xlim=(-lim, lim), ylim=(-lim, lim), aspect="equal", xlabel="In-phase", ylabel="Quadrature",
          title="Before equalization (synchronize.vi output)\nauto-scaled: amplitude is ~0.04, not 1")
ax[0].legend(loc="upper left", fontsize=8, frameon=False)
ax[1].scatter(r_nb[TRAIN.size:TRAIN.size + N_DATA].real, r_nb[TRAIN.size:TRAIN.size + N_DATA].imag,
              s=9, color=BLUE, linewidths=0)
ax[1].set(xlim=(-1.5, 1.5), ylim=(-1.5, 1.5), aspect="equal", xlabel="In-phase",
          title=f"After 1-tap equalizer (L$_f$+1 = 1)\nBER = {ber_nb:.3f}")
for a in ax:
    a.grid(alpha=0.5)
    a.axhline(0, color=MUTED, lw=0.6)
    a.axvline(0, color=MUTED, lw=0.6)
fig.suptitle(f"Sec 3.1 simulated: narrowband channel, T = 10 µs, SNR = {SNR_NB} dB, "
             f"{CFO_RES:.0f} Hz residual CFO", fontsize=10)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "Lab4_sim_narrowband_constellation.png"), dpi=160)

# =========================================================================================
# Sec 3.2: wideband packets -> LS channel estimates -> power-delay profile
# =========================================================================================
SNR_WB = 20
L = 5                        # channel estimate length 6 => L = 5
N_PKT = 8
BAD_PKT = 5                  # simulate one frame-detection error (receiver starts 8 symbols late)
n_true = np.arange(-2, 12)   # true composite channel includes precursors and a long tail
hhat = np.zeros((N_PKT, L + 1), dtype=complex)
bers = np.zeros(N_PKT)
log("=== Sec 3.2 wideband: per-packet LS channel estimates ===")
log("pkt  timing_eps   |h^[0..5]|^2" + " " * 34 + "BER(Lf+1=6)  keep")
for p in range(N_PKT):
    eps = rng.uniform(-T_WB / 4, T_WB / 4)           # RX oversample 2 -> timing error within +-T/4
    gains = GAINS * (1 + 0.15 * (rng.standard_normal(GAINS.size) + 1j * rng.standard_normal(GAINS.size)))
    h = discrete_channel(T_WB, gains, eps, n_true)
    bits, data = qpsk(N_DATA)
    s = np.concatenate([TRAIN, data, np.zeros(N_ZEROS)])
    y = through_channel(s, h, n_true[0], SNR_WB)
    if p == BAD_PKT:
        y = np.concatenate([y[8:], np.zeros(8)])
    hhat[p] = ls_channel_estimate(y, TRAIN, L)
    r, f, nd, J = receive(y, Lf=5)
    bers[p] = np.mean(qpsk_demod(r[TRAIN.size:TRAIN.size + N_DATA]) != bits)
    keep = bers[p] <= 0.10
    log(f"{p:3d}  {eps*1e9:+6.1f} ns   " + " ".join(f"{v:.3f}" for v in np.abs(hhat[p]) ** 2)
        + f"     {bers[p]:.3f}       {'yes' if keep else 'NO (frame error)'}")
kept = bers <= 0.10
pdp = np.mean(np.abs(hhat[kept]) ** 2, axis=0)
pdp_norm = pdp / pdp.max()
log("Averaged PDP over kept packets (normalized): " + ", ".join(f"{v:.3f}" for v in pdp_norm))
log("Averaged PDP in dB:                           " + ", ".join(f"{10*np.log10(v):.1f}" for v in pdp_norm))
excess = np.sum(pdp_norm * np.arange(L + 1) * T_WB) / np.sum(pdp_norm)
rms_est = np.sqrt(np.sum(pdp_norm * (np.arange(L + 1) * T_WB) ** 2) / np.sum(pdp_norm) - excess ** 2)
log(f"Mean excess delay = {excess*1e9:.0f} ns, RMS delay spread from estimated PDP = {rms_est*1e9:.0f} ns")
log()

fig, ax = plt.subplots(figsize=(7.5, 4.4))
tau_us = np.arange(L + 1) * T_WB * 1e6
ax.bar(tau_us, 10 * np.log10(pdp_norm) + 40, bottom=-40, width=0.09, color=BLUE,
       label=f"average of {kept.sum()} kept packets")
for p in np.where(kept)[0]:
    ax.scatter(tau_us, 10 * np.log10(np.abs(hhat[p]) ** 2 / pdp.max()), s=14, color=INK, alpha=0.35,
               linewidths=0, label="individual packets (same scale)" if p == np.where(kept)[0][0] else None)
for x, v in zip(tau_us, 10 * np.log10(pdp_norm)):
    ax.annotate(f"{v:.1f}", (x, v), textcoords="offset points", xytext=(0, 4), ha="center", fontsize=8,
                color=INK)
ax.set(xlabel="Delay  τ = n·T  (µs),  T = 0.2 µs", ylabel="P[n] = E{|ĥ[n]|²}  (dB, rel. peak)",
       ylim=(-40, 5), xticks=tau_us,
       title=f"Sec 3.2 simulated power-delay profile\n(SNR = {SNR_WB} dB, L+1 = 6, "
             f"{kept.sum()} of {N_PKT} packets kept)")
ax.grid(alpha=0.5, axis="y")
ax.legend(frameon=False, fontsize=8, loc="upper right")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "Lab4_sim_power_delay_profile.png"), dpi=160)

# =========================================================================================
# Directions 3(c)/(d): sampling h(tau) at T_nb vs T_wb
# =========================================================================================
tau = np.linspace(0, 2.5e-6, 1000, endpoint=False)
h_cont = np.exp(-tau / 0.7e-6) * (0.6 + 0.4 * np.cos(2 * np.pi * tau / 0.9e-6))   # illustrative h(tau)
fig, ax = plt.subplots(figsize=(7.5, 3.8))
ax.plot(tau * 1e6, h_cont, color=MUTED, lw=2, label="continuous-time |h(τ)| (support [0, 2.5 µs))")
n_wb = np.arange(13)
hv = np.exp(-n_wb * T_WB / 0.7e-6) * (0.6 + 0.4 * np.cos(2 * np.pi * n_wb * T_WB / 0.9e-6))
ax.vlines(n_wb * T_WB * 1e6, 0, hv, color=BLUE, lw=2)
ax.scatter(n_wb * T_WB * 1e6, hv, color=BLUE, s=36, zorder=3, label="wideband h[n], T = 0.2 µs: 13 taps")
ax.scatter([0], [1.0], s=110, facecolors="none", edgecolors=ORANGE, linewidths=2, zorder=4,
           label="narrowband h[n], T = 10 µs: 1 tap (next sample at 10 µs)")
ax.axvline(2.5, color=INK, lw=1, ls="--")
ax.annotate("support ends\n2.5 µs", (2.5, 0.75), xytext=(-6, 0), textcoords="offset points", ha="right",
            fontsize=8, color=INK)
ax.set(xlabel="τ (µs)", ylabel="|h|", xlim=(-0.1, 2.8), ylim=(0, 1.15),
       title="Directions Q3(c): the same channel sampled by each system")
ax.grid(alpha=0.5)
ax.legend(frameon=False, fontsize=8, loc="upper right")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "Lab4_sim_tap_resolution.png"), dpi=160)

# =========================================================================================
# Sec 3.3 demo: wideband, equalizer length 1 vs 6 (constellation + BER vs SNR)
# =========================================================================================
eps0 = 0.25 * T_WB
h0 = discrete_channel(T_WB, GAINS, eps0, n_true)
bits, data = qpsk(N_DATA)
s = np.concatenate([TRAIN, data, np.zeros(N_ZEROS)])
y = through_channel(s, h0, n_true[0], 18)
fig, ax = plt.subplots(1, 2, figsize=(9, 4.4))
log("=== Sec 3.3 demo (wideband channel, SNR 18 dB, single packet) ===")
for a, Lf, c in [(ax[0], 0, ORANGE), (ax[1], 5, BLUE)]:
    r, f, nd, J = receive(y, Lf)
    rd = r[TRAIN.size:TRAIN.size + N_DATA]
    ber = np.mean(qpsk_demod(rd) != bits)
    log(f"Lf+1 = {Lf+1}: chosen nd = {nd}, training LS error J = {J:.3f}, BER = {ber:.3f}")
    a.scatter(rd.real, rd.imag, s=9, color=c, linewidths=0)
    a.set(xlim=(-1.8, 1.8), ylim=(-1.8, 1.8), aspect="equal", xlabel="In-phase",
          title=f"L$_f$+1 = {Lf+1}  (n$_d$ = {nd}),  BER = {ber:.3f}")
    a.grid(alpha=0.5)
ax[0].set_ylabel("Quadrature")
fig.suptitle("Sec 3.3 simulated: wideband channel after direct LS equalizer, SNR = 18 dB", fontsize=10)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "Lab4_sim_equalizer_demo.png"), dpi=160)

snrs = np.arange(0, 16, 2)
N_MC = 150
ber_curve = {0: [], 5: [], 'awgn': []}
for snr in snrs:
    errs = {0: 0, 5: 0, 'awgn': 0}
    for _ in range(N_MC):
        eps = rng.uniform(-T_WB / 4, T_WB / 4)
        h = discrete_channel(T_WB, GAINS, eps, n_true)
        bits, data = qpsk(N_DATA)
        s = np.concatenate([TRAIN, data, np.zeros(N_ZEROS)])
        y = through_channel(s, h, n_true[0], snr)
        for Lf in (0, 5):
            r, *_ = receive(y, Lf)
            errs[Lf] += np.sum(qpsk_demod(r[TRAIN.size:TRAIN.size + N_DATA]) != bits)
        r, *_ = receive(through_channel(s, np.array([1.0 + 0j]), 0, snr), 0)   # AWGN-only sanity check
        errs['awgn'] += np.sum(qpsk_demod(r[TRAIN.size:TRAIN.size + N_DATA]) != bits)
    for Lf in (0, 5, 'awgn'):
        ber_curve[Lf].append(max(errs[Lf], 0.5) / (N_MC * 2 * N_DATA))
log("BER vs SNR on the wideband lab channel (Monte Carlo, %d packets/pt; floor 1/%d):" % (N_MC, N_MC * 500))
log("SNR(dB): " + "  ".join(f"{s:>7d}" for s in snrs))
for Lf in (0, 5):
    log(f"Lf+1={Lf+1}: " + "  ".join(f"{b:7.1e}" for b in ber_curve[Lf]))
log("AWGN   : " + "  ".join(f"{b:7.1e}" for b in ber_curve['awgn']))

fig, ax = plt.subplots(figsize=(6.5, 4.2))
ax.semilogy(snrs, ber_curve[0], "-o", color=ORANGE, lw=2, ms=7, label="L$_f$+1 = 1")
ax.semilogy(snrs, ber_curve[5], "-s", color=BLUE, lw=2, ms=7, label="L$_f$+1 = 6")
from math import erfc
snr_f = np.linspace(0, 14, 200)
ax.semilogy(snr_f, [0.5 * erfc(np.sqrt(10 ** (x / 10) / 2)) for x in snr_f], "--", color=MUTED, lw=2,
            label="AWGN only, theory Q(√SNR) (reference)")
ax.set_ylim(1e-7, 1)
ax.set(xlabel="SNR (dB)", ylabel="BER", title="Simulated BER, wideband lab channel (QPSK, direct LS eq.)")
ax.grid(alpha=0.5, which="both")
ax.legend(frameon=False)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "Lab4_sim_ber_vs_snr.png"), dpi=160)

with open(os.path.join(HERE, "sim_results.txt"), "w") as fh:
    fh.write("\n".join(out_lines) + "\n")
