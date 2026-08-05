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

## Front-end mapping

The app maps the CSV into a smaller runtime shape:

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
- `Image URL` → image grid

Any populated non-identity field may also appear in the category page's `Source Fields` review block.

## Normalization rules

- `Slug` is derived from `Category` in the app rather than stored in the CSV.
- Whitespace is trimmed on load.
- Unknown columns are ignored safely.
- Existing compatibility columns such as `Core_Reasoning` are preserved because the app still reads them.

## Editorial constraints

- Never list multiple declarations for a single category.
- If the form splits into incompatible sub-forms, keep the parent unresolved or use child categories already present in the CSV.
- Prefer filling supported fields over adding new structure.

