# Design System

The canonical design specification is [`design/design.md`](./design/design.md).

## Implemented system

- Greek-stele proportion and lapidary micro-labels
- Orthodox icon-panel treatment for DECLARED entries
- apophatic absence treatment for EMPTY entries
- modern monospace data layer and compact register structure
- restrained gold limited to canonization moments
- responsive table on desktop and dedicated mobile register rows
- light and candlelight-dark themes built entirely from CSS tokens

The original Gemini-era system is superseded. `src/styles/global.css` is the implementation contract; reusable motifs and states live in `src/components/`.
