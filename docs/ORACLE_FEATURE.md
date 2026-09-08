# Oracle Feature

The Oracle is an optional local editorial assistant. It is not a public product surface and it never issues or publishes an institutional ruling.

## Intended workflow

- load the canonical Constitution and case schema
- accept category evidence or a challenge supplied by the editor
- draft or critique a structured case file
- mark unsupported claims and missing evidence explicitly
- save output outside the canon until a human reviews and commits it

## What it does not do

- appear in the public Vercel build
- accept public API keys
- write or publish canonical content automatically
- override the one-declaration-or-empty rule
- turn model output into evidence

## Migration state

The former browser-direct implementation has been removed from `src/pages/` and preserved at `src/studio/OracleStudio.astro` as migration reference. It still reflects the retired CSV-era prompt and is not considered the final local studio.

The replacement is blocked on the structured Constitution and case-file schema. Until then, the preserved component must not be imported into a public route.
