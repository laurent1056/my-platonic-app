# Decision: Rebuild Platonic Ideal as one Astro repository with a founder-first v1

## Status
decided

## Date
2026-09-03

## Context
The project inherited multiple app lineages, duplicate repositories, and a
design direction that needed to be made concrete. The product needs one
canonical home and a v1 that is useful before commerce, community, or external
validation is added.

## Options considered
1. Continue iterating on the old React/Gemini export and its mixed schemas.
2. Rebuild the application in Astro + Tailwind inside the single existing
   `my-platonic-app` repository.
3. Start a new public repository and postpone product work until the structure
   is resolved.

## Decision
Use the existing GitHub repository as the only active home. Rebuild the product
from scratch in Astro + Tailwind, retain the category data, rulebook, and useful
docs, and focus v1 on the index, crawlable category pages, product images, and
the private Oracle authoring tool. Treat revenue, public submissions, and
commerce as later decisions.

## Why
Astro matches the need for static, crawlable category dossiers. A clean rebuild
removes the Gemini-era architecture and schema confusion while preserving the
editorial work that gives the product its identity. The founder-first scope
matches the only current stakeholder and lets the product earn clarity before
commercial or community complexity is introduced.

## Evidence
- The current application is already structured as an Astro static site with CSV-driven routes and a private Oracle [source/adhoc/2026-09-03-project-baseline/README.md](../source/adhoc/2026-09-03-project-baseline/README.md)
- The product requirements define a static catalog with category pages and explicitly exclude e-commerce, accounts, community features, and backend APIs [source/adhoc/2026-09-03-project-baseline/docs/PRD.md](../source/adhoc/2026-09-03-project-baseline/docs/PRD.md)
- Laurent selected Astro + Tailwind, the catalog/spec-sheet direction, and the index/category/images/Oracle v1 scope (stakeholder-verbal, Laurent, 2026-09-03)
- Laurent stated that he is the only stakeholder and primary customer for now (stakeholder-verbal, Laurent, 2026-09-03)

## Explicitly NOT doing
- Continue the old React/Gemini export as the active architecture [source/adhoc/2026-09-03-project-baseline/CONSOLIDATION_AND_LAUNCH_PLAN.md](../source/adhoc/2026-09-03-project-baseline/CONSOLIDATION_AND_LAUNCH_PLAN.md)
- Add public submissions, voting, comments, accounts, or community moderation in v1 [source/adhoc/2026-09-03-project-baseline/docs/PRD.md](../source/adhoc/2026-09-03-project-baseline/docs/PRD.md)
- Commit to a revenue model before the editorial register and founder-facing product are coherent (stakeholder-verbal, Laurent, 2026-09-03)

## What would reverse this
Revisit the architecture if the Astro build cannot generate a green, crawlable
category dossier for every canonical CSV row by 2026-09-30, or revisit the
founder-first scope if Laurent explicitly approves an external stakeholder,
public submission, or revenue experiment before that date.

## Remaining ambiguities
- The future revenue model and its editorial disclosure requirements are not
  decided.
- The current 8 in-review category rows still need individual editorial
  resolution.
- There is no external behavioral evidence for the public audience yet.

## Linked
- Strategy: [knowledge/strategy.md](../knowledge/strategy.md) § North-star metric, Priorities, Tensions
- Stakeholders informed: [stakeholders/laurent-courtines.md](../stakeholders/laurent-courtines.md)
