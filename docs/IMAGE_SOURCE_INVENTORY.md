# Model source inventory (not a public image library)

**Checked:** 2026-09-10  
**Scope:** 48 current `DECLARED` entries  
**Canonical data:** [`src/data/image-source-inventory.json`](../src/data/image-source-inventory.json)

This is the research queue for the product-identity layer. It answers “where
can we inspect the named object?” and “where can a visitor acquire it?” It is
not a public image library. The source page is never treated as a license and
its photography is never rendered or copied. Public pages use only approved
local interpretive plates or the diagrammatic glyph.

## Current readout

| Measure | Count |
| --- | ---: |
| Declared products covered | 48 |
| Image-bearing source pages located | 41 |
| Leads needing exact model or variant work | 5 |
| No current source located | 2 |
| Exact identity matches | 22 |
| Rights-cleared for republication | 0 |

“Confirmed” means that an image-bearing page was found. It does not mean that
the image can be copied. “Exact” means the source identity matches the current
declared subject as recorded; it does not override the rights check.

## Exact identity and model source

These are the strongest model-identity and acquisition references:

`PI-001` Lodge L10SK3 · `PI-003` Estwing E3-16C · `PI-009` Lodge EC6D43 ·
`PI-012` Makita 6302H · `PI-016` Tom Bihn Synik 30 · `PI-020` White’s
Semi-Dress · `PI-022` Hanks Gunner · `PI-024` Bahco 8071 · `PI-028` Narex
Semi-Dress · `PI-022` Hanks Gunner · `PI-024` Bahco 8071 · `PI-026` Levi’s
501 Shrink-to-Fit · `PI-028` Narex Richter Extra set · `PI-029` Channellock 430 · `PI-030` Stanley FMHT38325S ·
`PI-033` Klean Kanteen Classic 27 oz · `PI-037` Opinel No. 8 · `PI-038` Mead
09932 · `PI-040` John Boos R01 · `PI-046` Seiko SNK809 · `PI-047` Alden 990 ·
`PI-055` Werner NXT1A06 · `PI-059` Tilley T5 · `PI-060` Dachstein DW-3112 ·
`PI-062` Merkur 34101.

The manifest contains the source page, seller or maker, variant, region, image
status, rights status, identity status, and next recommended use for every
record. The validation command ensures that every current declared row has
one and only one inventory record:

```bash
npm run validate:images
npm run validate:images -- --verbose
```

## Editorial operating rule

The public page has two distinct, non-image layers:

1. **Interpretive plate:** the antiquity-style image generated for Platonic
   Ideal, clearly captioned as AI-generated and not product photography. This
   communicates the meaning of the Form.
2. **Model source handoff:** a text record and link to the current exact model
   page. This supports inspection, availability checks, and acquisition without
   importing the source page's photography.

No source-page image is silently promoted to evidence. The source inventory
remains useful even though the public visual policy is permanently plate-only.

## Next pass

1. Normalize the ambiguous register models: Victorinox 40520 vs 5.2063.20,
   the Tramontina saucepan, OXO kettle, Gyokucho saw, sleeping bag maker,
   Springbar Highline 6, cooler size, pencil lead size, and the other `or`
   variants called out in the manifest.
2. Verify that each acquisition link resolves to the exact model named by the
   ruling, and record a replacement lead when a page disappears.
3. Keep the source handoff useful even when a product is sold out, discontinued,
   or region-limited; availability is a visitor-facing caveat, not an image
   requirement.
4. Add generated visual assets only through
   `src/data/product-plates.ts`. The public component must never render a
   source-page photograph.
