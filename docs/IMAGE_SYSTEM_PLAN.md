# Platonic Ideal — Product Image System

**Status:** Implementation specification  
**Purpose:** Give every validated product a trustworthy, visually consistent
specimen image without weakening the evidence standard.

## Current state

The current register has 100 rows:

- 48 `DECLARED` entries;
- 12 `EMPTY` entries;
- 40 entries in review (`CANDIDATE`, `CONDITIONAL`, `CONSUMABLE`, or
  `SPLIT_REQUIRED`).

The first interpretive release now covers 12 declared Form dossiers with
approved local plates. The remaining declared entries retain the glyph
fallback until their exact identity and image treatment are ready.

The remote URLs are useful leads, not a production-ready image library. A URL
does not establish permission to republish an image, prove that the image is
the exact model under judgment, or guarantee that the host will continue to
serve it.

## Image principle

The image is a specimen plate, not an advertisement.

Every production image must answer three questions:

1. Is this the exact product, model, variant, and region being judged?
2. Do we have a defensible right to display it?
3. Can a visitor see enough of the construction or identity to understand why
   it belongs to the ruling?

If any answer is unknown, the page keeps the diagrammatic product glyph and
labels the image as pending. A beautiful but misidentified image would damage
the authority of the register more than an honest absence.

## Visual direction: the specimen portrait

Use one consistent visual grammar for declared products:

- portrait-oriented or square crop, normally 4:5 or 1:1;
- quiet weathered-marble, charcoal, or neutral studio ground;
- object isolated or photographed frontally at a readable scale;
- no promotional badges, sale text, lifestyle clutter, or star ratings;
- maker marks, model plates, fasteners, interfaces, and replaceable parts may
  appear as secondary detail plates;
- restrained grayscale or low-saturation treatment so the object belongs to the
  catalog, while the DECLARED nimbus/gold remains the state signal;
- consistent edge margin and optical centering across products;
- `object-fit: contain`, never a crop that removes the feature being judged.

The product should look observed and catalogued—closer to a museum specimen,
technical manual, or icon panel than an ecommerce thumbnail.

## Source hierarchy

Use sources in this order:

1. **Original Platonic photography** — preferred. Photograph the exact object,
   variant, service points, and any identifying mark. Obtain a simple model and
   location release when another person, private property, or a recognizable
   setting appears.
2. **Permissioned manufacturer or distributor image** — acceptable when the
   owner explicitly permits editorial republication or provides a press/media
   license. Record the permission and scope in the manifest.
3. **Public-domain or Creative Commons image** — acceptable when it depicts the
   exact object or is clearly labelled as a representative historical artifact.
   Preserve attribution, license, source URL, and any ShareAlike obligation.
4. **Licensed stock or commissioned photography** — acceptable when the license
   covers the intended web, PDF, and future commercial uses.
5. **External image URL** — temporary research reference only. Do not rely on
   hotlinking for production.

Do not use AI-generated imagery to impersonate exact product photography or to
prove a declared object's model, construction, logo, control, or service
interface. An invented detail turns a visual aid into false evidence.

An AI-generated **interpretive plate** is allowed as a separate, clearly
labelled visual layer. It may express the meaning of a Form—a cast-iron pan as
an archetype, for example—but it must be marked as an interpretation, must not
carry the exactness value `exact-model`, and must never be the only support for
a product claim. The caption should say that it is AI-generated and not
product photography. This is the visual treatment used by the first 12
interpretive plates in the repository.

## Image record

The image layer should be independent from the register CSV. A product can have
multiple images, while the register row should continue to describe the ruling.

```ts
export type ImageRole = 'hero' | 'detail' | 'service' | 'maker-mark' | 'evidence'
export type ImageStatus = 'pending' | 'approved' | 'rejected' | 'needs-review'

export interface ProductImage {
  id: string
  productId: string
  role: ImageRole
  path: string
  alt: string
  caption?: string
  credit: string
  license: string
  sourceUrl: string
  permissionRecord?: string
  exactness: 'exact-model' | 'exact-family' | 'representative'
  region?: string
  capturedOrRetrievedAt: string
  verifiedAt: string
  status: ImageStatus
}
```

Only `approved` images should be rendered by the public image component.
`exact-family` and `representative` images must say so in the caption and
cannot be used to silently imply that the photographed object is the exact
SKU. An `editorial-interpretation` image is a visual interpretation of the
Form, not product identity, even when it appears in the hero position.

## Repository layout

Approved local assets should eventually live under:

```text
public/
└── images/
    └── products/
        ├── pi-001-lodge-l10sk3/
        │   ├── hero.webp
        │   ├── detail-cooking-surface.webp
        │   └── service-mark.webp
        └── ...
```

The image manifest should live beside the typed product records, for example
`src/data/product-images.ts`. The CSV's `Image URL` field remains a migration
reference until every approved asset has a local identity, credit, and status.

## Editorial workflow

### 1. Queue

Generate the queue from `DECLARED` entries first, ordered by importance:

- homepage feature and the first 12–15 most useful declarations;
- the remaining declared set;
- candidates and conditional Forms only after their exact subject is stable;
- never create a “product image” for an EMPTY verdict.

### 2. Identity check

Before an image is approved, record the manufacturer, model identifier,
variant, region, and the visual feature that distinguishes it from adjacent
models. If a brand has silently changed the product, create a new product
record rather than reusing the old image.

### 3. Rights check

Record the license or permission in the manifest. “Found on Google,” “on the
manufacturer website,” and “OpenGraph image” are not licenses. Keep the source
URL and retrieval date even for owned or permissioned photography.

### 4. Preparation

Normalize orientation, crop, dimensions, compression, and filename. Preserve
the original outside the web asset directory when the source license requires
it. Generate WebP or AVIF derivatives only from an approved original.

### 5. Review

The reviewer checks exactness, rights, alt text, contrast, crop, and mobile
behavior. The glyph remains the fallback if the image fails to load. The page
must never show a broken image icon or an uncredited remote image.

## Page treatment

On a declared Form or product dossier:

- the hero image sits inside the specimen panel with the nimbus behind it;
- the caption states the exact model and image credit;
- a “View service details” or “Inspect evidence” action is more prominent than
  a purchase link;
- detail/service images appear below the ruling argument, attached to the claim
  they help a visitor inspect;
- image source and license are visible without opening developer tools.

On an EMPTY page:

- do not show a generic product photo as a consolation prize;
- use the absence treatment and the “what the category would require” copy;
- representative imagery may appear only if it explains a failure mode and is
  explicitly labelled as representative evidence.

## Launch target

The first credible image release is not “all 100 images at any cost.” It is:

- approved hero images for the homepage feature and the first 12–15 declared
  Form dossiers (12 are now complete);
- a complete image manifest and visible credits;
- a stable glyph fallback for every other entry;
- no placeholder URL exposed as if it were a product image;
- a repeatable intake process for the remaining declared set.

Once the product and evidence entities exist, the image pipeline can expand to
all validated products without changing the public ruling model.
