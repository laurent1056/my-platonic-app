# Platonic Ideal — Site Maturity Plan

**Status:** Proposed implementation blueprint  
**Research basis:** Top 100 constitutional research completed 2026-09-10  
**Active authority:** Constitution 1.1.0

## The product we are building

Platonic Ideal is not a product-comparison store and not a ranked review site.
It is a public register of judgments:

> For a defined Form, one exact product may be declared—or the Form remains
> honestly unresolved or empty.

The mature site should make that judgment easy to discover, easy to
understand, and difficult to misread. A visitor should be able to move from a
broad category to the exact Form being judged, inspect the named product, see
the evidence and limits, and understand what would cause the ruling to change.

The completed Top 100 research (see [`docs/research/README.md`](./research/README.md)) makes the required structure visible. A
`Television` is not one Form. A `Router` may resolve inside a wired firewall
Form but not as a universal Wi-Fi recommendation. A `Smartphone` may contain a
repairable long-support child Form without making Fairphone the universal
winner. The site needs to show those relationships instead of flattening them.

## Current state

The current Astro rebuild is a strong constitutional shell, but its runtime
model is still a flattened historical register:

- `public/platonic_ideal.csv` is the only application data source;
- `src/data/register.ts` maps each row directly to one `RegisterEntry`;
- every row gets one `/category/[slug]/` page;
- search and filters operate on the rendered table and are not shareable URLs;
- a parent category and its child Form cannot be represented cleanly;
- evidence, cases, and ruling history live beside the display data rather than
  being first-class page entities;
- product images and purchase links are optional fields rather than a
  structured product record.

This is sufficient for the founding register and the 68-row migration view
(64 original entries plus four legacy child rows awaiting stable-ID
reconciliation).
It is not the final information architecture for 100 researched categories,
child Forms, public evidence receipts, and product dossiers.

## Canonical content model

The application should move toward this relationship:

`Domain → Category → Form → Case → Ruling → Product → Evidence`

Each layer has a distinct job.

### Domain

A browseable area such as Kitchen & Cooking, Outdoor & Utility, Electronics,
or Household Systems.

Suggested fields:

- `id`
- `slug`
- `name`
- `description`
- `displayOrder`
- `iconOrMark`

Domains are navigation, not a new ranking system.

### Category

The public concept a visitor recognizes: Smartphone, Camera, Water Heater,
or Razor.

Suggested fields:

- `id`
- `slug`
- `domainId`
- `name`
- `backlogNumber`
- `parentCategoryId` when the category is itself a child of a larger concept
- `summary`
- `currentState`: `DECLARED`, `EMPTY`, `IN_REVIEW`, or `SPLIT_REQUIRED`
- `formIds`
- `lastReviewed`

A category may remain unresolved while one or more of its child Forms are
declared. That is a meaningful public state, not a data error.

### Form

The coherent, bounded version of a category that the Constitution actually
judges.

Suggested fields:

- `id`
- `slug`
- `categoryId`
- `name`
- `statement`
- `ordinaryUse`
- `essentialConstraints`
- `exclusions`
- `jurisdiction`
- `permanenceMechanism`
- `status`
- `currentCaseId`

Examples:

- `Smartphone` → `Repairable long-support Android smartphone`
- `Router` → `Wired home/small-office firewall appliance`
- `Headphones` → `Wired open-back reference headphones`
- `Water Heater` → `50-gallon electric storage water heater`

The Form statement must never be reverse-engineered from the chosen product.

### Case

The editorial and constitutional work record behind a proposed or current
ruling.

Suggested fields:

- `id`
- `categoryId`
- `formId`
- `constitutionVersion`
- `workflowStatus`
- `candidateProductIds`
- `gateFindings`
- `hardDisqualifierFindings`
- `counterCase`
- `evidenceGaps`
- `confidence`
- `adjudicator`
- `decisionDate`
- `evidenceReceiptId`

Cases remain nonterminal while material evidence is missing. The private
Oracle may draft case language, but it cannot create a ruling or mutate this
record automatically.

### Ruling

The public conclusion and its history.

Suggested fields:

- `id`
- `formId`
- `verdict`
- `productId` when `DECLARED`
- `effectiveDate`
- `constitutionVersion`
- `caseId`
- `evidenceReceiptId`
- `supersedesRulingId`
- `revocationTrigger`
- `history`

The current ruling is a view over the append-only public history. A changed
model must not silently overwrite the old one.

### Product

The exact object being named, not a brand or family.

Suggested fields:

- `id`
- `manufacturer`
- `modelName`
- `modelIdentifier`
- `variant`
- `region`
- `productUrl`
- `priceAtReview`
- `availabilityNote`
- `imageIds`
- `serviceUrl`
- `partsUrl`
- `lastVerified`
- `reReviewTriggers`

