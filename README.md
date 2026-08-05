# Platonic Ideal

A React-based catalog for durable, rebuildable products. Each category resolves to exactly one product declaration or EMPTY with explicit reasoning.

## Features

- Searchable category index
- Category detail pages with reasoning, caveats, and failure modes
- Methodology page describing the declaration standard
- Oracle draft-writing tool backed by Anthropic
- CSV-driven content loaded from `public/platonic_ideal.csv`
- Header-aware source field review for auditing CSV content in the UI
- GitHub Pages deployment with baseline SEO metadata and runtime title/description updates

## Development

```bash
npm install
npm run dev
npm run build
npm run deploy
```

## Canonical Data

The site uses one canonical dataset:

- `public/platonic_ideal.csv`

There is no secondary CSV source of truth. Content, schema, and rendered sections should reconcile back to this file.

## Documentation

Core project docs live in `docs/`:

- `docs/PRD.md`
- `docs/DATA_MODEL.md`
- `docs/CONTENT_GUIDE.md`
- `docs/CONTENT_TEMPLATES.md`
- `docs/ROUTES_AND_VIEWS.md`
- `docs/SEO_METADATA.md`
- `docs/DEPLOYMENT.md`
- `docs/TESTING.md`
- `docs/DESIGN_SYSTEM.md`
- `docs/SEARCH_AND_FILTER.md`
- `docs/ACCESSIBILITY.md`
- `docs/SECURITY_PRIVACY.md`
- `CONTRIBUTING.md`

## Project Note

This root `platonic-ideal/` directory is the canonical source project. The app uses a single primary dataset at `public/platonic_ideal.csv`, and the category view exposes populated CSV column headers as reviewable source fields in the UI.
