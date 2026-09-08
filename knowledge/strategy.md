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
2. **Make the register institutionally trustworthy.** Treat the Constitution
   as the normative authority, validate case/evidence/ruling/challenge records
   at build time, preserve the evidence receipt, and resolve the current
   `CANDIDATE`, `SPLIT_REQUIRED`, `CONDITIONAL`, and `CONSUMABLE` rows only
   through explicit re-adjudication. The CSV remains migration-compatible, not
   a shortcut around the evidence floor.
3. **Prove the founding case before scaling commerce.** Re-adjudicate
   Everyday Pocket Knife from first principles, keep the public verdict and
   reasoning free, and test a one-time `$24` evidence dossier with 20 qualified
   EDC/personal-carry buyers. The first success threshold is 10 dossier
   purchases and 5 reports of reduced or ended comparison shopping in 30 days.

## Explicit non-goals
<!-- What we are deliberately NOT doing this period. This is the most valuable section. -->
- Checkout implementation, fulfillment automation, affiliate ranking, or a
  marketplace before the founding case and willingness-to-pay test.
- Public submissions, voting, comments, accounts, and community moderation.
- A comparison engine that returns many “best” products, or a category tree that
  evades the one-declaration-or-empty rule.
- Analytics, CRM, or backend infrastructure before the founder-facing product
  is coherent and useful.
- Product selection influenced by sponsorship, payment, affiliate economics, or
  popularity.

## Bets vs. commitments
- **Bets** (testing): see [`hypotheses/`](../hypotheses/)
- **Commitments** (decided): see [`decisions/`](../decisions/)

## Last reviewed
<!-- Date. Updated whenever strategy is meaningfully revised. -->
2026-09-08

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

### T2 — Public authority vs. paid research convenience
- **Signal:** The accepted founding-case decision keeps the public verdict and
  decisive reasoning free while testing a one-time paid evidence dossier at
  `$24`, with payment never affecting the verdict. [Founding-case decision](../decisions/2026-09-08-constitution-and-paid-dossier-boundary.md)
- **What it tensions:** A dossier can fund research, but hidden decisive
  reasoning, sponsored placement, or paid petitions would destroy the authority
  proposition.
- **Possible resolution:** Keep the Constitution, evidence receipt, verdict,
  and ruling history public; test only research depth and convenience as the
  paid layer. Revisit the offer if the founding test misses 10 purchases in 30
  days or buyers cannot explain what they paid for.

### T3 — Founder-primary product vs. external usefulness
- **Signal:** Laurent is the only stakeholder and primary customer for now, with
  no formal discovery rhythm (stakeholder-verbal, Laurent, 2026-09-03).
- **What it tensions:** The aspiration for a public, useful register has not yet
  been tested with people other than its maker.
- **Possible resolution:** Optimize first for founder utility, then run small,
  deliberate external validation before community or commerce features.
