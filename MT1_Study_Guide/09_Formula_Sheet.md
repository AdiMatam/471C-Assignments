# 09 — Formula Sheet (write this from memory on Monday)

Conventions follow the lecture / HW2 solutions. ⭐ = "I should be able to derive this too". 📌 sections below were in HW2/HW3 (highest priority); the Pulse shaping, Detection/BER, Synchronization and Equalization sections were *not* in a homework (likely out of scope).

## Entropy
$H=-\sum p_i\log_2p_i$; max $\log_2M$ (uniform).  Capacity $C=B\log_2(1+\text{SNR})$ (concept only).

## Probability / processes 📌
- Mean $E[X]=\int xf$; Var $=E[X^2]-\mu^2$; Uniform$[a,b]$: $\tfrac{a+b}2,\tfrac{(b-a)^2}{12}$.
- $R_{xx}[n_1,n_2]=E[x[n_1]x^*[n_2]]$; $C_{xx}=R-\mu\mu^*$. WSS: constant mean + lag-only covariance. IID ⇒ $C=\sigma^2\delta[k]$.
- Complex Gaussian $\mathcal{CN}(0,\sigma^2)$: real & imag independent $\mathcal N(0,\sigma^2/2)$.
- $P_y=|H|^2P_x$.  PSD $=\mathcal F\{C_{xx}\}$; power $=C_{xx}(0)=\int P$.  $e^{-a|\tau|}\leftrightarrow\frac{2a}{a^2+(2\pi f)^2}$.
- Bandwidths: 3-dB (half power), null-to-null, fractional containment $\int_{-B}^BP=\alpha\int P$.

## Fourier / sampling 📌
- rect$(t/T)\leftrightarrow T$sinc$(fT)$; sinc$(t/T)\leftrightarrow T$rect$(Tf)$; $\Lambda(t/T)\leftrightarrow T\text{sinc}^2(fT)$; shift ↔ phase; modulation ↔ shift.
- Nyquist: $T\le1/W$ (complex baseband total width $W$, i.e. $[-W/2,W/2]$).
- $X(e^{j2\pi f})=\frac1T\sum_nX_c\!\left(\frac{f-n}T\right)$; D/C: $x_c(t)=\sum x[n]\text{sinc}\frac{t-nT}{T}$.
- ⭐ DT equivalent: $h[n]=\int\text{sinc}(\tau W)h_c(nT-\tau)d\tau$ ($TW=1$); delay $\tau_k$ ⇒ $\text{sinc}(n-\tau_k/T)$.

## Passband ↔ baseband 📌
- ⭐ $x_p=\text{Re}\{xe^{j2\pi f_ct}\}=x_I\cos-x_Q\sin$; down: $x=\text{LPF}\{2x_pe^{-j2\pi f_ct}\}$; $X_p=\tfrac12[X(f-f_c)+X^*(-f-f_c)]$.
- Channel: $h(f)=h_p(f+f_c)$, no extra factor; path $(a,\tau)$ ⇒ $a\,e^{-j2\pi f_c\tau}\delta(t-\tau)$.
- Chain: $h_c\to h_p$ (BPF) $\to h(t)\to h[n]$, $T=1/W$.

