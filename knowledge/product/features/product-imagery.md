# Product imagery

## Meta
- Owner: Laurent Courtines
- Status: scoping
- Priority: P1
- Last updated: 2026-09-03

## Problem
The register should feel tangible and memorable, but many categories do not yet
have a verified product image. A missing or legally unclear image can make a
declared product feel unfinished, while an image can become misleading if it is
not the exact model being declared.

## Target users
- [Founder-operator](../../users/personas.md) — chooses and credits imagery
- [External durable-goods shopper](../../users/personas.md) — future reader

## Success metrics
- Every declared category has either a verified product image with credit/source
  metadata or an intentional specimen glyph fallback.
- Empty categories are not forced into decorative product imagery.
- Images preserve performance, accessibility, and dark/light theme legibility.

## Risks
Image rights, hotlink stability, model mismatch, privacy, and visual hierarchy
could compromise trust. A product photo may imply endorsement beyond the
editorial argument.

## Dependencies
Canonical `Image URL` field, image-credit policy, product-source verification,
Astro public assets, responsive image treatment, and fallback glyphs.

## Timeline
Start with the declared set after the register schema is stable; do not block
the first founder-facing route on full image coverage.

## Evidence
- The inherited image notes contain partial extraction results and categories
  without product images [source/image-urls](../../../source/adhoc/2026-09-03-project-baseline/docs/reference/product_image_urls.md).
- The design language treats the product as an icon and documents an image/glyph
  system [source/design-language](../../../source/adhoc/2026-09-03-project-baseline/docs/design/design.md).
- The image-credit note identifies a Plato portrait source and the need to record
  credits [source/image-credits](../../../source/adhoc/2026-09-03-project-baseline/docs/design/IMAGE_CREDITS.md).

## Linked
- Hypotheses: [product-imagery](../../../hypotheses/product-imagery.md)
- Decisions: [2026-09-03 rebuild decision](../../../decisions/2026-09-03-rebuild-as-astro-single-repo.md)
- Metrics: [product metrics](../metrics.md)
- Stakeholders affected: [Laurent Courtines](../../../stakeholders/laurent-courtines.md)

## Open questions
- Which sources are durable enough for production: owned assets, public-domain
  images, manufacturer assets, or linked originals?
- Should the first pass prioritize all `DECLARED` categories or a representative
  set that demonstrates the visual system?

## Follow-up after launch
Audit broken image URLs, source credits, and declared-model mismatches during the
first content maintenance review.
