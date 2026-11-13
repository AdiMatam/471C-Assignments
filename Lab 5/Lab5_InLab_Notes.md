# Lab 5 In-Lab Notes (raw data)

Settings: TX/RX 4 MS/s, oversample 20 → $1/T = 200$ kHz, $T = 5\,\mu s$; $N_t = 22$; channel est. length 2; equalizer length 4; capture 2 ms; Correct Frequency Offset = TRUE. Carrier = 915 MHz.

## Q1 — Inherent offset (TX = RX = 915 MHz)

| Run | Freq. offset (Hz) |
|---|---|
| 1 | 2.05004 |
| 2 | 6.9894 |
| 3 | -2.51126 |
| 4 | -2.8157 |
| 5 | -4.38263 |

Mean ≈ **−0.13 Hz**, std ≈ 4.6 Hz → effectively **0 Hz**; scatter is estimation noise. Suggests TX/RX share a reference clock (same USRP / shared reference / loopback) — confirm setup and note in report.

## Q2 — Moose range

$f_M = \frac{1}{2 T N_t} = \frac{1}{2 \cdot 5\,\mu s \cdot 22} \approx 4.545$ kHz → range ≈ ±4.55 kHz.

## Q3 — TX carrier for $0.8 f_M$

$0.8 f_M \approx 3636$ Hz; inherent ≈ 0 → **TX = 915.003636 MHz**, RX = 915 MHz.

## Observations for Q4

- TX = 915.002825 MHz (+2825 Hz, ≈ 0.62 $f_M$): estimate ≈ **2478 Hz ± 50 Hz** (~20 runs) — ~350 Hz low. Estimate already degrading as correlator timing becomes less reliable.
- TX = 915.003636 MHz (0.8 $f_M$): constellation **scattered uniformly — no QPSK clusters** (`messed_up_constellation.png`). Screenshot run: freq. offset = **254.85 Hz** (other runs ~3314 Hz → estimate unstable/garbage), SNR = **−12.2 dB**, BER = **0.516**, average BER = **0.506** (≈ random guessing). Channel estimate ≈ 0 (−0.005, −0.0004). "Packet Detected" still lit → detector *declares* a frame but at the wrong timing, so Moose / channel est. / equalizer all run on wrong samples.

## Section 3.2 — Self-referenced sync (same TX = 915.003636 MHz)

Method: **"Self Reference w/ Power Normalization"** (enum options: Sliding Correlator / Self Ref with Power Normalization / Windowing). Screenshot: `self_ref_constellation.png`.

- Constellation: **4 clean QPSK clusters** at $(\pm0.7, \pm0.7)$.
- Freq. offset = **3615.99 Hz** (vs. 3636 Hz applied; ~0.5% error).
- SNR = **8.13 dB**; BER = **0**; average BER = **0** (20 iterations).
- Frame offset = 970; delay = 2.225e-4 s.

| | Sliding Correlator | Self Ref w/ Power Norm. |
|---|---|---|
| Freq. estimate | 254.85 Hz (unstable) | 3615.99 Hz |
| SNR | −12.2 dB | 8.13 dB |
| Avg BER | 0.506 | 0 |
| Constellation | uniform scatter | 4 clean clusters |

→ Section 3.3 demo items 2 & 3 demonstrated.

## Pitfall (for "problems encountered")

- Initially read the `offset` field on `top_rx` (stable 810–811) as frequency offset; it is the **frame offset** (sample index of detected frame). Correct field is the freq. offset indicator.
