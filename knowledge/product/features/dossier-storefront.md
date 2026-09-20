# Dossier storefront

## Meta
- Owner: Laurent Courtines
- Status: Stripe-hosted purchase flow implemented; external launch configuration remains
- Last updated: 2026-09-19

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
- Account and legacy cart/checkout workflows remain local previews; the paid
  path now uses Stripe-hosted checkout rather than a site-hosted payment form.
- A concrete 157-page declared-edition PDF now exists locally, covering 48
  recommendations. The storefront now identifies that edition as the paid
  product and exposes the stable edition ID `platonic-ideal-declared-1940`
  [declared dossier](../../../source/adhoc/2026-09-18-platonic-ideal-dossier-declared-1940.pdf).
- The public 100-category catalog remains free. The paid offer is explicitly
  the 48-recommendation declared edition; it does not claim to be a paid copy
  of all 100 public categories [homepage snapshot](../../../source/market/2026-09-18-platonic-ideal-homepage.md).
- The implementation includes a Stripe Payment Link creation script, a
  server-side Stripe webhook, a paid-session check, a private Vercel Blob
  download route, and an optional Resend delivery email.

## Evidence and validation
- Implementation and route map: [design pass](../../../docs/design/dossier-storefront.md).
- Commercial boundary: [accepted decision](../../../decisions/2026-09-08-constitution-and-paid-dossier-boundary.md).
- Generated 146 pages including all 100 category routes; automated build and
  storefront checks plus desktop/mobile browser review.

## Remaining work
- Create the live Stripe product, one-time price, Payment Link, and webhook
  endpoint using the deployment configuration documented in the repository.
- Upload the 157-page PDF to a private Vercel Blob store and set its pathname;
  the paid file is intentionally not committed to `public/`.
- Add the production Stripe, Blob, and (optionally) Resend environment values
  in Vercel, then complete a Stripe test-mode purchase and webhook replay before
  enabling live mode.
- Replace the remaining preview privacy, terms, refund, and support copy with
  approved production policies before accepting public sales.
- The public register still has 40 non-terminal editorial rows; that remains a
  catalog-quality issue, not a claim that the paid edition covers those rows.
