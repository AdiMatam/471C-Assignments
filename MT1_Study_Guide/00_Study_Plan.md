# EE 471C — Midterm 1 Study Plan

**Exam: Mon Oct 19, 2026.** Written from the Canvas material in `MT1 Snapshot/` plus Labs 1–3 and HW1–3. Syllabus: *"two midterm exams based on topics covered in the lecture and the lab."*
Closed-note, no formula sheet (maybe a few generic hard-to-memorize formulas supplied — don't count on it).

> **Honesty note on sources.** The slide PDFs lose most equations in text extraction, so the derivations in these guides are rebuilt from the slide structure + the standard textbook (Heath, *Digital Wireless Communication*) + your HW2 solutions. Where lecture conventions matter (e.g. the √2 in up/down-conversion) I follow *your* HW2 solution/lecture figures. If a guide disagrees with your notes or a graded solution, **trust the graded solution** and tell me.
>
> `SignalProcessingFundamentals.pdf` is now included (folded into guide 02). The Oct 14 lecture ends at SC-FDE; OFDM proper is only introduced, and the *Oct 21* material (comparison, OFDM channel estimation, CFO/Moose) is **after** the exam.

## Files in this folder (in the order the material was taught)

| # | File | Canvas source | Weight |
|---|------|---------------|--------|
| 01 | `01_Big_Picture_and_Information.md` | Comms System Overview, entropy, Practice1, Introduction | Light–medium |
| 02 | `02_Math_Toolkit.md` | Probability_RandomVariables, SignalProcessingFundamentals, BandlimitedSignals, Class Questions | **Heavy** |
| 03 | `03_Passband_Baseband_Channels.md` | BandlimitedSignals (2nd half), PulseAmpModulation (1st half) | **Heavy** |
| 04 | `04_PAM_Constellations_AWGN.md` | PulseAmpModulation (2nd half), AWGNPulseShaping (1st half) | **Heavy** |
| 05 | `05_Pulse_Shaping_Matched_Filter_Multirate.md` | AWGNPulseShaping, FilterImplementation, DigitalFilterImplementation | **Heavy** |
| 06 | `06_ML_Detection_and_BER.md` | DigitalFilterImplementation (2nd half) | **Heavy** |
| 07 | `07_Synchronization_and_Flat_Channel_Estimation.md` | Lecture 10_WCLab, Frame_Synchronization | Medium–heavy |
| 08 | `08_Frequency_Selective_Equalization_SCFDE.md` | Freq_Selective_Channel | Medium–heavy |
| 09 | `09_Formula_Sheet.md` | everything | Memorize this |

Each guide has: **why it matters → concepts built from the ground up → worked examples → traps → self-test → lab link.**

## 📌 Scope update (from your instructor): Midterm 1 = what the homeworks cover
Nothing beyond what HW1–HW3 touch will be tested (lecture/PDF material not yet in a homework is out). Homework ≠ exact mirror of the exam, so know the *method*, not just the posted numbers. Nothing was deleted from the guides — they're tagged with 📌 instead.

| Guide | Homework link | Priority for MT1 |
|---|---|---|
| 02 Math toolkit | HW2 Q1 (DT equivalent channel), HW2 Q2 (PSD), HW3 Q1 (bandwidths, sampling, DT covariance/PSD) | 🟢 **High** (Parts C–D especially; Parts A–B = prerequisites) |
| 03 Passband/baseband | HW2 Q3, HW3 Q2 (full channel chain $h_c\to h_p\to h\to h[n]$) | 🟢 **Highest** |
| 04 Constellations | HW2 Q4, HW3 Q3 (zero-mean + normalize) | 🟢 **Highest** (Section 2); sections 3–4 prerequisite-level |
| 01 Big picture | HW1 only (research: devices, carriers, 6G) | 🟡 Background / low |
| 05 Pulse shaping | none | ⚪ Likely out of scope (skim) |
| 06 ML & BER | none (labs only) | ⚪ Likely out (cheap to remember BPSK BER) |
| 07 Synchronization | none (Lab 3 only) | ⚪ Likely out |
| 08 Equalization / SC-FDE | none | ⚪ Likely out |

**Revised plan:** spend most of the time on guides 02 → 03 → 04 (and redo HW2 Q1–Q4 and HW3 Q1–Q3 blind, twice, changing the numbers each time). That's a realistic two-day job; guides 05–08 become optional reading if you finish early. The original day-by-day schedule below still works if you want the full course.

## Where the exam questions will probably come from
The instructor's own words (syllabus): *"all chapters include many examples, which are taken from past homework and exam problems."* So:
1. **HW1–HW3 problems are the best predictor** (they're literally the template). Redo them blind.
2. The "Example" slides in each lecture (discrete-time equivalent channel, 100 m channel example, normalize a constellation, SNR at the front end, M-QAM union bound, 4-PAM timing, LS equalizer).
3. `Practice1.pdf` (multiple-choice, big-picture) and `Class Questions.pdf` (entropy, BPSK waveform, triangle FT, IFT, uniform RV, MA process).
4. Lab-derived: BPSK vs QPSK BER, eye diagrams / pulse shaping, timing offset recovery (MOE).

## Time plan (compressed — exam is in ~2 days)
Assume you're fully restarting, so the first pass is *understanding*, the second is *doing without notes*.

**Sat Oct 17 (today) — foundations**
- 01 (45 min), 02 (2.5 h: probability + random processes + sampling + PSD/bandwidth), 03 (2 h: complex envelope + baseband equivalent channel).
- End of day: redo **Class Questions 1–6** and **HW2 Q1–Q3** blind.

**Sun Oct 18 — the core of the exam**
- 04 (1.5 h), 05 (2.5 h incl. the multirate identities — draw them yourself), 06 (2 h).
- End of day: redo **HW3 Q1–Q3** and **HW2 Q4** blind; compute BPSK/QPSK BER by hand; derive matched filter from Cauchy–Schwarz without notes.

**Mon Oct 19 (exam evening) — second half + consolidation**
- Morning: 07 (1.5 h) and 08 (2 h).
- Afternoon: `09_Formula_Sheet.md` — write it from memory on blank paper, compare, repeat. Timed mini-mock (see below).
- Don't learn new material in the last 2 hours.

## Suggested priority if time gets short (we'll trim once you're in it)
1. Baseband equivalent channel & discrete-time equivalent channel (HW2/HW3 repeat this)
2. Constellation mean/energy/normalization
3. PSD + bandwidth definitions; sampling
4. Matched filter ⇒ Nyquist/RC/SRRC; excess bandwidth
5. ML detection, Voronoi, Q-function BER (BPSK/QPSK)
6. Multirate Tx/Rx
7. Timing offset / MOE; frame sync correlator
8. LS channel estimation; LS equalizer; CP + DFT equalization
9. Entropy/Shannon big picture (cheap points — don't skip!)

## Timed mini-mock (do on Monday, 60 min, closed notes)
1. Entropy of a 4-ary source with given probabilities. (5 min)
2. Passband channel `h_c(t)=Σ aₖδ(t−τₖ)` with `fc`, `W` → `h_p`, `h(t)`, `h[n]`. (15 min)
3. Normalize a given constellation (mean → energy → scale). (8 min)
4. 3-dB bandwidth + fractional-power bandwidth of an exponential-covariance process. (10 min)
5. QPSK/BPSK BER expression in terms of Es/N0 and Q; explain the 3 dB gap. (7 min)
6. Raised-cosine: bandwidth for given symbol rate and α; sample rate; samples per symbol. (5 min)
7. Short answers: why matched filter? what does a timing offset do to the eye? what does a cyclic prefix do? (10 min)

## How I suggest we use the next session
- Tell me which guide feels shakiest and I'll build a **problem set with worked solutions** for it.
- Tell me what to cut (e.g. entropy depth, polyphase details) once you've been through the first pass.
- I can quiz you interactively, one question at a time.
