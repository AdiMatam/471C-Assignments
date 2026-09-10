# Lab 1, Part 2 — Pre-Lab Answers (NI USRP-2901)

*Note: the lab manual references the NI USRP-2920 / "USRP-292x" family. Our lab hardware is the NI USRP-2901, so the specs below are pulled from the official NI USRP-2901 datasheet (National Instruments, doc. 374925C-01) instead of the 2920/292x help files the manual points to.*

## USRP-specific questions

**1. What is the range of allowable carrier/center frequency supported by the NI-USRP?**

70 MHz to 6 GHz, for both the transmitter and receiver (the USRP-2901 has two local oscillators — one shared by both TX channels, one shared by both RX channels — so TX and RX can be tuned to different frequencies, but the two TX channels always share one frequency and the two RX channels always share one frequency).

**2. What is the maximum allowable bandwidth supported by the NI-USRP?**

56 MHz maximum instantaneous real-time bandwidth (same figure for TX and RX).

**3. What is the maximum sampling rate of the NI-USRP?**

The USRP-2901 doesn't publish a single fixed ADC/DAC clock rate the way the 292x's "100 MS/s ADC" spec does — instead NI specifies a maximum I/Q (complex baseband) rate that depends on mode:

| Mode | Max I/Q rate |
|---|---|
| Streaming (continuous, to/from host) | 15 MS/s |
| Burst, one channel | 61.44 MS/s |
| Burst, two channels | 30.72 MS/s |

The ADC and DAC are both 12-bit converters, and their effective rate scales with the configured I/Q sample rate. NI notes actual throughput also depends on the USB3 chipset, number of active channels, and host computer performance (and drops further, to ≤8 MS/s, over USB 2.0).

**4. Why do you think the DDC is implemented? What is its main benefit?**

The digital down converter (DDC) performs decimation — mixing the received signal to baseband and lowpass-filtering/downsampling it — entirely in the USRP's onboard FPGA rather than in software on the host PC. The benefit is twofold: (1) it lets the receiver acquire only the (typically much smaller) bandwidth of the signal of interest instead of streaming the full front-end sample rate over the host link, drastically cutting the data volume that has to cross USB/Ethernet and be stored/processed; and (2) hardware decimation is far faster and more deterministic than doing the same filtering/downsampling in software on the host, so it's done on the FPGA where it can keep up with the ADC in real time.

## General concept questions

**1. In your own words, describe what the bandwidth of an instrument is.**

Bandwidth is the width of the range of frequencies an instrument (or channel, or signal) can handle at once. For a receiver/transmitter, it's the span of frequencies over which the front end can faithfully acquire or generate a signal without significant attenuation, distortion, or aliasing — e.g., a 56 MHz instantaneous bandwidth means the USRP can capture or produce all frequency content within a 56 MHz window centered on its tuned carrier frequency in a single acquisition.

**2. What is meant by the sampling rate of an instrument?**

The sampling rate is how many discrete time-domain samples per second the instrument's ADC (on receive) or DAC (on transmit) produces/consumes. It's a rate in samples/second (or complex I/Q samples/second for a baseband-equivalent signal), and by the Nyquist theorem it must be at least twice the bandwidth of the signal being captured or generated in order to represent that signal without aliasing.

**3. Why are these specifications important for designing a transmitter and receiver in a wireless communications system?**

Bandwidth and sampling rate together bound what signals the hardware can actually create or observe. The occupied bandwidth of your modulated waveform must fit within the instrument's instantaneous bandwidth, or parts of the signal will be filtered out or aliased. Likewise, the DAC/ADC sampling rate sets the symbol rates and oversampling factors you're allowed to choose at the transmitter and receiver (per Nyquist, sample rate ≥ 2× the signal bandwidth), and it determines how much data must be streamed to/from the host per second — which is exactly why the USRP-2901's decimation (DDC) and its lower "streaming" rate versus "burst" rate matter in practice: they trade off signal bandwidth/fidelity against how much data the USB/host link and software can actually sustain continuously.

## Sources

- [USRP-2901 Specifications (NI, doc. 374925C-01, PDF)](http://www.testdynamics.co.za/Product/PDF/USRP2901.pdf)
- [USRP-2901 product page](https://www.ni.com/en/shop/hardware/software-defined-radios/model-usrp-2901)
- [NI USRP-2901 Sampling Rate — NI Knowledge Base](https://knowledge.ni.com/KnowledgeArticleDetails?id=kA03q000000x07UCAQ&l=en-US)