## Modulation 📌
- $x(t)=\sqrt{E_x}\sum s[n]g_{tx}(t-nT)$, $\|g_{tx}\|=1$; bit rate $\log_2M/T$; power $E_x/T$; $P_x(f)=\frac{E_x}T|G_{tx}(f)|^2$.
- ⭐ Normalize: $\mu=\frac1M\sum s$; $s'=s-\mu$; $E'=\frac1M\sum|s'|^2$; $\tilde s=s'/\sqrt{E'}$.
- Unnormalized avg energy: BPSK 1, QPSK 2, $M$-PAM $\frac{M^2-1}3$, square $M$-QAM $\frac{2(M-1)}3$, $M$-PSK 1.
- AWGN: $N_0=k_BT_e$ ($k_B=1.38\!\times\!10^{-23}$, $T_e=290$K ⇒ −174 dBm/Hz); noise power $N_0B$; SNR$=E_x/N_0$; dB $=10\log_{10}$.

## Pulse shaping
- ⭐ Matched: $g_{rx}(t)=g_{tx}^*(-t)$ (Cauchy–Schwarz).  Nyquist: $g(nT)=\delta[n]\Leftrightarrow\frac1T\sum_kG(f-\frac kT)=1$.
- RC: $B=\frac{1+\alpha}{2T}$ (one-sided), passband width $\frac{1+\alpha}T$, decay $1/t^3$; SRRC = $\sqrt{G_{rc}}$ at TX **and** RX.
- Tx: $c[n]=(\uparrow_Ls)*g_{tx}$, polyphase $g^{(\ell)}[n]=g[nL+\ell]$. Rx: filter then $\downarrow M$ = polyphase branches at low rate. $M/N=T_N/T_M$.

## Detection / BER
- ⭐ ML: $\hat s=\arg\min_s|y-\sqrt{E_x}s|^2$; Voronoi = perpendicular bisectors.
- PEP $=Q\!\left(\sqrt{E_xd^2/2N_0}\right)$; union $\le(M-1)Q\!\left(\sqrt{E_xd_{\min}^2/2N_0}\right)$; unit-energy QAM $d_{\min}=\sqrt{6/(M-1)}$.
- ⭐ BPSK: $Q(\sqrt{2E_x/N_0})$; QPSK bit: $Q(\sqrt{E_x/N_0})$ (same as BPSK in $E_b/N_0$); BER≈SER/$\log_2M$ (Gray).
- $Q(x)\le\frac12e^{-x^2/2}$.

## Synchronization / estimation
- MOE: $J(\tau)=E|y(nT+\tau)|^2$, $k^*=\arg\max_k\frac1P\sum_n|r[nM+k]|^2$.
- Frame sync: $\hat n_d=\arg\max_n|\sum_ks_{tr}^*[k]y[n+k]|$. Barker-7: $+1+1+1-1-1+1-1$.
- ⭐ LS: $\hat x=(A^*A)^{-1}A^*b$; orthogonality $A^*(b-A\hat x)=0$. Flat $\hat h=\frac{\sum s^*_{tr}y}{\sum|s_{tr}|^2}$. LS=ML for IID Gaussian.
- CFO: $y[n]\propto e^{j2\pi f_enT}$; $\hat f_e=\frac1{2\pi T(N-1)}\sum\angle(y[n]y^*[n-1])$.

## Equalization
- $y[n]=\sum_{\ell=0}^Lh[\ell]s[n-\ell]+v$. ⭐ LS EQ: $f=(H^*H)^{-1}H^*e_{n_d}$, $H$: $(L_f+L+1)\times(L_f+1)$; $L_f\approx4L$.
- LMMSE: $f=(\mathcal H\mathcal H^*+N_0I)^{-1}\mathcal He_{n_d}$; $N_0\to\infty$ matched filter, $N_0\to0$ LS.
- DFT, circular conv ↔ product; linear = circular if zero-padded to $\ge N_1+N_2-1$.
- ⭐ CP: length $L_c\ge L$; discard first $L_c$; $Y[k]=H[k]S[k]+V[k]$; ZF $Y/H$; MMSE $\frac{H^*}{|H|^2+N_0/E_s}Y$.

## Numbers worth remembering
$10\log_{10}2=3.01$ dB; $Q(1)=0.159$, $Q(2)=0.0228$, $Q(3)=1.35\!\times\!10^{-3}$, $Q(4)=3.2\!\times\!10^{-5}$; $c=3\times10^8$ m/s.


Rect → sinc, shifted in time:

rect((t−t0)/T) ↔ T·sinc(fT)·e^{−j2πf t0}

The sinc is the same, and the shift only adds a phase factor.

Sinc → rect, shifted in frequency (your case, with rect((f−fc)/W)):

rect((f−fc)/W) ↔ W·sinc(Wt)·e^{+j2πfc t}