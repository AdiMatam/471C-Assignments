# Lab 3 — Pre-Lab Submission

## Symbol Timing Recovery Questions

**1. Show that in the absence of noise, α and φ in Eq. (2) have no impact on the maximum output energy solution.**

After matched filtering, with no noise,

```
y(nT + τ) = α e^{jφ} sqrt(Ex) Σ_m s[m] g((n-m)T + τ - τd)
```

With zero-mean, uncorrelated symbols of unit energy, `E|s[m]|^2 = 1`, so

```
J(τ) = E|y(nT + τ)|^2 = |α e^{jφ}|^2 · Ex · Σ_m |g(mT + τ - τd)|^2
     = α^2 · Ex · Σ_m |g(mT + τ - τd)|^2        
```

- φ drops out because `|e^{jφ}| = 1`.

**2. What are the two critical assumptions used to formulate the indirect maximization of the output energy? How can flat fading / AWGN impact the method, and how might you mitigate this with parameter selection?**

Assumptions:

1. Expectation and derivative can be interchanged where expectation is replaced by time average over P symbols.
2. Derivative can be approximated as first order 'center' point difference (like finite differncing method): `d/dτ y*(nT+τ) ≈ y*(nT+τ+δ) - y*(nT+τ-δ)`

Impact of the channel:

- AWGN adds a random term to every sample, so the time-averaged statistic `J_δ[k]` is a noisy estimate.
- Flat fading (attenuation α) scales the useful part of `J_δ[k]` by `α^2` while noise is unchanged, which lowers the effective SNR of the statistic

Mitigation via parameters:

- Increase P to average over more symbols which should ideally approach true expectation.
- Choose δ | M to correct for noise. Too small of a δ increases suspectability to high frequency noise in the signal (due to the nature of a finite time derivative). Large values of M (upsampling factor) allow you to choose a smaller δ, however... allowing for a more fine derivative estimate.

**3. After downsampling a sequence originally sampled at rate 1/Tz by a factor M, what is the sample period of the resulting signal?**

The new sample period is **M · Tz**.

## Timing Error Statistic ε(N)

Ts was held constant across the sweep by scaling the RX sample rate with N. 
	Ts = 7.2 µs (TX oversample 4, TX sample rate 0.5556M, delay 2.448 µs)
	 RX sample rate = N × 0.13889M). 
	 N = 14 has no valid sample-rate pair with Ts=7.2 µs, so used Ts = 7.28 µs with (TX 0.5495M, RX 1.9231M, delay 2.475 µs). Roughly comparable.

![[Lab3_timing_error.png]]

| N   | Max Energy                     | Early-Late Gate |
| --- | ------------------------------ | --------------- |
| 2   | 0.025600                       | 0.115600        |
| 4   | 0.008900                       | 0.008637        |
| 6   | 0.000044                       | 0.009172        |
| 8   | 0.002334                       | 0.007722        |
| 10  | 0.001720                       | 0.002540        |
| 12  | 0.000044 / 0.002120 (two runs) | 0.004183        |
| 14  | 0.000295                       | 0.002918        |
| 16  | 0.001174                       | 0.001742        |
| 18  | 0.000133                       | 0.001309        |
| 20  | 0.000528                       | 0.001675        |

**Observations**

- **Trend:** ε falls as N grows for both algorithms, because the estimator can only choose one of N sample phases per symbol. Curve is not smooth because 0.34\*Ts does not fall exactly as a multiple 1/N.
- **Max Energy vs Early-Late Gate:** Max Energy is lower than Early-Late Gate at almost every N except N=4. Expected that this was a specific random case (non-deterministic output). EL Gate is way more sensitive to random data due to the finite-diff derivative described above.


