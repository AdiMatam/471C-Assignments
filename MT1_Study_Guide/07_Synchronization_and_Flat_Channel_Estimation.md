# 07 — Synchronization & Channel Estimation in Frequency-Flat Channels (Weeks 8–9)

*Sources: Lecture 10_WCLab (impairments, symbol timing / MOE), Frame_Synchronization (frame sync, least squares, flat channel estimation, carrier frequency offset), Lab 3 and its pre-lab.*

> 📌 **Not in HW1–HW3** (timing recovery was Lab 3 / its prelab). **Likely out of scope** for Midterm 1 per your instructor; lowest priority after guide 08.

## Why this matters
The previous blocks assumed a perfect link: right sampling instant, known start of the packet, known gain/phase. Here we remove those assumptions one at a time. Lab 3 (timing recovery) is the lab version, so expect questions on MOE.

## 1. The frequency-flat channel and its three problems
A **single-path (flat)** baseband channel: $h(t)=\alpha e^{j\phi}\delta(t-\tau_d)$ ⇒ $r(t)=h\,x(t-\tau_d)+v(t)$, $h=\alpha e^{j\phi}$ complex. $|H(f)|=\alpha$ **flat**. After matched filter and sampling at $nT+\tau$:
$$y(nT+\tau)=h\sqrt{E_x}\sum_ms[m]\,g\big((n-m)T+\tau-\tau_d\big)+v$$
Three unknowns, three fixes (order of attack):
| Unknown | Impairment | Fix |
|---|---|---|
| **Fractional delay** $d\in[0,T)$ | symbol timing mismatch ⇒ **ISI** | **symbol synchronization** (timing recovery) |
| **Integer delay** $n_d$ symbols | frame/packet start unknown | **frame synchronization** |
| **Complex gain $h=\alpha e^{j\phi}$** | amplitude + phase distortion (rotates/scales the constellation) | **channel estimation + equalization** |
| (plus) **carrier frequency offset** | constellation rotates over time | frequency offset estimation |
(Propagation delay is rarely the dominant source of latency; applications differ in delay tolerance.)

**Approaches:** *burst mode* — operate on frames; estimate and correct once per frame using **training** (the approach used here); *continuous mode* — adaptive tracking; and *decision-directed* modes combine both.

## 2. Symbol synchronization (timing recovery)
**Why needed:** with the Nyquist pulse, zero ISI holds *only* if we sample at the instants $nT+\tau_d$. Sampling elsewhere ⇒ ISI (eye partially closed). Sinc pulses are very sensitive; RC with larger $\alpha$ less so.
**Goal:** estimate $\tau_d$ (mod $T$) and sample there.
**Digital approaches (we do pure digital):**
- *Oversampling method* (RX oversample factor $M_{rx}$ large): sample at $T/M_{rx}$, pick the best of $M_{rx}$ phases.
- *Interpolation/resampling method* ($M_{rx}$ small, e.g. 2): resample at a fractional offset using rational resampling ($N:M_{rx}$).

