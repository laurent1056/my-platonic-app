# SEO Metadata

This document describes the SEO behavior the current app actually supports.

## What is implemented

### Static shell metadata in `index.html`

- title baseline
- meta description
- canonical link
- Open Graph title, description, and URL
- Twitter summary card basics
- robots tag

### Runtime metadata updates in the SPA

The app updates:

- `document.title`
- meta description
- `og:title`
- `og:description`
- `og:url`
- `twitter:title`
- `twitter:description`
- canonical link

## Current metadata strategy

### Home

- title: `Platonic Ideal`
- description: broad project summary

### Index

- title: `The Index | Platonic Ideal`
- description: category-count-based browse summary

### Methodology

- title and description explain the rules and evidence standard

### Oracle

- title and description explain the draft-assist role

### Category view

- declared rows use `Model | Category | Platonic Ideal`
- empty rows use `Category (Empty) | Platonic Ideal`
- descriptions are derived from one-liner, core reasoning, or a safe fallback

## Canonical URL policy

The app does not expose crawlable per-category routes. Because navigation is internal SPA state rather than URL state, the canonical URL remains the project root:

- `https://laurent1056.github.io/my-platonic-app/`

This is intentional and more truthful than pretending the site has static per-category pages.

## What is not implemented

- server-rendered metadata
- unique crawlable category URLs
- dynamic OG image generation
- filter-state indexing

## Verification

- inspect served HTML for default metadata tags
- navigate between views and confirm title/description changes in the browser
- ensure empty categories never produce blank or misleading titles

