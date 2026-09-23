---
title: Axiom reduction in the formal core
axis: formalization
status: open
opened: 2026-06-11
updated: 2026-09-23
---

**Statement.** Reduce the 14 stated axioms of the Lean core (4 on the
prediction chain, 10 interval-arithmetic certificates for the K3 block)
toward zero.

**Why it matters.** "15 to N" is the program's cleanest public progress
metric: machine-checked, monotone, and impossible to spin. First step taken
on 2026-09-08: the K3-block axiom `PSLQ_null_in_TCS_basis` was discharged
in K7-Lean, bringing the count from 15 to 14.

**Known constraints.** The core builds with 0 sorry; the 33 exact relations
and the variance aggregation are axiom-free. The 10 K3 certificates are
trusted numerical facts (interval enclosures from a second, exact rational
engine cross-checked 28000/28000); discharging them means verified interval
arithmetic inside Lean, bounded but heavy. The 4 prediction-chain axioms
package literature results (Cheeger-type bounds, gluing theorems); they are
the real formalization frontier and may require upstream Mathlib work.

**Next step.** Discharge the 10 remaining K3 certificates first (mechanical, bounded);
treat the 4 literature axioms as a separate long-horizon track.
