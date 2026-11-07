# 11 — Practice Set Solutions

⚠️ Only open this after you've attempted all of `10_Practice_Set.md`. Numerical values were checked with a script; my worked answers follow the lecture/HW2 conventions, so if your posted HW solution uses a different scaling convention, follow that one.

---

## Problem 1 — Discrete-time equivalent channel

**(a)** $T=1/W=100$ ns (so $TW=1$).

**(b)** Using $h[n]=\displaystyle\int\text{sinc}(\tau W)\,h_c(nT-\tau)\,d\tau$ and the sifting property:
$$h[n]=\text{sinc}\!\left(n-\tfrac{150}{100}\right)+0.5\,\text{sinc}\!\left(n-\tfrac{300}{100}\right)=\text{sinc}(n-1.5)+0.5\,\text{sinc}(n-3)$$

**(c)** $\tau_1/T=3$ is an integer ⇒ $\text{sinc}(n-3)=\delta[n-3]$, so this path contributes exactly one tap, $0.5$ at $n=3$. The $150$ ns path has $\tau_0/T=1.5$, a half-sample delay, so it smears.

**(d)** $h[n]=\text{sinc}(n-1.5)+0.5\,\delta[n-3]$:

| $n$ | −1 | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|---|
| $\text{sinc}(n-1.5)$ | 0.127 | −0.212 | 0.637 | 0.637 | −0.212 | 0.127 | −0.091 |
| $+0.5\delta[n-3]$ | 0 | 0 | 0 | 0 | +0.5 | 0 | 0 |
| **$h[n]$** | **0.127** | **−0.212** | **0.637** | **0.637** | **0.288** | **0.127** | **−0.091** |

(Check: $\text{sinc}(0.5)=2/\pi=0.637$; $\text{sinc}(1.5)=-2/(3\pi)=-0.212$; $\text{sinc}(2.5)=2/(5\pi)=0.127$.)

**(e)** The channel is a pure delay, which is exactly representable in discrete time only if it's a multiple of $T$. A fractional delay is realized by sinc interpolation of the sampled signal, and the sinc is infinite and decays like $1/n$, so the equivalent filter has infinite support (in practice truncated to a few taps).

---

## Problem 2 — Power spectrum and a WSS check

**(a)** $C_{xx}(\tau)=\sigma^2e^{-a|\tau|}$ with $\sigma^2=3$, $a=4$. Using $e^{-a|\tau|}\leftrightarrow\dfrac{2a}{a^2+(2\pi f)^2}$:
$$P_x(f)=\frac{3\cdot8}{16+(2\pi f)^2}=\boxed{\frac{24}{16+4\pi^2f^2}}$$
Total power $=C_{xx}(0)=\boxed{3}$ (also $=\int P_x\,df$).
(Equivalent in $\omega$: $P_x(\omega)=\dfrac{24}{16+\omega^2}$.)

**(b)** $x[n]=s[n]-0.8s[n-1]$.
- Mean: $E[x[n]]=0-0.8\cdot0=0$ (constant).
- Covariance: $C_{xx}[n,n-k]=E[x[n]x[n-k]]$:
 - $k=0$: $\sigma_s^2(1+0.64)=2\cdot1.64=\mathbf{3.28}$
 - $k=\pm1$: $E[(s[n]-0.8s[n-1])(s[n-1]-0.8s[n-2])]=-0.8\sigma_s^2=\mathbf{-1.6}$
 - $|k|\ge2$: $0$.
- Mean constant and covariance depends only on $k$ ⇒ **WSS**. (It is not white: neighbors are negatively correlated.)
- PSD: $P_x(e^{j2\pi f})=\sigma_s^2\,|1-0.8e^{-j2\pi f}|^2=2\,(1.64-1.6\cos2\pi f)=\mathbf{3.28-3.2\cos2\pi f}$ — equals $\sum_kC_{xx}[k]e^{-j2\pi fk}=3.28-1.6\cdot2\cos2\pi f$ ✓. Highpass shape: small at $f=0$ (0.08), big at $f=\tfrac12$ (6.48).

---

## Problem 3 — Bandwidth and sampling

Total power $=3$.

**(a)** $P_x(0)=24/16=1.5$; half $=0.75$: $\dfrac{24}{16+(2\pi f)^2}=0.75\Rightarrow16+(2\pi f)^2=32\Rightarrow(2\pi f)^2=16\Rightarrow f=\dfrac{4}{2\pi}$
$$\boxed{B_{3\text{dB}}=\frac{2}{\pi}\approx0.637\text{ Hz}}$$

