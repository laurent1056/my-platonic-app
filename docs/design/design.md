# Platonic Products — Design Language

**A datasheet with the gravity of an inscription.**

This is the canonical design specification for the rebuild (Astro + Tailwind). It supersedes the earlier `docs/DESIGN_SYSTEM.md` from the Gemini-era app. The working reference implementation is [`mockup-catalog-spec.html`](./mockup-catalog-spec.html); every token and component below maps to it.

---

## 1. Concept — *The Canon*

Plato gave us the **Form**: the single perfect Idea that every real object imperfectly imitates. This project is a register of Forms for manufactured goods — for each category, the one product that approaches the ideal, or the honest declaration that none does yet. That premise is already ancient. The design is **built from that lineage, not decorated with it.**

Three traditions, one modern surface:

| Tradition | What it gives us | Where it lives in the product |
|---|---|---|
| **The Greek stele** — carved inscription, not typeset page | Authority through restraint; lapidary capitals; proportion; the meander as the unbroken standard | Wordmark, section eyebrows, verdict stamps, masthead rule |
| **The Orthodox icon & iconostasis** — canonized images ranked in tiers | A DECLARED product is *canonized*: framed, gilded, given a nimbus, ranked in the register | Specimen plates, the index-as-register, the gold reserved for DECLARED |
| **The apophatic (*via negativa*)** — defining the divine by what it is *not* | EMPTY as a finding of equal gravity: we inscribe the ideal's absence and the shape it would have to take | The EMPTY plate, "what the category would require" |

The **modern half** keeps this from becoming a museum piece: monospace data, hairline rules, tabular numerals, information-design discipline. The tension between *inscription* and *datasheet* is the entire identity. Lose either and it fails — pure classicism reads as a wine label; pure spec-sheet reads as a parts catalog.

> **One line to hold in your head:** *It should feel like a canonical register carved by someone who also owns a caliper.*

---

## 2. Principles

1. **Declare, don't persuade.** The register states verdicts; it never markets. Copy is lapidary — short, certain, in the present tense. ("No product qualifies." not "Unfortunately, we couldn't find a great option.")
2. **Emptiness is a finding.** EMPTY entries get the same structural weight, the same plate, the same gravity as DECLARED ones. The apophatic verdict is the intellectual heart of the project — treat it as first-class, never as an error state.
3. **Gold is precious.** Like leaf on an icon, gold is rationed. It marks canonization (DECLARED) and nothing else. If gold appears more than once or twice per view, it has been debased.
4. **Every flourish is structural.** The meander marks a true division; the nimbus marks a true honor; the drop cap opens a true argument. No ornament that doesn't encode something.
5. **The data layer stays modern.** All values — prices, models, dates, confidence, codes — are monospace and tabular. This is the discipline that earns the right to be ornamental elsewhere.
6. **Proportion over decoration.** Generous inscription-margins, a strict type scale, hairline rules. Restraint is the classical virtue we're actually borrowing.
7. **The product drawing is an icon** — in both senses. Frontal, flattened, essential line-work, never a photorealistic render (see §9).

---

## 3. Color

The palette reads as **weathered marble, basalt ink, and iron-oxide** — the pigments of a red-figure vase and a Byzantine panel — with **gold rationed for canonization**. It deliberately avoids the flat cream + terracotta + serif template: the ground is a cool sage-grey, not cream; the ink is gunmetal, not black; and a monospace data layer runs through everything.

### Tokens — Light (`:root`)

