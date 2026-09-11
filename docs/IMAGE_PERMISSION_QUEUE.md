# Archived exact image permission queue

**Status:** retired by decision; no permission has been granted
**Checked:** 2026-09-10  
**Purpose:** preserve the earlier identity research without making exact
product photography part of the public image system.

## Operating rule

The manufacturer or seller page is useful for identity, purchase, and model
verification. It is not automatically a license to copy its photographs.
Platonic Ideal has decided not to use exact product photography in the public
site, even if a permission later becomes available.

The public site does not use this queue. It shows the clearly labelled
interpretive plate and the “Inspect exact model” handoff.

## Historical exact-model leads

These were the highest-value exact-model leads from the earlier image plan.
They are retained for provenance and acquisition links only; no outreach is
required for the current plate-only release.

| Reference | Exact subject | Rights state | Contact route | Status |
| --- | --- | --- | --- | --- |
| PI-001 | Lodge L10SK3, 12 in cast-iron skillet | Not cleared | `info@lodgecastiron.com` / [Lodge contact](https://www.lodgecastiron.com/pages/contact) | Draft |
| PI-003 | Estwing E3-16C, 16 oz curved-claw hammer | Not cleared | [Estwing contact form](https://www.estwing.com/contact-us/) | Draft |
| PI-009 | Lodge EC6D43, 6 qt enameled Dutch oven | Not cleared | `info@lodgecastiron.com` / [Lodge contact](https://www.lodgecastiron.com/pages/contact) | Draft |
| PI-012 | Makita 6302H, 1/2 in corded drill | Not cleared | [Makita U.S.A. contact form](https://makitatools.com/company/contact-us/) | Draft |
| PI-016 | TOM BIHN Synik 30 | Not cleared | `emailus@tombihn.com` / [TOM BIHN FAQ](https://www.tombihn.com/pages/faq) | Draft |
| PI-020 | White’s Semi-Dress work boots | Not cleared | `service@whitesboots.com` / [White’s customer support](https://whitesboots.com/pages/customer-support) | Draft |
| PI-022 | Hanks Gunner 1.5 in full-grain belt | Not cleared | `support@hanksbelts.com` / [Hanks contact](https://www.hanksbelts.com/pages/contact-hanks-belts) | Draft |
| PI-024 | Bahco 8071, 8 in adjustable wrench | Not cleared | [Bahco contact form](https://www.bahco.com/int_en/contact) | Draft |

## Other historical leads

These records already have an exact or near-exact source lead in
`src/data/image-source-inventory.json`. They remain source references only.

| Reference | Exact subject | Current image use |
| --- | --- | --- |
| PI-026 | Levi’s 501 Shrink-to-Fit, raw 100% cotton | Purchase/identity lead only |
| PI-028 | Narex Richter Extra four-piece chisel set | Purchase/identity lead only |
| PI-029 | Channellock 430, 10 in tongue-and-groove pliers | Identity lead |
| PI-030 | Stanley FatMax, 25 ft tape measure | Identity lead |
| PI-033 | Klean Kanteen Classic, 27 oz single-wall | Identity lead |
| PI-037 | Opinel No. 8 stainless pocket knife | Identity lead |
| PI-038 | Mead 09932 composition notebook | Identity lead |
| PI-040 | John Boos R01 maple cutting board | Identity lead |
| PI-046 | Seiko SNK809 automatic watch | Purchase/identity lead only |
| PI-047 | Alden 990 plain-toe blucher | Identity lead |
| PI-055 | Werner NXT1A06, 6 ft fiberglass ladder | Identity lead |
| PI-059 | Tilley T5 cotton duck hat | Identity lead |
| PI-060 | Dachstein DW-3112 boiled-wool mittens | Purchase/identity lead only |
| PI-062 | Merkur 34C / 34101 double-edge safety razor | Identity lead |

## Historical permission notes

[`IMAGE_PERMISSION_REQUEST.md`](./IMAGE_PERMISSION_REQUEST.md) is retained as
an archived note from the earlier plan. Do not use it for the current release:
we are not seeking or displaying product photography.

If the product-image policy changes in the future, the permission record must
still be explicit and must come from someone authorized to grant the rights.

## If the policy changes in the future

Before introducing any non-plate image in a future policy revision:

- exact manufacturer, model identifier, variant, and region match the ruling;
- the source or photographer has granted the required rights;
- the original image and permission record are archived;
- the manifest has explicit rights, visible credit, source URL, and review
  metadata;
- the caption does not imply that a representative image is the exact SKU;
- the interpretive plate remains the primary public visual;
- `npm run validate:images` and the full production build pass.

**Current count:** 0 exact product photographs by design. This is a product
decision, not a missing-data bug.
