# Hypotheses — static register and category dossiers

<!-- Paths in this file are relative to THIS file's location. -->

## Meta
- Feature: [static register and category dossiers](../knowledge/product/features/static-register.md)
- Status: active
- Created: 2026-09-03
- Last updated: 2026-09-03

## Value risk
### H-V1: A singular model-or-empty verdict with visible reasoning will help a motivated reader finish a category decision without comparing an endless list.
- **Origin:** proactive
- **Confidence:** low
- **Evidence for:**
  - The product requirements define the product around one category, one ideal product, or an explicit empty verdict [source/PRD](../source/adhoc/2026-09-03-project-baseline/docs/PRD.md)
- **Evidence against:**
  _(none yet)_
- **Open questions / caveats:**
  - No external reader has confirmed that a singular verdict is more useful than a shortlist.
- **Test:** Use the register for 5 real founder category questions; then ask 3 external readers to complete one category decision when external discovery is in scope.
- **Decision trigger:** Promote only if users can explain the verdict and report that the page reduced, rather than redirected, their search; demote if users need a comparison list to act.
- **Status:** active
- **Resolution:** —

## Usability risk
### H-U1: A browse index that leads to a clear above-the-fold dossier verdict will let a reader orient and act without learning the underlying editorial system first.
- **Origin:** proactive
- **Confidence:** low
- **Evidence for:**
  - The current product surface includes an index, crawlable category dossiers, and first-class declared/empty treatments [source/README](../source/adhoc/2026-09-03-project-baseline/README.md)
- **Evidence against:**
  _(none yet)_
- **Open questions / caveats:**
  - The current local build has not been tested with an external task-based usability session.
- **Test:** Observe whether a first-time reader can find a category, identify its state, and state the recommended action in under two minutes.
- **Decision trigger:** Promote if 4 of 5 observed sessions succeed without explanation; redesign if users miss the verdict or mistake an empty state for a loading error.
- **Status:** active
- **Resolution:** —

## Feasibility risk
### H-F1: Astro plus the canonical CSV can generate a stable, maintainable static route for every category without a backend.
- **Origin:** proactive
- **Confidence:** low
- **Evidence for:**
  - The application README documents Astro build-time mapping, a CSV validator, and generated category routes [source/README](../source/adhoc/2026-09-03-project-baseline/README.md)
- **Evidence against:**
  _(none yet)_
- **Open questions / caveats:**
  - Schema cleanup and future image sourcing could introduce build-time failure modes.
- **Test:** Run validation, type checking, and a production build after schema cleanup and confirm route, sitemap, and asset counts.
- **Decision trigger:** Promote after two clean builds from a fresh install; revise the architecture if route generation requires runtime data or manual page edits.
- **Status:** active
- **Resolution:** —

## Viability risk
### H-B1: A founder-operated static register can deliver enough value to justify continued work before a revenue model is chosen.
- **Origin:** proactive
- **Confidence:** low
- **Evidence for:**
  - The current requirements intentionally keep the product static and out of e-commerce, accounts, and backend APIs [source/PRD](../source/adhoc/2026-09-03-project-baseline/docs/PRD.md)
- **Evidence against:**
  _(none yet)_
- **Open questions / caveats:**
  - Continued founder use is not a business model and no external willingness-to-pay signal exists.
- **Test:** Use the product through a complete content/design iteration and record whether it changes Laurent's own buying or research behavior; defer monetization testing until the editorial value is stable.
- **Decision trigger:** Keep active if founder use creates repeated decisions or content; open a separate revenue hypothesis if external usage or commercial demand appears.
- **Status:** active
- **Resolution:** —

## Other risk
### H-O1: Greek stele, Orthodox icon, and apophatic motifs can make canonical status memorable without reducing legibility or accessibility.
- **Origin:** proactive
- **Confidence:** low
- **Evidence for:**
  - The design language specifies restrained motifs, semantic status encoding, and accessibility requirements [source/design-language](../source/adhoc/2026-09-03-project-baseline/docs/design/design.md)
- **Evidence against:**
  _(none yet)_
- **Open questions / caveats:**
  - Aesthetic preference is currently founder evidence, not audience evidence.
- **Test:** Run the keyboard, contrast, reduced-motion, and task-completion checks against the redesigned routes; then collect qualitative reactions from external readers when available.
- **Decision trigger:** Preserve motifs if they improve recognition without failing accessibility; reduce ornament if it competes with the verdict or controls.
- **Status:** active
- **Resolution:** —

## Lifecycle

This file is active and pre-ship. No hypothesis is promoted at initialization.
