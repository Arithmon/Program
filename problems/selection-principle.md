---
title: The selection principle
axis: selection
status: active
opened: 2026-06-11
updated: 2026-06-18
---

**Statement.** Why this geometry? Identify the principle that selects K7,
the Betti pair (21, 77), and the assignment of formulas to observables, or
demonstrate that no such principle is needed beyond consistency.

**Why it matters.** This is the program's problem number one. The landscape
gives up uniqueness; Arithmon bets on it. The bet is only won if selection is
explained, not assumed.

**Known constraints.** The geometry is not generic, and the evidence is
arithmetic before it is physical: the polarizing K3 lattice, Nikulin type
(15, 7, 1), is a classified reflective point (60-root reflection lattice, a
Petersen-graph stratum, automorphisms by S5); the fiber carries a symplectic
automorphism group containing V4 x Z/5 through two distinct elliptic
fibrations; six structural obstructions separate the object from every
standard template. None of this yet amounts to a selection principle; it
amounts to the geometry being a distinguished point in several classifications
at once.

**What is now established (2026-06-18).** The question splits cleanly and the
two halves answer differently.

- *Topological rarity (Q-A).* (b2, b3) = (21, 77) is reached by no twisted
  connected sum construction (exhaustive 3852-config no-go, CHNP b2_max
  about 18); it sits in a genuine gap of the realized G2 Betti census
  (nearest realized (19, 65)); reached only via the
  Joyce-Karigiannis / Donaldson K3-fibration route. So (21, 77) IS rare as
  a G2 manifold. But rarity is representation-dependent: its CY3 shadow
  via the Kunneth decomposition CY3 x S^1, namely (h11, h21) = (21, 27),
  is realized by 668,607 distinct reflexive 4-polytopes in the
  Kreuzer-Skarke database. The G2 rarity argument does not transport to
  the CY3 representation of the same numbers.

- *Inverse-problem specialness (Q-B).* In a blind, mirage-proof sweep
  (alphabet size held constant across the grid; only the Betti leaf
  values change) over the full Kreuzer-Skarke Hodge range
  (b2, b3 each in [0, 491], 242,064 grid points), the
  Sieve methodology
  ([arithmon/sieve](https://github.com/arithmon/sieve), D33) re-runs
  the search per pair and asks how cheaply / how widely each pair fits
  the frozen Standard Model set. (21, 77) sinks BELOW THE MEDIAN on
  every discriminating axis: ~64% of grid pairs strictly beat it on
  Betti-sensitive coverage at the discriminating tolerance, and it sits
  in the expensive quartile at tight tau. The CY3 shadow (21, 27) is
  even less special. The verdict GROWS as the haystack grows: smaller
  prior grids were the conservative reading, in (21, 77)'s favour.
  Specialness, in the inverse-problem sense, is not where the geometry
  lives.

Reading. The two halves are independent and both honest. Q-B closes one
candidate channel for the selection principle: the Betti pair is not
arithmetically privileged at fitting the freeze, so the principle, if there
is one, is NOT "(21, 77) is the cheapest set of leaves to reach the
Standard Model." Q-A keeps the topological-distinguishedness channel
open, in the K3-lattice direction the constraints already named; it does
not amount to a principle on its own.

**Next step.** Continue mapping which classifications single out (15, 7, 1)
and (21, 77) simultaneously; test whether distinguishedness propagates from
the K3 lattice to the G2 level. Do not look for selection in the inverse-
problem statistic — that channel is closed by the landscape sweep.