| Token | Hex | Classical name | Use |
|---|---|---|---|
| `--paper` | `#E6E7E1` | Weathered Pentelic | Page ground |
| `--surface` | `#F1F1EC` | Dressed marble | Plates, raised cards |
| `--surface-2` | `#DEDFD8` | Shadowed stone | Table header, insets, meters |
| `--ink` | `#22272A` | Basalt | Primary text, DECLARED chip fill |
| `--muted` | `#5E645F` | Patina | Secondary text, labels |
| `--faint` | `#8A8F87` | Ash | Tertiary, row numbers |
| `--line` | `rgba(34,39,42,.16)` | Scribe line | Hairline rules |
| `--line-2` | `rgba(34,39,42,.34)` | Incised line | Structural rules, borders |
| `--accent` | `#8B3A2B` | Iron-oxide / bole | The single accent — rust, red-figure clay, and the red bole beneath gold leaf |
| `--gold` | `#9C7C33` | Chrysos (matte) | Canonization ornament only (see discipline below) |
| `--gold-lit` | `#B8963F` | Chrysos (lit) | Gold on ink / dark ground |
| `--empty` | `#8B3A2B` | — | State: EMPTY (uses accent) |
| `--review` | `#8A6D1F` | Attic ochre | State: in-review (candidate / split / conditional) |

### Tokens — Dark (`@media (prefers-color-scheme: dark)` and `:root[data-theme="dark"]`)

Dark is not an inversion — it's the **icon at candlelight / the cave wall**: a basalt ground with warm off-white inscription and gold that finally glows the way leaf does against a dark panel.

| Token | Hex |
|---|---|
| `--paper` | `#15181A` |
| `--surface` | `#1D2124` |
| `--surface-2` | `#23282B` |
| `--ink` | `#E4E6E0` |
| `--muted` | `#9BA199` |
| `--faint` | `#767C74` |
| `--line` | `rgba(228,230,224,.15)` |
| `--line-2` | `rgba(228,230,224,.32)` |
| `--accent` | `#CE6E56` |
| `--gold` | `#C8A24E` |
| `--gold-lit` | `#D8B15A` |
| `--empty` | `#CE6E56` |
| `--review` | `#C7A54E` |

> **Theme rule (robust pattern):** define the palette on `:root`, redefine tokens under `@media (prefers-color-scheme: dark)`, then redefine again under `:root[data-theme="dark"]` / `:root[data-theme="light"]` so the explicit toggle wins in both directions. Style components through tokens only — never hard-code a hex inside a component or a media query.

### Gold discipline (non-negotiable)

Gold has **low contrast** (~2.5:1 on marble) and is sacred to this system. Therefore:

- **Never** carry essential text in gold on the light ground. Body copy, values, and labels are always `--ink` / `--muted`.
- Gold is permitted **only** as: (a) the DECLARED nimbus mark, (b) a single gilded hairline under a DECLARED product name, (c) a versal drop-cap on a declared plate, (d) the wordmark diamond on ceremonial surfaces. Nowhere else.
- **Budget: at most one gilded element per plate, and one per masthead.** If you're reaching for a second, use `--accent` or `--ink`.

### State encoding (color is never the only signal)

| Verdict | Chip | Signal beyond color |
|---|---|---|
| **DECLARED** | Solid `--ink` fill, `--paper` text | Nimbus mark + gilded name rule; authoritative weight |
| **EMPTY** | Outline in `--empty`, transparent | Struck specimen bay ("No specimen admitted"); apophatic copy |
| **IN REVIEW** (candidate / split / conditional) | Outline in `--review` (ochre) | "— category must be divided" / status note in the model column |

Semantic state color is **separate from the accent** and must survive a greyscale test via the form differences above.

---

## 4. Typography

Three voices. The classical faces carry the *names and declarations*; the monospace carries the *evidence*; a quiet humanist sans handles UI chrome. Deliberately **not** Inter / Space Grotesk (the AI-safe defaults).

### Roles & recommended faces (self-hosted in production)

