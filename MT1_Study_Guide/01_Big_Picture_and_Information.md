# 01 — Big Picture & Information (Weeks 1–2)

*Sources: Comms System Overview, entropy.pdf (Shannon 1948), Practice1.pdf, Introduction.pdf, Class Question 1.*

> 📌 **Homework scope:** HW1 was research-only (device/carrier comparison, 6G); nothing here appeared in HW2/HW3. Per your instructor the exam sticks to homework-covered concepts, so treat this guide as **background / low priority** (the HW1 context: standards, bands, data rates). Entropy and Practice1 were in-class only.

## Why this matters
These are the cheapest points on the exam (multiple-choice / short answer / one entropy calculation), and the block diagram is the **map** for the whole course — every later topic is "block X of this diagram".

## 1. What "communication" is
Shannon: *the fundamental problem of communication is reproducing at one point, exactly or approximately, a message selected at another point.*

- **Transmitter → channel → receiver.** The channel includes analog circuitry *and* the propagation medium.
- **Analog vs digital: the only difference is the *source*.** Analog: the source $m(t)$ is a continuous-time waveform. Digital: the source is a bit sequence $b[n]$. **Both ultimately transmit a continuous-time electromagnetic wave** (Practice Q9: True). Digital ≠ "no analog hardware" and ≠ "wired vs wireless".

## 2. The digital communication chain (memorize the order)

```
TX: Source → Source coding → Encryption → Channel coding → Modulation → Analog processing → [Propagation medium]
RX: Sink   ← Source decoding ← Decryption ← Channel decoding ← Demodulation ← Analog processing ←
```
(Practice Q10 answer: **Source coding → Channel coding → Modulation**; encryption sits between source and channel coding.)

| Block | Job | Key idea |
|---|---|---|
| Source coding | **Compress** — remove redundancy | Limit = entropy of the source |
| Encryption | Secrecy | not about errors |
| Channel coding | **Add structured redundancy** to fight errors | rate $k/n$: rate-½ ⇒ 1 info bit → 2 coded bits |
| Modulation | **Bits → waveform** (symbols → pulses) | this course's focus |
| Demodulation | Recover info from received signal | detection |
| Analog processing | DAC, mixer/upconversion, PA, antennas, LNA | impairments (noise, CFO) live here |

Channel impairments (all of the above are true — Practice Q7 "all of the above"): **path loss, multipath, thermal noise**, plus frequency/timing offsets, interference.
**SDRs** (USRP) are attractive because **they're reconfigured in software** (Practice Q8), not because they have no analog front-end or antenna.

## 3. Entropy — the math behind source coding
For a discrete source with symbol probabilities $p_i$:

$$H(X) = -\sum_i p_i \log_2 p_i \quad \text{bits/symbol}$$

- Self-information of one outcome: $-\log_2 p_i$ (rare events carry more information).
- $0 \le H \le \log_2 M$; **max = $\log_2 M$ when all $M$ symbols are equally likely**; $H=0$ if one symbol is certain.
- **Source coding theorem (intuition):** you cannot compress below $H$ bits/symbol on average without loss; Huffman-type codes approach it (give short codewords to likely symbols).
- Why $\log$? Shannon: it's additive (two independent sources → entropies add), matches engineering intuition (N relays → N bits), and is mathematically convenient. Base 2 → "bits" (a term credited to Tukey).
- **Channel capacity** (Shannon, same paper, noisy-channel theorem): reliable communication is possible at any rate below capacity $C$; for the AWGN channel $C = B\log_2(1+\text{SNR})$ bits/s. Know it exists and what it says (the *ultimate* limit); detailed proofs are not course material.

### Worked example (Class Question 1)
Source $\{a,b,c,d\}$ with $P(a)=P(b)=P(d)=\tfrac18$, $P(c)=\tfrac12$ (as printed on `Class Questions.pdf`).

> ⚠️ **Flag:** those four probabilities sum to **7/8**, not 1, so the printed problem has a typo (likely $P(d)=\tfrac14$). Check your own notes for the intended values. The method is what the exam tests: plug into $H=-\sum p\log_2 p$.

