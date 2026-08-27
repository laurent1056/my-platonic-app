# SEO Metadata

Astro renders unique metadata directly into every static HTML page.

## Implemented

- crawlable category URLs
- unique title and description per dossier
- canonical URL per page
- Open Graph and Twitter metadata
- `robots.txt`
- generated XML sitemap via `@astrojs/sitemap`
- semantic headings and landmarks

## Category titles

- declared: `Category — Model · Platonic Ideal`
- empty: `Category — No product qualifies. · Platonic Ideal`
- in review: `Category — Declaration withheld. · Platonic Ideal`

Real non-placeholder images become `og:image` values. Placeholder URLs are intentionally excluded.