**(b)** Here $P_x(f)=\dfrac{24}{16+(2\pi f)^2}$ and total power $=3$.

*Power in $[-B,B]$:*
$$\int_{-B}^{B}\frac{24}{16+(2\pi f)^2}\,df$$

*Substitute $u=2\pi f$, so $df=\dfrac{du}{2\pi}$; the bounds become $\pm2\pi B$:*
$$=\frac{24}{2\pi}\int_{-2\pi B}^{2\pi B}\frac{du}{16+u^2}=\frac{12}{\pi}\int_{-2\pi B}^{2\pi B}\frac{du}{4^2+u^2}$$

*Anti-derivative, using $\displaystyle\int\frac{du}{a^2+u^2}=\frac1a\arctan\frac ua$ with $a=4$:*
$$=\frac{12}{\pi}\cdot\frac14\Big[\arctan\frac u4\Big]_{-2\pi B}^{2\pi B}=\frac3\pi\Big[\arctan\frac{2\pi B}{4}-\arctan\frac{-2\pi B}{4}\Big]$$

*arctan is odd, so $\arctan(-z)=-\arctan(z)$ and the bracket becomes $2\arctan\frac{2\pi B}{4}$:*
$$=\frac3\pi\cdot2\arctan\frac{2\pi B}{4}=\frac6\pi\arctan\frac{\pi B}{2}$$

*Fraction of total power (divide by 3):*
$$\frac{6/\pi}{3}\arctan\frac{\pi B}{2}=\frac2\pi\arctan\frac{\pi B}{2}$$
(check: $B\to\infty$ gives $\frac2\pi\cdot\frac\pi2=1$ ✓)

*Set it to $0.95$ and solve:*
$$\frac2\pi\arctan\frac{\pi B}{2}=0.95\;\Rightarrow\;\arctan\frac{\pi B}{2}=0.475\pi$$
$$\frac{\pi B}{2}=\tan(0.475\pi)=12.706\;\Rightarrow\;B=\frac{2(12.706)}{\pi}$$
$$\boxed{B_{95\%}\approx8.09\text{ Hz}}$$

**(c)** $f_s=3\cdot\dfrac{2}{\pi}=\dfrac6\pi\approx1.910$ Hz ⇒ $\boxed{T=\dfrac{\pi}{6}\approx0.5236\text{ s}}$.

**(d)** $C_{xx}[n]=C_{xx}(nT)=3e^{-4T|n|}=\boxed{3e^{-\frac{2\pi}{3}|n|}\approx3\,(0.1231)^{|n|}}$ ($4\cdot\pi/6=2\pi/3\approx2.094$).

**(e)** With $r=e^{-2\pi/3}=0.1231$:
$$P_x(e^{j2\pi f})=\sum_n3r^{|n|}e^{-j2\pi fn}=\boxed{\frac{3(1-r^2)}{1-2r\cos(2\pi f)+r^2}}$$
- $f=0$: $\dfrac{3(1-r^2)}{(1-r)^2}=3\dfrac{1+r}{1-r}=\mathbf{3.843}$
- $f=\tfrac12$: $3\dfrac{1-r}{1+r}=\mathbf{2.342}$.
(Sanity: the DT spectrum is the aliased sum of the CT spectrum, scaled; the ratio between $f=0$ and $f=\tfrac12$ is much milder than in CT because the CT spectrum has long tails that alias in.)

**(f)** The 95% bandwidth (8.09 Hz) is much wider than the 3-dB bandwidth (0.64 Hz). The Lorentzian-shaped spectrum has heavy tails: half the peak power density is reached early, but a lot of power sits far from DC. This is also why sampling at 3× the 3-dB frequency is **not** alias-free: the process isn't truly bandlimited.

---

## Problem 4 — Passband to discrete-time channel

Delays: $\tau_1=60/c=200$ ns, $\tau_2=105/c=350$ ns. $T=1/W=200$ ns.

**(a)** $h_c(t)=0.2\,\delta(t-200\text{ ns})+0.1\,\delta(t-350\text{ ns})$; 
$h_c(f)=0.2\,e^{-j2\pi f(200\text{ ns})}+0.1\,e^{-j2\pi f(350\text{ ns})}$.

**(b)** $h_p(t)=p(t)*h_c(t)$ with the ideal BPF $p(t)=2W\,\text{sinc}(Wt)\cos(2\pi f_ct)$ (unit passband gain over $|\,|f|-f_c|\le W/2$):
$$h_p(t)=0.2\,p(t-200\text{ ns})+0.1\,p(t-350\text{ ns})$$
In frequency, $h_p(f)=h_c(f)$ restricted to the two bands of width $5$ MHz around $\pm2.45$ GHz.

