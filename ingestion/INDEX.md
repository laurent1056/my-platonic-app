# Ingestion Modes

Every mode follows the same shape: **preserve source → load → process → route updates → surface what changed.**

**Step 0 for every mode** — copy the raw artifact verbatim to `source/<kind>/YYYY-MM-DD-<slug>.md` *before* any extraction or synthesis. The `source/` file is the audit anchor and never gets edited again. The matching `ingestion/<kind>/<same-name>.md` (created during synthesis) must link back to it. See repo-root `CLAUDE.md § Source preservation`.

All modes feed back into strategy when relevant — opportunities, user needs, and market signals can inform `knowledge/strategy.md` just as much as strategy informs which signals matter. When an ingested signal conflicts with strategy, append to `strategy.md § Tensions`. Do not reject the signal automatically.

## 1. Customer interview (`/ingest interview <file>` or paste transcript)

Input: transcript (raw or lightly cleaned).
Process:
0. **Preserve source.** Copy the raw input verbatim to `source/interviews/YYYY-MM-DD-<participant>.md` before anything else.
1. Extract: pains, JTBDs, current alternatives, surprising quotes, contradictions with prior insights.
2. Map to existing personas / segments (`knowledge/users/`).
3. Compare against active hypotheses — does anything confirm or contradict?
4. Generate up to 3 new hypothesis candidates if signal warrants.

Updates:
- `knowledge/users/insights.md` — themes
- `knowledge/users/personas.md` / `segments.md` — only if a persona meaningfully shifts
- `hypotheses/<feature>.md` — evidence-for / evidence-against entries (each linking to the matching `source/interviews/...md`)
- `ingestion/interviews/YYYY-MM-DD-<participant>.md` — synthesized record, with a link to its `source/` file

Surface: "Affected hypotheses: …. New candidates: …. Persona drift detected: yes/no."

## 2. Meeting / 1:1 notes (`/ingest meeting <file>`)

Input: notes from a 1:1, review, or cross-functional sync.
Process:
0. **Preserve source.** Copy raw notes verbatim to `source/meetings/YYYY-MM-DD-<topic>.md`.
1. Extract: decisions made, action items (mine vs theirs), stakeholder-specific signals, open questions.
2. If stakeholder(s) identifiable, update their `stakeholders/<slug>.md` (touchpoint log, open asks, concerns).
3. If a decision was made, draft a record in `decisions/` for PM confirmation.

Updates:
- `stakeholders/<slug>.md`
- `decisions/YYYY-MM-DD-<slug>.md` (draft) — link to the `source/` file as evidence
- `ingestion/meetings/YYYY-MM-DD-<topic>.md` — synthesized record, with a link to its `source/` file

## 3. Market / competitor intel (`/ingest market <url-or-file>`)

Input: article, screenshot, tweet, competitor changelog, analyst note.
Process:
0. **Preserve source.** Save URL + retrieved-at + full text/quote verbatim to `source/market/YYYY-MM-DD-<slug>.md`. For images, link the file in `source/market/assets/` and describe what was seen.
1. Identify which competitor / trend it touches.
2. Update the relevant file in `knowledge/market/competitors/` or `trends.md`.
3. Flag any active hypothesis or strategy element it contradicts or supports.

Updates:
- `knowledge/market/competitors/<slug>.md` or `trends.md` — link the `source/` file as the citation
- `hypotheses/*` if directly relevant
- `knowledge/strategy.md § Tensions` if the signal conflicts with strategy

## 4. Ad-hoc (`/ingest adhoc` or any unstructured dump)

Input: anything the PM thinks is worth capturing but isn't an interview / meeting / market signal.
Process:
0. **Preserve source.** Save the dump verbatim to `source/adhoc/YYYY-MM-DD-<slug>.md`.
1. Read it. Decide where it belongs.
2. If unclear, ask **one** question to disambiguate.
3. Route to the right area file. Never park indefinitely in `ingestion/adhoc/` — that folder is a sorting bench, not a graveyard.

Rule: every adhoc item is resolved (routed or discarded) within the same session. The `source/adhoc/` copy stays forever even if the synthesized `ingestion/adhoc/` record is deleted after routing.

## Migrated baseline records — 2026-09-03

The initial brain was seeded from the 24-file project snapshot. These are
working-memory records, each linked to its verbatim source artifact:

- [README](./adhoc/2026-09-03-readme.md)
- [Contributing](./adhoc/2026-09-03-contributing.md)
- [Consolidation and launch plan](./adhoc/2026-09-03-consolidation-launch-plan.md)
- [Canonical register CSV](./adhoc/2026-09-03-canonical-register-csv.md)
- [Accessibility](./adhoc/2026-09-03-accessibility.md)
- [Content guide](./adhoc/2026-09-03-content-guide.md)
- [Content templates](./adhoc/2026-09-03-content-templates.md)
- [Data model](./adhoc/2026-09-03-data-model.md)
- [Deployment](./adhoc/2026-09-03-deployment.md)
- [Design system](./adhoc/2026-09-03-design-system.md)
- [Editorial glossary](./adhoc/2026-09-03-editorial-glossary.md)
- [Oracle feature](./adhoc/2026-09-03-oracle-feature.md)
- [Product requirements](./adhoc/2026-09-03-prd.md)
- [Routes and views](./adhoc/2026-09-03-routes-views.md)
- [Search and filter](./adhoc/2026-09-03-search-filter.md)
- [Security and privacy](./adhoc/2026-09-03-security-privacy.md)
- [SEO metadata](./adhoc/2026-09-03-seo-metadata.md)
- [Testing](./adhoc/2026-09-03-testing.md)
- [Image credits](./adhoc/2026-09-03-image-credits.md)
- [Design language](./adhoc/2026-09-03-design-language.md)
- [Product image URL notes](./adhoc/2026-09-03-product-image-url-notes.md)
- [Product image help artifact](./adhoc/2026-09-03-product-image-help.md)
- [Vision PRD](./adhoc/2026-09-03-vision-prd.md)
- [Vision spreadsheet](./adhoc/2026-09-03-vision-spreadsheet.md)
