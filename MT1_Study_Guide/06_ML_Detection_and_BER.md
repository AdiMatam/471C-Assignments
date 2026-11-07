# 06 — Maximum-Likelihood Detection, Voronoi Regions, Probability of Error (Week 7)

*Sources: DigitalFilterImplementation (second half: ML detection, symbol error), Lab 1 (BER sim), Lab 2.1 (`decode.vi`, BER vs SNR).*

> 📌 **Not in HW1–HW3** (BER appeared in Lab 1/Lab 2 prelabs, not a homework). **Likely out of scope** per your instructor — but BPSK $Q(\sqrt{2E_s/N_0})$ and "nearest symbol" detection are cheap to remember, and you've already done them in the labs.

## Why this matters
This is how we **decide** which symbol was sent and **quantify performance**. The lab prelab (BPSK BER = $Q(\sqrt{2E_s/N_0})$, QPSK vs BPSK) is the core. Expect: derive ML rule, draw decision regions, compute BER/SER with Q-function, explain the 3 dB BPSK/QPSK gap, union bound.

## 1. The detection problem
After matched filtering + ideal sampling + Nyquist pulse (Block 05):
$$\boxed{y[n]=\sqrt{E_x}\,s[n]+v[n],\qquad v[n]\sim\mathcal{CN}(0,N_0)\ \text{IID}}$$
Given $y[n]$, guess $s[n]\in\mathcal C$.

## 2. Maximum-likelihood (ML) detection
- **Optimality:** if symbols are **equally likely**, ML minimizes the probability of detection error (it equals MAP in that case).
- **Likelihood of the observation given a hypothesis $s$:** 
 $$f(y\mid s)=\frac{1}{\pi N_0}\exp\!\left(-\frac{|y-\sqrt{E_x}\,s|^2}{N_0}\right)$$
 (complex Gaussian: real and imaginary parts independent $\mathcal N(\cdot,N_0/2)$).
- ML: $\hat s=\arg\max_{s\in\mathcal C}f(y\mid s)=\arg\max_s\big[-|y-\sqrt{E_x}s|^2\big]$ since $\log$ is monotone:
$$\boxed{\hat s[n]=\arg\min_{s\in\mathcal C}\ \big|y[n]-\sqrt{E_x}\,s\big|^2}$$
**ML for AWGN = minimum Euclidean distance (nearest-symbol) detection.**
- Noise variance **drops out** of the decision rule (it matters only for performance).
- Complexity: compare to $M$ symbols; simplifications via regions:

### Voronoi (decision) regions
The set of $y$ closest to symbol $s_m$ = **Voronoi region** of $s_m$; boundaries are **perpendicular bisectors** between neighbors.
- **BPSK:** boundary at 0 ⇒ $\hat s=\text{sign}(\text{Re}\,y)$.
- **QPSK:** the four quadrants ⇒ decide each bit independently from the sign of $\text{Re}\,y$ and $\text{Im}\,y$ (Gray map: bit1 from I, bit2 from Q) — which is why the lab's `decode.vi` can use sign tests.
- **M-QAM:** grid of rectangles; **M-PSK:** pie-slices.
(An observation falling in a region maps directly to the symbol generating it, so no distance computation needed.)

## 3. The Q-function
$$Q(x)=P(Z>x)=\int_x^\infty\tfrac{1}{\sqrt{2\pi}}e^{-t^2/2}dt,\quad Z\sim\mathcal N(0,1)$$
- $Q(0)=\tfrac12$; $Q(-x)=1-Q(x)$; decreasing; $Q(x)\approx\tfrac1{x\sqrt{2\pi}}e^{-x^2/2}$ for large $x$.
- **Chernoff-type bound:** $Q(x)\le\tfrac12e^{-x^2/2}$ ($x\ge0$) — handy for intuition about the exponential waterfall.
- For $X\sim\mathcal N(\mu,\sigma^2)$: $P(X>a)=Q\!\left(\frac{a-\mu}{\sigma}\right)$.

## 4. Probability of symbol error — building from the simplest case
### Pairwise error probability (PEP)
Two symbols $s_l$ (sent) and $s_m$: the detector prefers $s_m$ when the noise component along the line between them exceeds half the distance. That component is $\mathcal N(0,N_0/2)$ (one real dimension), so
$$\text{PEP}(s_l\to s_m)=Q\!\left(\frac{\sqrt{E_x}\,|s_l-s_m|/2}{\sqrt{N_0/2}}\right)=Q\!\left(\sqrt{\frac{E_x\,|s_l-s_m|^2}{2N_0}}\right)$$

### BPSK exact
$s=\pm1$, $|s_l-s_m|=2$, so 
$$\boxed{P_b^{\text{BPSK}}=Q\!\left(\sqrt{\frac{2E_x}{N_0}}\right)=Q(\sqrt{2\,\text{SNR}})}$$
Derivation (your lab pre-lab): send $+1$: $y=\sqrt{E_x}+v_R$, $v_R\sim\mathcal N(0,N_0/2)$; error iff $v_R<-\sqrt{E_x}$: $Q(\sqrt{E_x}/\sqrt{N_0/2})$. Symmetric for $-1$.

