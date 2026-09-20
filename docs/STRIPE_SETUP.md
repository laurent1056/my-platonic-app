# Stripe purchase setup

The live offer is one fixed product: the 157-page tagged PDF Declared Edition
with 48 recommendations, priced at `$24` one time. The site keeps the sales
page and fulfillment endpoints; Stripe hosts the checkout UI.

## Create the Stripe objects

Set `STRIPE_SECRET_KEY` in a local, uncommitted environment and run:

```bash
npm run stripe:create-payment-link
```

The script creates or reuses the product and price IDs supplied through
`STRIPE_PRODUCT_ID` and `STRIPE_PRICE_ID`, then creates a Payment Link that
redirects to:

```text
https://www.platonicidealguide.com/purchase/success/?session_id={CHECKOUT_SESSION_ID}
```

Copy the resulting Payment Link URL, product ID, and price ID into the
deployment environment. Run the script separately in Stripe test mode and
live mode; test and live objects are different.

## Vercel environment variables

Required for a working purchase and download:

```text
PUBLIC_STRIPE_PAYMENT_LINK_URL
STRIPE_SECRET_KEY
STRIPE_WEBHOOK_SECRET
STRIPE_PRODUCT_ID
STRIPE_PRICE_ID
BLOB_READ_WRITE_TOKEN
DOSSIER_BLOB_PATH
```

Optional for inbox delivery in addition to the confirmation-page download:

```text
RESEND_API_KEY
RESEND_FROM_EMAIL
SUPPORT_EMAIL
```

`STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, and `BLOB_READ_WRITE_TOKEN` must
remain server-only variables. Do not put them in `PUBLIC_` variables or commit
them to the repository.

## Private file delivery

Create a private Vercel Blob store and upload the final PDF. Set
`DOSSIER_BLOB_PATH` to the exact pathname of that private blob. The PDF should
not be copied into `public/`; `/api/dossier/download/` checks the Stripe session
and streams the private blob only after a paid session for the configured price
has been verified.

## Webhook

Register this production endpoint in Stripe:

```text
https://www.platonicidealguide.com/api/stripe/webhook/
```

Subscribe to:

- `checkout.session.completed`
- `checkout.session.async_payment_succeeded`

Copy the endpoint signing secret into `STRIPE_WEBHOOK_SECRET`. The webhook
verifies Stripe's signature against the raw request body and optionally sends a
download email when the Resend variables are configured.

## Test-mode launch check

Before switching to live mode:

1. Deploy with Stripe test-mode variables and a private test PDF.
2. Open `/dossier/`, follow the Stripe Payment Link, and complete a test payment.
3. Confirm the redirect reaches `/purchase/success/` with a session ID.
4. Confirm the download returns the test PDF only after payment verification.
5. Confirm the webhook shows a successful delivery in Stripe.
6. Replay the webhook once and confirm the fulfillment email is not duplicated.
7. Replace the test objects, blob, and webhook secret with live-mode values only
   after the approved terms, refund, privacy, and support disclosures are live.
