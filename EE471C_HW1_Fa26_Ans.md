# EE 471C / EE 38K-17 — Homework #1 Answers

## Wireless Devices Comparison

|                                    | Samsung Galaxy S25 Ultra                                      | iPhone 17 Pro Max                                                                               | Google Pixel 10 Pro                                                                              |
| ---------------------------------- | ------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| **Wireless technologies**          | Wi-Fi 7, 5G, Bluetooth 5.4, NFC, UWB                          | Wi-Fi 7, 5G, Bluetooth 6, NFC, UWB                                                              | Wi-Fi 7, 5G, Bluetooth 6, NFC, UWB                                                               |
| **Cellular standards**             | 5G NR, LTE                                                    | 5G NR, LTE                                                                                      | 5G NR, LTE                                                                                       |
| **Frequency bands**                | Sub-6 GHz + mmWave                                            | Sub-6 GHz + mmWave                                                                              | Sub-6 GHz; mmWave                                                                                |
| **Max claimed cellular data rate** | ~$10~\text{Gbps}$ theoretical peak (mmWave, Snapdragon modem) | Not officially published by Apple, but estimated theoretical peak ~$4$–$7~\text{Gbps}$ (mmWave) | Not officially published by Google, but estimated theoretical peak ~$6$–$7~\text{Gbps}$ (mmWave) |
| **Max claimed WiFi data rate**     | Wi-Fi 7, up to ~$5.8~\text{Gbps}$                             | Wi-Fi 7, max ~$2.9~\text{Gbps}$                                                                 | Wi-Fi 7, tri-band, up to ~$5.8~\text{Gbps}$                                                      |
| **Operating system**               | Android 15                                                    | iOS 26                                                                                          | Android 16                                                                                       |

## Cellular Provider Comparison

Providers chosen: **T-Mobile** and **AT&T** 

|                                                   | T-Mobile                                                                            | AT&T                                                       |
| ------------------------------------------------- | ----------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| **Cellular standards supported**                  | 5G SA + NSA, LTE                                                                    | 5G SA + NSA, LTE                                           |
| **Monthly charge, unlimited voice plan**          | ~\$45/mo (unlimited talk/text + 15GB high-speed data)                               | ~\$30/mo per line (unlimited talk/text, tiered data speed) |
| **Monthly charge, ≥10GB data plan**               | Included in the \$45/mo plan above                                                  | AT&T prepaid annual plan ~\$20/mo includes it              |
| **Voice roaming cost in Germany (no int'l plan)** | ~\$0.50/min                                                                         | ~\$2.00/min                                                |
| **Data roaming cost in Germany (no int'l plan)**  | Pay-per-use rate applies - international data/texting is included by default though | ~\$2.05/MB (≈ \$2,000+/GB)                                 |


## 6G Technology Exploration

- **Expected capabilities vs. 5G:** Target peak data rates around $1~\text{Tbps}$ (~100× 5G), end-to-end latency down to ~$1~\text{ms}$ (vs. ~10 ms for 5G).
- **Candidate frequency bands:** Continued use of sub-6 GHz and mmWave, plus new "upper mid-band" spectrum (~7–15 GHz) and sub-terahertz/THz spectrum (roughly 0.1–3 THz, with some research pushing toward 10 THz) for ultra-high-bandwidth links.
- **Potential applications:** Holographic communication, digital twins, tactile internet, extended reality (XR/AR/VR), **autonomous vehicles / connected robotics seems to a big one**
- **Implementation challenges:** Immature THz hardware (power amplifiers, antennas), very short range and high atmospheric absorption at THz (requiring dense small-cell deployment). Global rollout cost.
- **Leading organizations/countries:** China (Purple Mountain Laboratories, IMT-2030 group), South Korea (targeting early commercialization), the US (Next G Alliance, FCC), the EU/Finland (6G Flagship at Oulu, Hexa-X project).
- **Prototypes/testbeds:** China's Purple Mountain Labs Pre-6G outdoor trial network in Nanjing funcitonal for industrial manufacturing and some holographic comms use cases. European 6GStarLab test bed exploring LEO-based satellite 6G.

## Exploration Question

**Question for class:** Starlink's latency is down to ~25-30ms now (supposedly), getting close to what next-generation communication methods (6G) is promising. At what point do we think satellite internet becomes the norm / part of the standard cell network rather than being a separate, backup option? Feasible? 