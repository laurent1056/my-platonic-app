# Hypotheses — institution foundation

<!-- Paths in this file are relative to THIS file's location. -->

## Meta
- Feature: [institution foundation](../knowledge/product/features/institution-foundation.md)
- Status: active
- Created: 2026-09-08
- Last updated: 2026-09-08

## Value risk
### H-V1: A public Constitution and evidence receipt will make a singular verdict more trustworthy than an opaque recommendation score.
- **Origin:** proactive
- **Confidence:** medium
- **Evidence for:**
  - The project rulebook defines one product per category or `EMPTY` and requires explicit evidence and disqualifiers (chat, no artifact)
  - The Constitution makes the admission gates, evidence floor, revocation policy, and commercial boundary public [constitution](../constitution/CONSTITUTION.md)
- **Evidence against:**
  _(none yet)_
- **Open questions / caveats:**
  - No external reader has yet compared a constitutional receipt with a conventional buying guide.
- **Test:** Ask five qualified EDC/personal-carry buyers to explain a public verdict and identify what would overturn it; compare with an ordinary influencer recommendation.
- **Decision trigger:** Promote if readers can explain why the verdict exists and what would falsify it; revise if the rules feel like branding rather than evidence.
- **Status:** active
- **Resolution:** —

## Usability risk
### H-U1: A compact validator receipt will let a founder repair an incomplete case without learning the entire schema by trial and error.
- **Origin:** proactive
- **Confidence:** medium
- **Evidence for:**
  - The validator emits stable code, path, object ID, rule, message, and repair [source/validator](../scripts/lib/institution-validator.mjs)
  - The authoring workflow defines one canonical local command and distinguishes drafts from terminal records [source/workflow](../docs/INSTITUTION_WORKFLOW.md)
- **Evidence against:**
  _(none yet)_
- **Open questions / caveats:**
  - The first real multi-source case may reveal that errors need a richer evidence graph or editor affordance.
- **Test:** Time a fresh-clone maintainer from `npm ci` to a repaired terminal-fixture failure; target under five minutes to the first useful blocker.
- **Decision trigger:** Promote if the maintainer fixes the first blocker without opening implementation code; simplify or add a guided tool if not.
- **Status:** active
- **Resolution:** —

## Feasibility risk
### H-F1: Build-time JSON contracts and semantic validation can protect the institution without a database or runtime service.
- **Origin:** proactive
- **Confidence:** medium
- **Evidence for:**
  - The current Astro site already validates CSV data and builds static routes [source/validator](../scripts/validate-register.mjs)
  - The institution test suite covers terminal failures, duplicate IDs, missing references, ledger mismatch, and digest drift [source/tests](../scripts/test-institution.mjs)
- **Evidence against:**
  _(none yet)_
- **Open questions / caveats:**
  - The operational burden of append-only ledgers and evidence updates at 100+ categories is not yet observed.
- **Test:** Re-adjudicate the first Pocket Knife case through the new workflow and record elapsed time, errors, and manual exceptions.
- **Decision trigger:** Keep the file-based design if the case can be completed without validator exceptions; introduce stronger tooling only after repeated real friction.
- **Status:** active
- **Resolution:** —

## Viability risk
### H-B1: People will pay for research depth and convenience while the public authority remains free.
- **Origin:** proactive
- **Confidence:** low
- **Evidence for:**
  - The accepted founding-case boundary specifies a one-time `$24` evidence dossier and a 20/10/5 validation test [decision](../decisions/2026-09-08-constitution-and-paid-dossier-boundary.md)
  - The dossier is positioned as a way to avoid repeated comparison shopping, not as access to a hidden verdict (chat, no artifact)
- **Evidence against:**
  _(none yet)_
- **Open questions / caveats:**
  - There is no observed purchase signal, and the dossier contents and fulfillment path are not implemented.
- **Test:** After a credible founding ruling exists, invite 20 qualified EDC/personal-carry buyers and measure 10 purchases plus 5 reports of reduced or ended comparison shopping within 30 days.
- **Decision trigger:** 0–2 purchases stops infrastructure work; 3–9 revises the offer once; 10+ supports a second category test.
- **Status:** active
- **Resolution:** —

## Other risk
### H-O1: Paid research depth can remain independent from editorial outcome.
- **Origin:** proactive
- **Confidence:** medium
- **Evidence for:**
  - The Constitution prohibits payment from affecting selection, placement, score, challenge disposition, or decisive reasoning [constitution](../constitution/CONSTITUTION.md)
- **Evidence against:**
  _(none yet)_
- **Open questions / caveats:**
  - Fulfillment and affiliate disclosure rules will need review before commerce ships.
- **Test:** Red-team the first dossier against the public ruling and confirm every decisive claim remains available in the free evidence receipt.
- **Decision trigger:** Block the offer if a buyer must pay to understand or falsify the ruling.
- **Status:** active
- **Resolution:** —

## Lifecycle

This file is active and pre-ship. No hypothesis is promoted at initialization.
