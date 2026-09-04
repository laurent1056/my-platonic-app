# Testing

## Required commands

```bash
npm run validate:data
npm run check
npm run build
```

## Current build contract

- validator accepts all 68 rows and blocks malformed CSV, duplicate slugs, invalid statuses, and declaration/model violations
- Astro type check returns zero errors, warnings, or hints
- production build generates 72 pages plus the sitemap

## Browser smoke matrix

- desktop and 390px mobile layouts have no body-level horizontal overflow
- mobile register uses dedicated stacked rows; desktop uses the data table
- search, status filter, and all three sort modes update both layouts
- category pages render for DECLARED, EMPTY, and IN REVIEW
- light/dark switch persists on the device
- methodology loads and anchors navigate correctly
- Oracle loads with no key and does not affect browsing
- browser console remains free of errors

## Accessibility checks

- keyboard-visible focus on every interactive element
- 44px minimum primary controls and mobile register targets
- light and dark text/state contrast meet WCAG 2.1 AA
- table headings, page landmarks, form labels, verdict text, and image alternatives remain semantic
