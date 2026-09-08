# Security and Privacy

## Current model

- static-first site on Vercel
- no user accounts
- no public mutation endpoint or server-side persistence in the current release

## Oracle caveat

- the Oracle is not emitted into the public build
- its retired browser implementation is preserved under `src/studio/` as migration reference only
- the replacement will run as a local editorial workflow and will consume the canonical Constitution
- no Oracle output may publish or mutate canonical content without human review
- credentials remain local environment values and must never enter Git, browser storage, or generated output

## Privacy posture

- no analytics integration is part of the current tracked product
- no cookies are required for browsing the catalog
- a future challenge-intake endpoint requires a separate retention, validation, bot-protection, and private-storage review before activation

## Dependency audit

CI audits production dependencies at high severity before building. `package.json`
temporarily overrides the Vercel routing utility's legacy `path-to-regexp@6.1.0`
dependency with patched `6.3.0` (GHSA-9wv6-86v2-598j). Remove the override when
Vercel drops the legacy dependency, after confirming `npm audit` remains clean.
