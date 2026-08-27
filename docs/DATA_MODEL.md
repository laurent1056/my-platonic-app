# Data Model

The site is powered by one canonical CSV:

- `public/platonic_ideal.csv`

## Canonical header set

The current schema is:

1. `Number`
2. `Category`
3. `Status`
4. `Model`
5. `Price`
6. `Form Definition`
7. `Form Statement`
8. `Card Snippet (Why this ends the search)`
9. `Core Reasoning`
10. `Core_Reasoning`
11. `Key Disqualifiers`
12. `Key_Disqualifiers`
13. `Maintenance / Replacement Cycle`
14. `Permanence Mechanism`
15. `Images Needed`
16. `Image URL`
17. `Alternates (non-declared)`
18. `Admission Test`
19. `Failure Modes`
20. `Confidence`
21. `Last Reviewed`
22. `Notes`

## Status semantics

- `DECLARED`: one model is named and defended
- `EMPTY`: no current product qualifies
- `CANDIDATE`: not yet ready for declaration, but still worth tracking
- `SPLIT_REQUIRED`: the parent category fragments into incompatible Forms
- `CONDITIONAL`: a named model depends on explicit operating conditions
- `CONSUMABLE`: replacement is intrinsic to the category and must be judged rationally

The public design groups every non-`DECLARED`/non-`EMPTY` source status under `IN REVIEW`, while preserving and displaying the precise source status.

## Build-time mapping

`src/data/register.ts` parses the CSV during the Astro build and maps it into a typed shape:

- `Category` → category label
- `Status` → status badge
- `Model` → product title when declared
- `Price` → price line
- `Card Snippet (Why this ends the search)` or `Form Statement` → one-liner
- `Core_Reasoning` or `Core Reasoning` → main reasoning
- `Key_Disqualifiers` or `Key Disqualifiers` → why-not-others section
- `Admission Test` → evidence fallback when `Evidence` is absent
- `Failure Modes` → failure modes card
- `Last Reviewed` → metadata card
- `Image URL` → a real product image only when the URL is not a placeholder; otherwise the site uses its specimen-glyph system

Category pages render the mapped editorial fields directly into static HTML.

## Normalization rules

- `Slug` is derived from `Category` in the app rather than stored in the CSV.
- Whitespace is trimmed on load.
- Unknown columns are ignored safely.
- Existing compatibility columns such as `Core_Reasoning` are preserved because the app still reads them.

## Editorial constraints

- Never list multiple declarations for a single category.
- If the form splits into incompatible sub-forms, keep the parent unresolved or use child categories already present in the CSV.
- Prefer filling supported fields over adding new structure.