The product page must state the exact variant and jurisdiction. “Framework
Laptop” or “Speed Queen” is not enough; the page needs the model/platform
record that was actually judged.

### Evidence

The public receipt for the claims that matter.

Suggested fields:

- `id`
- `sourceUrl`
- `publisher`
- `sourceRole`
- `evidenceClass`
- `claim`
- `claimType`: `DOCUMENTED_FACT`, `EDITORIAL_INFERENCE`, or `EVIDENCE_GAP`
- `retrievedAt`
- `independenceGroup`
- `commercialRelationship`
- `supportsOrContradicts`

The visitor should not have to trust the page's prose without seeing what
supports it.

## Public information architecture

### Primary routes

| Route | Purpose |
|---|---|
| `/` | Orientation, thesis, current census, featured declaration, and entry into the register |
| `/register/` | Full browseable register with shareable filters and search |
| `/domain/[slug]/` | Browse categories within one domain |
| `/category/[slug]/` | Parent category page: current state, Forms, scope, and resolution path |
| `/form/[slug]/` | The actual judged Form and its current ruling |
| `/product/[slug]/` | Exact product dossier, service identity, images, and acquisition links |
| `/methodology/` | Plain-language explanation of the admission test and evidence standard |
| `/constitution/` | Normative authority, version, digest, challenge boundary, and independence |
| `/ruling/[id]/` | Stable address for a public ruling receipt and history |
| `/evidence/[id]/` | Optional public source receipt when a source needs its own address |

The existing `/category/[slug]/` route should remain valid during migration.
For a category with one Form, it may redirect or canonicalize to the Form page.
For a split category, it should remain the parent overview.

### Parent category page

Every category page should answer these questions in order:

1. What does this category mean in the register?
2. Is the parent resolved, split, empty, or still under review?
3. What Forms exist beneath it?
4. What does each Form include and exclude?
5. Which Form, if any, has a current declaration?
6. Why is the parent not being given a false universal answer?

For `Smartphone`, the correct page may say “The broad category is not one
Form” and then link to “Repairable long-support Android smartphone.” That is a
stronger experience than placing Fairphone under a generic headline and
inviting a predictable objection.

### Form page

The Form page is the central editorial object. It should contain:

- the Form statement and ordinary-use boundary;
- inclusion and exclusion rules;
- status chip and constitutional version;
- the current product or an explicit “no product qualifies” finding;
- the short answer: why this ends the search inside this Form;
- five-gate findings;
- key disqualifiers and how they were handled;
- maintenance, failure modes, and permanence mechanism;
- strongest counter-case and disposition;
- evidence receipt with source classes and retrieval dates;
- confidence and last review;
- revocation/re-review triggers;
- a restrained acquisition action when commercial links are available.

The CTA should be “Read the ruling” or “Inspect the evidence” before it is
“Buy now.” A purchase link can exist, but it must never determine the ruling.

### Product page

The product page is not a second review and not a comparison page. It is the
identity and service dossier for the exact object named by one or more Forms.

It should show:

- manufacturer, model, exact identifier, variant, and region;
- product image with source/license credit;
- the Form(s) in which this object is declared;
- the product's role in the ruling, not a generic star rating;
- core construction and service interfaces;
- maintenance and replacement cycle;
- known failure modes and repair routes;
- current availability and price snapshot, clearly dated;
- official product, service, parts, and acquisition links;
- the ruling history and re-review triggers.

If the same product appears in two distinct Forms, each relationship must be
explicit. A product page does not become a universal endorsement merely
because it has more than one relationship.

## Filters and browse behavior

Filters should help a visitor find a kind of judgment, not simulate a ranking
engine.

### Initial filters

- **Domain:** Kitchen, Clothing, Outdoor, Electronics, Household Systems, and
  Personal Care/Misc.
- **Public state:** Declared, Empty, In review, Split required, Conditional,
  or Consumable.
- **Permanence mechanism:** Repairable, rebuild-based, warranty-based,
  rational renewal, or consumable.
- **Form shape:** single resolved Form, parent with child Forms, or unresolved
  parent.
- **Price band:** only as a dated practical field, never as a quality score.
- **Confidence:** 1–5, with the meaning explained; not a star rating.
- **Region:** only when availability, safety, law, or service access changes
  the case.
- **Has product image:** useful for content operations, not a judgment.

### URL behavior

The register should encode filters in the URL so a visitor can share a view:

`/register/?domain=electronics&state=declared&mechanism=repairable`

Search text can be encoded as `q=`. Sort should be limited to canonical order
and alphabetical order; confidence may be an optional editorial view but must
not imply a leaderboard.

