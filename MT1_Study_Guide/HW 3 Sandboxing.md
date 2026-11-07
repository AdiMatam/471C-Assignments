# HW 3 — Problem 2(a)

**Given:** $h_c(t)=\sum_{k=0}^{9} 0.8^{k}\,\delta\!\left(t-k\cdot 10^{-7}\right)$

**Find:** $h_c(f)$

## Solution

Fourier transform, using $\delta(t-\tau)\;\longleftrightarrow\; e^{-j2\pi f\tau}$:

$$
h_c(f)=\int_{-\infty}^{\infty} h_c(t)\,e^{-j2\pi f t}\,dt=\sum_{k=0}^{9} 0.8^{k}\,e^{-j2\pi f k\cdot 10^{-7}}
$$

Let $z = 0.8\,e^{-j2\pi f\cdot 10^{-7}}$. The sum is a finite geometric series, $\sum_{k=0}^{9} z^k=\dfrac{1-z^{10}}{1-z}$:

$$
\boxed{\,h_c(f)=\frac{1-0.8^{10}\,e^{-j2\pi f\cdot 10^{-6}}}{1-0.8\,e^{-j2\pi f\cdot 10^{-7}}}\,}
$$

with $0.8^{10}\approx 0.1074$.

---

# HW 3 — Problem 2(b)

**Given:** ideal bandpass filter $p(t)=2W\,\mathrm{sinc}(Wt)\cos(2\pi f_c t)$, with $f_c=1700$ MHz and $W=20$ MHz.

**Find:** $h_p(t)$, the equivalent passband channel (the cascade of $p$ and $h_c$).

## Solution

The cascade is a convolution, $h_p(t)=(p*h_c)(t)$. In frequency:

$$
P(f)=\mathrm{rect}\!\left(\tfrac{f-f_c}{W}\right)+\mathrm{rect}\!\left(\tfrac{f+f_c}{W}\right),
\qquad h_p(f)=P(f)\,h_c(f)
$$

The BPF has unit gain on the bands $|f\mp f_c|<W/2$.

Convolving with $\delta(t-\tau_k)$ delays by $\tau_k$ (with $\tau_k=k\cdot10^{-7}$ s):

$$
h_p(t)=\sum_{k=0}^{9}0.8^{k}\,p(t-\tau_k)
$$

$$
\boxed{\,h_p(t)=\sum_{k=0}^{9}0.8^{k}\;2W\,\mathrm{sinc}\!\big(W(t-k\cdot10^{-7})\big)\cos\!\big(2\pi f_c(t-k\cdot10^{-7})\big)\,}
$$

with $W=20\times10^{6}$ and $f_c=1.7\times10^{9}$.

Equivalently, in frequency:

$$
h_p(f)=\left[\mathrm{rect}\!\left(\tfrac{f-f_c}{W}\right)+\mathrm{rect}\!\left(\tfrac{f+f_c}{W}\right)\right]\sum_{k=0}^{9}0.8^{k}e^{-j2\pi f k\cdot10^{-7}}
$$

**Simplification:** $f_c\tau_k=1700\times10^{6}\cdot k\cdot10^{-7}=170k$ is an integer number of cycles, so $\cos\!\big(2\pi f_c(t-\tau_k)\big)=\cos(2\pi f_c t)$. Then:

$$
h_p(t)=2W\cos(2\pi f_c t)\sum_{k=0}^{9}0.8^{k}\,\mathrm{sinc}\!\big(W(t-k\cdot10^{-7})\big)
$$

---

# HW 3 — Problem 2(c)

**Find:** the complex baseband equivalent channel $h(t)$.

## Solution

**Goal:** $h(t)$ maps the input envelope $x(t)$ to the output envelope $y(t)$, i.e. $y=h*x$.

**Step 1: start from $h_p$.** From (b), $h_p(f)=p(f)\,h_c(f)$, where $p(f)$ has two bands, at $+f_c$ and $-f_c$.

**Step 2: keep the $+f_c$ band only.**
- The negative band is the mirror image of the positive band, so it carries no new information.
- Take the band at $[f_c-\tfrac W2,\,f_c+\tfrac W2]$.

