---
title: Global residual bound on all of K3
axis: geometry
status: open
opened: 2026-06-11
updated: 2026-09-23
---

**Statement.** Extend the certified bound on the Calabi-Yau volume-form
residual from a box-local statement (4000 open boxes, Krawczyk-verified, with
the variance aggregation re-computed inside Lean) to a global bound on all of
K3.

**Why it matters.** The box-local certificate is the framework's rigor
anchor; a global bound would remove the locality caveat entirely.

**Correction (K7 erratum, 2026-08-22).** The box-local certificate does not
bound what this statement says: it bounds an auxiliary quantity, not the
Calabi-Yau volume-form residual. Measured on the same 4000 points in the
correct pullback convention, the residual variance is 5.3e-1 (ratio 3677 to
the certified value) and 522 points carry no positive-definite form. What
stands is the surface-level certification (each box contains an exact point
of K3) and the method. The premise of this problem is therefore withdrawn as
stated; see `K7/publications/ERRATUM_v3.5.md`.

**Known constraints.** The certificate formerly quoted here (variance
envelope 1321/10^7, 7.57x margin) applies to the auxiliary quantity only. Scoping concluded that a genuinely global bound is research-level
and that the only identified route is a Positivstellensatz / sum-of-squares
certificate over the orbifold chart.

**Next step.** SOS feasibility study on a reduced chart; no commitment until
the central lock (exact metric) settles priorities.
