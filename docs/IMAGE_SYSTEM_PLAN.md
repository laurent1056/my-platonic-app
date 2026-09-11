# Platonic Ideal — Interpretive Plate System

**Status:** Active public-image policy
**Decision:** the public site uses generated antiquity-style interpretive plates
only. Exact manufacturer, retailer, Creative Commons, and owned product
photography are not part of the public visual system.

The ruling names a commercial model, but the page communicates the Form that
the model exemplifies. The plate makes that meaning memorable; the written
ruling and evidence establish the claim; the source handoff lets a visitor
inspect or acquire the exact model. A plate is never evidence that a particular
SKU looks exactly as shown.

## Current state

The current register has 100 rows:

- 48 `DECLARED` entries;
- 12 `EMPTY` entries;
- 40 entries in review (`CANDIDATE`, `CONDITIONAL`, `CONSUMABLE`, or
  `SPLIT_REQUIRED`).

All 48 declared Form dossiers now have approved local plates. No declared
entry relies on the glyph fallback. EMPTY and nonterminal entries still do not
receive public product art.

The remote URLs are useful leads, not a production-ready image library. A URL
does not establish permission to republish an image, prove that the image is
the exact model under judgment, or guarantee that the host will continue to
serve it.

## Image principle

The public image is a specimen plate, not an advertisement and not an exact
product photograph. Every public visual must be:

1. a local asset generated as an editorial interpretation of the Form;
2. clearly labelled as AI-generated and not product photography;
3. recognisable as the declared model's physical language—silhouette, material,
   proportion, color, and defining functional construction—without logos,
   readable text, packaging, or invented SKU-specific details;
4. paired with a written ruling and a separate source handoff for exact-model
   inspection or acquisition.

The diagrammatic product glyph remains the honest fallback while a plate is
awaiting review. A beautiful but misidentified image would damage the
authority of the register more than an honest absence.

## Model-faithful interpretation

The image target is **model-faithful, not model-identical**. The declared model
is a design reference, not an image to reproduce. A strong plate should let a
visitor understand why the named object belongs to the category while making
clear that the plate is Platonic Ideal's interpretation.

For each new or revised plate, identify three to five visual anchors from the
model record and public specifications:

- overall silhouette and proportions;
- primary material, finish, and characteristic color;
- distinctive functional geometry or hardware;
- the construction detail that matters to the ruling; and
- the era or use-context cues that make the object recognisable.

Those anchors may be translated into the catalog's limestone, basalt, nimbus,
and relief language. The result should not reproduce the source image's camera
angle, crop, lighting, background, arrangement, or distinctive retail styling.
Never add a logo, wordmark, readable model number, package, serial mark, or
proprietary graphic treatment. If a visitor could mistake the plate for a
manufacturer or retailer photograph, reject it and regenerate.

The named model remains the subject of the written ruling and source handoff;
the plate is a model-informed visual metaphor for the Form. Its caption must
continue to say that it is AI-generated and not product photography.

## Visual direction: the specimen portrait

Use one consistent visual grammar for declared products:

- portrait-oriented or square crop, normally 4:5 or 1:1;
- quiet weathered-marble, charcoal, or neutral studio ground;
- object isolated and depicted frontally at a readable scale;
- no promotional badges, sale text, lifestyle clutter, or star ratings;
- service points and replaceable parts may be interpreted as legible visual
  cues, but never as an invented exact-SKU photograph;
- restrained grayscale or low-saturation treatment so the object belongs to the
  catalog, while the DECLARED nimbus/gold remains the state signal;
- consistent edge margin and optical centering across products;
- `object-fit: contain`, never a crop that removes the feature being judged.

The product should look observed and catalogued—closer to a museum specimen,
technical manual, or icon panel than an ecommerce thumbnail.

## Plate-only source rule

There is no public image-source hierarchy. There is one public visual source:
the approved local interpretive plate generated for Platonic Ideal.

The separate source inventory may contain manufacturer, retailer, catalogue,
Creative Commons, or other pages. Those records exist only to:

- verify the identity and availability of the exact model;
- give a visitor an “Inspect exact model” or acquisition handoff;
- preserve editorial provenance for the ruling.

