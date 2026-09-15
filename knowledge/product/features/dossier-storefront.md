# Dossier storefront

## Meta
- Owner: Laurent Courtines
- Status: design prototype implemented locally
- Last updated: 2026-09-14

## Intent
The user requested standard ecommerce page patterns, then clarified that the
single commercial product is the dossier and every page should lead to it
(chat, no artifact). Physical products remain editorial subjects.

## Implemented
- Dossier-focused home, one product detail page, shared site-wide offer, nine
  collection routes, and searchable visual catalog preserving existing filters.
- Cart, no-charge checkout, confirmation, account, saved items, journal, support,
  and situational page templates. All share the same dossier destination.
- Existing $24 one-time offer used as a design reference. Public decisive
  reasoning remains free; canonical CSV and institution records are unchanged.
- Account and purchase workflows are local previews, not live authentication,
  transactions, delivery, or purchase entitlements.

## Evidence and validation
- Implementation and route map: [design pass](../../../docs/design/dossier-storefront.md).
- Commercial boundary: [accepted decision](../../../decisions/2026-09-08-constitution-and-paid-dossier-boundary.md).
- Generated 146 pages including all 100 category routes; automated build and
  storefront checks plus desktop/mobile browser review.

## Remaining work
Final dossier content and coverage, payment, delivery, account policy, verified
support contact, and production legal notices remain unimplemented. This design
pass does not supersede the founding-case evidence or validation requirements.
