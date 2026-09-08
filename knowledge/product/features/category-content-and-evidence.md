# Category content and evidence

## Meta
- Owner: Laurent Courtines
- Status: building
- Priority: P0
- Last updated: 2026-09-08

## Problem
The register carries valuable editorial reasoning, but the canonical CSV still
has duplicate compatibility columns and 8 rows that are not final declarations
or empty findings. The content now needs two explicit contracts: the CSV
migration contract for the live site and the Constitution-backed case/evidence
contract for any new terminal ruling.

## Target users
- [Founder-operator](../../users/personas.md) — author and reviewer
- [External durable-goods shopper](../../users/personas.md) — future reader

## Success metrics
- One documented field per concept; no duplicate reasoning/disqualifier columns.
- Every current row is either `DECLARED` with one model or `EMPTY`, unless a
  deliberate decision records why a temporary review state remains.
- The current 68-row baseline can be audited and the register can grow toward
  100 without bypassing the evidence rules.
- North-star progress is tracked in [product metrics](../metrics.md).

## Risks
The one-answer rule may force false precision when a category genuinely splits;
the answer may also be weakened by unsupported product claims or stale evidence.
The current row count and the 100-category ambition can reward breadth over rigor.

## Dependencies
Canonical CSV, Constitution, evidence ledger, case schemas, validator, content
guide/templates, category research, and explicit editorial decisions for the
in-review rows.

## Timeline
Resolve schema ambiguity and current in-review rows before treating the 100-
category milestone as a launch gate.

## Evidence
- The data model records 22 columns, including duplicate compatibility fields,
  and defines the status semantics [source/data-model](../../../source/adhoc/2026-09-03-project-baseline/docs/DATA_MODEL.md).
- The consolidation plan counts 48 `DECLARED`, 12 `EMPTY`, and 8 unresolved
  rows in the baseline [source/launch-plan](../../../source/adhoc/2026-09-03-project-baseline/CONSOLIDATION_AND_LAUNCH_PLAN.md).
- The editorial guide states that a category should end with one defensible
  model or an honest empty finding [source/content-guide](../../../source/adhoc/2026-09-03-project-baseline/docs/CONTENT_GUIDE.md).
- The Constitution requires three verified evidence items across independent
  classes, primary technical/service evidence, a counter-case, and confidence
  of at least 4/5 before a terminal ruling [constitution](../../../constitution/CONSTITUTION.md).

## Linked
- Hypotheses: [category-content-and-evidence](../../../hypotheses/category-content-and-evidence.md)
- Decisions: [2026-09-03 rebuild decision](../../../decisions/2026-09-03-rebuild-as-astro-single-repo.md)
- Metrics: [product metrics](../metrics.md)
- Stakeholders affected: [Laurent Courtines](../../../stakeholders/laurent-courtines.md)

## Open questions
- Which existing in-review rows should resolve to `EMPTY`, and which need a
  narrower category definition?
- Which evidence classes and source roles are most probative for each product
  family while still satisfying the constitutional floor?
- When should a validated case replace the corresponding CSV row in the public
  projection?

## Follow-up after launch
Track revision frequency, revoked declarations, and categories that repeatedly
return to review. Use those signals to improve the editorial process rather than
quietly weakening the rule.
