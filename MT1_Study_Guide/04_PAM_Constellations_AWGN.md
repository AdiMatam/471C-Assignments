# 04 — Pulse Amplitude Modulation, Constellations, Energy/Power/Bandwidth, AWGN (Weeks 5–6)

*Sources: PulseAmpModulation (second half), AWGNPulseShaping (first half), HW2 Q4, HW3 Q3, Practice/Class Q2, Lab 1 & Lab 2.1.*

> 📌 **In homework (⇒ likely important):** 📌 **HW2 Q4** (zero-mean normalized constellation) and **HW3 Q3** (16-APSK mean / zero-mean / energy / scale factor / plot). Section 2 (constellations, the 4-step normalization) is the homework-backed core. Sections 3–4 (power/bandwidth, AWGN/SNR/dB) were not in a homework; they're the prerequisites for BER — know them at a lighter level.

## Why this matters
This is the **transmitter**: bits → symbols → pulses. Constellation normalization (HW2 Q4, HW3 Q3) is a near-guaranteed question; the energy/SNR bookkeeping is the glue for every BER formula.

## 1. Linear complex pulse amplitude modulation

```
bits → [Symbol mapping] → s[n] → [pulse train, one s[n] per T] → [pulse-shaping filter g_tx(t)] → [gain √Ex] → x(t)
```
$$\boxed{x(t)=\sqrt{E_x}\sum_{n}s[n]\,g_{tx}(t-nT)}$$
- $s[n]\in\mathcal C$ (a **constellation**, complex numbers); $T$ = symbol period; **symbol rate** $1/T$; **bit rate** $\log_2 M/T$ for $M$ symbols.
- $g_{tx}(t)$: **unit-energy** pulse, $\int|g_{tx}|^2=1$. $E_x$: **symbol energy** (the *only* place we add energy).
- Special cases: **PAM** (real symbols; wireline), **QAM** (square grid), **PSK** (constant magnitude; EDGE), **QPSK = 4-QAM**.
- "Linear" because superposition of shifted, scaled pulses.

## 2. Constellations
A constellation = **alphabet of symbols + bit-to-symbol mapping**. Course assumptions: **equally likely, zero-mean, unit average energy.**

### Common constellations (unnormalized → normalized)
| Name | Symbols | Avg energy (unnormalized) | Normalize by |
|---|---|---|---|
| **BPSK** | $\{+1,-1\}$ | 1 | — |
| **M-PAM** | $\{\pm1,\pm3,\dots,\pm(M-1)\}$ | $(M^2-1)/3$ | $1/\sqrt{(M^2-1)/3}$ (4-PAM: $\div\sqrt5$) |
| **QPSK** | $\{1+j,-1+j,-1-j,1-j\}$ | 2 | $1/\sqrt2$ |
| **M-PSK** | $e^{j2\pi m/M}$, $m=0..M-1$ | 1 | — |
| **M-QAM** (square, $M$ = power of 4) | $\{(2a-\sqrt M-1)+j(2b-\sqrt M-1)\}$ | $2(M-1)/3$ | $1/\sqrt{2(M-1)/3}$ (16-QAM: $\div\sqrt{10}$) |

Usage: 4/16/64-QAM in cellular and WLAN, 256-QAM in 802.11ac, higher in microwave backhaul.

### Gray coding
Adjacent constellation points differ in **exactly one bit**. Why: the most likely error is to a nearest neighbor, so one *symbol* error ⇒ (usually) one *bit* error ⇒ BER ≈ $P_{\text{sym}}/\log_2M$. QPSK Gray map (lab convention): the two bits map independently to I and Q (e.g. first bit → sign of real, second → sign of imag), so QPSK = two independent BPSKs on I and Q.

### Mean and energy of a constellation
$$\mu=\frac1M\sum_{m}s_m\qquad E=\frac1M\sum_m|s_m|^2\ \ (\text{for a zero-mean set } E=\text{avg. energy})$$
- Non-zero mean ⇒ a **DC component** at baseband (problematic for hardware: DC offset/leakage) and wasted power. So we remove it.
- Normalize so $E=1$ to *control the transmit power* purely through $E_x$.

