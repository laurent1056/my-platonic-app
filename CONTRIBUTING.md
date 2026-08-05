# Contributing

Platonic Ideal is intentionally content-driven and opinionated.

## Current ground rules

- The canonical implementation is this repo's app and data only.
- The canonical dataset is `public/platonic_ideal.csv`.
- Every category resolves to one declaration, one empty verdict, or a clearly labeled non-final status such as `CANDIDATE`.
- Do not reintroduce duplicate CSVs, alternate schemas, or parallel app copies into the tracked project.

## Content changes

- Edit `public/platonic_ideal.csv`.
- Preserve the current 22-column header set and order.
- Keep tone calm, specific, and non-promotional.
- Prefer expanding existing fields over inventing new columns.
- If a field is blank and the app already supports it, fill it with useful content before proposing code changes.

## Front-end changes

- Keep the current five views only: `home`, `index`, `category`, `methodology`, `oracle`.
- Preserve GitHub Pages compatibility and the existing lightweight SPA structure.
- SEO work should stay truthful to the static SPA; do not imply server rendering or crawlable per-category routes that do not exist.

## Before merging

- Run `npm run build`.
- Run `npm run lint`.
- Check at least:
  - one `DECLARED` category
  - one `EMPTY` category
  - one `CANDIDATE` category
  - the Methodology view
  - the Oracle view

