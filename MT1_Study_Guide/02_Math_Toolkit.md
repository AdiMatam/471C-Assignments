# 02 — Math Toolkit: Probability, Random Processes, Sampling, PSD, Bandwidth (Weeks 3–4)

*Sources: Probability_RandomVariables, SignalProcessingFundamentals, BandlimitedSignals (first half), Class Questions 3–6, HW2 Q1–Q2, HW3 Q1.*

> 📌 **In homework (⇒ likely important):** **HW2 Q1** discrete-time equivalent system (Part C), **HW2 Q2** PSD of an exponential correlation (Part D), **HW3 Q1** 3-dB bandwidth / 90% containment / sampling period / DT covariance + PSD (Part D worked example). Parts A–B (probability, random processes) are the prerequisites for those but were not themselves homework questions — know the definitions, don't over-invest in the examples. Class Questions 1–6 were in-class only.

## Why this matters
Noise, data, and the channel are all modeled as **random processes**, and everything about bandwidth and sampling is Fourier analysis. HW3 Q1 (PSD → 3-dB bandwidth, fractional-power bandwidth, sampling, DT covariance/PSD) is a direct template for an exam question.

---
## Part A — Probability refresher

### Continuous random variables
- **pdf** $f_X(x)\ge0$, $\int f_X=1$. **CDF** $F_X(x)=P(X\le x)=\int_{-\infty}^x f_X$. $P(a<X\le b)=F(b)-F(a)=\int_a^b f$.
- **Mean** $\mu=E[X]=\int x f_X(x)\,dx$. **Variance** $\sigma^2=E[(X-\mu)^2]=E[X^2]-\mu^2$ — in signals, variance of a zero-mean signal = its **power**.
- Expectation of a function: $E[g(X)]=\int g(x)f_X(x)dx$. Linearity: $E[aX+b]=aE[X]+b$; $\text{Var}(aX+b)=a^2\text{Var}(X)$.

**Uniform on $[a,b]$:** mean $(a+b)/2$, variance $(b-a)^2/12$.
**Gaussian $\mathcal N(\mu,\sigma^2)$:** $f(x)=\frac{1}{\sqrt{2\pi\sigma^2}}e^{-(x-\mu)^2/(2\sigma^2)}$. Sums of independent Gaussians are Gaussian (means add, variances add). Linear transforms stay Gaussian.
Others on the slide (for recognition): Rayleigh (magnitude of complex Gaussian — fading, later), Weibull, log-normal, gamma.

**Class Question 5:** $f_x=\tfrac12$ on $[0,2)$. $\mu=\int_0^2 x\tfrac12dx=1$. $E[x^2]=\int_0^2 x^2\tfrac12dx=\tfrac43$. $\sigma^2=\tfrac43-1=\tfrac13$ ✓ (matches $(2-0)^2/12$).

### Discrete random variables
pmf $p_m=P(X=x_m)$; mean $\sum_m x_mp_m$; variance $\sum_m(x_m-\mu)^2p_m$. Bernoulli, Binomial, Geometric, Poisson are named on the slide — know that bits are Bernoulli($\tfrac12$) for "random data".

---
## Part B — Random (stochastic) processes

**Idea:** a random signal is modeled as an *ensemble*; at each time $n$ the value $x[n]$ is a random variable; each experiment gives one *realization*. We use them for (i) transmitted data, (ii) thermal noise, (iii) the changing propagation channel.

### Characterizations
- 1st order: distribution of each $x[n]$. 2nd order: joint distribution of $x[n_1],x[n_2]$. Full characterization needs all orders — usually unavailable, so we use **moments**.
- **Mean** $\mu_x[n]=E[x[n]]$
- **Autocorrelation** $R_{xx}[n_1,n_2]=E\big[x[n_1]x^*[n_2]\big]$
- **Autocovariance** $C_{xx}[n_1,n_2]=R_{xx}[n_1,n_2]-\mu_x[n_1]\mu_x^*[n_2]$. For **zero-mean** processes $C=R$ (most of this course).
- **Variance** $=C_{xx}[n,n]$ = power of a zero-mean process.
- **Uncorrelated:** $C_{xx}[n_1,n_2]=0$ for $n_1\ne n_2$. **Orthogonal:** $R_{xx}[n_1,n_2]=0$ for $n_1\ne n_2$. (Same thing for zero-mean.)
- **Cross-correlation** $R_{xy}[n_1,n_2]=E[x[n_1]y^*[n_2]]$: a measure of similarity between two processes. *In wireless: correlating a received noisy signal with a known header to find where the frame starts* (Block 07).
	- **==NOTE: Did this in DSP Lab with PN-headers -- then identified start-of-frame==**

