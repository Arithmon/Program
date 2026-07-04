---
title: The selection principle
axis: selection
status: active
opened: 2026-06-11
updated: 2026-07-04
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

**What is now established (2026-07-04).** The next step announced above has
been carried out, in both directions, and a third route has been audited.
All three close.

- *Lattice propagation (Q-A, settled negatively by mechanism).* The
  distinguishedness of the lattice keeps growing: it is realized as the
  invariant lattice of non-symplectic involutions on hyperkahler fourfolds
  of K3^[2] type, and it is the unique named exception of the published
  mirror-existence lemma for that setting. But none of it reaches b3 = 77,
  for independent structural reasons that are now proved rather than
  suspected: (i) b2 = 21 is equivalent to rank-one monodromy, so the S5
  lattice symmetry is broken to a stabilizer before it can act on the
  monodromy data; (ii) 77 counts components of the discriminant link and
  lives in the link complement, a factor disjoint from the lattice data in
  the Donaldson cohomology model (the factor 11 of 77 = 7 x 11 appears in
  none of the lattice-derived invariants actually swept: S5 irreps and
  their sums, products and powers, the Petersen graph counts, the full
  root diagram); (iii) the only higher-hyperkahler type that can host the
  lattice has zero odd cohomology, so there is nothing on that side to
  match a link count against. Distinguished, yes; selecting, no.

- *Diophantine route (audited, closed as a principle).* The published
  system ((rank + Ngen) b2 = Ngen b3, b2 + b3 = S) is linear with nonzero
  determinant, so a unique rational solution always exists; integrality is
  a divisibility comb, not a filter. The solution factors as
  (b2, b3) = k (Ngen, rank + Ngen) with k = S / (rank + 2 Ngen); at
  (8, 3, 98) this reads (21, 77) = 7 x (3, 11). All selection power sits
  in the single integer choice S = 98, which remains underived in the
  source papers, and one of their screening premises (realizability
  requires b2 >= 9) is contradicted by the literature census (27 of the 65
  known compact G2 manifolds have b2 < 9, including Joyce's (0, 215)).
  The authors of that route have themselves downgraded the claim to a
  "unique candidate solution" (May 2026).

**Residue.** The open problem now reduces to a single statement: derive
b2 + b3 = 98 = dim K7 x dim G2 (equivalently k = 7) from a pre-registered
principle. In the factored form (b2, b3) = dim K7 x (Ngen, rank + Ngen),
the selection question dissolves into the standard physical inputs
(7, 3, 8): dimension, generations, rank. Until 98 = 7 x 14 is derived,
it is an observation, not a principle, and must not be used as one.

**Next step.** Only the residue qualifies: a pre-registered derivation of
b2 + b3 = dim K7 x dim G2. The inverse-problem channel, all presently
specified lattice-to-b3 propagation mechanisms, and the Diophantine route
are closed; the honest standing verdict is "a distinguished point in
several classifications at once, with no selection principle behind it so
far", now established channel by channel rather than assumed out of
caution. A propagation mechanism nobody has specified yet would reopen
Q-A; it would have to enter through the link complement, where 77 lives.
