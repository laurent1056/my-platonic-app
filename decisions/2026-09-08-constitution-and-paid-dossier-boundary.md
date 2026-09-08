# Decision: Establish the Constitution as authority and monetize research depth, not verdicts

## Status
decided

## Date
2026-09-08

## Context
The Astro rebuild has a public register, but the inherited CSV does not yet
carry the full evidence, lifecycle, challenge, or terminal-admissibility
contract required by the authority proposition. At the same time, the founding
commercial idea is now clearer: readers may pay for a complete research dossier
without paying for a favorable outcome. The product needs one decision that
keeps those two systems separate.

## Options considered
1. Continue treating the CSV status field as the product authority and defer
   the commercial boundary.
2. Establish a versioned Constitution and validated case/evidence/ruling system,
   keep the public ruling free, and test a one-time paid dossier.
3. Add accounts, public submissions, affiliate ranking, and a metered paywall
   before the founding case is re-adjudicated.

## Decision
Use the versioned Constitution as the normative authority for new institution
records. Require evidence-backed case files, append-only ruling events, and
formal evidence-based challenges before a case can become terminal `DECLARED`
or `EMPTY`. Preserve the existing CSV as migration-compatible site data until
each row is explicitly re-adjudicated.

The public Constitution, verdict, decisive reasoning, evidence receipt, and
ruling history remain free. After the founding case and a small validation test,
the product may sell a one-time `$24` evidence dossier containing research
convenience and depth. Payment must never affect selection, placement, score,
challenge disposition, or the decisive public reasoning.

## Why
The authority proposition depends on rules that are inspectable and difficult
to game. A machine profile, schema, semantic validator, and public receipt make
the standard operational rather than merely rhetorical. Separating the free
verdict from paid depth protects trust while creating a narrow, testable revenue
hypothesis.

## Evidence
- The Constitution defines one current exact model or `EMPTY`, an evidence
  floor, public revocation, and commercial independence [constitution](../constitution/CONSTITUTION.md)
- The approved founding-case plan specifies a public ruling plus a one-time
  paid dossier and a 20/10/5 validation test (chat, no artifact)
- The current application has a CSV validator but no constitutional
  referential-integrity or terminal-admissibility checks [source/validator](../scripts/validate-register.mjs)
- The inherited CSV contains unresolved statuses and compatibility-column drift
  that require explicit re-adjudication before they can be treated as rulings [source/launch-plan](../source/adhoc/2026-09-03-project-baseline/CONSOLIDATION_AND_LAUNCH_PLAN.md)

## Explicitly NOT doing
- No affiliate ranking, sponsored verdicts, paid placement, popularity voting,
  guaranteed declarations, or pay-to-play petitions (chat, no artifact)
- No accounts, membership, metered paywall, broad public nominations, or public
  submissions in the founding launch (chat, no artifact)
- No Pocket Knife declaration in the institution foundation; the case begins as
  `DRAFT` and must be re-adjudicated from first principles (chat, no artifact)
- No payment integration, webhook, or private dossier fulfillment in the
  Constitution foundation unit (chat, no artifact)

## What would reverse this
Revisit the commercial offer after the founding validation test: if 50 qualified
visits produce 0–2 purchases, stop infrastructure work; if they produce 3–9,
revise the offer once; if they produce 10 or more purchases and at least 5
reports of reduced or ended comparison shopping within 30 days, test additional
categories. Revisit the authority boundary only through a new explicit decision
if paid access is shown to be necessary for trust or sustainability.

## Remaining ambiguities
- The exact contents and fulfillment mechanism of the first dossier are not yet
  implemented.
- The public ruling ledger and challenge UI are contracts now, not shipped
  public workflows.
- No external buyer has yet confirmed willingness to pay or the perceived value
  of research depth.

## Linked
- Strategy: [knowledge/strategy.md](../knowledge/strategy.md) § 1–2 quarter priorities and T2
- Roadmap: [knowledge/product/roadmap.md](../knowledge/product/roadmap.md)
- Institution feature: [knowledge/product/features/institution-foundation.md](../knowledge/product/features/institution-foundation.md)
- Constitution workflow: [docs/INSTITUTION_WORKFLOW.md](../docs/INSTITUTION_WORKFLOW.md)
