# EE 471C Homework #2 Solutions

## (1) Discrete-Time Equivalent System for $h(t) = \delta(t-\tau_0) + \alpha\delta(t-\tau_1)$

	**Setup (discrete-time processing of a bandlimited continuous-time signal).** We want to replace the cascade

$$x[n] \xrightarrow{\text{D/C}} x_c(t) \xrightarrow{h_c(\tau)} y_c(t) \xrightarrow{\text{C/D}} y[n]$$

(sampling period $T$ on both converters) with a single equivalent discrete-time system $x[n]\to h[\ell]\to y[n]$. The ideal D/C reconstructs

$$x_c(t) = \sum_n x[n]\,\text{sinc}\!\left(\frac{t-nT}{T}\right)$$

which is bandlimited to $W=1/T$ (Nyquist sampling), so only the portion of the channel that lies inside that band, $\mathsf h_{\text{low}}(f) = \text{rect}(f/W)\,\mathsf h_c(f)$, can affect $x_c(t)$; equivalently in the time domain

$$h_{\text{low}}(t) = W\int \text{sinc}(\tau W)\,h_c(t-\tau)\,d\tau$$

Carrying $\mathsf y_c(f) = \mathsf h_{\text{low}}(f)\mathsf x_c(f)$ through the C/D sampler and using the (alias-free, since $x_c$ is bandlimited) relation $X_c(f/T) = T\,X(e^{j2\pi f})$ gives a clean discrete-time transfer function $\mathsf h(e^{j2\pi f}) = T\,\mathsf h_{\text{low}}(f)$, whose time-domain samples are the equivalent discrete-time channel taps:

$$\boxed{h[n] = T\,h_{\text{low}}(nT) = TW\int \text{sinc}(\tau W)\,h_c(nT-\tau)\,d\tau = \int \text{sinc}(\tau W)\,h_c(nT-\tau)\,d\tau}$$

where the last equality uses $TW=1$ (sampling at exactly the Nyquist rate).

**Apply the given $h_c(t) = \delta(t-\tau_0)+\alpha\delta(t-\tau_1)$.** Plug into the boxed formula and use the sifting property of the Dirac delta on each term:

$$h[n] = \int \text{sinc}(\tau W)\Big[\delta\big(nT-\tau-\tau_0\big) + \alpha\,\delta\big(nT-\tau-\tau_1\big)\Big]d\tau$$

$$= \text{sinc}\big((nT-\tau_0)W\big) + \alpha\,\text{sinc}\big((nT-\tau_1)W\big)$$

Since $W = 1/T$ at Nyquist sampling, $(nT-\tau_0)W = n - \tau_0/T$, so

$$\boxed{h[n] = \text{sinc}\!\left(n - \frac{\tau_0}{T}\right) + \alpha\,\text{sinc}\!\left(n-\frac{\tau_1}{T}\right)}$$

This is an infinite-support (IIR) discrete-time channel in general, because a pure delay is only exactly realizable in discrete time via sinc interpolation unless the delay lands exactly on a sample instant.


---

## (2) Power Spectrum of $R_{xx}(\tau) = e^{-2\beta|\tau|}$

The power spectral density is the Fourier transform of the autocorrelation function (Wiener–Khinchin theorem):

$$S_{xx}(\omega) = \int_{-\infty}^{\infty} R_{xx}(\tau)\,e^{-j\omega\tau}\,d\tau = \int_{-\infty}^{\infty} e^{-2\beta|\tau|} e^{-j\omega\tau}\,d\tau$$

Split the integral at $\tau=0$:

$$S_{xx}(\omega) = \int_{-\infty}^{0} e^{2\beta\tau} e^{-j\omega\tau}\,d\tau + \int_{0}^{\infty} e^{-2\beta\tau} e^{-j\omega\tau}\,d\tau$$

$$= \int_{-\infty}^{0} e^{(2\beta - j\omega)\tau}\,d\tau + \int_{0}^{\infty} e^{-(2\beta+j\omega)\tau}\,d\tau$$

$$= \left[\frac{e^{(2\beta-j\omega)\tau}}{2\beta-j\omega}\right]_{-\infty}^{0} + \left[\frac{-e^{-(2\beta+j\omega)\tau}}{2\beta+j\omega}\right]_{0}^{\infty}$$

$$= \frac{1}{2\beta - j\omega} + \frac{1}{2\beta+j\omega} = \frac{(2\beta+j\omega) + (2\beta - j\omega)}{(2\beta)^2+\omega^2}$$

$$\boxed{S_{xx}(\omega) = \frac{4\beta}{4\beta^2+\omega^2}}$$

In terms of ordinary frequency $f$ (Hz), with $\omega = 2\pi f$:

$$S_{xx}(f) = \frac{4\beta}{4\beta^2 + 4\pi^2 f^2} = \frac{\beta}{\beta^2+\pi^2 f^2}$$

