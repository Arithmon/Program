---
title: Axiom reduction in the formal core
axis: formalization
status: open
opened: 2026-06-11
updated: 2026-06-11
---

**Statement.** Reduce the 15 stated axioms of the Lean core (4 on the
prediction chain, 11 interval-arithmetic certificates for the K3 block)
toward zero.

**Why it matters.** "15 to N" is the program's cleanest public progress
metric: machine-checked, monotone, and impossible to spin.

**Known constraints.** The core builds with 0 sorry; the 33 exact relations
and the variance aggregation are axiom-free. The 11 K3 certificates are
trusted numerical facts (interval enclosures from a second, exact rational
engine cross-checked 28000/28000); discharging them means verified interval
arithmetic inside Lean, bounded but heavy. The 4 prediction-chain axioms
package literature results (Cheeger-type bounds, gluing theorems); they are
the real formalization frontier and may require upstream Mathlib work.

**Next step.** Discharge the 11 K3 certificates first (mechanical, bounded);
treat the 4 literature axioms as a separate long-horizon track.
