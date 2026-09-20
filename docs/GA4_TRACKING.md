# GA4 measurement

The storefront sends measurement to Google Analytics 4 property `G-5GF42RQENS` through the existing Google tag in `src/layouts/SiteLayout.astro`. The site disables GA4's automatic page view and emits one controlled `page_view` event from `src/scripts/analytics.ts` so the funnel is not double-counted.

## Event vocabulary

| Site action | GA4 event | Important parameters |
| --- | --- | --- |
| Any page load | `page_view` | `page_type`, `funnel_stage`, `page_path`, `page_location` |
| Dossier product page | `view_item` | `items`, `item_id`, `item_name`, `item_category`, `value`, `currency`, `edition_id` |
| Home/header/offer dossier CTA | `select_item` | `items`, `item_list_name`, `value`, `currency`, `edition_id` |
| Live Stripe Payment Link click | `begin_checkout` | `items`, `item_list_name`, `value`, `currency`, `edition_id` |
| Verified paid return from Stripe | `purchase` | `transaction_id`, `value`, `currency`, `items`, `purchase_mode`, `edition_id` |
| Public sample PDF click | `dossier_download` | `download_type=sample`, `access_type=public`, `trial_download=true`, `file_name`, `file_extension`, `edition_id` |
| Paid dossier download click | `dossier_download` | `download_type=paid_dossier`, `access_type=paid`, `trial_download=false`, `transaction_id`, `file_name`, `edition_id` |

The browser may also report GA4's automatic `file_download` event for the public PDF if Enhanced Measurement is enabled. `dossier_download` is the canonical product event because it distinguishes the sample from paid fulfillment and carries the dossier-specific fields.

## Funnel interpretation

The primary purchase funnel is:

`page_view (home)` → `select_item` → `page_view (dossier)` → `view_item` → `begin_checkout` → `purchase` → `dossier_download (paid_dossier)`

The public trial path is measured separately:

`page_view` → `dossier_download (sample, trial_download=true)`

The old cart and checkout pages are explicitly sandbox routes. Their events are prefixed with `preview_` and do not emit real `purchase` or paid `dossier_download` events.

## GA4 admin follow-up

The code can send parameters, but GA4 does not automatically expose arbitrary parameters in standard reports. In GA4 Admin, register these event-scoped custom dimensions if reporting on them is needed:

- `page_type`
- `funnel_stage`
- `download_type`
- `access_type`
- `trial_download`
- `edition_id`
- `purchase_mode`
- `item_list_name`

Mark `purchase` as a key event. Consider marking `begin_checkout` and `dossier_download` as key events only if they represent meaningful business outcomes for the reporting period; the public sample is intentionally not a purchase conversion.

## Measurement limits

The download events measure a user initiating the browser download link. The paid delivery endpoint still controls entitlement and serves the protected file; GA4 is not a byte-level delivery or anti-sharing system. Stripe remains the source of truth for payment, and the verified `session_id` is used as the GA4 `transaction_id` so revisiting a success page does not create a new order in normal GA4 processing.
