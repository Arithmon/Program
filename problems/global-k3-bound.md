---
title: From a certified atlas to a certified metric on K3
axis: geometry
status: active
opened: 2026-06-11
updated: 2026-09-23
---

**Statement.** Produce a certified evaluation of the Ricci-flat (Calabi-Yau)
metric on one explicit K3 surface: an algorithm that evaluates the metric
with a global, machine-checked error bound, rather than a closed formula.

**Why it matters.** The geometry this program rests on is only known
numerically. A certified evaluator would turn "a good approximation" into a
statement with a proved error, everywhere on the surface.

**Where it stands.** The first layer is public:
[Arithmon/K3](https://github.com/Arithmon/K3) (concept DOI
[10.5281/zenodo.22047469](https://doi.org/10.5281/zenodo.22047469)) certifies
the analytic geometry of an explicit K3 surface, a finite holomorphic atlas
whose chart domains, transitions and branch continuations are machine-checked.
No Ricci-flat metric is claimed there. Work toward the certified evaluation of
the metric is in progress; no result is claimed.

**Correction (K7 erratum, 2026-08-22).** An earlier formulation of this problem
started from a box-local "certified bound on the Calabi-Yau residual". That
bound certifies an auxiliary quantity, not the Calabi-Yau residual: in the
correct pullback convention the residual variance of that ansatz is 5.3e-1 and
522 of its 4000 points carry no positive-definite form. See
`K7/publications/ERRATUM_v3.5.md`.

**Next step.** Complete the certified evaluator and publish it the way the
atlas was published: with the certificates and a one-command verification.
