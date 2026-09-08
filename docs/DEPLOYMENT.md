# Deployment

Platonic Ideal deploys from `main` to Vercel as a static-first Astro application. Public editorial pages are prerendered; server endpoints may be added selectively through the Vercel adapter.

## Configuration

- repository: `laurent1056/my-platonic-app`
- source branch: `main`
- Vercel project: `laurent1056-4779s-projects/my-platonic-app`
- production URL: `https://my-platonic-app.vercel.app/`
- Astro `site`: `https://my-platonic-app.vercel.app`
- Astro `base`: none; the site is served from `/`
- framework adapter: `@astrojs/vercel`

Set `SITE_URL` at build time only when moving production to a custom domain. Preview deployments intentionally retain the production canonical origin.

## Delivery workflow

Vercel's Git integration creates a preview for non-production branches and a production deployment for `main`. GitHub Actions does not publish the application; `.github/workflows/ci.yml` independently runs:

1. `npm ci`
2. Astro type checking
3. CSV validation
4. the Astro production build
5. generated-output verification

The output verifier fails when generated pages contain the retired GitHub origin or `/my-platonic-app/` base, when internal assets do not resolve, when canonical URLs are wrong, when the Oracle is public, or when required category routes are absent.

## Parallel cutover

The former GitHub Pages deployment remains available as a temporary rollback target for seven days after the Vercel production build passes verification. Do not delete the `gh-pages` branch during that window.

After the rollback window:

1. confirm production and preview deployments are healthy
2. remove GitHub Pages as an active publishing target
3. replace the old Pages site with a redirect if preserving its inbound links is valuable
4. remove the `gh-pages` branch only after explicit confirmation

## Post-deploy verification

- `/`, `/methodology/`, and representative `DECLARED`, `EMPTY`, and `IN REVIEW` category routes return `200`
- CSS, fonts, the favicon, and Plato portrait resolve from root-relative URLs
- `/my-platonic-app/*` redirects to the equivalent root route
- the public `/oracle/` route returns `404`
- the register contains 68 pre-canon source entries until the constitutional migration changes that contract
- `sitemap-index.xml` and `robots.txt` use the production origin
- every page contains a unique production canonical URL and description
- no browser console errors occur in desktop or mobile smoke tests

## Rollback

If the Vercel deployment fails after promotion, restore traffic to the frozen GitHub Pages target and revert the responsible `main` commit. Do not edit generated Vercel output or the rollback branch by hand.
