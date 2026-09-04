# Data rules

> Source-of-truth per metric, naming conventions, what counts as evidence.

## Source of truth per metric
<!-- For each tracked metric: where the canonical value lives. Two systems disagreeing is a signal, not a margin of error. -->
Product/category facts live in [`public/platonic_ideal.csv`](../public/platonic_ideal.csv). The typed build-time mapper is [`src/data/register.ts`](../src/data/register.ts), and the build validator is [`scripts/validate-register.mjs`](../scripts/validate-register.mjs). Operational product metrics live in [`knowledge/product/metrics.md`](../knowledge/product/metrics.md).

## Naming conventions
<!-- Event names, property names, segment definitions. Consistency over cleverness. -->
Category labels remain human-readable in the CSV; slugs are derived by the
Astro mapper. Status values must remain in the documented enum. `DECLARED` has
one model; `EMPTY` has no model; all other statuses are explicitly unresolved
or conditional and must not be presented as declarations.

## Evidence quality

What counts as evidence, by tier:

1. **Direct customer evidence** — quotes, interviews, support tickets, recorded behavior.
2. **Product analytics** — instrumented events, cohort behavior, funnel metrics.
3. **Stakeholder opinions** — internal but informed.
4. **Market / competitor signals** — directional, not definitive.
5. **Internal speculation** — lowest weight. Label as assumption.

## TODO
Deduplicate the two compatibility pairs (`Core Reasoning` / `Core_Reasoning`
and `Key Disqualifiers` / `Key_Disqualifiers`) in the canonical CSV, preserve a
single documented field name, and keep the validator green.
