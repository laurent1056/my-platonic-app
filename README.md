# PM Brain

A markdown-native second brain for a product operator — a PM, product lead, or anyone accountable for one product or initiative with judgment-heavy work and scattered inputs.

## What this is

- One repo. Markdown files. Versioned with git.
- One `CLAUDE.md` operating manual the agent reads at the start of every session.
- Pre-task load, post-task update — every task. No silent drift.

No vector database. No embeddings. No auto-tagging. The system is inspectable, editable, and auditable.

## How to start a session

1. Open this repo in Claude Code (or any agentic IDE).
2. The agent reads [`CLAUDE.md`](./CLAUDE.md) automatically.
3. Start a task. The agent routes through [`INDEX.md`](./INDEX.md) to the relevant area.

## First-week priorities

1. **Ingest one real category or product research note** — `/ingest adhoc`. See how the system turns founder research into durable context.
2. **Prep your next focused build session** — `/prep laurent-courtines`. In this founder-only phase, prep is a self-review rather than an external 1:1.
3. **Run `/review` on Friday.** The maintenance sweep is where most systems quietly die. Build the habit early.

## How the system thinks

- **Working memory vs durable knowledge.** Raw ingestion lives in `ingestion/`. Only recurring, decision-relevant, strategy-relevant signals get promoted into `knowledge/`.
- **Hypotheses vs decisions.** Bets being tested live in `hypotheses/`. Commitments made live in `decisions/`. They behave differently and stay queryable separately.
- **Flag, never gate.** The system surfaces conflicts, missing hypotheses, and strategy tensions. The PM resolves them. This is a reasoning system, not a compliance system.
- **Contradictions are preserved.** When evidence genuinely conflicts, the system writes the conflict down instead of flattening it into false consensus.

Full positioning and the five structural differentiators: [docs/overview.md](./docs/overview.md).

## Folder map

```
CLAUDE.md           Operating manual. Read every session.
INDEX.md            Master routing.
source/             Immutable evidence (if migrated from existing artifacts).
knowledge/          Durable, synthesized — strategy, product, users, market, org.
stakeholders/       One file per person.
hypotheses/         Feature-scoped, 5 risk areas (value/usability/feasibility/viability/other).
decisions/          Append-only log. Status: pending | decided | superseded.
rules/              How this PM runs discovery, prioritization, shipping, writing, data.
ingestion/          Working memory — interviews, meetings, market, adhoc.
maintenance/        Weekly sweep reports.
docs/               Workflows, schemas, overview, evolution guide.
Temp/               Scratch. Gitignored. Created on demand the first time you need it.
```

## Reference docs

- **[docs/overview.md](./docs/overview.md)** — What this is, what makes it different, what it's not. Read first.
- **[docs/workflows.md](./docs/workflows.md)** — Every slash command, what it loads, what it updates.
- **[docs/schemas.md](./docs/schemas.md)** — Cross-index of all schemas.
- **[docs/system-evolution.md](./docs/system-evolution.md)** — How to keep the system useful over time. The 8 failure modes and the 2-week / monthly / quarterly refinement cadence. Load before maintenance reviews.

## Platonic Ideal application

This PM Brain lives in the same repository as the product it supports. The
product is Platonic Ideal: a static editorial register that names one product
per category—or records an explicit `EMPTY` finding when no current product
qualifies.

The application is the Astro site in `src/`, with the canonical register in
[`public/platonic_ideal.csv`](./public/platonic_ideal.csv). Its current surface
includes the browse index, crawlable category dossiers, methodology, a local-only
Oracle authoring reference, and the Greek/Orthodox-inspired visual system in
[`docs/design/design.md`](./docs/design/design.md).

Use the application commands from the product README preserved at
[`source/adhoc/2026-09-03-project-baseline/README.md`](./source/adhoc/2026-09-03-project-baseline/README.md):

```bash
npm install
npm run dev
npm run check
npm run build
```

Product requirements and editorial rules remain in [`docs/`](./docs/). The
PM Brain folders at the repository root are the operating memory for strategy,
evidence, hypotheses, decisions, and maintenance; they do not replace the
product documentation.
