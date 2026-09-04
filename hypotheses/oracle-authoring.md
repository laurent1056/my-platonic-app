# Hypotheses — Oracle authoring

## Meta
- Feature: [Oracle authoring](../knowledge/product/features/oracle-authoring.md)
- Status: active
- Created: 2026-09-03
- Last updated: 2026-09-03

## Value risk
### H-V1: A private Oracle that drafts against the current rulebook will reduce the time needed to turn category research into a reviewable dossier.
- **Origin:** proactive
- **Confidence:** low
- **Evidence for:**
  - The Oracle feature is defined as an optional drafting helper for CSV content [source/oracle-feature](../source/adhoc/2026-09-03-project-baseline/docs/ORACLE_FEATURE.md)
- **Evidence against:**
  _(none yet)_
- **Open questions / caveats:**
  - No timed authoring session or draft-quality review has been recorded.
- **Test:** Time two comparable category drafts with and without the Oracle, then count unsupported claims and edits required.
- **Decision trigger:** Keep active if it reduces drafting time without increasing correction burden; narrow or remove it if it creates more review work than it saves.
- **Status:** active
- **Resolution:** —

## Usability risk
### H-U1: Clear warnings that the Oracle is a draft assistant, plus a structured output aligned to the CSV, will keep the author in control.
- **Origin:** proactive
- **Confidence:** low
- **Evidence for:**
  - The product docs say the Oracle never publishes, votes, or changes the canonical CSV [source/oracle-feature](../source/adhoc/2026-09-03-project-baseline/docs/ORACLE_FEATURE.md)
- **Evidence against:**
  _(none yet)_
- **Open questions / caveats:**
  - The rebuilt prompt may still carry fields from the older Gemini-era schema.
- **Test:** Use the tool for a category with a known empty verdict and verify that the output is easy to copy into the current field structure without implying publication.
- **Decision trigger:** Revise prompt/output hierarchy if Laurent mistakes draft text for canonical content or cannot map it to the register.
- **Status:** active
- **Resolution:** —

## Feasibility risk
### H-F1: A browser-only, user-keyed Oracle can remain optional and isolated from static browsing.
- **Origin:** proactive
- **Confidence:** low
- **Evidence for:**
  - The current application documents a private browser-based Oracle and says browsing does not depend on a key [source/README](../source/adhoc/2026-09-03-project-baseline/README.md)
- **Evidence against:**
  _(none yet)_
- **Open questions / caveats:**
  - Provider API behavior, browser CORS, and key persistence require live smoke testing.
- **Test:** Run the route with no key, a user-supplied key, provider failure, and empty output; confirm each state is recoverable and does not affect other routes.
- **Decision trigger:** Keep it client-side only if no credential or draft is sent anywhere except the intended provider request.
- **Status:** active
- **Resolution:** —

## Viability risk
### H-B1: The Oracle's cost and risk can stay bounded while it serves one founder and does not create a public service obligation.
- **Origin:** proactive
- **Confidence:** low
- **Evidence for:**
  - V1 scope is founder-led and the Oracle is private rather than a backend product capability [source/PRD](../source/adhoc/2026-09-03-project-baseline/docs/PRD.md)
- **Evidence against:**
  _(none yet)_
- **Open questions / caveats:**
  - Provider costs and any future public/revenue use are not planned.
- **Test:** Record qualitative usefulness and approximate request volume during a real drafting batch without adding analytics by default.
- **Decision trigger:** Reassess provider, limits, or scope if use becomes public, expensive, or commercially material.
- **Status:** active
- **Resolution:** —

## Other risk
### H-O1: Strongly stated Oracle caveats can prevent unsupported AI claims from entering the editorial register.
- **Origin:** proactive
- **Confidence:** low
- **Evidence for:**
  - The security documentation says Oracle output is draft text and not trusted fact [source/security](../source/adhoc/2026-09-03-project-baseline/docs/SECURITY_PRIVACY.md)
- **Evidence against:**
  _(none yet)_
- **Open questions / caveats:**
  - There is no review dataset of Oracle outputs and no automated claim verification.
- **Test:** Sample the first 10 drafts, mark unsupported claims, and update the prompt or review checklist before using outputs in the CSV.
- **Decision trigger:** Disable or constrain the Oracle if unsupported claims recur in drafts used for publication.
- **Status:** active
- **Resolution:** —