- **As printed** (formula applied literally): $H = 3\cdot\tfrac18\cdot3 + \tfrac12\cdot1 = \tfrac{13}{8} = 1.625$ bits.
- **With the likely fix** $\{\tfrac18,\tfrac18,\tfrac12,\tfrac14\}$: $H = 2\cdot\tfrac18\cdot3 + \tfrac12\cdot1 + \tfrac14\cdot2 = 0.75+0.5+0.5 = 1.75$ bits/symbol.

Either way $H<2$, so a fixed 2-bit/symbol code wastes bits. For the fixed distribution, a Huffman code with lengths $c:1,\ d:2,\ a:3,\ b:3$ averages $0.5+0.5+0.375+0.375=1.75$ bits — exactly $H$, because every probability is a power of ½.

## 3b. The rest of the overview deck (block by block)

### Why digital?
Suitable for digital data; reproducible high-quality digital components (analog parts vary in spec and give continuous outputs, digital is robust thanks to discrete levels); easier **security**; **more robust to noise**; easy to support **multiple rates** and **multiple users**; easy to **reconfigure (SDR)**; **compression is simpler**; **DSP rides Moore's law** (lower power and cost) while analog components advance more slowly. Digital still uses a **finite set of waveforms** (e.g. BPSK with a rectangular pulse: "0"→$+1$ pulse, "1"→$-1$ pulse).

### Source coding
- Purpose: **compression**. **Lossless** (e.g. zip: perfect reconstruction) vs **lossy** (e.g. JPEG: reconstruction is approximate — the overview slide lists "perfect reconstruction" for lossless only; lossy gives a close copy).
- Entropy = amount of information per message = **average codeword length of the best possible lossless compressor**; it measures the efficiency of a source coding algorithm. For a binary source $H=-p_1\log_2p_1-p_2\log_2p_2$ (max 1 bit at $p=\tfrac12$).
- Example pipeline (JPEG): 8×8 blocks → DCT → quantizer → entropy encoder, with table specifications; decoder is the reverse.

### Encryption / decryption (what was covered)
- **Encryption:** convert information into something hard for an unintended recipient to understand; a component of a **security protocol**; typically needs a **key exchange**. **Decryption** removes it so the decoded signal is readable. (Lab link: `top_tx.vi` passes the key bit sequence to `top_rx.vi` through a queue — the Lab 2 concluding question.)
- **Secret-key (symmetric):** one key used for both encryption and decryption.
 - **Block ciphers:** encrypt data block by block — used in **3G and 4G**.
 - **Stream ciphers:** generate a **pseudorandom key stream that is bitwise XORed with the data** — used in **IEEE 802.11 and Bluetooth**. (XOR with the same stream decrypts: $b\oplus k\oplus k=b$.)
- **Public-key (asymmetric):** a **pair of keys**, public (freely distributed) and private (secret). Data encrypted with the **public** key can only be decrypted with the corresponding **private** key (confidentiality). Data encrypted with the **private** key can only be decrypted with the **public** key — this is **signing**: it proves the sender is who they claim to be.
- Position in the chain: after source coding, before channel coding. It is *not* an error-control block (Practice Q3).

