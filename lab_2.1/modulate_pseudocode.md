# modulate.vi — pseudocode

Inputs: `input bit stream` (U8[]), `modulation type` (string, from mod params in), `Symbol Energy` (DBL, default 1), `error in`
Output: `output symbols` (CDB[]), `modulation parameters out` (pass-through), `error out`

```
error out = error in   // straight pass-through, both cases

case modulation type of:

  "BPSK":
    for each bit b in input bit stream:
      re = 1 - 2*b        // 0 -> +1, 1 -> -1
      im = 0
      s  = complex(re, im)   // already unit energy
    end for

  "QPSK":
    // split bits into consecutive pairs: (b0,b1), (b2,b3), ...
    for each pair (b_re, b_im) in input bit stream:
      re = 1 - 2*b_re      // first bit of pair -> real sign
      im = 1 - 2*b_im      // second bit of pair -> imag sign
      s  = complex(re, im) / sqrt(2)   // normalize to unit energy (|s|^2 = 2 -> /sqrt2)
    end for

end case

output symbols = s_array * sqrt(Symbol Energy)   // scale each symbol
```

**Notes**
- Bit pairing for QPSK must match Table 1b Gray mapping: `00->1+j, 10->-1+j, 11->-1-j, 01->1-j`. The `1-2*bit` rule per component reproduces this exactly.
- Normalize *before* scaling by `sqrt(Symbol Energy)`, so default (`Symbol Energy=1`) reproduces the unit-energy constellations in Fig. 2.
- In LabVIEW: use a bit-array Reshape/decimate (even/odd or index pairs) to split QPSK bit pairs, `1-2*x` via Subtract from constant, `Re/Im To Complex` to build symbols, and wire `error in -> error out` unchanged through both case frames.

## LabVIEW how-to: modulate.vi

Iterating an array in LabVIEW = a **For Loop** with **auto-indexing**, not manual indexing.

**BPSK case:**
1. Drop a For Loop in the BPSK frame; wire `input bit stream` straight onto its left border. The tunnel shows `[ ]` (array) — this auto-indexes: loop count = array length, one bit `b` fed per iteration. No need to wire the count terminal.
2. Inside: `1 - 2*b` (Multiply `b*2`, then Subtract from constant `1`) -> `Re/Im To Complex` `re` input; wire `0` constant into `im`.
3. Wire the complex output to the right border with auto-indexing on (default) -> builds the output symbol array directly, no Build Array needed.

**QPSK case (split into pairs before the loop):**
1. **Decimate 1D Array** on `input bit stream` -> output 0 = even-index bits, output 1 = odd-index bits. Since pairs are `(b0,b1),(b2,b3),...`, output 0 = all "real" bits, output 1 = all "imag" bits, aligned by position.
2. For Loop with *both* decimated arrays wired onto the border, auto-indexing on both -> lockstep `b_re`, `b_im` per iteration.
3. Inside: `re = 1-2*b_re`, `im = 1-2*b_im` -> `Re/Im To Complex` -> divide by `sqrt(2)` (Square Root of constant `2`, or `1.41421356` constant).
4. Auto-indexed output -> array of normalized QPSK symbols.

**After the case structure (both branches):** multiply the whole symbol array by `sqrt(Symbol Energy)`. No loop needed — `Multiply` is polymorphic and broadcasts a scalar over an array automatically.

Gotcha: auto-indexing is a per-tunnel toggle — right-click and confirm "Enable Indexing" is checked if the loop count looks wrong.

---

# decode.vi — pseudocode

Input: `input symbols` (CDB[]), `modulation type` (string, from mod params in), `error in`
Output: `estimated bit sequence` (U8[]), `error out`

ML detection on BPSK/QPSK's symmetric constellations reduces to a per-component sign test — no need for `Symbol Energy` here (scaling by a positive constant doesn't change which constellation point is nearest).

```
error out = error in   // straight pass-through, both cases

case modulation type of:

  "BPSK":
    for each symbol y in input symbols:
      re = Re(y)
      bit = (re < 0) ? 1 : 0     // inverse of modulate's 1-2b mapping
    end for
    estimated bit sequence = bit_array

  "QPSK":
    for each symbol y in input symbols:
      re = Re(y)
      im = Im(y)
      b_re = (re < 0) ? 1 : 0
      b_im = (im < 0) ? 1 : 0
    end for
    estimated bit sequence = interleave(b_re_array, b_im_array)   // b0,b1,b2,b3,... order

end case
```

**Notes**
- Decision rule is exactly the inverse of modulate's `1-2*bit`: `bit=0 -> re=+1`, `bit=1 -> re=-1`, so `re<0 -> bit=1`.
- QPSK must re-interleave `b_re`/`b_im` back into the original bit order (opposite of Decimate 1D Array in modulate.vi), otherwise bits come out permuted.

## LabVIEW how-to: decode.vi

**BPSK case:**
1. For Loop, auto-index `input symbols` onto the left border -> one complex symbol `y` per iteration.
2. **Complex To Re/Im** on `y`, keep only `re`.
3. **Less Than 0?** on `re` -> boolean -> **Boolean To (0,1)** -> U8 bit.
4. Auto-indexed output tunnel -> `estimated bit sequence` directly (order already matches, no interleave needed).

**QPSK case:**
1. For Loop, auto-index `input symbols` onto the left border -> one complex symbol `y` per iteration.
2. **Complex To Re/Im** -> `re`, `im`.
3. `re < 0` and `im < 0` (two **Less Than 0?** comparisons) -> two **Boolean To (0,1)** -> `b_re`, `b_im` per iteration.
4. Auto-index both outputs -> `b_re` array and `b_im` array.
5. **Interleave 1D Arrays** on `(b_re array, b_im array)` -> reconstructs `b0,b1,b2,b3,...` order -> wire to `estimated bit sequence`.

Same gotcha as modulate: confirm auto-indexing is enabled on every array tunnel, or the loop count/shape will be wrong.
