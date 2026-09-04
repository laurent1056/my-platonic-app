# Ingestion: security and privacy posture

- Captured: 2026-09-03
- Shape: adhoc migration
- Source: [verbatim security note](../../source/adhoc/2026-09-03-project-baseline/docs/SECURITY_PRIVACY.md)

## Observation

- The product is a static site with no accounts or server-side persistence.
- The Oracle sends a user-supplied Anthropic API key directly from the browser; persistent storage is explicit opt-in, and the key is not committed.
- Oracle output is draft text, not trusted fact; browser-direct keys are suitable only for a private authoring surface, not a public multi-user workflow.
- No analytics or cookies are part of the current browsing experience.

## Interpretation / route

Route to oracle-authoring, rules/shipping, metrics, and project-specific off-limits.

## Open question

- Recheck credential handling whenever the Oracle becomes public or commercial.
