# Strategy

> The north star. Loaded at the start of any prioritization, planning, or review task. Updated only deliberately — drift is surfaced, not silently absorbed.

## North-star metric
<!-- From interview. One metric, with definition and current value. -->

**Provisional north star: evidence-complete, current category dossiers.** A
dossier counts when its status, model-or-empty verdict, Form reasoning,
disqualifiers, permanence mechanism, admission test, failure modes, confidence,
review date, and image decision are explicit enough to publish. Current baseline
is 68 category rows: 48 `DECLARED`, 12 `EMPTY`, and 8 unresolved rows grouped by
the UI as `IN REVIEW`. This is an operational product metric, not a measure of
external demand; no public analytics are instrumented yet.

## 1–2 quarter priorities
<!-- 3 max. Ordered. Each with: what, why now, what success looks like. -->
1. **Ship the coherent static register.** Finish the Astro rebuild as a clear,
   fast browse experience with an index, crawlable category dossiers, first-
   class `DECLARED` and `EMPTY` states, product imagery, and the catalog/spec-
   sheet visual language. Success is a green check/build, a usable index, and a
   route for every current category.
2. **Make the register editorially trustworthy.** Freeze the CSV schema,
   remove compatibility-column ambiguity, validate every row at build time, and
   resolve the current `CANDIDATE`, `SPLIT_REQUIRED`, `CONDITIONAL`, and
   `CONSUMABLE` rows to a defensible declaration or `EMPTY` finding before
   expanding the register toward 100 categories.
3. **Use the founder loop to learn what deserves expansion.** Keep the Oracle
   private and make it useful for drafting and critique. Use Laurent's own
   browsing and authoring sessions to improve the product before investing in
   external discovery or a revenue model.

## Explicit non-goals
<!-- What we are deliberately NOT doing this period. This is the most valuable section. -->
- E-commerce checkout, affiliate revenue, or a marketplace; the eventual revenue
  model is intentionally unresolved.
- Public submissions, voting, comments, accounts, and community moderation.
- A comparison engine that returns many “best” products, or a category tree that
  evades the one-declaration-or-empty rule.
- Analytics, CRM, or backend infrastructure before the founder-facing product
  is coherent and useful.

## Bets vs. commitments
- **Bets** (testing): see [`hypotheses/`](../hypotheses/)
- **Commitments** (decided): see [`decisions/`](../decisions/)

## Last reviewed
<!-- Date. Updated whenever strategy is meaningfully revised. -->
2026-09-03

## Tensions
<!-- Maintenance and ingestion append here when signals conflict with the strategy. Tensions are not rejections — new bets, features, opportunities, and user needs can inform strategy just as strategy informs them. Each entry: signal, what it tensions, possible resolutions (update strategy / reject signal / hold as open tension). PM resolves deliberately. -->

### T1 — Singular verdict rule vs. unresolved rows
- **Signal:** The inherited baseline contains 8 rows that the UI groups as
  `IN REVIEW`, including `CANDIDATE`, `SPLIT_REQUIRED`, `CONDITIONAL`, and
  `CONSUMABLE` states. [Baseline launch plan](../source/adhoc/2026-09-03-project-baseline/CONSOLIDATION_AND_LAUNCH_PLAN.md)
- **What it tensions:** The editorial commitment to one model per category or
  `EMPTY`.
- **Possible resolution:** Resolve each row before calling the register complete;
  preserve a provisional state only while the evidence work is explicitly open.

### T2 — Current editorial scope vs. future revenue
- **Signal:** The current requirements define the product as a static catalog,
  not e-commerce or a marketplace. [Current PRD](../source/adhoc/2026-09-03-project-baseline/docs/PRD.md)
  Laurent also stated that revenue is a longer-term interest whose model has not
  been worked through (stakeholder-verbal, Laurent, 2026-09-03).
- **What it tensions:** A future desire to generate revenue could pull the v1
  register toward affiliate links, commerce, or commercial bias before trust is
  established.
- **Possible resolution:** Keep v1 editorial and model revenue as a later,
  evidence-led decision with explicit disclosure and reversal criteria.

### T3 — Founder-primary product vs. external usefulness
- **Signal:** Laurent is the only stakeholder and primary customer for now, with
  no formal discovery rhythm (stakeholder-verbal, Laurent, 2026-09-03).
- **What it tensions:** The aspiration for a public, useful register has not yet
  been tested with people other than its maker.
- **Possible resolution:** Optimize first for founder utility, then run small,
  deliberate external validation before community or commerce features.
