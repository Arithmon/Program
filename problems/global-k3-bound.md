---
title: Global residual bound on all of K3
axis: geometry
status: open
opened: 2026-06-11
updated: 2026-06-11
---

**Statement.** Extend the certified bound on the Calabi-Yau volume-form
residual from a box-local statement (4000 open boxes, Krawczyk-verified, with
the variance aggregation re-computed inside Lean) to a global bound on all of
K3.

**Why it matters.** The box-local certificate is the framework's rigor
anchor; a global bound would remove the locality caveat entirely.

**Known constraints.** The current certificate gives a variance envelope of
1321/10^7 with 7.57x safety margin, formally aggregated from raw rational
enclosures. Scoping concluded that a genuinely global bound is research-level
and that the only identified route is a Positivstellensatz / sum-of-squares
certificate over the orbifold chart.

**Next step.** SOS feasibility study on a reduced chart; no commitment until
the central lock (exact metric) settles priorities.