| Role | Recommended | Why | Fallback stack |
|---|---|---|---|
| **Inscriptional caps** — wordmark, section eyebrows (`§01`), verdict stamps | **Cinzel** | Literally Roman inscriptional capitals — the stele, cut into stone. Letterspaced, used *sparingly*. | letterspaced `"Palatino Linotype", Palatino, Georgia, serif` uppercase |
| **Display serif** — category & product names, the declarations | **Cormorant** (Garamond lineage) | High-contrast humanist classical serif; refined, "Platonic," reads as considered rather than corporate | `"Iowan Old Style", "Palatino Linotype", Palatino, "Book Antiqua", Georgia, serif` |
| **Body serif** — reasoning, prose | **EB Garamond** or **Spectral** | Manuscript warmth at reading sizes; pairs with the display without a clash | same old-style stack |
| **Data / mono** — every value, price, code, date, confidence | **IBM Plex Mono** or **JetBrains Mono** | Modern spec-sheet register; keeps the caliper in the room | `ui-monospace, "SF Mono", "DejaVu Sans Mono", Menlo, Consolas, monospace` |
| **UI micro-labels** — column heads, chips, captions | quiet humanist sans (e.g. **Public Sans**, **Libre Franklin**) | Neutral chrome that doesn't fight the serifs | `ui-sans-serif, system-ui, -apple-system, "Helvetica Neue", Arial, sans-serif` |

**Production note:** self-host and subset via `@font-face` (WOFF2). Do **not** hotlink Google Fonts — a strict CSP and performance both forbid it. The current mockup runs entirely on the fallback system stacks, so the design degrades gracefully if a face fails to load.

### Scale (modular, ~1.2)

| Token | rem | px | Use |
|---|---|---|---|
| `--fs-label` | 0.6875 | 11 | Uppercase micro-labels, letter-spacing `.14em` |
| `--fs-micro` | 0.75 | 12 | Captions, codes |
| `--fs-data` | 0.8125 | 13 | Monospace values in tables |
| `--fs-body` | 0.9375 | 15 | Body prose |
| `--fs-cat` | 1.02 | ~16 | Index category names (serif) |
| `--fs-plate` | clamp(1.5rem, 3.4vw, 2.15rem) | — | Specimen plate titles (serif) |
| `--fs-thesis` | clamp(2.1rem, 6vw, 3.5rem) | — | Masthead statement (serif), `text-wrap: balance` |

**Rules:** headings get `text-wrap: balance`; running prose caps near **65 characters**; all numerals use `font-variant-numeric: tabular-nums`; uppercase labels always carry letter-spacing (`.12–.2em`).

---

## 5. Layout & grid

- **The plate** — content max-width **~1120px**, centered, with generous inscription-margins (`clamp(14px, 3.5vw, 40px)` inline). White space is the classical material; don't fill it.
- **Hairline discipline** — structure is drawn with `--line` / `--line-2`, never with boxes-within-boxes. One weight of rule per job.
- **The index** — a full-bleed register table with `overflow-x: auto` so the body never scrolls sideways; a `min-width` keeps columns honest on mobile.
- **The plates** — a two-column grid at ≥860px that stacks to one column below. Each plate is bordered like an icon panel, with registration crosshairs at opposing corners (see §8).
- **Reject the background grid.** (Removed per direction — graph-paper reads as wireframe, not inscription. The ground stays plain marble.)

---

## 6. The classical vocabulary — motifs & flourishes

Every motif below has a **usage rule and a budget.** The failure mode here is gaudiness; the budget prevents it.

### The meander (Greek key)
The single most recognizable Greek border — an unbroken, continuous line folding back on itself. It encodes *the continuous, unbroken standard*.
- **Use:** one horizontal meander band in the **masthead only**, as the rule beneath the wordmark row. A thinner, lower-contrast echo may separate `§01` / `§02` section heads.
- **Never** a full four-sided border. One band, once. Render as a small repeating SVG tile or CSS mask so it scales crisply.
- **Budget: 1 prominent per page.**

### The nimbus (halo)
A saint in an icon wears a nimbus; a DECLARED product wears a restrained one — the mark of canonization.
- **Use:** a thin `--gold` arc or a small filled gold roundel (6px) preceding the **DECLARED** stamp, or a hairline gold semicircle behind the entry number on a declared plate.
- **Budget: 1 per declared plate. Never on EMPTY or IN REVIEW.**

### The gilded rule
- **Use:** a single 1px `--gold` hairline directly under the DECLARED product name (the one place the product is "lit"). EMPTY plates get an `--accent` hairline instead — struck, not gilded.
- **Budget: 1 per plate.**

