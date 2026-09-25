# Part 1 — Pre-Lab Submission

## PSK Modulation Questions

**1. PSK is a constant envelope modulation scheme, meaning all symbols have equal energy after modulation. What is the energy of the BPSK and QPSK modulated symbols shown in Tables 1(a) and 1(b) respectively?**

- BPSK, `|+1|^2 = |-1|^2 = 1` → **energy = 1** (same for both symbols)
- QPSK, `|1+j|^2 = 1^2+1^2 = 2` → **energy = 2** (same for all symbols because all have real and complex magnitudes of 1)

**2. In `modulate.vi`, what should be the default value for the Symbol Energy of the modulated sequence?**

**1** -> which is unit energy. Constellation is already normalized to "unit avg" so leaving Symbol Energy=1 means `modulate.vi` will output the normalized constellation points.

**3. Consider a uniformly distributed random bit stream `{b_n}` that is BPSK modulated so each symbol has energy `Es`. In an AWGN channel, what is the average probability of bit error as a function of SNR using ML estimation? (Noise is real Gaussian, `N(0, N0/2)`.)**

Model: `y = sqrt(Es)*s + v`
`s` can be +1 or -1. 
`v` is distribution given `N(0, N0/2)`

Error occurs when, say, s=+1 is sent but y < 0 or v < -sqrt(Es) is detected.

```
P(error | s=+1) = P(v < -sqrt(Es)) = Q( sqrt(2*Es/N0) )
```

Same holds for s=-1 because the BPSK scheme is symmetric
Average BER is then `Q( sqrt(2*Es/N0) )` . 

Can express SNR as Es / N0, **so average BER: `Q(sqrt(2*SNR))`** -- for the BPSK case.

## BER Curve for QPSK and BPSK

![[Lab2_BER_PLOT.png|542]]
***Ran 1000 iterations on packet length=500 bits***
Error rate for BPSK falls off faster than that for QPSK (by factor of sqrt(2)).

# Part 2 — Pre-Lab Submission

## Pulse Shaping and Matched Filtering Questions

**1. `MT Generate Filter Coefficients.vi` requires an input for the number of pulse shaping samples per symbol — the oversample factor used to design the filter. When using this VI in `pulse_shaping.vi`, where do you obtain this parameter from? Give any relevant cluster names and/or variable names.**

The oversampling factor comes from the `modulation parameters in` struct. Unbundled it to yield (among other fields) `pulse shaping parameters` and `TX oversample factor`, the latter is wired into MT Generate Filter Coefficients VI.

**2. Impairments visible in the eye diagram can occur at many places along the communication path (source to sink). What are some of the places where impairments visible in the eye diagram might occur (name at least three)?**

- **The channel itself**: AWGN closes the eye vertically, blurring the lines/plots. 
- **Receiver timing/symbol synchronization**: a sampling offset (or clock inconsistency over time) might show up as smaller eye opening.
- **Receiver matched filtering**: if `g_rx[n]` isn't truly matched to `g_tx[n]` (bad match filter), might see aliasing

**3. When using inconsistent sampling rates at the transmitter and receiver, the symbol rate `1/Ts` must remain constant.**

**(a) In terms of the sampling rates at the transmitter and receiver (`1/T_M` and `1/T_N` respectively), what is the relation between the oversample factor at the transmitter (`M`) and receiver (`N`)?**

  ```
T = M · T_M (taking M samples per symbol and T_M is time per symbol)
T = N · T_N  
  ```

Setting the two equations equal to each other, arrive at `M/N = T_N/T_M`
So, `M/N` is really just the ratio of the transmitter's sampling rate to receiver sampling rate.

**(b) What can you say about the type of number the ratio `T_M/T_N` (the ratio of the receiver's sampling rate to the transmitter's) must be?**

`T_M/T_N = N/M`. Since `M` and `N` must both be positive integers, `T_M/T_N` must be a **rational number.** Not necessarily an integer though.
