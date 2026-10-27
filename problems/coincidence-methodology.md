---
title: A shared standard for counting coincidences
axis: epistemic
status: active
opened: 2026-06-12
updated: 2026-10-27
---

**Statement.** Build a framework-independent standard for the question: how
surprising is a set of claimed exact relations between mathematical
invariants and measured physical constants? A declared expression space,
explicit complexity measures, a family of null models with look-elsewhere
correction, and a scorecard that any framework can be run through, including
the program's own.

**Why it matters.** The field has no shared instrument for this question;
claims oscillate between uncritical acceptance and reflexive dismissal, and
the verdicts (Eddington on one side, the quantum Hall relation on the other)
are only sorted in hindsight. Every other axis of the program inherits its
credibility from this one, and the standard stands on its own: it survives
even if the founding framework falls.

**Known constraints.** The instrument must pass calibration before it is
allowed to score anything we care about: deliberately constructed fake
frameworks must be condemned, Eddington's 136-then-137 must fail with a
penalty for the revision, the quantum Hall relation must pass, with the duty
to report which components and policies separate them, including where the
frozen rule surprises its own author, as it did. Searching
expressions against measured values before the target list is frozen would
invalidate the exercise, so the freeze must be deposited with a dated DOI
first; a data update (new PDG edition, new global fit) is a new freeze
version, and verdicts against the old version stand.

**Next step.** The instrument lives in
[arithmon/Sieve](https://github.com/arithmon/sieve). Current state: inputs
frozen and deposited (DOI
[10.5281/zenodo.20666879](https://doi.org/10.5281/zenodo.20666879),
2026-06-12, before any search ran); four null models implemented;
calibration complete at scaffold budget (fakes condemned, historical
verdicts reproduced); the decision rule itself frozen (v1.1) and the held-out
fail wing run against it: four historical claims excluded, with the results,
the erratum discipline and both readings of one ambiguous frozen sentence
published in the companion preprint (*Preregistration Requires a Decision
Rule*, v2.2, concept DOI
[10.5281/zenodo.21706145](https://doi.org/10.5281/zenodo.21706145)). The constructive side, the rebate that distinguishes a
relation which is a theorem of a pre-specified structure from one found by
search, now has a stated definition and a machine-checked formal layer in
[arithmon/lean](https://github.com/arithmon/lean) (Lean 4: certified
expression-space counts, the rebate arithmetic). Next: the positive wing under a fresh pre-registered freeze (v1.2), the Koide
case, deeper enumeration, and the per-relation audit of the founding
framework.
