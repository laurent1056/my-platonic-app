# Top 100 research index

The research pass now covers the complete Top 100 backlog. These reports are
the working editorial record; they do not themselves emit public rulings.
Constitution 1.1.0 still requires a bounded Form, evidence packet,
counter-case, adjudication, and ruling event before a product or EMPTY result
becomes terminal.

## Coverage

| Range | Record | State |
|---:|---|---|
| 1–64 | `public/platonic_ideal.csv` | Existing canonical register entries |
| 65–73 | [`batch-07-categories-065-073.md`](./batch-07-categories-065-073.md) | Research captured from prior analysis |
| 74–83 | [`batch-08-categories-074-083.md`](./batch-08-categories-074-083.md) | Research report committed |
| 84–93 | [`batch-09-categories-084-093.md`](./batch-09-categories-084-093.md) | Research report committed |
| 94–100 | [`batch-10-categories-094-100.md`](./batch-10-categories-094-100.md) | Research report committed |

## The numbering reconciliation

The live CSV now contains 100 records. Rows 1–64 remain the founding register;
rows 65–68 are the researched furniture sequence, and rows 69–100 are the
remaining research records. Four legacy child rows were migrated into
[`legacy-child-rows-065-068.md`](./legacy-child-rows-065-068.md) so their Form
constraints remain visible without creating duplicate top-level slugs.

Those four child rows are not being silently discarded. They remain in the
migration record while the mature data model assigns stable Category and Form
IDs. The final public census should be based on those IDs, not on historical
row numbers.

## Promotion queue

1. Reconcile the four legacy child rows with stable Category and Form IDs.
2. Convert each research disposition into a bounded Category + Form record.
3. Attach evidence receipts and identify missing counter-case evidence.
4. Resolve split parents before declaring any child Form.
5. Emit terminal rulings through the institution workflow.
6. Promote only adjudicated records into the public register and generate their
   Form, product, and ruling routes.

This separation keeps the site honest: “researched” means the question has
been worked through; “declared” means the institution has completed its public
constitutional process.
