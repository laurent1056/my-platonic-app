# Ingestion: data model

- Captured: 2026-09-03
- Shape: adhoc migration
- Source: [verbatim data model](../../source/adhoc/2026-09-03-project-baseline/docs/DATA_MODEL.md)

## Observation

- The site is powered by `public/platonic_ideal.csv` and maps status, model, reasoning, disqualifiers, admission test, failure modes, review date, and image URL into static category pages.
- Status semantics include `DECLARED`, `EMPTY`, `CANDIDATE`, `SPLIT_REQUIRED`, `CONDITIONAL`, and `CONSUMABLE`.
- The current mapper preserves compatibility columns and derives slugs from category names.

## Interpretation / route

Route to rules/data, category-content-and-evidence, and the schema-cleanup task.

## Open question

- Freeze one field name per concept without losing useful inherited content.