The source URL is never rendered as an image, hotlinked, copied, or promoted to
evidence. Permission to use a source photograph is therefore not a launch
dependency—and even a future permission does not replace the plate without an
explicit revision to this policy.

AI generation must not impersonate an exact product photograph or prove a
declared object's model, construction, logo, control, or service interface. An
invented detail turns a visual aid into false evidence. The plate may express
the meaning of a Form—a cast-iron pan as an archetype, for example—but it must
always be labelled as a representative editorial interpretation.

## Image record

The image layer should be independent from the register CSV. A product can have
multiple images, while the register row should continue to describe the ruling.

```ts
export type PlateRole = 'hero'
export type PlateStatus = 'pending' | 'approved' | 'rejected' | 'needs-review'
export type PlateExactness = 'representative'
export type PlateKind = 'editorial-interpretation'

export interface ProductPlate {
  id: string
  productId: string
  role: PlateRole
  kind: PlateKind
  path: string
  alt: string
  caption: string
  credit: string
  license: string
  exactness: PlateExactness
  region?: string
  capturedOrRetrievedAt: string
  verifiedAt: string
  status: PlateStatus
}
```

Only `approved` plates should be rendered by the public image component. Every
public record has `exactness: 'representative'`,
`kind: 'editorial-interpretation'`, and a caption disclosing that it is
AI-generated and not product photography.

## Repository layout

Approved local plates live under:

```text
public/
└── images/
    └── products/
        ├── pi-001-frying-pan/
        │   └── hero.webp
        └── ...
```

The plate manifest lives beside the typed product records at
`src/data/product-plates.ts`. The CSV's `Image URL` field remains a historical
source reference for model inspection; it is never a public image asset.

## Editorial workflow

### 1. Queue

Generate the plate queue from `DECLARED` entries first, ordered by importance:

- homepage feature and the most useful declarations first;
- the full declared register before any unresolved entry;
- candidates and conditional Forms only after their exact subject is stable;
- never create a public plate for an EMPTY verdict or an unresolved entry.

### 2. Model context

Record the manufacturer, model identifier, variant, region, and the physical
qualities the plate is meant to evoke. Record the three to five visual anchors
used in the prompt. This keeps the interpretation attached to the actual
ruling without asking the image to prove the ruling.

### 3. Generate and prepare

Generate a single editorial interpretation, then normalize orientation,
dimensions, compression, and filename. Keep the generation output outside the
web asset directory until it has passed review. Do not add logos, readable text,
packaging, or exact-SKU claims during preparation.

### 4. Review

The reviewer checks category recognisability, single-subject clarity, antiquity
treatment, alt text, contrast, crop, mobile behavior, caption disclosure, and
credit. The glyph remains the fallback if the plate fails to load. The page
must never show a broken image icon or an uncredited remote image.

### 5. Approve

Set the manifest record to `approved`, copy the selected local asset into
`public/images/products/`, and run `npm run validate:plates`. No permission
request or external photo is required for this workflow.

## Page treatment

On a declared Form or product dossier:

- the hero image sits inside the specimen panel with the nimbus behind it;
- the caption calls it an interpretive plate and says it is not product photography;
- a “View service details” or “Inspect evidence” action is more prominent than
  a purchase link;
- “Inspect exact model” points to the source page for inspection or purchase;
- the source reference says that the public release is plate-only.

On an EMPTY page:

- do not show a generic product image or plate as a consolation prize;
- use the absence treatment and the “what the category would require” copy;
- any future explanatory illustration would be a separate, explicitly labelled
  editorial diagram—not a product plate.

## Launch target

The credible image release is not “all 100 images at any cost.” It is:

- approved plates for all 48 declared Form dossiers;
- a complete plate manifest and visible generation disclosures;
- a stable glyph fallback for any future entry that is not yet approved;
- no source-page URL exposed as if it were a product image;
- a repeatable intake process for future declarations.

The full declared set is now covered without changing the public ruling model.
Future plate work—and any replacement of an existing plate—should follow the
model-faithful interpretation rule when a candidate becomes a stable
declaration or an existing image needs a closer visual match. Exact product
photography is intentionally excluded from this release plan.
