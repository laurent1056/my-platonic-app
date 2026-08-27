# Routes and Views

Platonic Ideal is an Astro static site. Navigation uses real URLs and every category dossier is independently crawlable.

## Routes

- `/my-platonic-app/` — orientation, census, searchable register, featured declaration
- `/my-platonic-app/category/[slug]/` — one static dossier per CSV row
- `/my-platonic-app/methodology/` — admission test, evidence, EMPTY, and revocation policy
- `/my-platonic-app/oracle/` — private browser-based authoring studio
- `/my-platonic-app/404.html` — absent route treatment

## Category branches

- `DECLARED` — product icon or real image, gold nimbus, named model, complete argument
- `EMPTY` — struck specimen bay, “No product qualifies,” apophatic requirements
- all other source statuses — public `IN REVIEW` state with the precise source status retained

## URL behavior

Slugs are generated from category names in `src/data/register.ts`. Astro produces all category routes at build time through `getStaticPaths()`.