### The versal / illuminated initial
Orthodox manuscripts open a passage with an oversized initial.
- **Use:** the first letter of "Why it ends the search" (DECLARED) or "Why the search stays open" (EMPTY) set as a 3-line drop-cap in Cormorant — `--accent` on EMPTY, `--gold` **only** if it hasn't spent the plate's gold budget elsewhere (usually it has → default to `--ink`/`--accent`).
- **Budget: 1 per plate, optional.**

### Lapidary capitals (the stele)
Inscriptions are cut in capitals. The wordmark, section eyebrows, verdict chips, and column heads are letterspaced uppercase — the "carved" register. Body and names are mixed-case (the "written" register). The contrast between carved and written is intentional.

### Registration crosshairs (the panel frame)
Thin corner marks at opposing corners of each plate — half machinist's registration mark, half icon-panel corner. They frame the specimen as a panel without a heavy border.
- **Budget: 2 corners per plate (opposing), 11px, `--line-2`.**

### Numbering as canon
Entry numbers (`No. 001`) are canonical catalogue numbers — like a canon of works or the numbering of psalms. They're monospace, and they're *real* (they order the register), so the numbering is earned, not decorative.

---

## 7. Components

### Masthead (the title block)
Wordmark (Cinzel caps + gold diamond tick) and a monospace revision line (`THE REGISTER · REV 2026.08 · ENTRIES N = 68`) over a **meander band**. Below: the thesis in display serif (*"One product per category. Or none."* — "none" in `--accent` italic), a one-sentence dek, and the **summary strip**.

### Summary strip
Four cells, hairline-divided: `CATEGORIES 68 · DECLARED 48 · EMPTY 12 · IN REVIEW 8`. Big monospace numerals; EMPTY in `--empty`, IN REVIEW in `--review`. This is the register's census — the first thing scanned.

### Index / the register table
Columns: `No.` · `Category` (serif) · `Verdict` (chip) · `The Model` (mono; EMPTY shows "— no product qualifies" in `--faint`) · `Price` (mono, right-aligned) · `Conf.` (meter). Hairline row rules; hover tints the row `--sel` and — on DECLARED rows only — surfaces a faint gilded left edge (the honor, on hover). Ranked like tiers of an iconostasis.

### Status chip
See §3 state table. Uppercase, letterspaced, 700 weight. DECLARED = solid; EMPTY / IN REVIEW = outline.

### Confidence meter
A 5-segment bar filled to the value, plus the monospace integer. Scale-honest: it shows *level*, not a claimed denominator. (Data currently ranges 2–4.)

### Specimen plate — DECLARED
Panel with registration corners. Header: entry number, category (serif), DECLARED chip **+ nimbus**, reference code (`PP-001`). A **specimen bay** holds the product *icon* (line-art, §9). Then the **canonized name** (serif) with its **gilded rule** and price. Fields: Form Definition · Why It Ends the Search (with optional versal) · Permanence tag · Key Disqualifiers (dashed list) · Admission Test (checklist, all ✓). Footer stamp: `LAST REVIEWED …` + confidence pips.

### Specimen plate — EMPTY (apophatic)
Same panel, same gravity — the *via negativa* made visible. The specimen bay is **struck**: a fine diagonal hatch bearing **"No specimen admitted."** In place of a canonized name, the declaration *"No product qualifies."* (serif italic, `--empty`). Fields: **Why the Search Stays Open** (the reasoning) · **What the Category Would Require** — an *unchecked* checklist in `--empty` (open, hatched boxes: the requirements the market has not met) · **Standing Verdict** ("Empty is not a gap in the register — it is a finding."). This component is the project's thesis; give it your best craft.

### Footer
Monospace colophon. Quiet.

---

## 8. Iconography — *the product is an icon*

Product illustrations follow the **icon / engraving** convention, not photography:

