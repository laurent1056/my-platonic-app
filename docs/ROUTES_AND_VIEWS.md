# Routes and Views

Platonic Ideal is a static-first Astro site on Vercel. Navigation uses real URLs and every category dossier is independently crawlable.

## Routes

- `/` — orientation, census, searchable register, featured declaration
- `/category/[slug]/` — one prerendered dossier per CSV row
- `/methodology/` — admission test, evidence, EMPTY, and revocation policy
- `/constitution/` — digest-pinned public authority, evidence floor, challenge boundary, and commercial independence
- `/404.html` — absent route treatment

The Oracle is an editorial tool, not a public route. Its retired browser implementation is preserved under `src/studio/` until it is rebuilt as a local authoring workflow against the canonical Constitution.

## Category branches

- `DECLARED` — product icon or real image, gold nimbus, named model, complete argument
- `EMPTY` — struck specimen bay, “No product qualifies,” apophatic requirements
- all other source statuses — public `IN REVIEW` state with the precise source status retained

## URL behavior

Slugs are generated from category names in `src/data/register.ts`. Astro produces all category routes at build time through `getStaticPaths()`.