This is a classic Lorentzian spectrum — low-pass shaped, with 3-dB bandwidth set by $\beta$ (consistent with an exponentially-decaying correlation being "smoother" for small $\beta$ and "noisier/faster-decorrelating" for large $\beta$).

---

## (3) Channel Model: $d = 100\,\text{m}$, attenuation $= 0.1$, $W = 5\,\text{MHz}$, $f_c = 2\,\text{GHz}$

**Propagation delay:**

$$\tau = \frac{d}{c} = \frac{100}{3\times10^8} = 3.333\times10^{-7}\,\text{s} = 333.3\,\text{ns}$$

### a. LTI model $h_c(t)$

The physical channel is pure free-space propagation: a fixed delay $\tau$ and an amplitude attenuation $\alpha=0.1$, with no multipath or frequency-selective behavior given in the problem. As an LTI system this is a scaled, delayed impulse:

$$\boxed{h_c(t) = \alpha\,\delta(t-\tau) = 0.1\,\delta(t - 333.3\,\text{ns})}$$

### b. Passband channel $h_p(t)$

The transmitted signal is a real passband (RF) waveform $x_p(t) = \text{Re}\{x(t)e^{j2\pi f_c t}\}$ that physically propagates through the medium described by $h_c(t)$ above. Because $h_c(t)$ is a pure delay/attenuation (flat magnitude, linear phase — no frequency-dependent distortion), it acts identically on the passband signal itself:

$$\boxed{h_p(t) = h_c(t) = 0.1\,\delta(t-333.3\,\text{ns})}$$

i.e. $y_p(t) = h_p(t) * x_p(t) = 0.1\, x_p(t-\tau)$.

### c. Baseband equivalent channel $h(t)$

Substitute $x_p(t) = \text{Re}\{x(t)e^{j2\pi f_c t}\}$ into $y_p(t) = \alpha\, x_p(t-\tau)$:

$$y_p(t) = \alpha\,\text{Re}\{x(t-\tau)e^{j2\pi f_c(t-\tau)}\} = \text{Re}\Big\{\big[\alpha e^{-j2\pi f_c\tau}\,x(t-\tau)\big]e^{j2\pi f_c t}\Big\}$$

so the baseband-equivalent received signal is $y(t) = \alpha e^{-j2\pi f_c\tau}\,x(t-\tau)$, giving

$$\boxed{h(t) = \alpha\, e^{-j2\pi f_c \tau}\,\delta(t-\tau)}$$

The magnitude is preserved ($|h(t)|=\alpha$ at $t=\tau$), but the carrier delay introduces a phase rotation $\theta = -2\pi f_c\tau$. Numerically:

$$f_c\tau = (2\times10^9)(3.333\times10^{-7}) = 666.667 \text{ cycles}$$

Only the fractional part matters (mod 1 cycle): $666.667 \bmod 1 = 0.667 \Rightarrow \theta = -2\pi(0.667) = -240^\circ \equiv +120^\circ$.

$$h(t) = 0.1\,e^{j120^\circ}\,\delta(t-333.3\,\text{ns}) \approx (-0.05 + j0.0866)\,\delta(t - 333.3\,\text{ns})$$

This is a good illustration of how even a small propagation delay produces a large, essentially "random-looking" carrier phase rotation at GHz carrier frequencies — the reason coherent receivers need phase/timing recovery.

### d. Discrete-time equivalent channel $h[n]$

Using the boxed result from Part (1), $h[n] = \int\text{sinc}(\tau W)h_c(nT-\tau)\,d\tau$, sampled at the baseband Nyquist rate $T=1/W$ for the $W=5\,\text{MHz}$ complex baseband signal:

$$T = \frac{1}{W} = \frac{1}{5\times10^6} = 200\,\text{ns}$$

Since $h(t)$ (Part c) is a single delayed/scaled impulse $\alpha e^{-j2\pi f_c\tau}\delta(t-\tau)$, the discrete-time equivalent is a single sinc-interpolated tap sequence, exactly Part (1)'s result with $\tau_0=\tau$, $\alpha \to \alpha e^{-j2\pi f_c\tau}$, and no second path:

$$\boxed{h[n] = \alpha\,e^{-j2\pi f_c\tau}\,\text{sinc}\!\left(n - \frac{\tau}{T}\right)}$$

Numerically, $\dfrac{\tau}{T} = \dfrac{333.3\,\text{ns}}{200\,\text{ns}} = 1.667$, which does **not** land on an integer sample — the delay falls between samples $n=1$ and $n=2$, so energy leaks into multiple taps:

$$h[n] = 0.1\,e^{j120^\circ}\,\text{sinc}(n-1.667), \qquad n\in\mathbb{Z}$$

If a simple single-tap approximation is desired (rounding to the nearest sample), the dominant tap is at $n_0=\text{round}(1.667)=2$:

$$h[n] \approx 0.1\,e^{j120^\circ}\,\delta[n-2]$$

---