### IID
All samples independent and identically distributed ⇒ $C_{xx}[k]=\sigma^2\delta[k]$ (white). Most common model for data symbols and noise.

### Wide-sense stationary (WSS)
1. mean is constant, $\mu_x[n]=\mu$;
2. correlation/covariance depends **only on the lag**: $C_{xx}[n_1,n_2]=C_{xx}[n_1-n_2]$.
No assumption on higher-order distributions. IID ⇒ WSS. **To show WSS you must check both conditions.**

### Gaussian noise models
- **Real AWGN:** IID $\mathcal N(0,\sigma^2)$; $C[k]=\sigma^2\delta[k]$.
- **Circularly symmetric complex Gaussian $\mathcal{CN}(0,\sigma^2)$:** $v=v_R+jv_I$ with $v_R,v_I$ **independent** $\mathcal N(0,\sigma^2/2)$. Then $E|v|^2=\sigma^2$, $E[v^2]=0$, magnitude is Rayleigh, phase uniform. **The variance splits equally between real and imaginary — central to BER later** (this is why BPSK sees noise variance $N_0/2$).
- Noise variance relation (look ahead): $N_0=k_BT_e$.

### LTI filtering of a WSS process
If $x$ is WSS and $y=h*x$: $y$ is WSS, $\mu_y=\mu_x\sum h[n]$ (i.e. $H(0)$), $C_{yy}=h*h^{\sim}*C_{xx}$ (with $h^{\sim}[n]=h^*[-n]$), and in frequency **$P_y(f)=|H(f)|^2P_x(f)$**. White noise through a filter ⇒ colored noise with spectrum $\sigma^2|H|^2$.

### Ergodicity
One long realization suffices: **time averages → ensemble moments** (for most WSS processes). That's why we can estimate power/covariance from a single captured signal, and why Lab simulations averaged over time work. (Slide's subtlety: stationarity ⇒ one realization's average converges to the mean; ergodicity ⇒ averaging across realizations & time agree.)

### Worked examples
**Class Q6 — moving average.** $s[n]$ IID zero-mean, $C_{ss}[k]=\sigma_s^2\delta[k]$; $x[n]=s[n]+0.5s[n-1]$.
- Mean: $E[x[n]]=0$ (constant).
- $C_{xx}[n,n-k]=E[x[n]x^*[n-k]] = \sigma_s^2\big(\delta[k]+0.25\delta[k]+0.5\delta[k-1]+0.5\delta[k+1]\big)$
 $\Rightarrow C_{xx}[0]=1.25\sigma_s^2,\ C_{xx}[\pm1]=0.5\sigma_s^2,\ \text{else }0$.
- Depends only on $k$, mean constant ⇒ **WSS**. Not white (neighbors correlated). Check via PSD: $P_x(e^{j2\pi f})=\sigma_s^2|1+0.5e^{-j2\pi f}|^2=\sigma_s^2(1.25+\cos 2\pi f)$ ✓ equals FT of the covariance.

---
## Part C — Continuous-time signals, Fourier transforms, sampling

### Fourier toolbox you must have at your fingertips
$X(f)=\int x(t)e^{-j2\pi ft}dt,\quad x(t)=\int X(f)e^{j2\pi ft}df$

| Property           | Time                 | Frequency                            |       |          |     |       |
| ------------------ | -------------------- | ------------------------------------ | ----- | -------- | --- | ----- |
| Linearity          | $ax+by$              | $aX+bY$                              |       |          |     |       |
| Delay              | $x(t-t_0)$           | $e^{-j2\pi ft_0}X(f)$                |       |          |     |       |
| Modulation (shift) | $x(t)e^{j2\pi f_0t}$ | $X(f-f_0)$                           |       |          |     |       |
| Scaling            | $x(at)$              | $\tfrac1{                            | a     | }X(f/a)$ |     |       |
| Convolution        | $x*y$                | $XY$                                 |       |          |     |       |
| Product            | $xy$                 | $X*Y$                                |       |          |     |       |
| Conjugate          | $x^*(t)$             | $X^*(-f)$                            |       |          |     |       |
| Parseval           | $\int                | x                                    | ^2dt$ | $\int    | X   | ^2df$ |
| Real signal        |                      | $X(-f)=X^*(f)$ (conjugate symmetric) |       |          |     |       |

