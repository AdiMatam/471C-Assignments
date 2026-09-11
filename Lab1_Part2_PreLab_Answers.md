# Lab 1, Part 2 — Pre-Lab Answers

## USRP-specific questions

**1. What is the range of allowable carrier/center frequency supported by the NI-USRP?**

> 70 MHz to 6 GHz, for both the transmitter and receiver.

**2. What is the maximum allowable bandwidth supported by the NI-USRP?**

> 56 MHz maximum bandwith (for both TX and RX)

**3. What is the maximum sampling rate of the NI-USRP?**

> Could not find a single clock rate in the docs for USRP-2901. Found the following information, itemized per operating mode.

| Mode | Max I/Q rate |
|---|---|
| Streaming (continuous, to/from host) | 15 MS/s |
| Burst, one channel | 61.44 MS/s |
| Burst, two channels | 30.72 MS/s |

**4. Why do you think the DDC is implemented? What is its main benefit?**

> The digital down converter (DDC) performs decimation which involves receiving lowpass-filtering/downsampling the received signal in hardware/FPGA. Main benefit: hardware decimation is significantly faster than running the same filtering algorithm in SW, occurring in real-time/less delay.

## General concept questions

**1. In your own words, describe what the bandwidth of an instrument is.**

> Bandwidth is the width of the range of frequencies an instrument (or channel, or signal) can handle at once. For a receiver/transmitter, it's the span of frequencies over which the front end can faithfully acquire or generate a signal without significant attenuation, distortion, or aliasing — e.g., a 56 MHz instantaneous bandwidth means the USRP can capture or produce all frequency content within a 56 MHz window centered on its tuned carrier frequency in a single acquisition.

**2. What is meant by the sampling rate of an instrument?**

The sampling rate is how many discrete time-domain samples per second the instrument's ADC (on receive) or DAC (on transmit) produces/consumes. It's a rate in samples/second (or complex I/Q samples/second for a baseband-equivalent signal), and by the Nyquist theorem it must be at least twice the bandwidth of the signal being captured or generated in order to represent that signal without aliasing.

**3. Why are these specifications important for designing a transmitter and receiver in a wireless communications system?**

Bandwidth and sampling rate together bound what signals the hardware can actually create or observe. The occupied bandwidth of your modulated waveform must fit within the instrument's instantaneous bandwidth, or parts of the signal will be filtered out or aliased. Likewise, the DAC/ADC sampling rate sets the symbol rates and oversampling factors you're allowed to choose at the transmitter and receiver (per Nyquist, sample rate ≥ 2× the signal bandwidth), and it determines how much data must be streamed to/from the host per second — which is exactly why the USRP-2901's decimation (DDC) and its lower "streaming" rate versus "burst" rate matter in practice: they trade off signal bandwidth/fidelity against how much data the USB/host link and software can actually sustain continuously.