The filter state must degrade gracefully without JavaScript. The initial HTML
should contain the complete register or a useful server-rendered subset, and
the client enhancement should only refine it.

### Search fields

Search should cover:

- category name;
- Form name and statement;
- manufacturer and exact model;
- domain;
- permanence mechanism;
- public state;
- short ruling summary.

Evidence claims should be discoverable within the dossier, but raw source text
does not need to become a global search index in the first implementation.

## Visual maturity

The current catalog/spec-sheet direction remains the right structural base,
but the interface should become more editorially legible as the data model
grows.

- Keep the modern catalog language: numbered records, specimen plates,
  monospace identifiers, hairline rules, and the meander as a restrained
  structural mark.
- Use the Greek/Orthodox flourishes to distinguish states, not to decorate
  every surface. A declared Form may receive the nimbus/gold canonization
  treatment; a split or EMPTY Form should remain visually dignified and
  un-gilded.
- Make parent/child relationships visible through hierarchy and labels rather
  than a dense graph or dashboard.
- Avoid a background grid. The page should feel like a legible register,
  archive, or technical catalogue—not a generic SaaS analytics screen.
- Give evidence and revision history the same visual dignity as the product
  image. Authority comes from the receipt, not only the hero object.

## Implementation sequence

### Unit 1 — Normalize the register

Create a typed content layer under `src/content/` or `src/data/` with separate
records for domains, categories, Forms, products, cases, rulings, and
evidence. Keep a CSV import/export adapter for the inherited 68-row data while
the constitutional records are migrated.

Deliverables:

- stable IDs and slugs;
- parent/child Form relationships;
- a single `currentRuling` view per Form;
- compatibility mapping for legacy CSV rows;
- validation that every terminal ruling has a case and evidence receipt.

### Unit 2 — Build the browseable register

Add `/register/`, domain pages, shareable URL filters, and visible state
counts. Preserve the current homepage as an orientation layer, but let the
register become the proper browse destination.

Deliverables:

- no-JavaScript useful register markup;
- URL-synchronized search and filters;
- domain/category/Form hierarchy;
- split and unresolved states that are understandable without opening the
  Oracle.

### Unit 3 — Build Form dossiers

Refactor the existing category dossier into a parent category page plus a Form
page. Move constitutional language, counter-cases, evidence receipts, and
review metadata into reusable dossier components.

Deliverables:

- `/category/[slug]/` parent pages;
- `/form/[slug]/` canonical judgment pages;
- evidence class display;
- explicit current status and re-review triggers;
- no hidden alternatives or runner-up rankings.

### Unit 4 — Build product dossiers and images

Add the exact Product entity, image credit record, product/service/parts links,
and dated availability fields. Follow the [Product Image System](./IMAGE_SYSTEM_PLAN.md)
for exactness, rights, local assets, and the specimen-portrait treatment.
Product pages should be generated only when a Form relationship exists.

Deliverables:

- `/product/[slug]/`;
- image source/license credits;
- model and variant identity block;
- maintenance and parts panel;
- commercial links isolated from the ruling text.

### Unit 5 — Complete the public institution loop

Add public ruling history, challenge receipts, revocation notices, and a
read-only evidence index. Keep the Oracle private and draft-only.

Deliverables:

- stable ruling URLs;
- append-only history display;
- evidence receipt pages;
- challenge intake boundary;
- validator coverage for all page data.

## Commercial boundary

The public verdict, Form definition, decisive reasoning, and evidence receipt
remain free. Monetization may sell convenience and depth:

- a printable dossier/PDF;
- a saved research packet or email digest;
- product acquisition links, clearly disclosed;
- a paid submission/research intake that buys editorial work, never a favorable
  verdict;
- premium historical or category reports.

The paywall must never hide the decisive reason for a ruling or create a
different paid verdict. The site becomes valuable because the public standard
is inspectable, not because the conclusion is secret.

## Invariants for every future release

1. No page calls a product “the ideal” without naming the exact Form.
2. No parent category receives a universal winner when the case is split.
3. No terminal ruling appears without a case, Constitution version, evidence
   receipt, counter-case, and decision date.
4. No filter creates a hidden ranking or “best for you” personalization.
5. No commercial relationship can edit the ruling or remove contrary evidence.
6. No model-family label is allowed where the evidence judged one exact
   variant.
7. No revocation erases the old public history.

## Recommended first implementation unit

Start with **Unit 1: Normalize the register**, then expose a read-only
`/register/` route using the same current 68 entries. This gives us a mature
information architecture without pretending the 100 researched categories are
already terminal. Once the case files and evidence packets are adjudicated, the
new Forms and products can flow into the same pages without another redesign.
