# Dossier storefront design pass

Implemented 2026-09-14. The user clarified: “we sell a single product, the dossier, from every page.” This pass applies familiar ecommerce layouts to that offer without turning editorial products into merchandise.

## Offer and boundaries

- One commercial product: **The Platonic Ideal Dossier**, with the previously approved **$24 one-time** price as the design reference. The shared offer lives in `src/data/dossier.ts`.
- Header CTA on every public route, including all 100 existing category pages. Most pages also end with a shared dossier offer; category pages include a compact offer beside the research.
- Category verdicts, decisive reasoning, methodology, and Constitution stay free. Existing CSV and institutional evidence records are unchanged.
- Dossier coverage, final file format, delivery, authentication, payment integration, and binding policies are not complete. Purchase and account routes explicitly identify themselves as previews; no credentials or payment information can be entered.
- A single local preview state remembers cart presence, saved status, and completion of a no-charge checkout preview. It never represents purchase entitlement. No network request is made by the commerce script.

## Design system extension

The existing sage, basalt, and iron-oxide tokens remain the palette. Cormorant Garamond carries headlines; Libre Franklin carries controls and body copy; the existing Cinzel wordmark and IBM Plex Mono labels retain the identity. New styles are isolated in `src/styles/storefront.css`.

| Pattern | Role | Behavior and accessibility |
| --- | --- | --- |
| Shared header | Familiar catalog/dossier/journal navigation; search, account, cart | Named icon links, current-page states, mobile reflow, theme control |
| DossierCover | Plato-led product identity without suggesting a physical product for sale | Shared portrait cover, accessible image description, visible full-size image credit, explicit digital cover concept |
| DossierOffer | One reusable conversion panel | Common destination and price; compact variant on category pages |
| CategoryCard | Free editorial research entry | Real category route, visible verdict, interpretive art, honest empty state |
| Catalog | Listing and search results | Text, collection, exact or grouped verdict, ownership mechanism, and evidence/alphabetical sorting; result announcements, empty state, reset |
| AccountPage | Reader account templates | Navigation, local saved-item state, preview history, honest unavailable states |
| Commerce state | Demonstrate the one-product journey | Quantity fixed at one; duplicate prevention; remove, save, checkout; guarded local storage and cross-tab refresh |
| Form field | Checkout and account design | Visible labels, disabled illustrative sensitive fields, no submission |
| FAQ | Progressive disclosure | Native keyboard-accessible details/summary |

The catalog accepts both the previous `domain`, `state`, `mechanism`, `sort=category/confidence` query parameters and the new `collection`, `verdict`, `sort=az` forms. Empty verdicts and specific research statuses remain filterable.

## Page coverage

| Requested page | Implemented route / adaptation |
| --- | --- |
| Home | `/` |
| Category / collection | `/register/`, `/collections/[domain]/` (9 collections) |
| Product detail | `/dossier/`; existing `/category/[slug]/` remain free research |
| Search results | `/search/?q=...` |
| Cart | `/cart/` |
| Checkout | `/checkout/` — no-charge preview |
| Confirmation | `/order-confirmation/` — preview result, not a receipt |
| Login | `/account/login/` |
| Register | `/account/register/`; `/register/` remains the editorial catalog |
| Password reset | `/account/password-reset/` — no email sent |
| Account dashboard | `/account/` |
| Order history | `/account/orders/` |
| Order detail | `/account/orders/preview/` |
| Addresses | `/account/addresses/` — digital delivery requires no shipping address |
| Payment methods | `/account/payment-methods/` — no provider or saved cards |
| Wishlist | `/account/wishlist/` — saved dossier on this device |
| Landing / campaign | `/campaign/` |
| Blog index | `/journal/` |
| Blog post | `/journal/[slug]/` — 3 editorial notes |
| About | `/about/` |
| Contact | `/contact/` — guidance, no unconfigured submission form |
| FAQ / help | `/help/` |
| Shipping / returns | `/shipping-returns/` — digital delivery; final terms pending |
| Privacy | `/privacy/` — preview notice, not final production policy |
| Terms | `/terms/` — preview notice, not binding purchase terms |
| 404 | `/404.html` and normal missing-route handling |
| Store locator | `/store-locator/` — digital publication, no invented locations |
| Brand / vendor | `/brands/` — editorial independence |
| Gift card | `/gift-card/` — no gift-card product or recipient collection |
| Size guide | `/size-guide/` — format / reading guidance |
| Compare | `/compare/` — public research versus dossier, not competing physical products |
| Subscription management | `/account/subscriptions/` — one-time purchase, no renewal |

`/page-directory/` links to every family for review. Account, checkout, search, and unfinished policy routes are noindex; non-indexable preview routes are excluded from the sitemap.

## Validation

- `npm test`: Astro checks, 13 institutional tests, data/image/plate/institution validation, build verification, and six storefront checks.
- Build generates 146 HTML pages, including all 100 category routes.
- Browser verification: desktop and mobile layouts; image loading; primary dossier CTA; search, empty results, clearing filters; saved dossier; cart; no-charge checkout and confirmation.
- Existing register and image-source warnings are retained; editorial records were not changed as part of a design pass.

## Production work still required

Finalize the actual dossier and offer scope, follow `docs/design/DOSSIER_PDF_ART_DIRECTION.md` while building its image and quotation ledger, configure hosted payment and verified fulfillment, decide whether accounts are needed, and supply final support/contact and policy information. The current design must not be described as a live store.
