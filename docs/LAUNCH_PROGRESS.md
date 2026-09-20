# Launch progress

This is the local, reversible launch-readiness record for the canonical Astro
repository. It is intentionally honest about what is implemented and what
still requires approved editorial evidence or an external service decision.

## Pass 1 — baseline and guardrails

- Changed: scoped Astro type checking away from private `tmp/` and generated
  `output/` artifacts; ignored those generated directories; added
  `npm run audit:launch`.
- Passed: `npm run check` now completes with 0 errors, 0 warnings, and 0
  hints. Baseline data is 100 rows, 48 declared, 12 empty, and 40
  non-terminal.
- Remaining: the launch audit correctly fails because 40 rows are not final,
  one declared row contains an unresolved model alternative, declared support
  fields are incomplete, and commerce/disclosures are preview-only.

## Pass 2 — public language and founder context

- Changed: the homepage now states the promise in ordinary language; public
  catalog filters expose only Our picks, No qualifying picks, and Research in
  progress; internal workflow codes are removed from public search metadata;
  the About page publishes a conservative founder-origin section from the
  approved founder record.
- Passed: internal status labels no longer appear in catalog controls, and the
  site retains the Constitution’s one-product-or-none language.
- Remaining: unresolved editorial states remain in the source register because
  the Constitution and research queue explicitly say they are not terminal
  rulings. They cannot be converted without evidence and adjudication.

## Pass 3 — evidence trail and sandbox conversion path

- Changed: category pages now show a separated evidence trail; the site records
  local, consent-gated measurement events; the homepage has a clearly marked
  email-signup preview that discards the address; the dossier has a local
  checkout-to-confirmation-to-sandbox-fulfillment path.
- Passed: `npm run check`, `npm run build`, `npm run test:storefront`, and
  generated-output verification pass. The build emits 146 pages and all 100
  category routes.
- Remaining: no real payment provider, fulfillment entitlement, email sender,
  analytics destination, refund policy, or production privacy/terms package is
  activated. The sandbox does not claim to be a live purchase.

## Pass 4 — release hygiene and local smoke test

- Changed: the register validator now treats explicit natural-language
  alternatives as a warning while allowing ordinary measurement and SKU
  slashes; preview analytics/email storage is resilient when browser storage is
  unavailable; the storefront suite asserts that internal research codes do
  not leak into the public register.
- Passed: `npm test` (typecheck, 13 institution tests, build, dist verification,
  and 7 storefront tests), `npm run audit:prod` (0 production vulnerabilities),
  and a local browser smoke test across the homepage, a declared category, an
  empty category, dossier, cart, checkout, and sandbox confirmation with no
  console errors.
- Remaining: `npm run audit:launch` remains intentionally red until the
  non-terminal categories receive evidence packets and ruling events, the
  declared support fields are complete, and Laurent approves production
  commerce, email, analytics, disclosure, and fulfillment changes.

## Pass 5 — founder narrative and refrigerator source correction

- Changed: the approved first-person founder narrative now appears as a full
  About essay and a shorter homepage founder letter. It names Laurent’s
  Catholic faith, uses “cultural conflict” rather than a narrower culture-war
  label, explains the cognitive-load problem, records the AI-building motive,
  and states the public-verdict / dossier boundary.
- Changed: the Refrigerator entry’s copied range/oven disqualifiers were
  replaced with the refrigerator-specific failure, repair, and future-product
  requirements already present in its research record.
- Passed: the refreshed About, homepage, and Refrigerator routes were checked
  in the local browser with no console errors; the build and storefront tests
  pass.
- Remaining: the founder narrative is now ready for Laurent’s own final
  read-aloud and factual sign-off. It does not resolve the separate editorial
  and production launch blockers in the release gate below.

## Current release gate

The repository is buildable and the public experience is inspectable, but it is
not launch-ready under the supplied goal. The next safe editorial pass needs
approved evidence packets and human adjudication for the 40 non-terminal rows.
The next safe commercial pass needs Laurent’s explicit approval of a payment,
email, analytics, privacy, refund, and fulfillment setup before any external
write or real customer data collection.

## Pass 6 — Stripe-hosted paid edition wiring

- Changed: the commercial offer is now explicitly the 157-page tagged PDF
  Declared Edition containing 48 recommendations. The public 100-category
  register remains free and is not represented as paid coverage.
- Changed: the product page no longer uses the local cart as its purchase path.
  A production `PUBLIC_STRIPE_PAYMENT_LINK_URL` will send buyers directly to
  Stripe-hosted Checkout.
- Changed: added a Stripe Payment Link creation script, a signed webhook route,
  paid-session verification, a private Vercel Blob download route, and optional
  Resend email delivery. No payment secret or dossier PDF is stored in Git.
- Changed: the static-first Vercel build now emits the purchase confirmation and
  commerce API routes in its server bundle while retaining the public pages as
  prerendered HTML.
- Passed: `npm test`, including the storefront, dossier-parity, institution,
  build, and Vercel output checks.
- Remaining: create the Stripe objects, configure Vercel environment variables,
  upload the PDF to private Blob storage, register the webhook, test a payment
  in Stripe test mode, and publish approved privacy, terms, refund, and support
  disclosures before turning on live sales.
