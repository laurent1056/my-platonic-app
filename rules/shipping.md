# Shipping rules

> Definition of done, launch checklist, post-launch measurement window.

## Definition of done
<!-- What it takes for a feature to be considered shipped. Beyond merge: rollout state, telemetry, docs, support readiness. -->
For the current static product: relevant `npm run check`, `npm run validate:data`,
and `npm run build` pass; category routes render from the canonical CSV; the
index, `DECLARED`, `EMPTY`, and Oracle flows work in a browser; images have an
explicit source or fallback; accessible labels and canonical metadata are
present; and the relevant product docs are updated.

## Launch checklist
<!-- The minimum pre-launch verification. Avoid bureaucracy; keep load-bearing items only. -->
- Validate the CSV and confirm the one-model-or-empty invariant.
- Build the site and verify the generated route count, sitemap, metadata, and
  404 behavior.
- Smoke-test light/dark themes, mobile index browsing, category pages, empty
  states, image fallbacks, and Oracle-without-a-key.
- Check no secrets, `_archive/`, debug exfiltration code, or local-only files
  entered the active tree.
- Obtain separate approval before any public push or deployment.

## Post-launch measurement window
<!-- How long to wait before evaluating, which metrics to read, when to consider the experiment concluded. -->
No public measurement window exists yet. After a public release, use the first
two weeks as a lightweight observation period only if privacy-respecting
analytics are deliberately added; otherwise use founder sessions and incoming
feedback as qualitative signals.

## TODO
Define public launch verification and measurement only when a release is
actually approved.
