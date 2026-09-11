# Exact image permission queue

**Status:** outreach packet prepared; no permission has been granted yet  
**Checked:** 2026-09-10  
**Purpose:** move exact product photography from “identity lead” to “approved
product image” without weakening the register’s authority.

## Operating rule

The manufacturer or seller page is useful for identity, purchase, and model
verification. It is not automatically a license to copy its photographs. An
image may be promoted into `src/data/product-images.ts` only when the queue
contains a permission record or an owned/public-domain/Creative-Commons
record that covers the intended use.

Until then, the public site continues to show the clearly labelled
interpretive plate and the “Inspect current source” handoff.

## First outreach wave

These are the highest-value exact-model leads for the first permission pass.
The contact route is a starting point, not evidence that permission has been
granted.

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

## Remaining exact-identity queue

These records already have an exact or near-exact source lead in
`src/data/image-source-inventory.json`. They should be contacted after the
first wave or handled by owned photography.

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

## Permission request

Use [`IMAGE_PERMISSION_REQUEST.md`](./IMAGE_PERMISSION_REQUEST.md) for each
maker or authorized seller. The request should name the exact model and
variant, identify the intended dossier URL, require visible credit and a
source link, and explicitly ask whether the grant covers the website, PDF,
newsletter, and clearly disclosed acquisition links.

Do not record an informal “sure” as licensed unless the responder has
authority to grant the rights. Record the named image, allowed channels,
territory, duration, required credit, restrictions, and the original message
or permission record.

## Promotion checklist

Before changing an image record from an interpretive plate to product
photography:

- exact manufacturer, model identifier, variant, and region match the ruling;
- the source or photographer has granted the required rights;
- the original image and permission record are archived;
- the manifest has `kind: 'product-photograph'`, the correct `exactness`,
  visible credit, source URL, and review date;
- the caption no longer implies that a representative image is the exact SKU;
- the interpretive plate remains available as editorial art where useful;
- `npm run validate:images` and the full production build pass.

**Current count:** 0 rights-cleared exact photographs. This is an honest
queue, not a missing-data bug.
