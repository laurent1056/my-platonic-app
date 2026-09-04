# Deployment

Platonic Ideal deploys as a static Astro site to GitHub Pages.

## Configuration

- repository: `laurent1056/my-platonic-app`
- source branch: `main`
- public URL: `https://laurent1056.github.io/my-platonic-app/`
- Astro `site`: `https://laurent1056.github.io`
- Astro `base`: `/my-platonic-app`

## Workflow

`.github/workflows/deploy.yml` runs on pushes to `main`:

1. check out the repository
2. install dependencies under Node 24
3. run data validation and the Astro build
4. upload the static artifact
5. deploy through the `github-pages` environment

In GitHub → Settings → Pages, set **Source** to **GitHub Actions**. The retired `gh-pages` branch is not the publishing source for the rebuild.

## Post-deploy verification

- home page and fonts load under the repository base path
- register contains 68 entries
- a DECLARED, EMPTY, and IN REVIEW dossier open at unique URLs
- methodology and Oracle routes load
- `sitemap-index.xml` and `robots.txt` resolve
- page source contains a unique canonical URL and description
