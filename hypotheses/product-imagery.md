# Hypotheses — product imagery

## Meta
- Feature: [product imagery](../knowledge/product/features/product-imagery.md)
- Status: active
- Created: 2026-09-03
- Last updated: 2026-09-03

## Value risk
### H-V1: A precise product image or intentional specimen glyph will make a declaration more memorable and easier to recognize.
- **Origin:** proactive
- **Confidence:** low
- **Evidence for:**
  - The design language explicitly treats the product as an icon and defines image/glyph behavior [source/design-language](../source/adhoc/2026-09-03-project-baseline/docs/design/design.md)
- **Evidence against:**
  _(none yet)_
- **Open questions / caveats:**
  - The product's value is primarily argumentative; imagery may be secondary.
- **Test:** Compare founder category review sessions with and without imagery on representative declared and empty pages.
- **Decision trigger:** Keep imagery prominent only if it improves recognition or comprehension without displacing the reasoning.
- **Status:** active
- **Resolution:** —

## Usability risk
### H-U1: Consistent image treatment and a clear glyph fallback will prevent missing assets from looking like broken content.
- **Origin:** proactive
- **Confidence:** low
- **Evidence for:**
  - The image reference notes distinguish successfully extracted images, partial/logo images, and categories with no image [source/image-urls](../source/adhoc/2026-09-03-project-baseline/docs/reference/product_image_urls.md)
- **Evidence against:**
  _(none yet)_
- **Open questions / caveats:**
  - The fallback's recognizability across product types is not tested.
- **Test:** Review all image states in light/dark themes and on mobile, including a declared category with no image and an empty category.
- **Decision trigger:** Redesign any fallback that reads as a loading failure or implies a model that is not declared.
- **Status:** active
- **Resolution:** —

## Feasibility risk
### H-F1: The current CSV image field and Astro public assets can support a reliable image layer without making the build fragile.
- **Origin:** proactive
- **Confidence:** low
- **Evidence for:**
  - The data model already maps an `Image URL` field and defines a glyph fallback for missing or placeholder URLs [source/data-model](../source/adhoc/2026-09-03-project-baseline/docs/DATA_MODEL.md)
- **Evidence against:**
  - Existing image research is partial and includes links that may be logos, metadata extracts, or unavailable product images [source/image-urls](../source/adhoc/2026-09-03-project-baseline/docs/reference/product_image_urls.md)
- **Open questions / caveats:**
  - Source ownership, hotlink stability, and build-time remote image behavior are unresolved.
- **Test:** Establish a small source/credit fixture set and verify rendering, alt text, fallback, and deploy-safe URLs.
- **Decision trigger:** Prefer local/owned or stable credited assets if remote URLs break or cannot be attributed reliably.
- **Status:** active
- **Resolution:** —

## Viability risk
### H-B1: Images can improve product value without creating a commercial endorsement or licensing burden that exceeds v1's capacity.
- **Origin:** proactive
- **Confidence:** low
- **Evidence for:**
  - V1 is explicitly a static editorial product and not e-commerce [source/PRD](../source/adhoc/2026-09-03-project-baseline/docs/PRD.md)
- **Evidence against:**
  _(none yet)_
- **Open questions / caveats:**
  - Future revenue or affiliate use could change image disclosure requirements.
- **Test:** Document source, credit, model match, and allowed use for the first declared-image set before broadening coverage.
- **Decision trigger:** Pause an image source if rights or commercial implications cannot be stated plainly.
- **Status:** active
- **Resolution:** —

## Other risk
### H-O1: Image credits and exact-model labeling can preserve trust when a source image is supplied by a manufacturer or third party.
- **Origin:** proactive
- **Confidence:** low
- **Evidence for:**
  - The project includes a dedicated image-credit note with a source record for its Plato portrait [source/image-credits](../source/adhoc/2026-09-03-project-baseline/docs/design/IMAGE_CREDITS.md)
- **Evidence against:**
  _(none yet)_
- **Open questions / caveats:**
  - Product-image rights and model identity need to be checked per asset.
- **Test:** Add visible or machine-readable credits and alt text to a representative image set, then audit every asset.
- **Decision trigger:** Keep only assets with an auditable source and a confirmed model match; otherwise use a glyph.
- **Status:** active
- **Resolution:** —
