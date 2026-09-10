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

The live CSV currently contains 68 rows. Rows 1–64 are the original Top 100
sequence. Rows 65–68 are legacy child categories created during an earlier
split pass (`Task Chair (New)`, `Task Chair (Used)`, and two food-storage
children); they occupy the same numeric range as the later Top 100 research.

Those four child rows are not being silently discarded. Before the researched
65–100 set is promoted, the data migration must preserve their useful Form
work, assign stable IDs, and decide whether they remain child Forms beneath a
parent category. The final public census should be based on stable category and
Form IDs, not on the historical row number.

## Promotion queue

1. Reconcile the four legacy child rows with the 65–100 research sequence.
2. Convert each research disposition into a bounded Category + Form record.
3. Attach evidence receipts and identify missing counter-case evidence.
4. Resolve split parents before declaring any child Form.
5. Emit terminal rulings through the institution workflow.
6. Promote only adjudicated records into the public register and generate their
   Form, product, and ruling routes.

This separation keeps the site honest: “researched” means the question has
been worked through; “declared” means the institution has completed its public
constitutional process.

