# Ingestion: Oracle feature

- Captured: 2026-09-03
- Shape: adhoc migration
- Source: [verbatim Oracle feature](../../source/adhoc/2026-09-03-project-baseline/docs/ORACLE_FEATURE.md)

## Observation

- The Oracle accepts a prompt, sends it to Anthropic from the browser, and returns draft text for manual review and CSV entry.
- It does not write the CSV, override the one-declaration rule, or become a required browsing dependency.
- Session storage is the default for the user key, optional local storage is explicit, and the site should work without a key.

## Interpretation / route

Route to oracle-authoring, security/privacy, and the founder-first roadmap.

## Open question

- Reconcile the prompt's output headings with the deduplicated canonical schema.
