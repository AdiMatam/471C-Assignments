# 05 — Optimal Pulse Shapes, Nyquist, Raised Cosine, and Digital (Multirate) Implementation (Weeks 6–7)

*Sources: AWGNPulseShaping, FilterImplementation, DigitalFilterImplementation (first half), Lab 2 Part 2 (pulse shaping / matched filtering), Lab 3 pre-lab.*

> 📌 **Not in HW1–HW3.** Per your instructor, concepts not yet covered by a homework won't be tested, so this guide is **likely out of scope for Midterm 1** (it was covered in lecture and Lab 2.2 only). Read it only after guides 02–04 are solid; the matched-filter / Nyquist / raised-cosine headline ideas are the part worth a skim.

## Why this matters
"Why a matched filter?", "what is the zero-ISI condition?", "what's the bandwidth of a raised-cosine signal?", and "implement this filter efficiently with upsampling/downsampling" are all standard exam fare, and they're the theory of Lab 2.2 (pulse shaping, eye diagrams).

## 1. The AWGN link, start to finish
```
TX: bits → symbol mapping → pulse train → g_tx(t) → gain √Ex → x(t) → [channel: +noise v(t)] →
RX: g_rx(t) → sample at nT (C/D, rate 1/T) → detection → inverse symbol mapping → bits
```
**Design problem:** choose $g_{tx}(t)$ and $g_{rx}(t)$ to maximize the **SINR** of the sampled output.

## 2. Sampled received signal
Let $g(t)=(g_{tx}*g_{rx})(t)$ be the **composite pulse**. After receive filter and sampling at $nT$ (perfect timing):
$$y[n]=\underbrace{\sqrt{E_x}\,g(0)\,s[n]}_{\text{desired}}+\underbrace{\sqrt{E_x}\sum_{m\ne n}s[m]\,g((n-m)T)}_{\text{intersymbol interference (ISI)}}+\underbrace{v[n]}_{\text{noise}}$$
- $v[n]=(g_{rx}*v)(nT)$: noise filtered by $g_{rx}$ ⇒ variance $N_0\|g_{rx}\|^2$.
- **SINR** $=\dfrac{S}{I+N}=\dfrac{E_x|g(0)|^2}{E_x\sum_{m\ne0}|g(mT)|^2+N_0\|g_{rx}\|^2}$ (unit-energy symbols).

## 3. Two conditions maximize SINR
**(1) Matched filter.** With $g(0)=\int g_{tx}(t)g_{rx}(-t)\,dt$, **Cauchy–Schwarz**:
$$|g(0)|^2=\left|\int g_{tx}(t)g_{rx}(-t)dt\right|^2\le\|g_{tx}\|^2\,\|g_{rx}\|^2$$
Signal-to-noise (ignoring ISI) $=\dfrac{E_x|g(0)|^2}{N_0\|g_{rx}\|^2}\le\dfrac{E_x\|g_{tx}\|^2}{N_0}=\dfrac{E_x}{N_0}$ — equality iff $g_{rx}(-t)\propto g_{tx}^*(t)$:
$$\boxed{g_{rx}(t)=g_{tx}^*(-t)}\ \ (\text{time-reversed conjugate = "matched" to the transmit pulse})$$
⇒ the matched filter achieves the maximum SNR $E_x/N_0$ (the energy captured divided by noise density). Intuition: correlate the received waveform with the known pulse shape — add up all the signal energy coherently while noise adds incoherently.
Then $g(t)=g_{tx}*g_{tx}^*(-t)$ = the **autocorrelation** of $g_{tx}$; $g(0)=\|g_{tx}\|^2=1$.

**(2) Zero ISI (Nyquist condition).** Need $g(mT)=0$ for $m\ne0$ with $g(0)=1$:
$$\boxed{g(nT)=\delta[n]}\ \Longleftrightarrow\ \frac1T\sum_{k=-\infty}^{\infty}G\!\left(f-\frac kT\right)=1\ \ \forall f$$
(the **Nyquist pulse criterion**: the periodic-in-$1/T$ replicas of $G(f)$ sum to a constant). Then $y[n]=\sqrt{E_x}s[n]+v[n]$, $v[n]\sim\mathcal{CN}(0,N_0)$ IID (because $g$ is Nyquist and $\|g_{rx}\|=1$ the filtered noise samples are uncorrelated).

