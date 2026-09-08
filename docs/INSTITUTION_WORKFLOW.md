# Institution workflow

This document explains how to move from product research to a case that could
eventually become a public Platonic Ideal ruling.

## Authority order

1. [`constitution/CONSTITUTION.md`](../constitution/CONSTITUTION.md) is the
   normative human-readable authority.
2. [`constitution/constitution.v1.json`](../constitution/constitution.v1.json)
   is the machine profile for the same version and is digest-pinned to the
   text.
3. `schemas/` defines the shape of evidence, cases, ruling events, and
   challenges.
4. `institution/evidence.json` is the evidence ledger. Evidence IDs are
   permanent and never reused.
5. `cases/` contains editorial case files. `DRAFT` is deliberately nonterminal.
6. `institution/rulings.json` contains append-only events for actual terminal
   rulings.
7. `institution/challenges.json` contains evidence-based challenges against
   existing rulings.
8. `public/platonic_ideal.csv` is the current site's migration-compatible
   register. It must not be treated as proof that a row has passed the
   Constitution.

## The authoring loop

1. Define one coherent category, ordinary use context, exclusions, and Form
   statement. If incompatible users require incompatible objects, use
   `SPLIT_REQUIRED` while the jurisdiction is resolved.
2. Create or update a case file with a permanent `PI-C-####` ID. Start at
   `DRAFT`; do not copy an inherited CSV `DECLARED` status into the case.
3. Add evidence items to `institution/evidence.json`. Each item needs a source,
   evidence class, claim, retrieval date, verification status, independence
   group, and commercial relationship.
4. Record findings for the five admission gates and ten hard disqualifiers.
   Facts, editorial inferences, and gaps must remain distinguishable.
5. Record failure modes, maintenance, repair economics, and the strongest
   counter-case. For `EMPTY`, also record the search protocol, serious
   candidate set, structural failure, and the future requirement that could
   reopen the category.
6. Run the validator:

   ```bash
   npm run validate:institution
   ```

7. Resolve every blocker. A green result means the files are internally
   consistent; it does not mean that a human has selected a product.
8. Only a human adjudicator may move a case to `DECLARED` or `EMPTY`, and the
   case must meet the terminal evidence and confidence floors. A ruling event
   is appended only after the public ruling and evidence receipt are ready.

## Terminal boundary

`DECLARED` requires one exact manufacturer/model/model identifier, all five
gates `PASS`, all hard disqualifiers `ABSENT`, at least three verified items
from three independent classes/groups, primary technical or service evidence,
an independent source, confidence `4/5` or better, no material gaps, and a
complete counter-case.

`EMPTY` requires a stable Form, credible market coverage, evidence of the
material failure or disqualifier, a future qualifying requirement, the same
evidence and confidence floors, and a counter-case to emptiness.

All other statuses are work states. They must never be displayed as terminal
verdicts.

## Error contract

Validator errors include a stable code, file path, object ID, rule, message, and
repair. Do not “fix” a failing case by weakening the validator or deleting an
evidence gap; either resolve the evidence or keep the case nonterminal.

## Oracle boundary

Oracle output is draft material only. It may identify missing fields or suggest
questions, but it cannot create evidence, verify a citation, publish a ruling,
or mutate a canonical ledger. Every material claim still needs a human-verified
evidence item.