- **Frontal or canonical three-quarter**, flattened, essential — the *Form* of the object, not a specific lit unit.
- **Line-only**, `currentColor`, consistent stroke weight (~2px major / ~1.4px detail), no fills, no gradients, no shadows.
- Think **red-figure vase drawing** meets **technical patent illustration** — a lineage that is simultaneously ancient Greek and modern spec-sheet.
- Hand-author as inline SVG where simple (see the skillet in the mockup); for anything intricate, draw once and store as an optimized SVG asset. Never raster.
- EMPTY categories have **no icon** — the struck bay stands in for the absent Form.

---

## 9. Motion

Restrained to the point of near-stillness — inscriptions don't animate. Permitted: row-hover tint (120ms), the DECLARED gilded-edge reveal on hover, theme cross-fade. **No** page-load theatrics, parallax, or scroll-jacking — extra motion here reads as un-serious and machine-made. Everything wrapped in `@media (prefers-reduced-motion: reduce)`.

---

## 10. Voice & tone

Lapidary and canonical. Present tense, declarative, unhedged.

- **DECLARED:** state the Form, then the model that meets it. "12-inch cast iron with 3–4 mm walls holds thermal mass and resists temperature drops."
- **EMPTY:** apophatic. Name the absence plainly, then inscribe what the ideal would require. Never apologetic.
- **Disqualifiers:** factual and specific, never snarky. "Non-stick coatings degrade in 2–5 years" — the fact does the work.
- Avoid marketing verbs (*discover, unlock, elevate*), exclamation, and second-person persuasion. The register addresses no one; it records.

---

## 11. Accessibility

- Body text always `--ink`/`--muted` on `--paper`/`--surface` — WCAG AA. **Gold never carries essential text** (§3).
- State never conveyed by color alone — chips differ in fill vs. outline, plus copy and form (§3).
- Visible keyboard focus (`outline: 2px solid var(--accent); outline-offset: 2px`).
- `prefers-reduced-motion` respected; `prefers-color-scheme` honored with an explicit override toggle.
- Meander/nimbus/hatch are decorative → `aria-hidden`; the verdict is always available as text.
- Tables use real `<th scope>`; icons carry `aria-hidden` with the meaning in adjacent text.

---

## 12. Implementation notes (Astro + Tailwind)

- **Tokens are the contract.** Define the CSS custom properties (§3) in a single `tokens.css` imported globally; mirror them into `tailwind.config` `theme.extend.colors` as `var(--…)` references so utilities and raw CSS agree.
- **Fonts:** self-host WOFF2 subsets via `@font-face`; expose as `--serif`, `--serif-display`, `--caps`, `--mono`, `--sans`. Ship the system fallback stacks so first paint is never blank.
- **Motifs as components:** `<Meander />`, `<Nimbus />`, `<RegistrationCorners />`, `<Chip verdict />`, `<ConfidenceMeter value />`, `<SpecimenPlate />` (branches DECLARED / EMPTY / REVIEW). Each enforces its own budget so pages can't over-gild.
- **Data-driven:** category pages render from the register (CSV → typed content collection). Verdict → component branch; missing model → EMPTY treatment automatically.
- **Static per category** for SEO/crawlability (the original goal): `/category/frying-pan` etc., each a full inscription.

---

## 13. Reject-list (what this is *not*)

- ❌ **Flat cream + serif + terracotta** template — we ground with gunmetal ink, sage marble, and a live monospace data layer; the classical elements are structural.
- ❌ **Gaudy gold** — no gold gradients, gold text runs, gold buttons, or more than the §3/§6 budget. Leaf, not paint.
- ❌ **Costume classicism** — no faux-marble textures, no laurel-wreath clip-art, no column graphics, no all-caps Trajan slathered over everything. The classicism is in proportion, restraint, and one earned motif at a time.
- ❌ **Inter / Space Grotesk** as the primary voice, emoji section markers, everything-centered, `rounded-lg` on every card, purple→blue gradient heroes.
- ❌ **Treating EMPTY as an error** — it is a finding, and it gets the plate.

---

*Reference implementation: [`mockup-catalog-spec.html`](./mockup-catalog-spec.html). When code and this document disagree, update whichever is wrong — but keep them in sync.*