Pairs: $\delta(t)\leftrightarrow1$; $\text{rect}(t/T)\leftrightarrow T\,\text{sinc}(fT)$; $\text{sinc}(t/T)\leftrightarrow T\,\text{rect}(Tf)$ where $\text{sinc}(x)=\sin(\pi x)/(\pi x)$; $e^{-a|t|}\leftrightarrow\frac{2a}{a^2+(2\pi f)^2}$; $\cos(2\pi f_0t)\leftrightarrow\tfrac12[\delta(f-f_0)+\delta(f+f_0)]$.

**Class Q3 — triangle.** $\Lambda(t/T)=\tfrac1T\text{rect}(t/T)*\text{rect}(t/T)$ ⇒ $\mathcal F\{\Lambda(t/T)\}=\tfrac1T\,[T\,\text{sinc}(fT)]^2=\boxed{T\,\text{sinc}^2(fT)}$.
**Class Q4 — IFT of $X(2f)\cos(2\pi ft_0)$.** $X(2f)\leftrightarrow\tfrac12x(t/2)$. Multiplying by $\cos(2\pi ft_0)$ in frequency = averaging two time shifts by $\pm t_0$: $\cos(2\pi f t_0)=\tfrac12(e^{j2\pi ft_0}+e^{-j2\pi ft_0})$ ⇒ $\boxed{\tfrac14\left[x\!\left(\tfrac{t+t_0}{2}\right)+x\!\left(\tfrac{t-t_0}{2}\right)\right]}$.
**Class Q2 — BPSK waveform.** 0→$+A$, 1→$-A$ ($A=3$), $g_{tx}=1/\sqrt T=1/\sqrt2$ on $[0,2]$. $x(t)=\sum s[n]g_{tx}(t-nT)$: bits $1,1,0,1$ ⇒ $-3/\sqrt2\approx-2.12$ on $[0,4)$ (two bits), $+2.12$ on $[4,6)$, $-2.12$ on $[6,8)$. Mapping table: $0\to+A,\ 1\to-A$.

