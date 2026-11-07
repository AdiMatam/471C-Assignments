# MT1 Practice #4c — Where the sinc and the delay come from

Oct 19, 2026 · @Aditya Matam · [Live doc](https://claude.ai/code/artifact/330886b4-0fc2-4b09-bcbb-08cfcbf721d7)

## Context

The 4c answer is just the 4a frequency response, shifted down by f\_c and cut to |f| ≤ W/2, then inverse-transformed. The sinc comes from that cut (a rect), and both exponentials come from shifting the 4a delay term e^(−j2πfτ).

Problem 4 (MT1 practice set, `10_Practice_Set.md`; answer in `11_Practice_Solutions.md` → Problem 4 (c)):

- Carrier f\_c = 2.45 GHz, absolute bandwidth W = 5 MHz.
- Path 1: 60 m, gain a₁ = 0.2, so τ₁ = 200 ns. Path 2: 105 m, gain a₂ = 0.1, so τ₂ = 350 ns.
- (c) asks for the complex baseband equivalent channel h(t).

The answer in the solution set is:

$$
h(t)=\sum_k a_k\,e^{-j2\pi f_c\tau_k}\;W\,\mathrm{sinc}\big(W(t-\tau_k)\big)
$$

Three pieces need explaining: the constant e^(−j2π f\_c τ\_k), the W sinc(W·), and the shift (t − τ\_k) inside the sinc. The rule we use is the one from guide 03, Step 3: take the positive band of h\_p, shift it to DC, and apply no ×2 factor (that factor is for signals, not channels).

## Where each factor comes from

One path's delay term in 4a is e^(−j2π f τ). After the shift f → f + f\_c it splits in two: a constant part and a part that still depends on f. Everything in 4c follows from that split.

| Factor in h(t) | What it is in frequency | Where it enters | What it does |
| --- | --- | --- | --- |
| a\_k | a\_k | 4a: path gain | Scales the path |
| e^(−j2π f\_c τ\_k) | e^(−j2π f\_c τ\_k), with no f in it | 4c: the shift turns f into f + f\_c, and the f\_c part becomes a constant | Rotates the path's phase (carrier phase) |
| (t − τ\_k) inside the sinc | e^(−j2π f τ\_k), linear in f | 4a: the delay, left over after the shift | Shifts the sinc to t = τ\_k (time-shift property) |
| W sinc(Wt) | rect(f/W) | 4b/4c: the band edges, now centered at 0 | Band-limits the impulse to ±W/2 |

The sinc in 4c is not the same as the one in 4b. In 4b it was modulated by cos(2π f\_c t). Down-conversion strips the cosine and leaves the plain lowpass sinc W sinc(Wt).

## Derivation, two ways

Both routes give the same h(t). Route A works in frequency and follows the solution's "shift the positive band down" line. Route B starts from 4b's h\_p(t) and stays in time, with no shortcuts.

### Route A: frequency domain

1. Start from 4a. Each path is a gain times a delay, and a delay τ transforms to e^(−j2π f τ):

$$
h_c(f)=\sum_k a_k\,e^{-j2\pi f\tau_k}
$$

2. Apply 4b's ideal BPF. It keeps two bands of width W, centered at +f\_c and −f\_c:

$$
h_p(f)=h_c(f)\left[\mathrm{rect}\!\left(\frac{f-f_c}{W}\right)+\mathrm{rect}\!\left(\frac{f+f_c}{W}\right)\right]
$$

3. Shift down by f\_c: h(f) = h\_p(f + f\_c), keeping only |f| ≤ W/2. Replace every f with f + f\_c. The +f\_c band becomes rect(f/W), centered at 0. The −f\_c band moves to −2f\_c, outside |f| ≤ W/2, so it is dropped:

$$
h(f)=\sum_k a_k\,e^{-j2\pi (f+f_c)\tau_k}\,\mathrm{rect}\!\left(\frac{f}{W}\right)
$$

4. Split the exponent. This is the step that produces both exponentials. Since (f + f\_c)τ = fτ + f\_cτ:

$$
h(f)=\sum_k \underbrace{a_k\,e^{-j2\pi f_c\tau_k}}_{\text{constant (no }f)}\;\cdot\;\underbrace{e^{-j2\pi f\tau_k}}_{\text{delay by }\tau_k}\;\cdot\;\underbrace{\mathrm{rect}(f/W)}_{\text{lowpass}}
$$

5. Inverse-transform one factor at a time.
   - rect(f/W) ↔ W sinc(Wt). To derive it, integrate e^(j2πft) over −W/2 to W/2. That gives sin(πWt)/(πt), which equals W sinc(Wt).
   - Multiplying by e^(−j2π f τ\_k) in frequency delays by τ\_k in time, so W sinc(Wt) becomes W sinc(W(t − τ\_k)).
     - *e^(−j2π f τ\_k) -> delta(t-t\_k) in time which is sifted against sinc()*
   - a\_k e^(−j2π f\_c τ\_k) has no f in it. It is a complex number and passes straight through.

$$
h(t)=\sum_k a_k\,e^{-j2\pi f_c\tau_k}\;W\,\mathrm{sinc}\big(W(t-\tau_k)\big)
$$

### ~~Route B: time domain, starting from 4b~~

~~The guide 03 convention is h(t) = LPF{ h\_p(t) e^(−j2π f\_c t) }, with no ×2 for the channel. From 4b, h\_p(t) = Σ a\_k p(t − τ\_k), where p(t) = 2W sinc(Wt) cos(2π f\_c t). Take a single path with delay τ:~~

~~p(t − τ) = 2W sinc(W(t − τ)) cos(2π f\_c (t − τ))~~

~~The carrier inside p was delayed too. That is where f\_cτ hides physically: delaying a cosine by τ shifts its phase by 2π f\_c τ.~~

~~Now multiply by e^(−j2π f\_c t), writing the cosine as two exponentials:~~

~~cos(2π f\_c (t − τ)) e^(−j2π f\_c t) = ½ e^(−j2π f\_c τ) + ½ e^(−j2π f\_c (2t − τ))~~

- ~~First term: constant in t. It is the carrier phase e^(−j2π f\_c τ).~~
- ~~Second term: oscillates at −2f\_c. The LPF removes it.~~

~~What survives is 2W × ½ × sinc × the phase:~~

~~h(t) = a e^(−j2π f\_c τ) W sinc(W(t − τ))~~

~~Sum over the two paths to get the same result as Route A. The ½ from splitting the cosine cancels the 2 in 2W, so the lowpass sinc has height W.~~

## Plugging in, and the link to 4d

With the numbers in, path 1 gets phase factor +1 and path 2 gets −1, so h(t) = 0.2 W sinc(W(t − 200 ns)) − 0.1 W sinc(W(t − 350 ns)), with W = 5 MHz.

| Path | a\_k | τ\_k | f\_c τ\_k (cycles) | Fractional part | e^(−j2π f\_c τ\_k) |
| --- | --- | --- | --- | --- | --- |
| 1 | 0.2 | 200 ns | 490 | 0 | +1 |
| 2 | 0.1 | 350 ns | 857.5 | 0.5 | e^(−jπ) = −1 |

**About the "≃ δ" line in the solution.** W sinc(Wt) has area 1, and it approaches δ(t) as W grows. The solution writes h(t) ≃ 0.2 δ(t − 200 ns) − 0.1 δ(t − 350 ns) "passed through the W/2 lowpass" as shorthand for the sinc form above. The sinc form is the exact answer.

**Into 4d, the same way you did Problem 1.** Sample with h\[n\] = T · h(nT), where T = 1/W = 200 ns, so TW = 1:

$$
T\cdot W\,\mathrm{sinc}\big(W(nT-\tau_k)\big)=\mathrm{sinc}\!\left(n-\frac{\tau_k}{T}\right)
\quad\Rightarrow\quad
h[n]=0.2\,\mathrm{sinc}(n-1)-0.1\,\mathrm{sinc}(n-1.75)
$$

sinc(n − 1) = δ\[n − 1\], which matches the boxed 4d answer.

**On the exam:** whenever h\_c(t) = Σ a\_k δ(t − τ\_k), the baseband h(t) has three parts per path.

1. Keep the gain a\_k.
2. Multiply by e^(−j2π f\_c τ\_k), reducing f\_c τ\_k mod 1 to get the angle.
3. Turn δ(t − τ\_k) into W sinc(W(t − τ\_k)): the same delay, now band-limited.
