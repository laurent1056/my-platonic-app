# Search and Filter

## Current behavior

The current implementation supports:

- free-text search by category
- free-text search by model when present
- status filter: all / declared / empty
- sort: alphabetical / declared first

## Product intent

- keep the interaction quiet and fast
- do not add faceted complexity unless the CSV actually supports it
- do not expose filters for fields that are only review metadata

## Scope boundary

No shareable querystring state, keyboard shortcut system, or advanced multi-filter logic is part of the current product.