## (4) Zero-Mean, Normalized Constellation from $C = \left\{ j,\ \dfrac{1-j}{\sqrt2},\ -j,\ \dfrac{-1-j}{\sqrt2} \right\}$

### Step 1 — Compute the mean

$$\mu = \frac{1}{4}\left[j + \frac{1-j}{\sqrt2} - j + \frac{-1-j}{\sqrt2}\right] = \frac{1}{4}\left[\frac{(1-j)+(-1-j)}{\sqrt2}\right] = \frac{1}{4}\cdot\frac{-2j}{\sqrt2} = -\frac{j}{2\sqrt2}$$

The constellation is **not** zero-mean as given ($\mu = -j/(2\sqrt2) \approx -j0.3536$), so we must remove the mean.

### Step 2 — Subtract the mean from each symbol

$$s_1' = j - \mu = j + \frac{j}{2\sqrt2} = j\left(1+\frac{1}{2\sqrt2}\right) = j\,\frac{2\sqrt2+1}{2\sqrt2}$$

$$s_2' = \frac{1-j}{\sqrt2} - \mu = \frac{2-2j}{2\sqrt2} + \frac{j}{2\sqrt2} = \frac{2-j}{2\sqrt2}$$

$$s_3' = -j - \mu = -j+\frac{j}{2\sqrt2} = j\left(-1+\frac{1}{2\sqrt2}\right) = -j\,\frac{2\sqrt2-1}{2\sqrt2}$$

$$s_4' = \frac{-1-j}{\sqrt2} - \mu = \frac{-2-2j}{2\sqrt2}+\frac{j}{2\sqrt2} = \frac{-2-j}{2\sqrt2}$$

**Check:** $\sum s_i' = \dfrac{(2\sqrt2+1)j - (2\sqrt2-1)j + (2-j) + (-2-j)}{2\sqrt2} = \dfrac{2j - 2j}{2\sqrt2}=0$ ✓ zero-mean confirmed.

### Step 3 — Normalize to unit average energy

Average energy of the zero-mean set:

$$|s_1'|^2 = \frac{(2\sqrt2+1)^2}{8} = \frac{9+4\sqrt2}{8}, \qquad |s_3'|^2 = \frac{(2\sqrt2-1)^2}{8} = \frac{9-4\sqrt2}{8}$$

$$|s_2'|^2 = \frac{2^2+1^2}{8} = \frac{5}{8}, \qquad |s_4'|^2 = \frac{(-2)^2+1^2}{8} = \frac{5}{8}$$

$$\sum_i |s_i'|^2 = \frac{(9+4\sqrt2)+5+(9-4\sqrt2)+5}{8} = \frac{28}{8} = 3.5 \quad\Rightarrow\quad E_{\text{avg}} = \frac{3.5}{4} = \frac{7}{8}$$

Normalization scale factor: $\dfrac{1}{\sqrt{E_{\text{avg}}}} = \sqrt{\dfrac{8}{7}} = \dfrac{2\sqrt2}{\sqrt7}$

Multiplying each $s_i'$ by $\dfrac{2\sqrt2}{\sqrt7}$, the $2\sqrt2$ in the denominators cancels cleanly:

$$s_1'' = j\,\frac{2\sqrt2+1}{2\sqrt2}\cdot\frac{2\sqrt2}{\sqrt7} = j\,\frac{2\sqrt2+1}{\sqrt7}, \qquad s_2'' = \frac{2-j}{2\sqrt2}\cdot\frac{2\sqrt2}{\sqrt7} = \frac{2-j}{\sqrt7}$$

$$s_3'' = -j\,\frac{2\sqrt2-1}{\sqrt7}, \qquad s_4'' = \frac{-2-j}{\sqrt7}$$

### Result

$$\boxed{C_{\text{norm}} = \left\{\ \frac{(1+2\sqrt2)\,j}{\sqrt7},\ \ \frac{2-j}{\sqrt7},\ \ \frac{(1-2\sqrt2)\,j}{\sqrt7},\ \ \frac{-2-j}{\sqrt7}\ \right\}}$$

Numerically ($\sqrt2\approx1.4142$, $\sqrt7\approx2.6458$):

| Symbol | Value |
|---|---|
| $s_1''$ | $\approx j\,1.4468$ |
| $s_2''$ | $\approx 0.7559 - j0.3780$ |
| $s_3''$ | $\approx -j\,0.6911$ |
| $s_4''$ | $\approx -0.7559 - j0.3780$ |

**Verification:**
- Zero-mean: real parts sum to $0.7559-0.7559=0$; imaginary parts sum to $1.4468-0.3780-0.6911-0.3780 \approx 0$ ✓
- Unit average energy: $\dfrac{1}{4}\sum|s_i''|^2 = \dfrac{1}{4}\cdot\dfrac{(9+4\sqrt2)+5+(9-4\sqrt2)+5}{7} = \dfrac{28/7}{4} = \dfrac{4}{4}=1$ ✓
