# Image release status

**Checked:** 2026-09-11
**Release:** Complete declared-form interpretive plate set

## Decision: plates are the public visual layer

Platonic Ideal will use antiquity-style interpretive plates as the standard
public hero treatment for declared Forms. Exact manufacturer photography is
optional future identity/evidence support, not a launch dependency. This lets
the site communicate the meaning of a ruling consistently without implying
that a generated image proves the exact SKU.

## What is live

The public site now has 48 approved local interpretive plates for all declared
Forms. They are deliberately antiquity-style images: a visual expression of
the Form, not a claim that the generated object is the exact commercial SKU.
Each record is labelled `editorial-interpretation`, `representative`, and
“AI-generated … not product photography” in `src/data/product-plates.ts`.
There are no declared products left on the glyph fallback.

The initial plate set covers:

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

The completed release adds the remaining declared Forms:

| Reference | Category | Public image treatment |
| --- | --- | --- |
| PI-025 | T-Shirt | Interpretive plate |
| PI-026 | Jeans | Interpretive plate |
| PI-027 | Jacket / Coat | Interpretive plate |
| PI-028 | Chisel | Interpretive plate |
| PI-031 | Tent | Interpretive plate |
| PI-032 | Sleeping Bag | Interpretive plate |
| PI-034 | Flashlight | Interpretive plate |
| PI-035 | Sweater | Interpretive plate |
| PI-036 | Cooler | Interpretive plate |
| PI-038 | Notebook | Interpretive plate |
| PI-039 | Pen | Interpretive plate |
| PI-042 | Bicycle | Interpretive plate |
| PI-043 | Dining Chair | Interpretive plate |
| PI-045 | Socks | Interpretive plate |
| PI-046 | Watch | Interpretive plate |
| PI-049 | Level | Interpretive plate |
| PI-050 | Drill Bits | Interpretive plate |
| PI-051 | Extension Cord | Interpretive plate |
| PI-052 | Camping Stove | Interpretive plate |
| PI-053 | Mechanical Pencil | Interpretive plate |
| PI-054 | Umbrella | Interpretive plate |
| PI-055 | Ladder | Interpretive plate |
| PI-056 | Wheelbarrow | Interpretive plate |
| PI-057 | Wallet | Interpretive plate |
| PI-058 | Briefcase | Interpretive plate |
| PI-059 | Hat | Interpretive plate |
| PI-060 | Gloves | Interpretive plate |
| PI-062 | Razor | Interpretive plate |

EMPTY and nonterminal entries do not receive product hero art. That distinction
is intentional: an absence verdict is not made more authoritative by inventing
a product image for it.

## Refinement direction: model-faithful, not model-identical

The next quality bar for new plates and targeted revisions is closer visual
fidelity to the declared model without copying a product image. Prompts may
use the model's observable silhouette, proportions, materials, colors, and
defining functional construction. They must not reproduce a source photo's
composition or add logos, readable marks, packaging, serial numbers, or
proprietary graphics. The plate remains an AI-generated interpretation, not
product photography.

The full 48-plate set remains live while individual plates are refined against
this rule. A revision should replace a plate only when it improves model
recognisability without increasing identity confusion.

## Exact photography: excluded from the public image system

The image-source inventory currently has 41 image-bearing leads for the 48
declared products, including 22 exact-identity leads. It has **zero**
rights-cleared images for republication. A manufacturer page, retailer page,
Google result, or OpenGraph image is a sourcing lead—not a license.

Accordingly, no remote product photograph has been copied into the public
asset directory. Platonic Ideal will not add manufacturer, retailer, owned,
public-domain, or Creative Commons product photography to the public site,
even if the rights question is later resolved. The interpretive plate and
source handoff remain separate layers: the plate communicates the meaning of
the ruling; the source record points to where the exact object can be inspected
or purchased.

The old exact-photo queue remains in the repository as a provenance record,
but it is retired and is not an active product requirement. The source records
remain useful only as links for visitors who want to inspect or acquire the
named model.

## Future image work

The declared set is complete. When a candidate becomes a stable declaration,
add its plate through the same manifest, disclosure, and validation workflow.
The plate is the final public visual; no exact product photograph should
silently replace it.
