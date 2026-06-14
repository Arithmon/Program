# Contributing to the Program

This repository is the charter: the hard core, the heuristics, the open
problems, and the confrontations scoreboard. Contributions here touch what the
program *commits to*, so the bar is honesty about register, not enthusiasm.

Org-wide rules (what helps, what does not, house style) are in the
[organization CONTRIBUTING](https://github.com/arithmon/.github/blob/main/CONTRIBUTING.md).
This file covers the two procedures the Program owns.

## Propose or attack an open problem

The problems live in [`problems/`](problems/), one file each, indexed in
[INDEX.md](INDEX.md), across five axes (geometry, selection, formalization,
epistemic, experimental).

- **Attack** an existing problem: a partial result, a constraint, or a refuted
  route. A refuted route is not a failure to hide; it is a theorem about the
  territory and it gets listed as one. Open an issue or a pull request against
  the relevant problem file.
- **Propose** a new problem: state it so progress on it is recognisable. Say
  what would count as a solution and what would count as a dead end. A problem
  no result could settle does not belong on the list.

The hard core itself (one sentence) does not move. Everything in the protective
belt can be revised or falsified; if you think the core is wrong, that is a
challenge to the whole program, and the place for it is an issue stating the
counterexample, not an edit.

## Challenge a frozen prediction

The scoreboard is [CONFRONTATIONS.md](CONFRONTATIONS.md): named predictions,
dated, against scheduled experimental data. A frozen prediction stands or falls
as stated.

- A prediction that the data has falsified: report it. A falsified prediction
  is recorded as falsified, in place. That is the scoreboard working, not a
  result to bury.
- A prediction you believe was edited after the relevant data arrived: report
  it with the commit history. Every register move (a statement changing shelf
  from proven, computed, conjectured, or falsifiable-bet) is a dated event, by
  rule. If one is not logged, that is a bug in our discipline and we want to
  know.

What you cannot do is ask for a frozen prediction to be quietly revised to
match new data. That is the one move the negative heuristic forbids absolutely.

## A note on registers

Every claim in the program sits on exactly one shelf: **proven** (machine-checked),
**computed**, **conjectured**, or **falsifiable-bet**. A contribution that moves
a claim between shelves must say so explicitly. Promoting a conjecture to
"proven" without a proof, or a bet to a result, is the failure this rule exists
to prevent.

---

<sub>GIFT is the founding framework of the Arithmon program.
Program: [arithmon.com](https://arithmon.com) ·
[github.com/arithmon](https://github.com/arithmon)</sub>
