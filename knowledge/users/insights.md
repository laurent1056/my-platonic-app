# User Insights

> Synthesized themes from interviews + analytics. Working memory lives in `ingestion/`. Items get promoted here only when they meet the [memory promotion bar](../../CLAUDE.md#memory-promotion--working-vs-long-term): recurring, decision-relevant, observed across sources, useful beyond one session.

## Provenance vocabulary

Every supporting-evidence row carries a provenance tag from the enum defined in `../../hypotheses/_SCHEMA.md`. The same rule applies here: tag honestly, don't fabricate. Path-typed tags (`[ingestion/...]`, `[source/...]`) MUST be working links.

## Active themes
<!-- Synthesized themes that are shaping current work. Each entry: theme + evidence rows (each tagged) + decision/feature relevance. -->

### The first user is the founder seeking decision relief
- **Evidence:**
  - Laurent explicitly describes himself as the primary customer and wants to make what he wants to see first (stakeholder-verbal, Laurent, 2026-09-03).
  - The product requirements frame the register as a tool for making durable, repairable decisions legible [source/adhoc/2026-09-03-project-baseline/docs/PRD.md](../../source/adhoc/2026-09-03-project-baseline/docs/PRD.md)
- **Relevance:** Shapes v1 toward a fast, opinionated category verdict and founder usability loop rather than community mechanics or revenue optimization.

### Integrity of the empty verdict is part of the value
- **Evidence:**
  - The inherited PRD treats `EMPTY` as a first-class category state rather than a missing result [source/adhoc/2026-09-03-project-baseline/docs/PRD.md](../../source/adhoc/2026-09-03-project-baseline/docs/PRD.md)
  - The inherited design language defines the empty state through apophatic reasoning and asks it to retain dignity [source/adhoc/2026-09-03-project-baseline/docs/design/design.md](../../source/adhoc/2026-09-03-project-baseline/docs/design/design.md)
- **Relevance:** Informs category page hierarchy, copy, imagery, and the one-declaration-or-empty integrity check.

## Contradictions
<!-- Where users meaningfully disagree. Preserve. Do not collapse into false consensus. Each side carries its own provenance tags. -->

### Founder utility is known; public demand is not
- **Side A:** The current product is intentionally founder-led, with Laurent as the primary customer (stakeholder-verbal, Laurent, 2026-09-03).
- **Side B:** The docs describe a public register and eventual broader use, but no external user interviews or behavioral data have been captured yet [source/adhoc/2026-09-03-project-baseline/docs/PRD.md](../../source/adhoc/2026-09-03-project-baseline/docs/PRD.md)
- **Why preserved:** It keeps the self-use strategy honest without pretending the public product is already validated.

## Retired
<!-- Themes that no longer hold or have been superseded. Keep them — they prevent re-running wrong assumptions. Note WHY retired and link the superseding evidence. -->

## TODO
Add external user evidence only when it exists; do not convert founder preference
into a general customer insight.