### The four Fourier transforms in this course
| Transform | Signal | Frequency variable | Used for |
|---|---|---|---|
| **CTFT** | continuous-time, aperiodic $x(t)$ | continuous $f$, $X(f)$ not periodic | bandwidth, PSD of CT signals, pulse shapes |
| **CTFS** | continuous-time, **periodic** (period $T$) | discrete harmonics $k/T$ | spectrum of a periodic signal = **comb** of impulses at $k/T$ with weights = Fourier-series coefficients $c_k=\frac1T\int_Tx(t)e^{-j2\pi kt/T}dt$ |
| **DTFT** | discrete-time $x[n]$ | continuous $f$, **periodic with period 1**: $X(e^{j2\pi f})=\sum_nx[n]e^{-j2\pi fn}$ | analysis of sampled signals and DT filters |
| **DFT** | **finite-length** $x[n]$, $n=0..N-1$ | $N$ discrete bins $k/N$ | real-time implementation via FFT (the DTFT's continuous $f$ is unusable in hardware); returns with OFDM/SC-FDE (Block 08) |

DTFT notes: unique on any interval of unit length (usually $[-\tfrac12,\tfrac12)$); **low frequencies are near 0 (or 1), high frequencies near $\pm\tfrac12$**; periodicity comes from the sum over integer $n$. A rect of width $T$ in time has a sinc-shaped CTFT with first null at $1/T$.

### Bandlimited signals & the sampling theorem
- A signal is **bandlimited to bandwidth $W$** (complex baseband) if $X(f)=0$ for $|f|>W/2$. (Real baseband with max frequency $B$: need $f_s\ge2B$.)
- **Nyquist (slide form):** a bandlimited $x_c(t)$ with highest frequency $f_N$ (the Nyquist frequency) is uniquely determined by its samples $x_c(nT)$ if $f_s=1/T>2f_N$; $2f_N$ is the **Nyquist rate**. 
- **Nyquist (complex baseband form):** sampling period $T\le1/W$ (rate $\ge W$ for complex baseband of two-sided width $W$) ⇒ **no information lost**; $x(t)$ is perfectly recoverable.
- **C/D (ideal sampler):** $y[n]=y_c(nT)$. Spectrum relation: $X_T(e^{j2\pi f})=\frac1T\sum_n X_c\!\left(\frac{f-n}{T}\right)$ — a scaled, *periodic* repetition of the CT spectrum (copies every $1/T$). Overlap ⇒ **aliasing**.
- **D/C (ideal reconstructor):** $x_c(t)=\sum_n x[n]\,\text{sinc}\!\left(\frac{t-nT}{T}\right)$ — sinc interpolation, produces a signal bandlimited to $1/T$.
- **Aliasing:** if $f_s<2f_N$ the periodic copies in $X(e^{j2\pi f})$ overlap (frequencies above $f_s/2$ fold back onto lower ones) and the signal can't be recovered. With $f_s>2f_N$ the copies of a triangle-shaped spectrum of height $A$ appear with height $A/T$, separated by gaps from $f_NT$ to $1-f_NT$. **Why $1/T$?** Sampling multiplies $x_c(t)$ by an impulse train $\sum_n\delta(t-nT)$, whose Fourier transform is an impulse train in frequency with spacing $1/T$ **and weight $1/T$**; convolving $X_c(f)$ with it makes each copy $1/T$ times the original.
- **Anti-aliasing filter (AAF):** an *analog* low-pass filter before the sampler. Better to remove high frequencies than to suffer aliasing distortion; it also stops **out-of-band noise from aliasing** into the band.
- **Sampling techniques** (recognition only): *impulse* sampling (theoretical, not implementable), *natural* sampling (multiplier is a switch; theoretical), *zero-order-hold* (ideal sample/hold needs instantaneous acquisition — impractical), *track/hold* (real ADC front end: signal is sampled and stored in a memory element).
- **Why bandlimited matters (the course thesis):** transmitted signals must stay inside spectrum masks (e.g. IEEE 802.11ad mask), the channel only matters within the signal's band (e.g. DSL: a 30 kHz–1 MHz band-selector), and the received signal is bandlimited — so **the entire chain can be represented in discrete time**, and DSP tools (filters, FFT) design and analyze it. Sampling + DSP + reconstruction replaces analog processing.
- **Discrete-time frequency** $f_d=f\,T$ (cycles/sample), periodic in 1.

### Discrete-time processing of a bandlimited continuous-time signal (HW2 Q1) 📌 *in homework*
Replace  $x[n]\xrightarrow{\text{D/C}}x_c\xrightarrow{h_c}y_c\xrightarrow{\text{C/D}}y[n]$ by a single DT filter $h[n]$.
- Only the part of $h_c$ inside the band $|f|\le W/2$ matters (the D/C output is bandlimited): $h_{\text{low}}(f)=\text{rect}(f/W)h_c(f)$.
- $H(e^{j2\pi f})=T\,h_{\text{low}}(f/T)$ ⇒ taps $\boxed{h[n]=T\,h_{\text{low}}(nT)=\int\text{sinc}(\tau W)\,h_c(nT-\tau)d\tau\quad(\text{when }TW=1)}$.
- **Sampling at exactly Nyquist ⇒ $TW=1$.** (Slide: "TW=1 if sampling at exactly Nyquist".)
- **Applied (HW2 Q1):** $h_c(t)=\delta(t-\tau_0)+\alpha\delta(t-\tau_1)\Rightarrow h[n]=\text{sinc}(n-\tau_0/T)+\alpha\,\text{sinc}(n-\tau_1/T)$. If a delay is an *integer number of samples* the sinc collapses to a $\delta$; a *fractional* delay smears over many taps (infinite-support). **This is the single most reusable trick in HW2/HW3.**

---
## Part D — Power spectrum and bandwidth

### Power spectral density (PSD)
Random signals have no conventional FT. For a **WSS** process, the PSD is **the Fourier transform of the autocovariance**:

$$P_x(f)=\int C_{xx}(\tau)e^{-j2\pi f\tau}d\tau\ \ (\text{CT}),\qquad P_x(e^{j2\pi f})=\sum_k C_{xx}[k]e^{-j2\pi fk}\ \ (\text{DT})$$

- Real and **non-negative**; real & even if $C$ is real & even.
- **Total power** $=C_{xx}(0)=\int P_x(f)df$. White noise: $P=N_0$ (flat).
- Filtering: $P_y=|H|^2P_x$.
- 📌 **Example (HW2 Q2, in homework):** $C_{xx}(\tau)=e^{-2\beta|\tau|}$ ⇒ $P_x(f)=\dfrac{4\beta}{4\beta^2+(2\pi f)^2}=\dfrac{\beta}{\beta^2+\pi^2f^2}$ (Lorentzian). General: $e^{-a|\tau|}\leftrightarrow\frac{2a}{a^2+(2\pi f)^2}$ with $a=2\beta$.

### Measures of bandwidth (baseband illustration: $B_{3dB}$, $B_{\text{first null}}$, $B_{99\%}$)
| Definition                                           | How to compute                                                                                     |
| ---------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| **Absolute**                                         | support of $P(f)$ (exactly zero outside)                                                           |
| **3-dB**                                             | $f$ where $P(f)$ falls to **½ of its max** (baseband: measured from 0 → positive-frequency extent) |
| **Null-to-null / first null**                        | distance to the first zero of the spectrum                                                         |
| **Fractional power containment $\alpha$ (e.g. 99%)** | smallest $B$ with $\int_{-B}^{B}P(f)df=\alpha\int P(f)df$ (leaves $(1-\alpha)/2$ in each tail)     |

**Passband:** same definitions but measured as the *width* of the band around $\pm f_c$. A passband signal of width $W$ ↔ complex baseband signal occupying $[-W/2,W/2]$.

### 📌 Worked example — HW3 Q1 (my worked check; verify with your own submission)
$C_{xx}(\tau)=e^{-|\tau|}$, $P_x(f)=\dfrac{2}{1+(2\pi f)^2}$; total power $=C(0)=1$.
- **a) 3-dB bandwidth:** $P(0)=2$, half $=1$ ⇒ $(2\pi f)^2=1$ ⇒ $\boxed{B_{3dB}=\tfrac1{2\pi}\approx0.159\text{ Hz}}$.
- **b) 90% power:** $\int_{-B}^{B}\frac{2}{1+(2\pi f)^2}df=\frac{2}{\pi}\arctan(2\pi B)=0.9$ ⇒ $2\pi B=\tan(0.45\pi)=6.314$ ⇒ $\boxed{B_{90\%}\approx1.005\text{ Hz}}$. (Note how much wider than 3-dB: heavy tails.)
- **c) Sample at twice the 3-dB frequency:** $f_s=2\cdot\frac1{2\pi}=\frac1\pi$ ⇒ $\boxed{T=\pi\text{ s}}$. (Not truly alias-free — spectrum isn't bandlimited — but that's what the problem asks.)
- **d)** $C_{xx}[n]=C_{xx}(nT)=\boxed{e^{-\pi|n|}}$.
- **e)** $P_x(e^{j2\pi f})=\sum_ne^{-\pi|n|}e^{-j2\pi fn}=\boxed{\dfrac{1-e^{-2\pi}}{1-2e^{-\pi}\cos(2\pi f)+e^{-2\pi}}}$ (geometric series $\sum r^{|n|}e^{-j\theta n}=\frac{1-r^2}{1-2r\cos\theta+r^2}$, $r=e^{-\pi}$).

