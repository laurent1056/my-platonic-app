# Testing

## Required commands

```bash
npm run validate:data
npm run validate:institution
npm run check
npm run build
npm run audit:prod
npm test
```

## Current build contract

- validator accepts all 68 rows and blocks malformed CSV, duplicate slugs, invalid statuses, and declaration/model violations
- Astro type check returns zero errors, warnings, or hints
- production build generates 72 HTML pages plus the sitemap after retiring the public Oracle and adding the Constitution route
- generated-output verification rejects the retired GitHub origin and repository base path, broken internal references, invalid canonical URLs, and a public Oracle route

## Browser smoke matrix

- desktop and 390px mobile layouts have no body-level horizontal overflow
- mobile register uses dedicated stacked rows; desktop uses the data table
- search, status filter, and all three sort modes update both layouts
- category pages render for DECLARED, EMPTY, and IN REVIEW
- light/dark switch persists on the device
- methodology loads and anchors navigate correctly
- `/oracle/` is absent from the public build
- `/my-platonic-app/*` redirects to the equivalent root route on Vercel
- browser console remains free of errors

## Accessibility checks

- keyboard-visible focus on every interactive element
- 44px minimum primary controls and mobile register targets
- light and dark text/state contrast meet WCAG 2.1 AA
- table headings, page landmarks, form labels, verdict text, and image alternatives remain semantic
