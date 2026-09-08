# Contributing

Platonic Ideal is intentionally content-driven and opinionated.

## Current ground rules

- The canonical implementation is this repo's app and data only.
- The canonical dataset is `public/platonic_ideal.csv`.
- The normative authority for new adjudication is `constitution/CONSTITUTION.md`
  plus its digest-pinned machine profile; the CSV remains migration-compatible
  until a row is explicitly re-adjudicated.
- Every category resolves to one declaration, one empty verdict, or a clearly labeled non-final status such as `CANDIDATE`.
- Do not reintroduce duplicate CSVs, alternate schemas, or parallel app copies into the tracked project.

## Content changes

- Edit `public/platonic_ideal.csv`.
- Preserve the current 22-column header set and order.
- Keep tone calm, specific, and non-promotional.
- Prefer expanding existing fields over inventing new columns.
- If a field is blank and the app already supports it, fill it with useful content before proposing code changes.

## Front-end changes

- Keep public editorial routes prerendered unless a server boundary is explicitly justified.
- Preserve root-hosted Vercel URLs, unique category routes, truthful canonical metadata, and the lightweight Astro architecture.
- Do not expose the Oracle as a public route. Its source under `src/studio/` is migration reference for a future local authoring tool.
- Add server endpoints narrowly; validate input, document secrets and retention, and keep external submissions outside canonical Git content until editorially admitted.

## Before merging

- Run `npm test`.
- Run `npm run validate:institution` when editing a Constitution, evidence,
  case, ruling, or challenge record.
- Check at least:
  - one `DECLARED` category
  - one `EMPTY` category
  - one `CANDIDATE` category
  - the Methodology view
  - the public `/constitution/` route and its canonical metadata
  - root assets, sitemap, canonical URLs, and `/my-platonic-app/*` redirects on a Vercel preview
  - that `/oracle/` is not publicly emitted
