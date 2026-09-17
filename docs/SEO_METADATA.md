# SEO Metadata

Astro renders search and social metadata directly into every static HTML page.

## Implemented

- crawlable category URLs
- unique, normalized, length-bounded title and description per page
- canonical URL per page
- absolute Open Graph and Twitter metadata, including image alt text
- JSON-LD for the organization, website, web page, and available breadcrumbs
- `robots.txt`
- generated XML sitemap via `@astrojs/sitemap`
- semantic headings and landmarks
- `noindex` on preview-only routes and the 404 document
- intrinsic dimensions on product plates to reserve image layout space

## Category titles

- declared: `Category: Model · Platonic Ideal`
- empty: `Category: No qualifying pick · Platonic Ideal`
- in review: `Category: Still researching · Platonic Ideal`

Category-specific plates become absolute `og:image` values. Pages without a plate use the approved Platonic Ideal editorial portrait as a consistent social fallback; no placeholder product URLs are emitted.
