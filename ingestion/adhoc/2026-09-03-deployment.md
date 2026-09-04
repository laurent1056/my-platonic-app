# Ingestion: deployment contract

- Captured: 2026-09-03
- Shape: adhoc migration
- Source: [verbatim deployment guide](../../source/adhoc/2026-09-03-project-baseline/docs/DEPLOYMENT.md)

## Observation

- The target is GitHub Pages for `laurent1056/my-platonic-app`, with Astro base path `/my-platonic-app`.
- GitHub Actions on `main` validates and builds the site, uploads the artifact, and deploys through the GitHub Pages environment.
- Post-deploy checks include home, declared/empty/in-review routes, methodology, Oracle, sitemap, robots, canonical URLs, and the 68-entry register.

## Interpretation / route

Route to rules/shipping, static-register, and the architecture decision.

## Open question

- Public deployment remains an externally visible action requiring separate approval.