**(c)** Shift the positive band down (no extra scale factor on the channel): $h(f)=h_p(f+f_c)$ on $|f|\le W/2$, giving
$$h(t)=\sum_k a_ke^{-j2\pi f_c\tau_k}\,[W\,\text{sinc}(W(t-\tau_k))]\ \ (\text{impulse bandlimited to }W/2)$$
Phases: 
- Path 1: $f_c\tau_1=2.45\text{ GHz}\times200\text{ ns}=490$ cycles ⇒ integer ⇒ phase $=0$ ⇒ factor $+1$.
- Path 2: $f_c\tau_2=857.5$ cycles ⇒ fractional part $0.5$ ⇒ phase $=-\pi$ ⇒ factor $e^{-j\pi}=-1$.
So $h(t)\simeq0.2\,\delta(t-200\text{ ns})-0.1\,\delta(t-350\text{ ns})$ (passed through the $W/2$ lowpass).

📎 **Where the sinc and $e^{-j2\pi f_c\tau}$ come from (full derivation):** [[12_Practice_4c_Explainer]] (live doc: [MT1 Practice #4c explainer](https://claude.ai/code/artifact/330886b4-0fc2-4b09-bcbb-08cfcbf721d7))

**(d)** $h[n]=\displaystyle\sum_ka_ke^{-j2\pi f_c\tau_k}\,\text{sinc}\!\left(n-\tfrac{\tau_k}{T}\right)$ with $\tau_1/T=1$, $\tau_2/T=1.75$:
$$\boxed{h[n]=0.2\,\delta[n-1]-0.1\,\text{sinc}(n-1.75)}$$

| $n$ | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| $-0.1\,\text{sinc}(n-1.75)$ | +0.013 | −0.030 | −0.090 | +0.018 |
| $+0.2\,\delta[n-1]$ | 0 | +0.2 | 0 | 0 |
| **$h[n]$** | **0.013** | **0.170** | **−0.090** | **0.018** |

(Values: $\text{sinc}(-1.75)=-0.1286$, $\text{sinc}(-0.75)=0.3001$, $\text{sinc}(0.25)=0.9003$, $\text{sinc}(1.25)=-0.1801$.)

**(e)** The direct path ($\tau_1=T$) lands exactly on sample 1 ⇒ one clean tap of 0.2. The reflected path ($\tau_2=1.75T$) is between samples ⇒ spread over many taps, with the largest at $n=2$ (the nearest sample) — and its carrier phase flips its sign relative to path 1.
The phase factors are the key insight: at GHz carriers a fraction of a nanosecond changes $f_c\tau$ by a large amount, so $e^{-j2\pi f_c\tau}$ looks random even though the envelope delay barely changes.

---

## Problem 5 — Normalize a constellation

$\mathcal C=\{1,\ 1+2j,\ -1+j,\ 3-j\}$.

**(a)** $\mu=\tfrac14\big[(1+1-1+3)+j(0+2+1-1)\big]=\tfrac14(4+2j)=\boxed{1+0.5j}$ ⇒ **not** zero-mean.

**(b)** Subtract $\mu$:
- $1-\mu=-0.5j$
- $1+2j-\mu=1.5j$
- $-1+j-\mu=-2+0.5j$
- $3-j-\mu=2-1.5j$
Sum: $(-0.5+1.5+0.5-1.5)j+(-2+2)=0$ ✓.

**(c)** Energies: $0.25,\ 2.25,\ 4.25,\ 6.25$ (e.g. $|-2+0.5j|^2=4+0.25$; $|2-1.5j|^2=4+2.25$). Average $E=\dfrac{0.25+2.25+4.25+6.25}{4}=\dfrac{13}{4}=\boxed{3.25}$.

**(d)** Scaling factor $1/\sqrt{3.25}=0.5547$ (i.e. $2/\sqrt{13}$):
$$\tilde{\mathcal C}=\{-0.277j,\ \ 0.832j,\ \ -1.109+0.277j,\ \ 1.109-0.832j\}$$
Check: $0.0769+0.6923+1.3077+1.9231=4.000$; $/4=1$ ✓.

**(e)** Sketch: points at $(0,-0.28)$, $(0,0.83)$, $(-1.11,0.28)$, $(1.11,-0.83)$ — an irregular 4-point set, centered at the origin.

---

## Problem 6 — Rectangular 8-point constellation

$\mathcal D=\{(a+2)+j(b+0.5)\}$ with $a\in\{-3,-1,1,3\}$, $b\in\{\pm1\}$.

**(a)** Mean of $a$ is 0 and of $b$ is 0, so $\mu=2+0.5j$ (just the shift).

**(b)** Zero-mean set: $\{a+jb\}$, a $4\times2$ rectangular grid. Average energy $=E[a^2]+E[b^2]=\dfrac{9+1+1+9}{4}+1=5+1=\boxed{6}$.

**(c)** Scale factor $=1/\sqrt6\approx0.408$.

**(d)** $\log_2 8=\mathbf3$ bits/symbol. Minimum distance of the zero-mean set is $2$ (spacing between adjacent grid points), so after normalization $d_{\min}=2/\sqrt6\approx0.816$.

---

## Problem 7 — Complex envelope

**(a)** $x_p=x_I\cos-x_Q\sin$ ⇒ $x_I=3$, $x_Q=4$ ⇒ $\boxed{x(t)=3+4j}$. Amplitude $A=|x|=5$; phase $\phi=\arctan(4/3)=53.13^\circ$:
$x_p(t)=5\cos(2\pi f_ct+53.13^\circ)$ (check: $5\cos\phi=3$, $-5\sin\phi=-4$ ✓).

**(b)** $y_p=A\cos(2\pi f_ct+\phi)=\tfrac A2\big[e^{j(2\pi f_ct+\phi)}+e^{-j(2\pi f_ct+\phi)}\big]$. Multiply by $2e^{-j2\pi f_ct}$: $Ae^{j\phi}+Ae^{-j(4\pi f_ct+\phi)}$. The LPF removes the $2f_c$ term, leaving $Ae^{j\phi}$ ✓. The factor 2 compensates the $\tfrac12$ that appeared when splitting the cosine into two exponentials (i.e. the $\div2$ at up-conversion).

**(c)** Absolute bandwidth $W=2.42-2.40=20$ MHz. At complex baseband it occupies $[-10,10]$ MHz, so the minimum complex sample rate is $W=20$ MS/s. (Directly sampling the real passband signal would need more than $2\times2.42$ GHz, which is why we down-convert first.)

**(d)** Baseband = signal's energy centered around 0 Hz (what the math/software works with, complex I+jQ). Passband = the same signal shifted up to a carrier $f_c$ so it can be radiated; up-conversion goes baseband→passband, down-conversion back.

---

## Problem 8 — Sampling and SNR

**(a)** A 6 kHz tone sampled at 8 kHz aliases to $|6-8|=\mathbf2$ kHz — **inside** the signal band (0–5 kHz), so it can't be filtered out afterwards ⇒ need an analog anti-aliasing filter before the sampler. The signal itself is **not** safely sampled either: Nyquist needs $f_s>2(5\text{ kHz})=10$ kHz, but $f_s=8$ kHz, so components between 4 and 5 kHz alias onto 3–4 kHz. Fix: sample above 10 kHz and add an analog anti-aliasing filter.

**(b)** $N_0=k_BT_e=1.38\times10^{-23}\times290=4.0\times10^{-21}$ W/Hz. Noise power $=N_0B=4.0\times10^{-21}\times20\times10^6=8.0\times10^{-14}$ W. 
SNR $=\dfrac{2\times10^{-6}}{8.0\times10^{-14}}=2.5\times10^{7}\ \Rightarrow\ 10\log_{10}(2.5\times10^7)\approx\boxed{74.0\text{ dB}}$.

**(c)** The formula $h[n]=T\,h_{\text{low}}(nT)=TW\int\text{sinc}(\tau W)h_c(nT-\tau)d\tau$ — the general form includes the factor $TW$ (the lowpass $\text{rect}(f/W)$ has impulse response $W\text{sinc}(Wt)$, and the DT filter picks up a factor $T$). At exactly Nyquist, $TW=1$, so the factor drops out. If you oversample ($TW<1$) the constant remains.

---

### Quick answer key
P1(d) $h[-1..5]=0.127,-0.212,0.637,0.637,0.288,0.127,-0.091$ · P2(a) $24/(16+4\pi^2f^2)$, power 3 · P2(b) $C=3.28,-1.6$ (WSS) · P3 $B_{3dB}=2/\pi$, $B_{95}\approx8.09$, $T=\pi/6$, $C[n]=3e^{-2\pi|n|/3}$ · P4 $h[n]=0.2\delta[n-1]-0.1\text{sinc}(n-1.75)$ · P5 $\mu=1+0.5j$, $E=3.25$ · P6 $\mu=2+0.5j$, $E=6$ · P7 $x=3+4j$, $A=5$, $\phi=53.13^\circ$ · P8 alias 2 kHz, SNR 74 dB.
