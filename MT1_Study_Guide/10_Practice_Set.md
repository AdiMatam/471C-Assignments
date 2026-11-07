# 10 — Midterm 1 Practice Set (problems only)

**Solutions are in `11_Practice_Solutions.md` — don't open it until you've attempted everything.**

Modeled on the homework-backed topics (HW2 and HW3), with **new numbers**. Conventions as in lecture: $x_p(t)=\text{Re}\{x(t)e^{j2\pi f_ct}\}$; $\text{sinc}(x)=\sin(\pi x)/(\pi x)$; speed of light $c=3\times10^8$ m/s; $k_B=1.38\times10^{-23}$ J/K, $T_e=290$ K. Closed-notes, no calculator tricks you couldn't do on exam day (a basic calculator for decimals is fine).

**Suggested use:** attempt blind, timed (~2 h total). Mark anything you got stuck on, then check solutions. Redo the stuck ones two hours later with changed numbers.

Tags: 🔵 = HW2 analogue, 🟣 = HW3 analogue, ⚪ = prerequisite / short.

---

## Problem 1 🔵 — Discrete-time equivalent channel (HW2 Q1)  *(≈10 min)*
A baseband signal of bandwidth $W=10$ MHz is sampled at the Nyquist rate. The physical channel is
$$h_c(t)=\delta(t-150\text{ ns})+0.5\,\delta(t-300\text{ ns}).$$
(a) What is the sampling period $T$?
(b) Derive the discrete-time equivalent channel $h[n]$ as an expression in terms of sinc functions.
(c) Which delay lands exactly on a sample instant? What does that do to its contribution to $h[n]$?
(d) Compute $h[n]$ numerically for $n=-1,0,1,2,3,4,5$ (three decimals).
(e) The channel only has two physical paths. Why does $h[n]$ have nonzero taps far from them (infinite support)?

## Problem 2 🔵 — Power spectrum (HW2 Q2) + a WSS check  *(≈10 min)*
(a) A zero-mean WSS process has covariance $C_{xx}(\tau)=3e^{-4|\tau|}$. Find $P_x(f)$ and the total power.
(b) $s[n]$ is real, zero-mean, IID with variance $\sigma_s^2=2$. Let $x[n]=s[n]-0.8\,s[n-1]$. Find the mean and covariance $C_{xx}[k]$ of $x[n]$ for all $k$, and decide whether $x[n]$ is WSS. Find $P_x(e^{j2\pi f})$.

## Problem 3 🟣 — Bandwidth and sampling (HW3 Q1)  *(≈20 min)*
Use the process from Problem 2(a): $C_{xx}(\tau)=3e^{-4|\tau|}$, $P_x(f)=\dfrac{24}{16+(2\pi f)^2}$.
(a) Compute the 3-dB bandwidth.
(b) Compute the fractional power containment bandwidth with $\alpha=0.95$.
(c) Find the sampling period $T$ so that you sample at **three times** the 3-dB frequency.
(d) Find the covariance function of $x[n]=x(nT)$.
(e) Find the power spectral density $P_x(e^{j2\pi f})$ of $x[n]$ and evaluate it at $f=0$ and $f=\tfrac12$.
(f) Which is wider, the 3-dB or the 95% bandwidth, and why does that make sense for this spectrum?

## Problem 4 🟣 — Passband to discrete-time channel (HW3 Q2 / HW2 Q3)  *(≈25 min)*
A wireless link has carrier $f_c=2.45$ GHz and absolute bandwidth $W=5$ MHz. A direct path travels 60 m with gain 0.2, and a reflected path travels 105 m with gain 0.1.
(a) Write the LTI channel model $h_c(t)$ and find its frequency response $h_c(f)$.
(b) Find the passband channel $h_p(t)$ obtained with the ideal bandpass filter $p(t)$ (center $f_c$, absolute bandwidth $W$).
(c) Find the complex baseband equivalent channel $h(t)$. Compute the phase rotation of each path (reduce $f_c\tau$ modulo 1).
(d) Find $h[n]$ assuming sampling at the Nyquist rate. Evaluate $h[n]$ for $n=0,1,2,3$.
(e) Interpret: which path produces a single clean tap, which produces a spread of taps, and why?

## Problem 5 🔵 — Normalize a constellation (HW2 Q4)  *(≈12 min)*
$$\mathcal C=\{\,1,\ \ 1+2j,\ \ -1+j,\ \ 3-j\,\}$$
(a) Compute the mean $\mu$. Is $\mathcal C$ zero-mean?
(b) Form the zero-mean constellation and verify it sums to zero.
(c) Compute its average energy.
(d) Give the scaling factor and the final zero-mean, unit-energy constellation. Verify the unit energy.
(e) Plot it (sketch).

## Problem 6 🟣 — Rectangular 8-point constellation (HW3 Q3 style)  *(≈10 min)*
Consider the 8-point constellation $\mathcal D=\{(a+2)+j(b+0.5):\ a\in\{-3,-1,1,3\},\ b\in\{-1,+1\}\}$ (a $4\times2$ grid shifted by $2+0.5j$).
(a) Find the mean $\mu$ of $\mathcal D$ (equally likely symbols).
(b) Give the zero-mean constellation and its average energy.
(c) Find the scaling factor that makes the zero-mean constellation unit-energy.
(d) How many bits per symbol does $\mathcal D$ carry? What is the minimum distance of the *normalized* constellation?

## Problem 7 ⚪ — Complex envelope  *(≈8 min)*
(a) Write the complex envelope $x(t)$ of $x_p(t)=3\cos(2\pi f_ct)-4\sin(2\pi f_ct)$. Express $x_p(t)$ as $A\cos(2\pi f_ct+\phi)$ and give $A$, $\phi$.
(b) Starting from $y_p(t)=A\cos(2\pi f_ct+\phi)$, show that the down-conversion $\text{LPF}\{2y_p(t)e^{-j2\pi f_ct}\}$ returns $Ae^{j\phi}$. Why is there a factor 2?
(c) A passband signal occupies $2.40$–$2.42$ GHz. What is its absolute bandwidth, and what is the minimum complex-baseband sample rate needed to represent it?
(d) One-line intuition: what is the difference between "baseband" and "passband"?

## Problem 8 ⚪ — Sampling and SNR (short)  *(≈10 min)*
(a) A real signal has maximum frequency 5 kHz and is sampled at $f_s=8$ kHz without an anti-aliasing filter. A 6 kHz interferer is present. At what frequency does it appear after sampling? Is the 5 kHz signal itself safely sampled?
(b) A receiver gets $2\ \mu$W of signal power over a $20$ MHz bandwidth with AWGN at $T_e=290$ K. Compute $N_0$, the noise power in the band, and the SNR in dB.
(c) State why the DT equivalent formula $h[n]=\int\text{sinc}(\tau W)\,h_c(nT-\tau)\,d\tau$ requires $TW=1$ in the form you used in Problem 1.

---

## Self-assessment checklist (after checking solutions)
- [ ] I can go $h_c\to h_p\to h(t)\to h[n]$ without notes, including the phase $e^{-j2\pi f_c\tau}$ and reducing $f_c\tau$ mod 1.
- [ ] I can compute 3-dB and fractional-power bandwidths for an exponential-covariance process.
- [ ] I remember the **4-step** constellation normalization (mean → subtract → energy → scale).
- [ ] I know when a sinc collapses to a delta (delay is an integer multiple of $T$).
- [ ] I can state the up/down-conversion scale factors (÷2 on the signal at up-conversion, ×2 after the LPF on down-conversion; **not** applied to the channel).
