# Institution foundation

## Meta
- Owner: Laurent Courtines
- Status: building
- Priority: P0
- Last updated: 2026-09-08

## Problem
The public register claims authority through strict rules, but the inherited
CSV does not yet enforce the evidence floor, model identity, terminal gates,
referential integrity, or public revision history. Without an institution layer,
a persuasive draft can look like a ruling and a paid product could be mistaken
for a paid outcome.

## Target users
- [Founder-operator](../../users/personas.md) — sole adjudicator and maintainer
- [External durable-goods shopper](../../users/personas.md) — future reader of
  public verdicts and evidence receipts

## Success metrics
- A clean clone can run `npm run validate:institution` in under five minutes.
- Terminal cases fail closed when they lack exact model identity, gate passes,
  evidence independence, confidence, or references.
- The public `/constitution/` route states the authority boundary and remains
  crawlable without exposing Oracle or paid dossier material.
- The founding Pocket Knife case remains visibly `DRAFT` until re-adjudicated.
- The institution foundation passes `npm test` and production build checks.

## Risks
The validator could become a second undocumented rulebook, or a structurally
valid case could still overstate a weak source. The CSV and new case system could
also drift into contradictory public answers. The authority layer must stay
small, inspectable, and subordinate to human evidence review.

## Dependencies
Constitution text and profile, JSON schemas, evidence/case/ruling/challenge
ledgers, semantic validator, Astro route/layout, CI, PM Brain links, and the
future founding-case evidence packet.

## Timeline
Foundation in the current implementation unit. Re-adjudicate Everyday Pocket
Knife and build the first public ruling projection only after the validator is
stable. Run the 20/10/5 founding validation test before implementing broader
commerce or public submissions.

## Evidence
- The Constitution establishes the terminal evidence floor, public revocation,
  and commercial independence [constitution](../../../constitution/CONSTITUTION.md)
- The engineering review identified CSV authority ambiguity, missing semantic
  checks, and the need for negative fixtures [institution workflow](../../../docs/INSTITUTION_WORKFLOW.md)
- The accepted commercial boundary keeps public rulings free and sells research
  depth separately [decision](../../../decisions/2026-09-08-constitution-and-paid-dossier-boundary.md)

## Linked
- Hypotheses: [institution-foundation](../../../hypotheses/institution-foundation.md)
- Decisions: [2026-09-08 Constitution and paid dossier](../../../decisions/2026-09-08-constitution-and-paid-dossier-boundary.md)
- Metrics: [product metrics](../metrics.md)
- Stakeholders affected: [Laurent Courtines](../../../stakeholders/laurent-courtines.md)

## Open questions
- What exact evidence packet will make the first Pocket Knife ruling worthy of
  publication?
- Which parts of the evidence receipt should be expanded into the first paid
  dossier without hiding decisive public reasoning?
- When should a validated ruling become a data source for the category route?

## Follow-up after launch
Measure validator repair time, case revision frequency, challenge quality,
revocations, dossier purchases, and reports that a ruling reduced comparison
shopping. Revisit the contract only when observed cases expose a repeated gap.
