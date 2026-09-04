# Oracle authoring

## Meta
- Owner: Laurent Courtines
- Status: building
- Priority: P1
- Last updated: 2026-09-03

## Problem
Category research and editorial writing are judgment-heavy. The Oracle should
help draft and critique an entry against the rulebook without becoming an
automatic publisher, a source of truth, or a replacement for editorial judgment.

## Target users
- [Founder-operator](../../users/personas.md) — sole current author

## Success metrics
- Laurent can submit a category question and receive a useful draft structure.
- The tool clearly distinguishes draft assistance from canonical content.
- No Oracle interaction mutates the CSV or publishes a verdict automatically.
- The tool remains usable without a configured key and does not affect public
  browsing.

## Risks
Hallucinated product facts, stale model knowledge, API-key handling, prompt
drift from the current schema, and false confidence could damage editorial trust.

## Dependencies
Current editorial schema, privacy/security rules, browser-only API behavior,
explicit user-supplied credentials, and a human review step before CSV edits.

## Timeline
Keep aligned with the founder-facing v1; refine after real authoring sessions,
not before the category dossier flow is coherent.

## Evidence
- The feature brief says the Oracle is an optional front-end drafting helper and
  never writes the canonical CSV [source/oracle-feature](../../../source/adhoc/2026-09-03-project-baseline/docs/ORACLE_FEATURE.md).
- The security note says the browser sends a user-supplied key directly to the
  provider and output is draft text, not trusted fact [source/security](../../../source/adhoc/2026-09-03-project-baseline/docs/SECURITY_PRIVACY.md).

## Linked
- Hypotheses: [oracle-authoring](../../../hypotheses/oracle-authoring.md)
- Decisions: [2026-09-03 rebuild decision](../../../decisions/2026-09-03-rebuild-as-astro-single-repo.md)
- Metrics: [product metrics](../metrics.md)
- Stakeholders affected: [Laurent Courtines](../../../stakeholders/laurent-courtines.md)

## Open questions
- Does the Oracle prompt use the final canonical field names after schema cleanup?
- Which draft checks catch unsupported claims before Laurent copies content into
  the register?

## Follow-up after launch
Review a sample of drafts after each meaningful prompt or schema change. Treat
any unsupported factual claim or accidental mutation as a release-blocking bug
for the authoring tool.
