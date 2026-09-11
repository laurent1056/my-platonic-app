# Image release status

**Checked:** 2026-09-10  
**Release:** Interpretive plate waves 01–02

## Decision: plates are the public visual layer

Platonic Ideal will use antiquity-style interpretive plates as the standard
public hero treatment for declared Forms. Exact manufacturer photography is
optional future identity/evidence support, not a launch dependency. This lets
the site communicate the meaning of a ruling consistently without implying
that a generated image proves the exact SKU.

## What is live

The public site now has 20 approved local interpretive plates for declared
Forms. They are deliberately antiquity-style images: a visual expression of
the Form, not a claim that the generated object is the exact commercial SKU.
Each record is labelled `editorial-interpretation`, `representative`, and
“AI-generated … not product photography” in `src/data/product-images.ts`.

The first wave covers:

| Reference | Category | Public image treatment |
| --- | --- | --- |
| PI-001 | Frying Pan | Interpretive plate |
| PI-003 | Hammer | Interpretive plate |
| PI-005 | Kitchen Knife | Interpretive plate |
| PI-007 | Saucepan | Interpretive plate |
| PI-009 | Dutch Oven | Interpretive plate |
| PI-012 | Drill | Interpretive plate |
| PI-013 | Kettle | Interpretive plate |
| PI-016 | Backpack | Interpretive plate |
| PI-018 | Hand Saw | Interpretive plate |
| PI-019 | Desk | Interpretive plate |
| PI-020 | Boots | Interpretive plate |
| PI-022 | Belt | Interpretive plate |
| PI-008 | Screwdriver | Interpretive plate |
| PI-024 | Adjustable Wrench | Interpretive plate |
| PI-029 | Pliers | Interpretive plate |
| PI-030 | Tape Measure | Interpretive plate |
| PI-033 | Water Bottle | Interpretive plate |
| PI-037 | Pocket Knife | Interpretive plate |
| PI-040 | Cutting Board | Interpretive plate |
| PI-047 | Shoes | Interpretive plate |

The remaining 28 declared products use the diagrammatic glyph until a local
interpretive plate is generated. EMPTY and nonterminal entries do not receive
product hero art.

## Exact photography: optional future identity layer

The image-source inventory currently has 41 image-bearing leads for the 48
declared products, including 22 exact-identity leads. It has **zero**
rights-cleared images for republication. A manufacturer page, retailer page,
Google result, or OpenGraph image is a sourcing lead—not a license.

Accordingly, no remote product photograph has been copied into the public
asset directory. Exact photography can enter the site as a secondary identity
or evidence layer only after one of these conditions is recorded:

1. Platonic Ideal owns the photograph;
2. the maker or authorized seller grants permission covering the intended
   website, dossier/PDF, newsletter, and any clearly disclosed acquisition
   link; or
3. the image is public domain or Creative Commons and the exact model,
   attribution, license, and any ShareAlike obligations are recorded.

Until then, the interpretive plate and source handoff remain separate layers:
the plate communicates the meaning of the ruling; the source record points to
where the exact object can be inspected or purchased.

The exact-photo queue remains prepared but is no longer a release blocker:
the permission request template is ready in `docs/IMAGE_PERMISSION_REQUEST.md`,
and the 22 exact-identity leads are recorded in
`src/data/image-source-inventory.json`. Permission from the makers or
authorized sellers, or photographs Platonic Ideal owns, can add a secondary
identity layer later. A real permission record is still required before an
exact image can be promoted.

## Next image batch

The next batch should add interpretive plates to the remaining high-confidence
declared products in the register. An exact product photograph must never
silently replace an interpretive plate: it should carry its own model, source,
rights, and review metadata in the image manifest.
