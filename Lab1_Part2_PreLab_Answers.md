# Lab 1, Part 2 — Pre-Lab Answers

## USRP-specific questions

**1. What is the range of allowable carrier/center frequency supported by the NI-USRP?**

> 70 MHz to 6 GHz, for both the transmitter and receiver.

**2. What is the maximum allowable bandwidth supported by the NI-USRP?**

> 56 MHz maximum bandwith (for both TX and RX)

**3. What is the maximum sampling rate of the NI-USRP?**

> Could not find a single clock rate in the docs for USRP-2901. Found the following information, itemized per operating mode.

| Mode                                 | Max I/Q rate |
| ------------------------------------ | ------------ |
| Streaming (continuous, to/from host) | 15 MS/s      |
| Burst, one channel                   | 61.44 MS/s   |
| Burst, two channels                  | 30.72 MS/s   |

**4. Why do you think the DDC is implemented? What is its main benefit?**

> The digital down converter (DDC) performs decimation which involves receiving lowpass-filtering/downsampling the received signal in hardware/FPGA. 
> Main benefit is that hardware decimation is significantly faster than running the same filtering algorithm in SW, occurring in real-time/less delay.

## General concept questions

**1. In your own words, describe what the bandwidth of an instrument is.**

> Bandwidth is the range of frequencies (max-min) that an instrument can handle at once. For a receiver/transmitter, it's the span of frequencies over which the analog "front-end" can acquire or synthesize a signal without distortion.

**2. What is meant by the sampling rate of an instrument?**

> The sampling rate is how many data samples per second the instrument can produce/consume. By Nyquist theorem, sampling rate must be at least 2x the max frequency present in the signal (in order to fully reconstruct/represent it without aliasing).

**3. Why are these specifications important for designing a transmitter and receiver in a wireless communications system?**

>Bandwidth and sampling rate bound bound what signals the hardware can create/observe (in TX vs RX operation). Bandwidth of the modulated waveform must be enclosed within the instrument's bandwidth - else, parts of the signal will be aliased/distorted. 
>
>Similarly, DAC/ADC sampling rate determines an upper bound on the symbol rate (information transfer) over a link. 