### 📌 Procedure: zero-mean normalized constellation (**memorize** — HW2 Q4, HW3 Q3)
1. **Mean:** $\mu=\tfrac1M\sum s_m$.
2. **Subtract:** $s_m'=s_m-\mu$ (check $\sum s'_m=0$).
3. **Energy:** $E'=\tfrac1M\sum|s'_m|^2$.
4. **Scale:** $\tilde s_m=s'_m/\sqrt{E'}$ ⇒ average energy exactly 1.

**HW2 Q4** ($C=\{j,\ \tfrac{1-j}{\sqrt2},\ -j,\ \tfrac{-1-j}{\sqrt2}\}$): $\mu=-j/(2\sqrt2)$, so it is *not* zero-mean. Subtract (your solution file has the full arithmetic): $s'=\{j\tfrac{2\sqrt2+1}{2\sqrt2},\ \tfrac{2-j}{2\sqrt2},\ -j\tfrac{2\sqrt2-1}{2\sqrt2},\ \tfrac{-2-j}{2\sqrt2}\}$, energies $\tfrac{9+4\sqrt2}{8},\tfrac58,\tfrac{9-4\sqrt2}8,\tfrac58$ ⇒ $E'=\tfrac14\cdot\tfrac{9+9+5+5}{8}=\tfrac{28}{32}=0.875$ ⇒ divide by $\sqrt{0.875}$.

📌 **HW3 Q3 (16-APSK, read from the figure: two rings of 8 points each, centered at $1+j$; inner radius $3-\sqrt2$, outer radius $3$):**
- (a) Mean: the rings are symmetric about their center, so $\mu=1+j$ (the cloud is just shifted from the origin).
- (b) Zero-mean constellation: $s'=s-(1+j)$ ⇒ 8 points at radius $3-\sqrt2$, 8 at radius $3$.
- (c) Average energy: $E=\tfrac12(3-\sqrt2)^2+\tfrac12(3)^2=\tfrac12(11-6\sqrt2)+\tfrac92=10-3\sqrt2\approx5.757$.
- (d) Scale factor $=1/\sqrt{E}=1/\sqrt{10-3\sqrt2}\approx0.417$.
- (e) Plot: same ring shape centered at the origin, radii $(3-\sqrt2)/\sqrt E\approx0.661$ and $3/\sqrt E\approx1.250$ (check: $\tfrac12(0.661^2+1.250^2)=1$ ✓).
(My worked check — confirm the 8+8 population against your figure.)

### Symbol energy vs constellation energy (don't mix)
- Constellation energy $E_s=E|s|^2=1$ (normalized).
- Symbol energy $E_x$ (a scalar gain) — the energy of the *transmitted* symbol: $\sqrt{E_x}\,s$ has energy $E_x$.
- Lab 2.1 `modulate.vi`'s "Symbol Energy" default = **1** (unit-energy constellation); the lab's raw tables (QPSK $\pm1\pm j$) have energy 2 until normalized.

## 3. Energy, power, bandwidth of $x(t)$
With unit-energy $g_{tx}$ and symbols iid, zero-mean, unit-energy:
- **Energy of $N$ symbols:** $N\,E_x$ (each symbol contributes $E_x$, pulses orthogonal if Nyquist).
- **Average transmit power:** $P=E_x/T$ (Joules/sec = Watts). (Equivalent: $E_x=PT$.)
- **PSD:** $x(t)$ is **cyclostationary** (not WSS); its (time-averaged) PSD is
 $$P_x(f)=\frac{E_x}{T}\,|G_{tx}(f)|^2$$
 ⇒ **bandwidth of $x(t)$ is determined entirely by the pulse shape $G_{tx}(f)$**, *not* by the constellation (given unit-energy zero-mean symbols).
- ⇒ So **design the pulse for bandwidth/ISI, design the constellation for energy/robustness.**

