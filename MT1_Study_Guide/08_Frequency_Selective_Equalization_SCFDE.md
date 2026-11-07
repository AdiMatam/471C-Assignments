# 08 — Frequency-Selective Channels, LS/LMMSE Equalization, DFT, Cyclic Prefix, SC-FDE (Week 9)

*Sources: Freq_Selective_Channel (Lecture 12), Oct 12 & Oct 14 lectures on the schedule. OFDM is introduced at the end of the Oct 14 lecture; comparison SC-FDE vs OFDM and OFDM channel estimation are Oct 21 — after the exam.*

> 📌 **Not in HW1–HW3.** **Likely out of scope** for Midterm 1 (and parts are Oct 21+). Lowest priority.

## Why this matters
Real channels have multipath. The "flat" model of Block 07 is a special case. The ideas here — **estimate the channel from training, then undo it** — culminate in SC-FDE/OFDM, the basis of 802.11 and 4G. Exam-ready skills: write the received signal model, set up the LS equalizer matrix, explain why/how the cyclic prefix works, and write the frequency-domain equalizer.

## 1. Frequency-selective channels
**Multipath:** $h(t)=\sum_k\alpha_k\delta(t-\tau_k)$ — each path has a complex gain and delay. $H(f)$ is **not constant** over the signal bandwidth ⇒ some frequencies attenuated more ⇒ **ISI**.
Two-path example: $h(t)=\delta(t)+\alpha\delta(t-\tau)\Rightarrow|H(f)|^2=1+\alpha^2+2\alpha\cos(2\pi f\tau)$ — periodic ripples with nulls when $\alpha\approx1$.
**Effective channel:** include the pulse shaping and matched filter: $g_{\text{eff}}(t)=g_{rx}*h*g_{tx}$ ⇒ looks like PAM with a new (ISI-causing) pulse.
**Assumptions:** channel **causal** (propagation can't predict) and **FIR** (long reflections are weak), order $L$ (assumed known):
$$\boxed{y[n]=\sum_{\ell=0}^{L}h[\ell]\,s[n-\ell]+v[n]}$$
(with $\sqrt{E_x}$ absorbed in $h[\ell]$ and $s$ unit-energy). Two-tap example $h[0],h[1]$: each output mixes the current and previous symbol.
**Solutions:** (i) *linear equalizer* (this section); (ii) decision feedback, (iii) ML sequence detection (high complexity); (iv) **frequency-domain equalization** with a cyclic prefix (next).

## 2. Linear equalization — least squares (LS) design
FIR equalizer $f[k]$, $k=0..L_f$ (order $L_f$), output $\hat s[n-n_d]=\sum_{k=0}^{L_f}f[k]\,y[n-k]$; $n_d$ = chosen **delay** (noncausal ideal ⇒ allow delay).
**Goal (noise-free):** $(h*f)[n]=\delta[n-n_d]$. As a linear system:
$$\mathbf H\,\mathbf f=\mathbf e_{n_d},\qquad \mathbf H:\ (L_f+L+1)\times(L_f+1)\ \text{Toeplitz and tall},\ \ \mathbf e_{n_d}=\text{unit vector with a 1 in position } n_d$$
- $\mathbf H$ is **full column rank** if at least one tap is nonzero; tall ⇒ overdetermined ⇒ **LS** (Block 07):
$$\boxed{\mathbf f_{n_d}=(\mathbf H^*\mathbf H)^{-1}\mathbf H^*\mathbf e_{n_d}},\qquad J_f(n_d)=1-\mathbf e_{n_d}^*\mathbf H(\mathbf H^*\mathbf H)^{-1}\mathbf H^*\mathbf e_{n_d}$$
- $J_f$ = squared error of the *combined channel+equalizer response* vs the ideal $\delta$ (ISI energy left). **Choose $n_d$ to minimize $J_f(n_d)$** (typically near the middle of the combined response).
- **Higher order $L_f$ ⇒ less residual ISI ($J_f\downarrow$) but more complexity**; rule of thumb $L_f\approx4L$. (Slide shows order 3, 5, 10 with $n_d=4,6,9$ — optimal delay grows with order.)
- Toeplitz structure ⇒ fast solvers exist.
- **Needs a channel estimate** $\hat h[\ell]$ first: estimated by LS from training (below), then used to build $\mathbf H$. Receiver: channel estimation → LS/LMMSE equalizer computation → equalize → detect.

### Channel estimation for FIR channels (LS with training)
Training $s_{tr}[0..N_{tr}-1]$; $y[n]=\sum_{\ell=0}^{L}h[\ell]s_{tr}[n-\ell]+v[n]$ ⇒ $\mathbf y=\mathbf S\,\mathbf h+\mathbf v$ with $\mathbf S$ a $(N_{tr}-L)\times(L+1)$ Toeplitz matrix of training symbols. 
$$\hat{\mathbf h}=(\mathbf S^*\mathbf S)^{-1}\mathbf S^*\mathbf y$$
Needs $N_{tr}\ge2L+1$ or so (tall); training with good autocorrelation (so $\mathbf S^*\mathbf S\approx N\mathbf I$) is best. Longer training ⇒ lower estimation error.

## 3. LMMSE equalizer (adds noise awareness)
**Background — LMMSE estimator.** Estimate zero-mean $\mathbf x$ from zero-mean observation $\mathbf y$ with a linear map $\hat{\mathbf x}=\mathbf G\mathbf y$ minimizing $E\|\mathbf x-\mathbf G\mathbf y\|^2$. **Orthogonality:** $E[(\mathbf x-\hat{\mathbf x})\mathbf y^*]=0$ ⇒ 
$$\mathbf G_{\text{MMSE}}=\mathbf C_{xy}\mathbf C_{yy}^{-1}\quad(\hat{\mathbf x}=\mathbf C_{xy}\mathbf C_{yy}^{-1}\mathbf y)$$
— $\mathbf C_{xy}$ *exploits the correlation between $x$ and $y$*, $\mathbf C_{yy}^{-1}$ *decorrelates the observation*.
**Equalizer:** with $\mathbf y_n=[y[n],\dots,y[n-L_f]]^T=\mathcal H\mathbf s_n+\mathbf v_n$ ($\mathcal H$ is the $(L_f+1)\times(L_f+L+1)$ convolution matrix), symbols IID unit variance, noise IID variance $N_0$, independent:
$$\mathbf C_{yy}=\mathcal H\mathcal H^*+N_0\mathbf I,\qquad \mathbf C_{y,s[n-n_d]}=\mathcal H\mathbf e_{n_d}\ \Rightarrow\ \boxed{\mathbf f_{n_d}=\big(\mathcal H\mathcal H^*+N_0\mathbf I\big)^{-1}\mathcal H\,\mathbf e_{n_d}}\quad(\hat s[n-n_d]=\mathbf f^*\mathbf y_n)$$
(taps conj-transposed as per your slides' convention; also choose the best $n_d$).
**Limits (memorize):**
- $N_0\to\infty$ (noise dominates) ⇒ **matched filter** (maximize SNR, ignore ISI).
- $N_0\to0$ ⇒ **LS / zero-forcing** solution (kills ISI, ignores noise; at spectral nulls it amplifies noise = **noise enhancement**).
LMMSE gives the best trade-off between ISI removal and noise amplification, so it's better than LS at low/medium SNR and the same at high SNR.

## 4. Why frequency-domain equalization?
Zero-forcing in the DTFT domain: $F(e^{j2\pi f})=1/H(e^{j2\pi f})$ — **perfect inversion**, but defined over continuous $f$ and infinite-length. We want something computable: **use the DFT** (finite $N$ points) — but the DFT diagonalizes **circular**, not linear, convolution. The **cyclic prefix** converts the linear convolution of the channel into a circular one.

### The DFT (background)
$$X[k]=\sum_{n=0}^{N-1}x[n]e^{-j2\pi kn/N},\qquad x[n]=\frac1N\sum_{k=0}^{N-1}X[k]e^{j2\pi kn/N}$$
Basis expansion for **finite-length** signals; FFT computes it in $O(N\log N)$ (power-of-2 $N$ best).
- **Circular shift:** $x[(n-m)\bmod N]\ \leftrightarrow\ e^{-j2\pi km/N}X[k]$.
- **Circular convolution:** $(x\circledast h)[n]=\sum_{m=0}^{N-1}x[m]\,h[(n-m)\bmod N]\ \leftrightarrow\ X[k]H[k]$ ($N$-point DFTs).
- **Linear vs circular:** the linear convolution of lengths $N_1$ and $N_2$ has length $N_1+N_2-1$. If both are **zero-padded to length $N\ge N_1+N_2-1$**, circular = linear. Otherwise the tail **wraps around** (circular wrapping effect) and corrupts the beginning.
- $H[k]$ for the channel = $N$-point DFT of $[h[0],\dots,h[L],0,\dots,0]$ = samples of the DTFT at $f=k/N$.

## 5. Single-carrier frequency-domain equalization (SC-FDE) with cyclic prefix
**Transmitter:** group the data into **blocks of $N$ symbols** $\mathbf s=[s[0],\dots,s[N-1]]$. Assemble a block of $N+L_c$ symbols with a **cyclic prefix** copy of the last $L_c$ symbols in front:
$$[\,s[N-L_c],\dots,s[N-1]\ |\ s[0],\dots,s[N-1]\,],\qquad L_c\ge L$$
**Channel:** linear convolution with $h$ (length $L+1$). 
**Receiver:** **discard the first $L_c$ received samples** (they contain ISI from the previous block — "neglect the first $L_c$ terms of the convolution"). The remaining $N$ samples are exactly the **circular convolution** of the block with $h$:
$$y[n]=(h\circledast s)[n]+v[n]\ \ \Rightarrow\ \ Y[k]=H[k]S[k]+V[k]$$
- The prefix acts as a **guard interval** (absorbs inter-block interference) and **creates the periodicity** needed for circular convolution.
- **Frequency-domain equalizer (one tap per frequency bin):**
 - **ZF:** $\hat S[k]=Y[k]/H[k]$ 
 - **MMSE:** $\hat S[k]=\dfrac{H^*[k]}{|H[k]|^2+N_0/E_s}\,Y[k]$ ($E_s$ = symbol energy; noise-regularized)
 then $\hat s=\text{IDFT}\{\hat S\}$ (**the IDFT is at the receiver** — data symbols live in the time domain; the equalizer is in frequency), then ML detection.
- **Channel estimation** in this setting: send a known block; $\hat H[k]=Y_{tr}[k]/S_{tr}[k]$ (or time-domain LS then DFT).
- **Cost:** overhead $L_c/(N+L_c)$; complexity $O(N\log N)$ vs long time-domain filters; **requires $L_c\ge L$** (the channel-length knowledge).
- **Frame sync** must find the **start of the cyclic prefix** (block boundary) — the previous block's correlator.
- **Zero-padding (ZP) alternative:** append $L_c$ zeros instead of a prefix; with overlap-add, also gives circular convolution, with no extra energy wasted, but needs a more complicated receiver. (Learning outcome: *justify the use of either*.)
- **OFDM preview:** put the **IDFT at the transmitter** (data symbols placed on subcarriers $S[k]$), prepend CP, DFT at receiver ⇒ each subcarrier is a flat channel with one-tap equalizer; no IDFT at the RX. (Compare in Oct 21 lecture.)

## 6. Putting together the receiver (frequency-selective)
RX: matched filter → symbol sync → frame sync (finds training/CP) → LS channel estimate → equalizer (time-domain LS/LMMSE **or** SC-FDE with DFT) → detection.

## Worked mini-example (two-tap ISI)
$h=[1,\ 0.5]$, BPSK $s\in\{\pm1\}$, no noise: $y[n]=s[n]+0.5\,s[n-1]$. 
- $H(e^{j2\pi f})=1+0.5e^{-j2\pi f}$; $|H|^2=1.25+\cos2\pi f\in[0.25,2.25]$.
- ZF frequency equalizer $1/(1+0.5e^{-j2\pi f})$ ⇒ time-domain $f[k]=(-0.5)^k$, $k\ge0$ (infinite!). A length-$(L_f+1)$ truncation leaves a residual error $\sim0.5^{L_f+1}$ — shows why higher order helps.
- With CP, $N=4$, $L_c=1$: block $[s_3|s_0,s_1,s_2,s_3]$; after discarding the prefix, $y[0]=s_0+0.5s_3$ (wraps!) — circular.

## Traps
- Matrix dimensions: $\mathbf H$ is $(L_f+L+1)\times(L_f+1)$ (tall), $\mathcal H$ is its flipped/transposed counterpart $(L_f+1)\times(L_f+L+1)$.
- LS error formula uses $\mathbf e_{n_d}$; choosing $n_d$ is part of the design.
- CP length must be **≥ $L$** (not $N$); CP ≠ extra data.
- Circular conv = linear conv **only** if zero-padded to $N_1+N_2-1$ — or after CP removal.
- ZF vs MMSE: ZF → noise enhancement at nulls.
- Frame sync points to CP start, not block start after removal.

## Self-test
1. Derive $\mathbf f=(\mathbf H^*\mathbf H)^{-1}\mathbf H^*\mathbf e_{n_d}$ from least squares.
2. For $L=2$, $L_f=3$: dimensions of $\mathbf H$? ($6\times4$.)
3. Explain, in three sentences, why a CP makes frequency-domain equalization possible.
4. Compute the 4-point DFT of $[1,1,0,0]$ and of the channel $[1,0.5,0,0]$; ZF-equalize $Y=H\cdot S$.
5. What happens to LMMSE as $N_0\to0$? As $N_0\to\infty$?
6. Overhead of $N=64$, $L_c=16$? (20%.)

## Lab link
Upcoming labs (channel estimation, synchronization, frequency offset, OFDM) build exactly on this: `LS` channel estimation with training, time-domain equalizer, and SC-FDE/OFDM with a CP. The USRP link you built in Labs 2–3 is the flat-channel special case.
