# Static register and category dossiers

## Meta
- Owner: Laurent Courtines
- Status: building
- Priority: P0
- Last updated: 2026-09-03

## Problem
The product's value is lost if a reader cannot move from the register to a
clear, independently linkable category verdict. The Astro rebuild should make
the index, category dossier, `DECLARED`, and `EMPTY` states feel like one
coherent instrument.

## Target users
- [Founder-operator](../../users/personas.md) — current primary user
- [External durable-goods shopper](../../users/personas.md) — future, unvalidated audience

## Success metrics
- Every canonical CSV row produces a stable category route and useful metadata.
- The index makes the model-or-empty verdict legible without requiring a
  comparison table.
- `npm run check`, `npm run validate:data`, and `npm run build` pass.
- North-star progress is tracked in [product metrics](../metrics.md).

## Risks
The singular editorial rule can be undermined by unresolved statuses, missing
content, or a visually impressive page that does not help a decision. The
public usefulness of the register is not externally validated yet.

## Dependencies
Canonical CSV, Astro route generation, design tokens/components, data validator,
metadata/sitemap configuration, and the eventual image fallback policy.

## Timeline
Current build phase; complete a founder-usable slice before expanding scope.

## Evidence
- The current product requirements make the index and category dossier the core
  product surface [source/PRD](../../../source/adhoc/2026-09-03-project-baseline/docs/PRD.md).
- The current application already uses Astro, CSV-driven routes, and a private
  Oracle [source/README](../../../source/adhoc/2026-09-03-project-baseline/README.md).

## Linked
- Hypotheses: [static-register](../../../hypotheses/static-register.md)
- Decisions: [2026-09-03 rebuild decision](../../../decisions/2026-09-03-rebuild-as-astro-single-repo.md)
- Metrics: [product metrics](../metrics.md)
- Stakeholders affected: [Laurent Courtines](../../../stakeholders/laurent-courtines.md)

## Open questions
- Which category-page interaction most clearly ends the search: the verdict,
  evidence, disqualifiers, or a product link?
- When should the first external usability check happen?

## Follow-up after launch
Use founder sessions first. If public measurement is deliberately added later,
check dossier opens, return visits, and outbound product-link interest during an
initial two-week observation window.