---
## Traps
- $\text{sinc}$ convention: course uses **normalized** $\sin(\pi x)/(\pi x)$ (zero crossings at integers).
- Covariance vs correlation differ unless zero-mean; WSS needs *both* mean-constant and lag-only.
- Complex noise: variance **splits** $\sigma^2/2$ per dimension.
- "Bandwidth" for baseband (one-sided from 0) vs passband (total width) — state which.
- 3-dB bandwidth uses **power** half ($-3$ dB ≈ ×½ in power), not amplitude half.

## Self-test
1. Mean and variance of Uniform$[0,2)$? (1, 1/3)
2. Show $x[n]=s[n]+0.5s[n-1]$ is WSS; give $C_{xx}$. 
3. FT of a triangle via two rects.
4. Compute $h[n]$ for $h_c(t)=\delta(t-1.5T)$ at Nyquist ($=\text{sinc}(n-1.5)$).
5. ==Define 3-dB and 99% bandwidth; which is bigger for a Lorentzian?==
6. ==If $C_{xx}(\tau)=e^{-5|\tau|}$, find $P_x(f)$ and the 3-dB bandwidth. ($P=\frac{10}{25+(2\pi f)^2}$; $B=\frac5{2\pi}$.)==

## Lab link
Lab 1's BER simulations assume IID complex Gaussian noise; Lab 2.2's oversampled TX/RX chains are the practical version of "D/C then C/D" and Nyquist sampling.
