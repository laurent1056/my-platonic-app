# Testing

## Required checks

- `npm run build`
- `npm run lint`

## Smoke test matrix

Check at least:

- Home view loads and search filters cards
- Index view search, filter, and sort work
- Category page renders for:
  - one `DECLARED` row
  - one `EMPTY` row
  - one `CANDIDATE` row
- Methodology view loads
- Oracle view loads without breaking the app

## Data checks

- only `public/platonic_ideal.csv` exists as the tracked dataset
- the CSV header set matches `docs/DATA_MODEL.md`
- no repo docs describe any retired duplicate dataset as active

## SEO checks

- default HTML contains title, description, OG, Twitter, and canonical tags
- runtime title changes when switching between home, index, methodology, oracle, and category views
- empty categories generate sensible titles without blank model text
