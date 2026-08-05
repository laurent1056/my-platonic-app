# Routes and Views

Platonic Ideal remains a single-page app with in-memory view state.

## Current view set

- `home`
- `index`
- `category`
- `methodology`
- `oracle`

## Home

- introduction
- search entry
- declared/empty totals
- highlighted category cards

## Index

- search
- status filter
- alphabetical or declared-first sort

## Category

Dedicated rendered sections:

- status
- model/category title
- one-liner
- Why This
- Why Not Others
- Evidence
- Failure Modes
- Caveats
- Where to Acquire
- Last Reviewed
- Permanence Mechanism

Review section:

- `Source Fields` lists any populated CSV headers not already treated as identity-only fields

## Methodology

Explains the declaration rules, evidence standard, disqualifiers, and what `EMPTY` means.

## Oracle

Draft-assist UI only. It helps author content but does not replace the CSV as source of truth.

## URL behavior

The app does not currently provide crawlable per-category routes. View state is internal, and canonical SEO falls back to the project root URL.