### QPSK exact
Normalized $s=\frac{\pm1\pm j}{\sqrt2}$: each dimension is BPSK with amplitude $\sqrt{E_x/2}$ ⇒ per-bit error 
$$P_b^{\text{QPSK}}=Q\!\left(\sqrt{\frac{E_x}{N_0}}\right)\quad(\text{Gray})$$
Symbol (either I or Q wrong): $P_s=1-(1-p)^2=2p-p^2$ with $p=Q(\sqrt{E_x/N_0})$.
**Why QPSK looks worse than BPSK at the same $E_s/N_0$:** it packs **2 bits** into one symbol of the same energy ⇒ each real dimension gets only $E_x/2$ ⇒ the Q-argument loses a factor $\sqrt2$ ⇒ **3 dB worse in $E_s/N_0$**. In terms of **$E_b/N_0$** ($E_b=E_x/\log_2M$) the two are **identical**: $Q(\sqrt{2E_b/N_0})$. (Your Lab 2 plot: "BPSK falls faster by √2 in the argument" = this.)

### Union bound
Hard to compute exactly in general ⇒ upper bound using PEPs:
$$P_s\le\frac1M\sum_{l}\sum_{m\ne l}\text{PEP}(s_l\to s_m)\ \le\ (M-1)\,Q\!\left(\sqrt{\frac{E_x\,d_{\min}^2}{2N_0}}\right)$$
with $d_{\min}=\min_{l\ne m}|s_l-s_m|$ (for the **unit-energy** constellation). The PEP "assumes only two symbols", so each term ignores other symbols ⇒ overcounts overlapping error regions ⇒ **upper bound, loose at low SNR, tight at high SNR**. 
- **$d_{\min}$ for unit-energy M-QAM:** $d_{\min}=\sqrt{\dfrac{6}{M-1}}$ (4-QAM: $\sqrt2$ ✓; 16-QAM: $\sqrt{0.4}$).
- Larger $M$ ⇒ smaller $d_{\min}$ ⇒ higher error rate at the same SNR: the **price of spectral efficiency**.
- Exact square-M-QAM formula (derivation not required): $P_s=1-\left[1-2\left(1-\tfrac1{\sqrt M}\right)Q\!\left(\sqrt{\tfrac{3\,\text{SNR}}{M-1}}\right)\right]^2$.

### Bit error rate
$\text{BER}\approx P_s/\log_2M$ for Gray coding at moderate/high SNR (one symbol error ≈ one bit error).

## 5. The waterfall
Error probability falls **exponentially** (steeply) with SNR — "waterfall" on a log-BER vs dB-SNR plot. Practical design: pick target BER (after error-control decoding ⇒ translates to a pre-decoding symbol error target) ⇒ choose transmit power, RF quality, modulation order.
Reference points for BPSK: BER $=10^{-3}$ at $E_s/N_0\approx6.8$ dB; $10^{-5}$ at $\approx9.6$ dB.

## Worked example — BPSK at $E_s/N_0=6$ dB
$\text{SNR}=10^{0.6}=3.98$; $\sqrt{2\cdot3.98}=2.82$; $Q(2.82)\approx2.4\times10^{-3}$. QPSK at the same $E_s/N_0$: $Q(\sqrt{3.98})=Q(2.0)=0.023$ — about 10× worse.

## Lab 1 & 2 connection
- **Lab 1:** BPSK, signal power 1, $10^4$ iterations per $N_0$, $N_0$ −10…0 dB ⇒ plot BER (log) vs $1/N_0$ (dB). Curve should match $Q(\sqrt{2/N_0})$.
- **Lab 2.1:** BPSK & QPSK BER vs SNR 0–10 dB; `decode.vi` implements ML (nearest symbol / sign tests). Bit error via Gray mapping.
- **Sec 3 qs:** "More noise power ⇒ received constellation clouds expand and overlap decision boundaries; BPSK is more robust than QPSK at equal symbol energy (larger $d_{\min}$ per symbol: 2 vs $\sqrt2$)."

## Traps
- Noise variance **per real dimension** is $N_0/2$. 
- Distinguish **SNR = $E_x/N_0$** from $E_b/N_0$.
- $d_{\min}$ is for the *unit-energy* constellation; $E_x$ carries the scale.
- ML = MAP only if symbols are equiprobable; ML = minimum distance because the AWGN is circularly symmetric (isotropic).
- Union bound is an upper bound on **symbol** error, not bit error.

## Self-test
1. Derive ML for AWGN in 3 lines.
2. Draw the Voronoi regions for 4-QAM and 8-PSK.
3. Compute BER for BPSK at $E_s/N_0=0,\ 4,\ 8$ dB.
4. Why is QPSK's BER worse than BPSK's at the same $E_s/N_0$ but the same at the same $E_b/N_0$?
5. Evaluate the union bound for 16-QAM at 10 dB.
