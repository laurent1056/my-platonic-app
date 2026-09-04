# Search and Filter

The register supports client-side interaction over statically rendered entries:

- full-text search across category, model, verdict, permanence, and summary
- public verdict filter: all / declared / empty / in review
- sort: canonical order / alphabetical / confidence
- live result count and a semantic no-results state

Desktop uses a dense register table. Mobile uses purpose-built stacked rows; the same script keeps both representations synchronized. Filter state is intentionally ephemeral and is not indexed or encoded in the URL.