### Channel coding / FEC
- Idea: **add known redundancy to correct (or detect) channel errors**. **Code rate** $=\dfrac{\#\text{uncoded bits}}{\#\text{coded bits}}$; repetition code rate $\tfrac13$: $0110\to000\,111\,111\,000$.
- **Error detection** (e.g. **CRC**, used in almost every protocol) vs **error correction** (FEC / ECC).
- **Block codes** (1950s): $k$ bits in, $n$ out (a rate-½ length-5 block code: 5 in, 10 out); CRC; **Reed–Solomon** (xDSL, DVB-S/S2, 802.11ad).
- **Convolutional codes:** convolve data with several FIR filters in the binary field and interleave outputs. Constraint length $v$; used in GSM, WCDMA, 802.11a/b/g/n/ac/ad. Example (5,7) rate ½: $c[2n]=i[n]\oplus i[n-1]\ldots$ (memory of 2 bits). **Decoding: Viterbi** (finds the sequence closest to the observation).
- **Trellis codes** (1980s): convolutional + explicit symbol mapping (combine coding and modulation), ATSC HDTV, Viterbi.
- **Turbo codes** (1993): convolutional with IIR filters + deep random interleaver, iterative MAP decoder, needs large blocks (~10,000), used in 3G WCDMA and **4G LTE**.
- **LDPC** (1960s, rediscovered 2000s): large block code, iterative MAP-type decoder, ~1,000-bit blocks, more complex decoding; 802.11ad.

### Modulation & demodulation
- Modulation maps bits to analog waveforms (linear/nonlinear; memoryless/with memory). **Baseband:** bits → symbol mapping (constellation, cardinality $M=2^{\text{bits/symbol}}$) → pulse train → pulse-shaping filter → $x(t)$. **Passband:** amplitude, phase or frequency of an RF carrier varies with the information: **ASK, PSK, FSK, M-QAM**.
- Demodulator: uses received samples to detect the transmitted sequence; may use a channel estimate, equalization, detection, memory. **Basic demod = matched filter (collects the energy of the whole symbol while minimizing noise) sampled at $t=kT$ → detector (an "educated guess")** — foreshadows Blocks 05–06.
- **Hard decision:** each coded bit is sliced to 0/1 using only the received sample (e.g. received $-0.2$ with $0\to+1$, $1\to-1$ ⇒ bit 1). **Soft decision:** decide by **distance** between the received sequence and each candidate codeword (e.g. repetition codeword $(1,1,1)$ vs $(-1,-1,-1)$ for received $(1,0.5,-0.5)$: distances $2.5$ vs $6.5$ ⇒ decide 0); used for sequence detection **with FEC** (better performance).

### Analog front end (AFE) and channel impairments
- AFE: band selection, LNA, mixing; e.g. **superheterodyne receiver** (mix with LO to an IF, channel selection, then I/Q mixing with $\cos/\sin$ at $f_{IF}$ and LPFs to get $I$ and $Q$). Includes all analog and mixed-signal processing.
- The "**channel**" in a model is the *combined* effect of analog processing + propagation (or just part of it).
- **Additive noise** (thermal motion of electrons; added in the AFE, small but not relative to the attenuated signal); **SNR = signal power / noise power**.
- **Path loss:** degradation of received signal with distance (and frequency: 5 GHz loses more than 2.4 GHz).
- **Multipath:** paths with gains $h_0,h_1,h_2$ and distances $d_0,d_1,d_2$ (delay $d_k/c$) plus noise $v(t)$ — modeled as an LTI system.
- **Cochannel interference** (frequency reuse) and **adjacent-channel interference** (spectral leakage; worse when the neighbor is strong/close).
- Practical TX/RX diagram example: **OFDM PHY of IEEE 802.11a** — digital modulation → analog processing → channel → analog processing → digital demodulation.

## 4. Practice1 — all answers with reasons
1. **B** digital = digital *source*.  2. **B** source encoder compresses.  3. **C** channel coding adds redundancy.  4. **B** rate ½: one info bit → two coded bits.  5. **C** modulator maps bits → analog waveforms.  6. **A** demod recovers info.  7. **D** all impairments.  8. **B** reconfigurable in software.  9. **True**.  10. Source coding → Channel coding → Modulation.

## 5. Course framing from `Introduction.pdf`
- Approach: **DSP view** — wireless signals are bandlimited, so by Nyquist the continuous channel can be treated as a **discrete-time LTI system**, transmitted/received signals as sequences. (This is why Block 02/03 exists.)
- Learning goals that map to exam topics: BER of BPSK/QPSK; pulse shaping ↔ sampling; excess bandwidth of raised cosine; sampled channel impulse response; training/estimation of frequency-selective channel; synchronization; equalization via SC-FDE/OFDM; cyclic prefix vs zero padding.

## Self-test
1. Name the TX blocks in order and what each does in one phrase.
2. Why does adding *redundancy* (channel coding) help while *removing* it (source coding) is also good? (Different redundancy: source redundancy is statistical/useless; channel redundancy is structured and designed to fight noise.)
3. For $M$ equiprobable symbols, what's $H$? (Maximum, $\log_2 M$.)
4. Compute $H$ for $\{1/2,1/4,1/8,1/8\}$ (=1.75 bits).

## Lab link
Lab 1's `source.vi`/`error_detect.vi` = the "source" and the BER-measuring "sink". BER vs SNR is the performance measure for the whole chain.