## 4. Nyquist pulses
### Sinc
$g(t)=\text{sinc}(t/T)$, $G(f)=T\,\text{rect}(Tf)$, bandwidth $\tfrac1{2T}$ (the **minimum possible** — the Nyquist rate: symbol rate $1/T$ needs ≥ $1/T$ of two-sided spectrum).
Problems in practice: **noncausal** (fix with delay), **must be truncated**, **brick-wall edge** is hard to realize, **slow $1/t$ decay** ⇒ huge **sensitivity to timing errors** (each timing error leaks ISI from many neighbors), and if sampled below Nyquist ⇒ aliasing.

### Raised cosine (RC) with roll-off $\alpha\in[0,1]$
$$G_{rc}(f)=\begin{cases}T&|f|\le\frac{1-\alpha}{2T}\\[2pt]\frac T2\left[1+\cos\!\left(\frac{\pi T}{\alpha}\left(|f|-\frac{1-\alpha}{2T}\right)\right)\right]&\frac{1-\alpha}{2T}<|f|\le\frac{1+\alpha}{2T}\\[2pt]0&\text{otherwise}\end{cases}$$
$$g_{rc}(t)=\text{sinc}\!\left(\tfrac tT\right)\frac{\cos(\pi\alpha t/T)}{1-4\alpha^2t^2/T^2}$$
- **Absolute (one-sided) bandwidth** $B=\dfrac{1+\alpha}{2T}$ — i.e. **excess bandwidth** $\alpha\cdot\frac1{2T}$ beyond the sinc; "**$\alpha$ × 100% excess bandwidth**".
- Two-sided (passband) width of the transmitted signal $=\dfrac{1+\alpha}{T}$. **Nyquist rate for RC signal** $=2B=(1+\alpha)/T$ complex samples/s — i.e. the sample rate must exceed this to avoid aliasing.
- $\alpha=0$ is the sinc; $\alpha=1$ is full cosine, $B=1/T$.
- Time domain: main lobe width/ISI-sensitivity controlled by $\alpha$; tails decay at best $\sim1/t^3$ (much faster than sinc ⇒ **robust to timing errors**; truncation hurts less).
- **Trade-off:** larger $\alpha$ = more bandwidth but easier to implement and more timing-error robust; smaller $\alpha$ = spectrally efficient but long ringing.

### Square-root raised cosine (SRRC)
We want the *composite* $g=g_{tx}*g_{rx}$ to be RC **and** $g_{rx}=g_{tx}^*(-t)$. In frequency $G(f)=|G_{tx}(f)|^2$ ⇒ $\boxed{G_{tx}(f)=G_{rx}(f)=\sqrt{G_{rc}(f)}}$ (real, even pulse). SRRC is **used in practice** at *both* TX and RX; the cascade is RC (zero ISI) and the receive filter is matched (max SNR).
- Noise after SRRC receive filter is colored in continuous time but **IID at symbol-rate sampling**.
- **Per-filter** SRRC is *not* itself Nyquist; only the cascade is.

### Example numbers (Lab 2.2 style)
Symbol rate $1/T=100$ ksym/s, $\alpha=0.5$: absolute baseband bandwidth $B=75$ kHz; occupied (passband) bandwidth 150 kHz; minimum complex sample rate $>150$ kS/s; with $M$ samples/symbol, $f_s=M/T$ (e.g. $M=4$: 400 kS/s).

## 5. Implementing pulse shaping in discrete time (multirate DSP)
Problem: the model "continuous pulse train × continuous filter" isn't directly implementable (no ideal D/C; $g_{tx}$ may have bandwidth beyond $1/(2T)$). Use a **discrete-time oversampled** version.

### Transmitter — upsampling + polyphase
- $g_{tx}(t)$ is bandlimited ⇒ sample it at $T_{tx}=T/M_{tx}$ ($M_{tx}=L$ = **samples per symbol**, "TX oversample factor") ⇒ $g_{tx}[n]=g_{tx}(nT_{tx})$ (design with MT Generate Filter Coefficients VI in the lab).
- Generated sequence: 
 $$c[n]=\sum_ks[k]\,g_{tx}[n-kL]=\big(\uparrow_L s\big)*g_{tx}\ ,$$ i.e. **zero-stuff** $s[n]$ ($L-1$ zeros after each symbol) then filter. Then D/A at rate $1/T_{tx}$.
- **Wasteful:** most filter inputs are zeros. **Polyphase / filter-bank form:** split $g_{tx}$ into $L$ sub-filters $g^{(\ell)}[n]=g_{tx}[nL+\ell]$, $\ell=0,\dots,L-1$. Then the $\ell$-th output phase is
 $$c[nL+\ell]=\sum_ks[k]\,g^{(\ell)}[n-k]\quad(\text{each sub-filter runs at the **symbol rate**})$$
 and the $L$ outputs are **interleaved** (commutator). Same output, ~$L\times$ fewer multiplies.
