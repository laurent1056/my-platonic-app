# Platonic Ideal

**One product per category. Or none.**

Platonic Ideal is a static editorial register of durable objects. Every category resolves to one named model that approaches the Form—or an explicit EMPTY finding explaining why no current product qualifies.

## Product surface

- searchable and sortable 68-entry register
- 68 crawlable category dossiers generated at build time
- first-class DECLARED, EMPTY, and IN REVIEW treatments
- methodology and public editorial standard
- private, browser-based Oracle drafting studio
- responsive light and dark themes
- per-page canonical metadata and XML sitemap
- CSV validation before every production build

## Stack

- [Astro](https://astro.build/) — static pages and build-time data mapping
- Tailwind CSS v4 — utility layer and token integration
- Papa Parse — canonical CSV parsing
- GitHub Pages — static hosting through GitHub Actions

## Development

```bash
npm install
npm run dev
npm run check
npm run build
npm run preview
```

`npm run build` validates the canonical data before producing 72 static pages.

## Canonical data

All editorial content originates in:

- `public/platonic_ideal.csv`

The build-time mapper is `src/data/register.ts`. It normalizes compatibility columns and generates stable category slugs. The validator is `scripts/validate-register.mjs`.

## Architecture

```text
src/
  components/       shared visual and semantic patterns
  data/register.ts  CSV → typed register entries
  layouts/          global metadata, navigation, footer
  pages/
    index.astro
    methodology.astro
    oracle.astro
    category/[slug].astro
  styles/global.css design tokens and responsive system
public/
  platonic_ideal.csv
scripts/
  validate-register.mjs
```

## Design

The visual system is documented in `docs/design/design.md`: a modern information register informed by the Greek stele, Orthodox icon panels, and the apophatic tradition. Classical flourishes encode meaning; they are not decorative wallpaper.

## Deployment

Pushes to `main` run `.github/workflows/deploy.yml`, which validates, builds, uploads, and deploys the site through GitHub Pages. Repository Pages settings must use **GitHub Actions** as the publishing source.

Public URL: `https://laurent1056.github.io/my-platonic-app/`

## Documentation

Product, editorial, data, accessibility, security, testing, SEO, and design documentation lives in `docs/`.
