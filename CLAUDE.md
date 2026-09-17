# 471C-Assignments — Context

EE 471C / EE 38K-17 Wireless Communications Lab. Hardware: **NI USRP-2901** SDR, LabVIEW-based labs.
Reference manual (not in repo): `~/Downloads/DWC-USRP - Student Lab Manual.pdf` — pages ~1-25 cover Lab 1 Parts 1 & 2.

## Lab 1, Part 1 — BER simulation (source.vi / error_detect.vi)
- `source.vi`, `error_detect.vi` — completed student VIs (filled in from `student_source.vit` / `student_error_detect.vit` templates).
- `awgn_simple_sim.vi` — simulator; `digital_comm.llb`, `control_type_defs.llb` — support subVI libs.
- BPSK, signal power = 1, ran 10^4 iterations per N0 point, N0 from -10 to 0 dB in 2 dB steps.
- `results.txt` — raw results, one line each: `N0_dB, BER`.
- `plot_ber.py` — reads `results.txt`, plots BER (log y) vs 1/N0 in dB (= -N0_dB, linear x), alpha=0.5 grid. Outputs `ber_plot.png`.
- `Lab1_Part2_PreLab_Answers.md` — pre-lab answers for this part.

## Lab 1, Part 2 — Intro to NI RF Hardware
- `sine_generation.vi`, `receiver.vi` — TX sine-gen and RX continuous IQ acquisition VIs built in-lab.
- `wcl_RF1.0.llb` — provided RF library containing `RXRF_config.vi`, `RXRF_init.vi`, `RXRF_recv.vi`, `TXRF_init.vi`, `TXRF_send.vi`, `RXRF_trigger_and_capture.vi`, `TXRF_prepare_for_transmit.vi`.
- Key fact: USRP IQ rate must be an integer decimation of the fixed 100 MS/s ADC rate (effective range 200 kS/s–25 MS/s); unsupported requests get coerced to nearest valid rate, reported via `niUSRP Configure Signal.vi`'s coerced-rate output.
- `lab1_questions.txt` — scratch answers (USRP ID: NI2901, etc.).

## Lab report
- `EE471C_Lab1_Report.md` — main write-up, in progress. Section 3.1–3.3 answered; images `IMG_8430.png` (obstructed) / `IMG_8431.png` (unobstructed) inlined in 3.1. Concluding questions (1-5, end of doc) **not yet answered**.

## HW1
- `EE471C_HW1_Fa26.pdf` — assignment; `EE471C_HW1_Fa26_Ans.md` — answers (device comparison, carrier comparison, 6G exploration, closing discussion question).
- **Open item:** closing "Exploration Question" is being reworded to a Starlink/satellite-comms theme (user's interest). Candidate phrasing proposed in chat, not yet finalized or written into the doc — confirm choice and insert next session.

## Misc
- `.obsidian/` — Obsidian vault config, not lab content.
