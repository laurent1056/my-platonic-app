# Constitution

This directory owns the rules that make a Platonic Ideal ruling admissible.

- [`CONSTITUTION.md`](./CONSTITUTION.md) is the normative human-readable text.
- [`constitution.v1.json`](./constitution.v1.json) is the machine-enforceable
  profile for the same release.
- [`CHANGELOG.md`](./CHANGELOG.md) records amendments without rewriting history.

The JSON profile stores the SHA-256 digest of the normative text. The
institution validator fails when they diverge. Cases pin a Constitution version;
the current CSV cannot confer constitutional validity on its own.

## Authority flow

```text
Constitution ───────────────┐
                           ▼
Evidence ledger ───────► Case file ───────► Ruling ledger ───────► Public ruling
                              ▲                    │
Oracle draft (noncanonical) ──┘                    ▼
                                             Challenge docket
                                                   │
                                                   └──► re-adjudication
```

During migration, `public/platonic_ideal.csv` remains the compatibility source
for the current static site. A row becomes Constitution-admissible only after a
validated case produces a ruling-ledger event.

For the authoring loop, see [`docs/INSTITUTION_WORKFLOW.md`](../docs/INSTITUTION_WORKFLOW.md).
Run `npm run validate:institution` before treating any case as publishable.