### Maximum-output-energy (MOE) criterion
For most pulse shapes the expected power at the sampler is **maximized at the correct timing**:
$$J(\tau)=E\big[|y(nT+\tau)|^2\big]=|h|^2E_x\sum_m|g(mT+\tau-\tau_d)|^2\ ,\qquad\hat\tau=\arg\max_\tau J(\tau)=\tau_d\ (\text{mod }T)$$
- $\alpha,\phi$ drop out (Lab 3 Q1): $|e^{j\phi}|=1$ and $\alpha^2$ just scales $J$ without moving its argmax. Requires zero-mean, uncorrelated, unit-energy symbols.
- Why max at $\tau_d$: the sum of squared pulse samples is largest when a sample lands on the pulse peak (energy is concentrated; at off-peak instants the symbols' energy is "smeared" and, with zero-mean uncorrelated symbols, power adds incoherently over neighbors).
- Plotted as $E|r(kT+\tau)|^2$ vs normalized error $|\tau-d|/T$: a bump peaking at 0 (the exact shape depends on the pulse and modulation).

**Non-adaptive MOE estimator:** let $r[n]$ = matched-filter output (before downsampling) at $M_{rx}$ samples/symbol. Replace expectation by a time average over $P$ symbols:
$$\hat J[k]=\frac1P\sum_{n=0}^{P-1}\big|r[nM_{rx}+k]\big|^2,\quad k=0,\dots,M_{rx}-1;\qquad k^*=\arg\max_k\hat J[k]$$
and then sample the matched-filter output at $nM_{rx}+k^*$ (equivalently: delay the filter by $k^*$ samples).

**Adaptive MOE estimator** (Lab 3 derivation): set $dJ/d\tau=0$:
$$\frac{dJ}{d\tau}=E\Big[2\,\text{Re}\{y^*(nT+\tau)\,\dot y(nT+\tau)\}\Big]$$
Approximations (the two "critical assumptions" from your pre-lab): 
1. **interchange derivative/expectation and replace the expectation by a time average over $P$ symbols;**
2. **replace the derivative by a first-order (central) difference** $\dot y\approx\big[y(\tau+\delta)-y(\tau-\delta)\big]/2\delta$ ⇒ only accurate if $\delta$ is small (heavy oversampling).
⇒ choose $k^*$ making $\hat J_\delta[k]=\frac1P\sum_n\text{Re}\{r^*[nM+k]\,(r[nM+k+\delta]-r[nM+k-\delta])\}$ closest to **zero** (at the maximum of $J$). 
- Noise: adds randomness to the statistic, SNR drops with attenuation $\alpha^2$; fix by **larger $P$** (longer packets / more averaging) and sensible $\delta$ and $M$ (balance difference-approx accuracy vs noise).
- **Impact of timing error on BER:** ISI reduces effective SINR; union-bound BER for 4-PAM rises quickly with $|\tau-d|/T$.
- Lab 3: $\varepsilon(N)$ = timing-estimate error vs RX oversample factor $N$ (normalized by $T_s$).

## 3. Frame synchronization
After symbol sync, an integer delay remains: the receiver doesn't know where the data starts. Example: 4-PAM carrying ASCII: "$-a,-a,+a,-3a,-a$" decodes to different characters depending on the starting offset.
**Use a known training/sync sequence $s_{tr}[0..N_{tr}-1]$** (also called preamble, pilot, reference signal) and **correlate**:
$$\hat n_d=\arg\max_n\ \Big|\sum_{k=0}^{N_{tr}-1}s_{tr}^*[k]\,y[n+k]\Big|^2$$
- It's the matched filter in discrete time (also the ML/LS solution for the unknown delay + gain).
- **Training design:** need sharp, **impulse-like autocorrelation** (good peak/sidelobe ratio) so noise/data don't create false peaks: **Barker codes** (e.g. length-7: $+1+1+1-1-1+1-1$), **Frank sequences** ($q=4,r=3$ ⇒ length-16 PSK), **Neuman–Hoffman** codes.
- **Periodic insertion** of training: correlate over $P$ periods (multiples of $N_{tot}$) ⇒ more robust peaks.
- Alternative: **energy detector** (detect when signal power turns on) — cruder.
- Example from slide: 8 train + 14 data (4-QAM), Barker-7, peaks every 21–22 samples at 5 dB SNR.
- Frame structure: $[$train$\,|\,$data$\,|\,$train$]$, $N_{tot}$ symbols per frame.

## 4. Least squares (LS) and ML estimation — the tool for everything that follows
Linear system $\mathbf A\mathbf x\approx\mathbf b$, $\mathbf A$: $N\times M$ known (data) matrix, $\mathbf x$: $M\times1$ unknown, $\mathbf b$: $N\times1$ observed.
- $N=M$, $\mathbf A$ invertible: $\mathbf x=\mathbf A^{-1}\mathbf b$. 
- **$N>M$, tall, full column rank ("overdetermined")** — no exact solution, minimize **squared error** $\|\mathbf b-\mathbf A\mathbf x\|^2$:
 - **Orthogonality principle:** $\mathbf A^*(\mathbf b-\mathbf A\hat{\mathbf x})=0$ — the error is orthogonal to every column of $\mathbf A$.
 - **Normal equations:** $\mathbf A^*\mathbf A\,\hat{\mathbf x}=\mathbf A^*\mathbf b$ ⇒ 
 $$\boxed{\hat{\mathbf x}=(\mathbf A^*\mathbf A)^{-1}\mathbf A^*\mathbf b}$$
 - **Geometry:** $\mathbf A\hat{\mathbf x}=\mathbf A(\mathbf A^*\mathbf A)^{-1}\mathbf A^*\mathbf b$ is the **projection** of $\mathbf b$ onto the column space of $\mathbf A$; error is the projection onto the orthogonal complement. Minimum squared error $=\mathbf b^*\big(\mathbf I-\mathbf A(\mathbf A^*\mathbf A)^{-1}\mathbf A^*\big)\mathbf b$.
- **LS = ML** when the noise is IID Gaussian: maximizing $\exp(-\|\mathbf b-\mathbf A\mathbf x\|^2/\ldots)$ ⇔ minimizing $\|\mathbf b-\mathbf A\mathbf x\|^2$ (the slide's note: *only true for IID Gaussian noise*).

## 5. Frequency-flat channel estimation and equalization
Suppose frame + symbol sync are solved. Model $y[n]=h\sqrt{E_x}\,s[n]+v[n]$ (absorb $\sqrt{E_x}$ in the known training: $\tilde h=h\sqrt{E_x}$).
- **Training:** known $s_{tr}[n]$, $n=0..N_{tr}-1$. Stack: $\mathbf y=\mathbf s_{tr}\,\tilde h+\mathbf v$ — a LS problem with $\mathbf A=\mathbf s_{tr}$ ($N_{tr}\times1$).
 $$\boxed{\hat{\tilde h}=(\mathbf s_{tr}^*\mathbf s_{tr})^{-1}\mathbf s_{tr}^*\mathbf y=\frac{\sum_ns_{tr}^*[n]y[n]}{\sum_n|s_{tr}[n]|^2}}$$
 A **correlator** ⇒ jointly gives frame sync (peak location) and channel estimate (value at the peak), **normalized to correct for scaling**.
- **Estimation error:** $\hat h-h\sim\mathcal{CN}(0,N_0/(E_xN_{tr}))$ for unit-energy training ⇒ **more training symbols ⇒ better estimate** (cost: overhead).
- **Detection with the estimate:**
 - *Equalize first:* $\hat y[n]=y[n]/\hat{\tilde h}$ (removes rotation + scaling) then standard ML detector.
 - *Or* include the estimate in the ML detector: $\hat s=\arg\min_s|y-\hat{\tilde h}s|^2$.
 - Using $\hat h$ adds a source of error; treat the estimation error as extra noise ⇒ SINR $\approx\dfrac{E_x}{N_0+E_x\sigma_e^2}$-like (replace noise variance by noise + error variance).
- **Receiver chain so far:** $r(t)\to$ matched filter $\to$ symbol sync $\to$ frame sync $\to$ channel estimate/equalize $\to$ detection.
- Some modulations are robust to this distortion without estimation (**differential QPSK**), at some performance cost.

## 6. Carrier frequency offset (CFO)
**Origin:** TX and RX oscillators are never identical: RX down-converts with $\hat f_c=f_c-f_e$ ⇒ the baseband signal is multiplied by $e^{j2\pi f_et}$ — **a continuously rotating constellation**.
In discrete time: 
$$y[n]=e^{j2\pi f_enT}\,h\sqrt{E_x}\sum_\ell s[n-\ell]\,\ldots+v[n]$$
- The rotation occurs **after** convolution with the unknown channel; "even small offsets cause severe degradation".
- It corrupts frame sync, channel estimation, and equalization; must be estimated and **derotated** (multiply by $e^{-j2\pi\hat f_enT}$).
**Simple estimator (sinusoid training):** use $s_{tr}[n]=1$ (a complex sinusoid in the received signal): $y[n]=he^{j2\pi f_enT}+v[n]$. Look at the **phase difference of adjacent samples**: $\angle\big(y[n]y^*[n-1]\big)\approx2\pi f_eT+\text{noise}$ ⇒ the (approximate) LS estimate is simply the **average**:
$$\hat f_e=\frac{1}{2\pi T}\cdot\frac1{N-1}\sum_{n=1}^{N-1}\angle\big(y[n]y^*[n-1]\big)$$
(unambiguous only for $|f_e|<\frac1{2T}$.) Noise is approximated as phase noise; the channel phase $\angle h$ cancels in the difference.
*(Moose algorithm / OFDM CFO come on Oct 21–26 — after the exam.)*

## Traps
- MOE: symbol timing resolves only the **fractional** delay $\in[0,T)$; frame sync handles integer symbol delays.
- LS formula has $\mathbf A^*$ (conjugate transpose) for complex data.
- LS=ML requires **IID Gaussian** noise.
- Correlator uses the **conjugate** of the training sequence.
- Don't conflate $h$ (channel) with $\tilde h=h\sqrt{E_x}$ — keep scaling consistent.

## Self-test
1. Write the MOE estimator and state when it works.
2. Why does adding noise break the adaptive MOE estimator, and which two parameters fix it?
3. Locate the frame start for $y=[0.1,\ 1.1,\ 0.9,\ 1.2,\ -0.8\ldots]$ with training $[+1,+1,+1,-1,-1]$.
4. Derive $\hat h$ via normal equations for $N_{tr}=1$ and $N_{tr}=100$; compare error variance.
5. With $T=1\,\mu$s and adjacent-sample phase advance of 0.2 rad, what's $\hat f_e$? ($\approx31.8$ kHz.)

## Lab link
Lab 3: MOE timing recovery in the VI, RC $\alpha=0.5$, QPSK 500-bit packets, flat channel $h=0.75e^{j\pi/4}$, delay $0.34T_s$, estimating $\varepsilon(N)$; frame sync via training in later labs.
