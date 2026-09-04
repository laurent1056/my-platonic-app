# Hypotheses — category dossier content

## Meta
- Feature: [category content and evidence](../knowledge/product/features/category-content-and-evidence.md)
- Status: active
- Created: 2026-09-03
- Last updated: 2026-09-03

## Value risk
### H-V1: Well-supported entries with explicit disqualifiers will make the register more trustworthy than unsupported product recommendations.
- **Origin:** proactive
- **Confidence:** low
- **Evidence for:**
  - The content guide requires a reasoned Form definition, core reasoning, disqualifiers, admission test, and failure modes [source/content-guide](../source/adhoc/2026-09-03-project-baseline/docs/CONTENT_GUIDE.md)
- **Evidence against:**
  _(none yet)_
- **Open questions / caveats:**
  - No external reader has compared an evidence-complete entry with a conventional buying guide.
- **Test:** Compare two representative dossiers with and without the evidence packet in founder and later external decision tasks.
- **Decision trigger:** Promote if evidence fields change confidence or action; simplify if readers ignore them without losing trust.
- **Status:** active
- **Resolution:** —

## Usability risk
### H-U1: A consistent category template can make long-form reasoning scannable rather than overwhelming.
- **Origin:** proactive
- **Confidence:** low
- **Evidence for:**
  - The inherited content templates define separate declared, empty, and candidate/child treatments [source/content-templates](../source/adhoc/2026-09-03-project-baseline/docs/CONTENT_TEMPLATES.md)
- **Evidence against:**
  _(none yet)_
- **Open questions / caveats:**
  - The amount of reasoning varies widely by product category.
- **Test:** Ask a first-time reader to locate the verdict, Form statement, disqualifiers, and failure modes on three pages.
- **Decision trigger:** Reorder or collapse fields if readers cannot find the reason for the verdict quickly.
- **Status:** active
- **Resolution:** —

## Feasibility risk
### H-F1: A frozen CSV contract plus a build validator can prevent malformed or contradictory rows from reaching the site.
- **Origin:** proactive
- **Confidence:** low
- **Evidence for:**
  - The current build contract includes a data validator and documents status/model constraints [source/data-model](../source/adhoc/2026-09-03-project-baseline/docs/DATA_MODEL.md)
- **Evidence against:**
  - The baseline still has duplicate compatibility columns and 8 unresolved statuses [source/launch-plan](../source/adhoc/2026-09-03-project-baseline/CONSOLIDATION_AND_LAUNCH_PLAN.md)
- **Open questions / caveats:**
  - The validator's final rules after schema cleanup are not yet defined.
- **Test:** Define one canonical header set, add duplicate-field and model/status checks, and run the validator against every current row and a small malformed fixture set.
- **Decision trigger:** Promote when invalid fixtures fail for the intended reason and the current dataset passes without manual exceptions.
- **Status:** active
- **Resolution:** —

## Viability risk
### H-B1: Editorial rigor can be maintained by one operator without requiring a heavyweight content-management system.
- **Origin:** proactive
- **Confidence:** low
- **Evidence for:**
  - The product is explicitly CSV-driven with no backend API or database in v1 [source/PRD](../source/adhoc/2026-09-03-project-baseline/docs/PRD.md)
- **Evidence against:**
  _(none yet)_
- **Open questions / caveats:**
  - The maintenance cost at 100 categories and beyond is unknown.
- **Test:** Time one complete category revision from research note through validated build; use the result to set a sustainable content batch size.
- **Decision trigger:** Add tooling or narrow scope if one revision repeatedly requires more effort than the founder can sustain.
- **Status:** active
- **Resolution:** —

## Other risk
### H-O1: The one-declaration-or-empty rule can preserve honesty when a category splits, if unresolved states are visible and actively resolved.
- **Origin:** proactive
- **Confidence:** low
- **Evidence for:**
  - The launch plan explicitly identifies `SPLIT_REQUIRED` and other in-review states as data-integrity work [source/launch-plan](../source/adhoc/2026-09-03-project-baseline/CONSOLIDATION_AND_LAUNCH_PLAN.md)
- **Evidence against:**
  _(none yet)_
- **Open questions / caveats:**
  - Some categories may need a narrower definition rather than a forced parent verdict.
- **Test:** Resolve the current in-review rows one at a time and record whether the result is a model, empty finding, or a justified category rewrite.
- **Decision trigger:** Keep the rule if it produces clearer category boundaries; create an explicit exception policy only if repeated evidence shows the rule is structurally insufficient.
- **Status:** active
- **Resolution:** —