## 4. Additive white Gaussian noise (AWGN)
**Thermal noise** is in every receiver. Model of the received complex baseband signal sampled at the matched-filter output: $y=x+v$.
Properties:
1. **Additive.**
2. $v[n]$ is **IID circularly symmetric complex Gaussian** $\mathcal{CN}(0,N_0)$: real & imag independent $\mathcal N(0,N_0/2)$.
3. $N_0=k_BT_e$ (**power spectral density**): $k_B=1.38\times10^{-23}$ J/K, $T_e$ = effective noise temperature; **assume $T_e=290$ K** if nothing else is given ⇒ $N_0\approx4\times10^{-21}$ W/Hz $=-174$ dBm/Hz.
4. **White** because IID — flat PSD (really limited by analog front-end filters to the signal bandwidth $B$): **noise power in bandwidth $B$ = $N_0B$**.

### SNR and dB
- **SNR (at the symbol level)** $=\dfrac{E_x}{N_0}$ (energy per symbol / noise PSD). At a receiver front end: $\text{SNR}=\dfrac{P_r}{N_0B}$.
- **dB:** $x_{\text{dB}}=10\log_{10}x$ for powers/energies. $+3$ dB ≈ ×2; $+10$ dB = ×10; $-3$ dB = ×½. $\text{dBm}=10\log_{10}(P/1\text{mW})$. (20log for amplitudes.)
- **Example (slide):** $P_r=1\,\mu$W, $B=9$ MHz, $T_e=290$K: noise $=N_0B=4.0\times10^{-21}\cdot9\times10^6=3.6\times10^{-14}$ W ⇒ SNR $=10^{-6}/3.6\times10^{-14}=2.8\times10^7\Rightarrow\boxed{74.4\text{ dB}}$.
- **Lab 1:** the simulation sweeps $N_0$ from −10 to 0 dB with signal power 1 ⇒ SNR from 0 to 10 dB; plotted vs $1/N_0$ in dB.

### Intuition (slide: 4-PAM at high vs low SNR)
Noise spreads the received samples around the ideal levels. Larger noise power (lower SNR) ⇒ clouds grow, overlap neighboring decision regions ⇒ errors. Also (Lab 2.1 Sec 3 Q2) **received constellation scatter widens as noise power increases**.

## 5. Practice: BPSK waveform (Class Q2)
Mapping $0\to+A,\ 1\to-A$; with $g_{tx}=1/\sqrt T$ on $[0,T]$: $x(t)=\sum s[n]g_{tx}(t-nT)$ is a staircase with levels $s[n]/\sqrt T$. $A=3,T=2$, bits $1,1,0,1$: $-2.12,-2.12,+2.12,-2.12$ each lasting 2 s over $[0,8]$.

## Traps
- Normalizing *before* removing the mean (order: mean → subtract → energy → scale).
- Using the **sum** of energies instead of the **average**.
- Mixing $E_x/N_0$ (SNR) with $E_b/N_0$ ($E_b=E_x/\log_2M$) — keep track of which a formula uses.
- Noise variance per dimension is $N_0/2$ (complex total $N_0$).
- $\text{SNR}_{dB}$ uses 10log for power, not 20.

## Self-test
1. Normalize 8-PSK offset by $0.3$ on the real axis (mean=0.3 ⇒ subtract; energy of the rest).
2. 16-QAM unnormalized average energy? ($10$.) Scale factor? ($1/\sqrt{10}$)
3. Transmit power if $E_x=2\times10^{-9}$ J, $T=1$ μs? (2 mW.)
4. Give $P_x(f)$ and bandwidth of a rect-pulse BPSK signal. (sinc² shape; null-to-null $2/T$.)
5. Why Gray coding? 

## Lab link
Lab 2.1: `modulate.vi` (bits → symbols, symbol energy default 1) and `decode.vi` (ML decode → bits). BPSK: $\{+1,-1\}$; QPSK: Gray-coded $\{1+j,-1+j,-1-j,1-j\}$ scaled to unit energy.