**Step 3: shift it down to DC.**
- Shifting left by $f_c$ means replacing $f$ with $f+f_c$:
$$h(f)=h_p(f+f_c)\quad\text{for } |f|\le \tfrac W2,\qquad 0 \text{ otherwise}$$
- Inside that band $p(f+f_c)=1$, so $h_p(f+f_c)=h_c(f+f_c)$:
$$h(f)=\mathrm{rect}\!\left(\tfrac fW\right)h_c(f+f_c)$$
- No extra factor of $\tfrac12$ or $2$ (the signal gets these, the channel doesn't).

**Step 4: go to the time domain.**
- Multiplying by $\mathrm{rect}(f/W)$ becomes convolving with $W\,\mathrm{sinc}(Wt)$.
- $h_c(f+f_c)\;\longleftrightarrow\;h_c(t)\,e^{-j2\pi f_c t}$ (a shift in $f$ gives an exponential in $t$).
$$h(t)=W\,\mathrm{sinc}(Wt)\,*\,\big[h_c(t)\,e^{-j2\pi f_c t}\big]$$

**Step 5: plug in $h_c(t)=\sum_k 0.8^k\,\delta(t-\tau_k)$, with $\tau_k=k\cdot10^{-7}$.**
- Multiplying by $e^{-j2\pi f_c t}$ sets $t=\tau_k$ at each delta (sifting):
$$h_c(t)\,e^{-j2\pi f_c t}=\sum_{k=0}^{9}0.8^k\,e^{-j2\pi f_c\tau_k}\,\delta(t-\tau_k)$$
- Convolving $W\,\mathrm{sinc}(Wt)$ with $\delta(t-\tau_k)$ delays the sinc by $\tau_k$:
$$\boxed{\,h(t)=\sum_{k=0}^{9}0.8^{k}\,e^{-j2\pi f_c \tau_k}\;W\,\mathrm{sinc}\!\big(W(t-\tau_k)\big)\,}$$

**Step 6: evaluate the phase.**
- $f_c\,\tau_k=(1700\times10^{6})(k\cdot10^{-7})=170\,k$
- $170k$ is an integer, so $e^{-j2\pi\cdot170k}=1$

$$h(t)=\sum_{k=0}^{9}0.8^{k}\,W\,\mathrm{sinc}\!\big(W(t-k\cdot10^{-7})\big),\qquad W=20\times10^{6}$$

**Sanity check:** if $f_c\tau_k$ were not an integer, each path would keep a constant phase $e^{-j2\pi f_c\tau_k}$ (a complex gain on that tap). Here every path gets phase $0$.

## Why not skip $h_p$? (direct route, same answer)

$h(t)$ maps $x(t)\to y(t)$, with up- and down-conversion mirrored on either end. $h_p$ is only the class's route to it, not required.

**Direct derivation:**
- $x_p=\mathrm{Re}\{x\,e^{j2\pi f_c t}\}$, so $X_p(f)=\tfrac12\big[X(f-f_c)+X^*(-f-f_c)\big]$
- Air channel: $Y_p(f)=h_c(f)\,X_p(f)$
- Down-convert and low-pass: $Y(f)=2\cdot\tfrac12\,h_c(f+f_c)\,X(f)$, for $|f|\le \tfrac W2$
- The $\tfrac12$ (up) and $2$ (down) cancel:
$$h(f)=h_c(f+f_c)\quad(|f|\le \tfrac W2)$$

**Same as the $h_p$ route:**
- $X_p$ is already zero outside the band, so $p(f)$ never changes the result.
- $h_p$ is just a name for "channel + in-band restriction".

**Is $h(t)$ just $h_c(t)$? No.**
- Up/down-conversion are mirrors: their scale factors cancel.
- They are not a "do nothing" pair, because the channel sits between them, at passband.
- The down-converter moves the channel's response around $+f_c$ to DC:
  - frequency domain: $f\to f+f_c$
  - time domain: $e^{-j2\pi f_c\tau_k}$ on each path
- The output LPF cuts it to $[-\tfrac W2,\tfrac W2]$, giving the $W\,\mathrm{sinc}$.

**Summary:** $h(t)$ = what the air does, seen from baseband = $h_c$ with its carrier-band slice moved to DC.

---

# HW 3 — Problem 2(d)

**Find:** the discrete-time equivalent channel $h[n]$, sampling at the Nyquist rate.

## Solution

Critical sampling: $T=1/W=50$ ns. Slide 16 gives $h[n]=T\,h_{\text{low}}(nT)$, which for critical sampling is:

$$
h[n]=\int \mathrm{sinc}(n-W\tau)\,h_c(\tau)\,e^{-j2\pi f_c\tau}\,d\tau
=\sum_{k=0}^{9}0.8^{k}\,e^{-j2\pi f_c\tau_k}\,\mathrm{sinc}\!\left(n-\tfrac{\tau_k}{T}\right)
$$

Here $\tau_k=k\cdot10^{-7}$ s, so $\tau_k/T=\dfrac{100\text{ ns}\cdot k}{50\text{ ns}}=2k$, and the phase factor is 1 as in (c):

$$
\boxed{\,h[n]=\sum_{k=0}^{9}0.8^{k}\,\mathrm{sinc}(n-2k)\,}
$$

Since $\mathrm{sinc}(m)=\delta[m]$ for integer $m$:

$$
h[n]=\sum_{k=0}^{9}0.8^{k}\,\delta[n-2k]=
\begin{cases}0.8^{n/2}, & n\in\{0,2,4,\dots,18\}\\[2pt] 0, & \text{otherwise}\end{cases}
$$