- **Noble identity:** $(\uparrow L)\to H(z^L)\ \equiv\ H(z)\to(\uparrow L)$ — filtering at the low rate then upsampling equals upsampling then filtering with the stuffed filter.

### Receiver — oversampling + downsampling
- A/D at $T_{rx}=T/M_{rx}$ (**oversampling** if $1/T_{rx}>$ Nyquist rate of the signal); $r[n]$ sampled; matched filter in discrete time: $g_{rx}[n]=g_{tx}^*[-n]$ (sampled at $T_{rx}$, so this needs $g_{rx}[n]=g_{rx}(nT_{rx})$ at the RX rate).
- Symbol-rate samples: **filter then downsample by $M_{rx}$**: $y[k]=\sum_nr[n]\,g_{rx}[kM_{rx}-n]$.
- **Wasteful:** compute all outputs, throw away $M_{rx}-1$ of every $M_{rx}$. Use the **downsampling (noble) identity**: split the *input* into $M_{rx}$ polyphase branches (delayed by $z^{-m}$, downsampled by $M_{rx}$), each filtered by sub-filter $g_{rx}^{(m)}$ at the **low rate**, then **sum** the branches. Same result, ~$M_{rx}\times$ fewer operations.
- **Using a different RX oversample rate than TX** (Lab 2.2): the symbol period must be the same on both sides: $T=M\,T_M=N\,T_N$ ($T_M$, $T_N$ = TX and RX sample periods) ⇒ $\dfrac MN=\dfrac{T_N}{T_M}=\dfrac{f_{s,\text{TX}}}{f_{s,\text{RX}}}$. Samples per symbol scale with sample rate: $M=f_{s,\text{TX}}T$, $N=f_{s,\text{RX}}T$.

### Resampling reference
- **Upsample by $L$:** insert $L-1$ zeros between samples (spectrum images appear — follow with LPF cutoff $\pi/L$ and gain $L$) = *interpolation*.
- **Downsample by $M$:** keep every $M$th sample (aliasing unless prior LPF cutoff $\pi/M$) = *decimation*.
- **Rational rate change $L/M$:** upsample by $L$, LPF at $\min(\pi/L,\pi/M)$, downsample by $M$.
- New sample period after downsampling a signal sampled at $T_z$ by $M$: **$M\,T_z$** (Lab 3 pre-lab Q3: for $T_z=T/M$ this equals $T$).

## 6. Eye diagram (lab)
Plot many overlaid symbol-length segments of the matched-filter output. **Open eye** = ISI-free at the best sampling instant. Vertical closure = noise/ISI; horizontal narrowing = timing jitter; sampling off the optimum instant shrinks the opening (ISI).
Impairments visible: AWGN (vertical blur), timing offset, bad/non-matched filter, channel ISI (Lab 2.2 pre-lab Q2).

## Traps
- RC bandwidth is $(1+\alpha)/(2T)$ **one-sided**; don't forget the factor 2 when converting to passband width/Nyquist sample rate.
- SRRC at **both** TX and RX, not RC at both.
- Matched filter is $g_{tx}^*(-t)$, includes **time reversal** and **conjugate**; for a real symmetric pulse it equals $g_{tx}(t)$.
- Zero ISI needs sampling at the **right instant** (see Block 07) — a timing offset breaks it.
- Polyphase index: $g^{(\ell)}[n]=g[nL+\ell]$ (TX), and don't confuse upsampling (zero-stuffing) with interpolation (zero-stuff + LPF).

## Self-test
1. State the Nyquist criterion in time and in frequency; show a sinc satisfies it.
2. Derive the matched filter with Cauchy–Schwarz (no notes).
3. $T=1\,\mu$s, $\alpha=0.25$: $B$? bandwidth of the passband signal? ($B=625$ kHz; 1.25 MHz.)
4. Write the TX polyphase equation for $L=4$ and a 16-tap $g_{tx}$ (4 taps per branch).
5. Why does a smaller $\alpha$ make the system more sensitive to timing errors?

## Lab link
Lab 2.2: `pulse_shaping.vi` (gets oversample factor from `modulation parameters in` → `TX oversample factor`), `matched_filtering.vi`, eye diagrams. Lab 3: raised-cosine ($\alpha=0.5$) with RX oversample factor $N$ varied, and the relation $M/N=T_N/T_M$ used for consistent symbol rates.
