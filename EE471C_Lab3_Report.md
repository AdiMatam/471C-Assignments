# EE471C Lab 3 — Symbol Timing Recovery (Report)

Setup: QPSK, packet length = 500 bits, Root Raised Cosine (α = 0.5, filter length = 8), channel h = 0.75e^{jπ/4}, noise power = −Inf dB, TX sample rate = 20 MSamp/s, TX oversample factor = 20, RX sample rate = 2 MSamp/s, RX oversample factor = 2, symbol timing recovery = Max Energy, capture time = 400 µs.

## In-Lab Questions

**1. What is the symbol rate of the system based on the parameters above?**

Symbol rate = TX sample rate / TX oversample factor = 20 MSamp/s ÷ 20 = 1 MSymbol/s,
QPSK carreis 2 bits per symbol, so actual **bit** **rate** is 2Mbit/s

**2. Vary the oversample factor N at the receiver. Observe the received constellation for N = 2, 4, 10 and 20. Describe how the relationship between sampling error and oversample factor N shows up on the signal constellation of `top_rx.vi`.**

The receiver can only choose its sampling instant from N phases per symbol. An error in sampling would appear as an output (from matched filter) being away from the pulse peak (resulting in spectral leakage across symbols). 

This looks like overlapping cluster regions on the QPSK constellation map. The leaking/smearing shrank as N increases:

- **N = 2:** largest possible leftover error (up to ±0.25 Ts), so the clusters are the most spread out and may overlap, which risks symbol errors. 
- **N = 4:** error up to ±0.125 Ts; clusters visibly tighter.
- **N = 10:** error up to ±0.05 Ts; clusters tight. 
- **N = 20:** error up to ±0.025 Ts; four small, tight clusters close to the ideal points, nearly points not even clusters.

**3. For each of the oversample factors in the previous question, what value did you set the RX sample rate to on the front panel of `top_rx.vi`?**

The symbol rate has to stay at 1 MSymbol/s, so RX sample rate = N × 1 MSamp/s:

| RX oversample factor N | RX sample rate |
|---|---|
| 2 | 2 MSamp/s |
| 4 | 4 MSamp/s |
| 10 | 10 MSamp/s |
| 20 | 20 MSamp/s |


---

## Directions for Lab Submission

**2. Discuss any problems you encountered and how you overcame them.**

- Shifting the waveform the wrong way. `Rotate 1D Array` rotates to the right for a positive count. The waveform has to be advanced by k_hat, so the count must be shifted by negative k_hat. Initially wired in reverse, so just needed a negate block.
- Keeping Ts fixed in the simulator. The USRP/simulator sample rates are offered at discrete values (because of how the decimators work). So couldn't get a trivial match for my initial setting of Ts=1 microsecond. For prelab, used Ts = 7.2 µs (valid for N = 2–12, 16, 18, 20) and Ts = 7.28 µs for N = 14, changing the delay to keep it at the specified 0.34\*Ts.

**3. What underlying assumption about the noise in the system has been made, but not stated explicitly in this lab? Why is it important for the maximum output energy problem?**

The noise is assumed to be white (equal across frequecn yband), zero-mean, and independent across symbols (stationary). 

This allows us to conclude that noise contributes the same σv² for every time step -- cross terms between signal and noise average to zero because noise is presumably WSS.

If the noise were colored or non-stationary or correlated with the actual signal, noise term could vary with time -- masking over the peak energy output and making it harder to selectively filter out.

**4. Air any grievances about the structure, content, or workload of this lab.**
- The manual seemed somewhat contradictory in the EL gate section because Table 2 talks about minimizing and the text says maximizing. Although I might be contextualizing it wrong.
