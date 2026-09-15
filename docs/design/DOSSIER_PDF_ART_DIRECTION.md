# Dossier PDF art direction

Decided 2026-09-15. The dossier should feel like the same publication on the storefront and inside the eventual PDF. Plato is the recurring visual witness: present on the cover, then echoed through openly licensed images of Greek antiquity and carefully sourced passages from the dialogues.

## Visual thesis

- Use Plato as the primary product identifier. The portrait belongs to the dossier itself, so it remains present wherever the cover appears.
- Treat antiquity as evidence and atmosphere, not costume. Favor sculpture, reliefs, vessels, architectural fragments, diagrams, inscriptions, and material details over generic columns or theatrical laurel imagery.
- Keep the current paper, basalt, iron-oxide, and muted-gold palette. Render historical images in restrained grayscale or mineral duotone so they belong to the editorial system.
- Give each image a job: establish a chapter idea, provide a pause in dense reading, or connect an abstract principle to a material object.

## Cover system

The shared web cover in `src/components/DossierCover.astro` is the starting point for the PDF cover:

1. Platonic Ideal and edition line
2. The Platonic Ideal Dossier title
3. Plato portrait with the Greek inscription `ΠΛΑΤΩΝ`
4. A short passage with work and Stephanus reference
5. Evidence · Judgment · Ownership colophon

The storefront uses the existing Silanion-type portrait from the Altes Museum. It is a Roman copy after a fourth-century BCE Greek original, photographed by Osama Shukir Muhammed Amin and licensed CC BY-SA 4.0. The crop, compression, and toning are adaptations, so the image credit and license must travel with full-size uses and appear in the PDF credit ledger.

## Interior image system

Use one large image at each chapter opening, with occasional smaller details where they support the argument. A chapter opener should pair:

- a chapter number and precise claim;
- one open image with a short factual caption;
- one verified passage from Plato;
- a complete source note in the image and quotation ledger.

Preferred source order:

1. Museum images explicitly marked CC0 or Public Domain, including Smithsonian Open Access, The Met Open Access, and Rijksmuseum.
2. Wikimedia Commons files with a clear Public Domain, CC0, CC BY, or CC BY-SA statement on the individual file page.
3. Commissioned or owned photography with written reuse terms.

“Free to view,” “educational use,” and an old subject are not enough. Rights attach to the photograph or scan as well as the ancient object. Record the exact asset page, creator, holding institution, object date, license, access date, and every adaptation.

## Approved quotation palette

These passages use Benjamin Jowett's translation. Project Gutenberg identifies the cited editions as public domain in the United States. Before commercial release, verify public-domain status in every intended sales territory and keep the translator, dialogue, and Stephanus reference with the quotation.

| Passage | Citation | Suggested use |
|---|---|---|
| “The many, as we say, are seen but not known, and the ideas are known but not seen.” | *Republic* VI, 507b | Cover or opening statement about Forms |
| “The beginning is the most important part of any work.” | *Republic* II, 377b | Introduction or research framing |
| “Beauty of style and harmony and grace and good rhythm depend on simplicity.” | *Republic* III, 400e | Design, restraint, and material clarity |
| “Knowledge which is acquired under compulsion obtains no hold on the mind.” | *Republic* VII, 536e | Reading path or reader agency |
| “The unexamined life is not worth living.” | *Apology* 38a | Closing reflection or methodology |

Source editions:

- [The Republic of Plato, translated by Benjamin Jowett, Project Gutenberg ebook 55201](https://www.gutenberg.org/ebooks/55201)
- [Apology, translated by Benjamin Jowett, Project Gutenberg ebook 1656](https://www.gutenberg.org/ebooks/1656)

## Attribution pattern

Keep reader-facing captions concise, then provide a complete credit ledger at the end of the PDF.

**Image caption**
Plato. Roman marble copy after a Greek original, 350–340 BCE. Altes Museum, Berlin.

**Image ledger**
Osama Shukir Muhammed Amin FRCP(Glasg), “Marble bust of the Greek philosopher Plato,” 2019. CC BY-SA 4.0. Cropped, compressed, and grayscale/sepia toned. Source URL and access date.

**Quotation note**
Plato, *Republic* VI, 507b, trans. Benjamin Jowett.

## Delta catalog reference

The user-supplied *Delta Power Tools 1940* catalog is a visual and editorial reference, not a template to reproduce. Its strongest lesson is that a product image earns attention by carrying evidence. Across 44 scanned pages, the catalog repeatedly pairs a large three-quarter machine view with construction details, cross-sections, operation sequences, dimensions, model tables, accessories, safety features, and practical reasons for each design choice.

The dossier should borrow that information density and confidence while keeping its own Platonic Ideal identity. It should not copy Delta illustrations, wording, page compositions, branding, or decorative details.

### Product plate families

Each category uses the smallest set of plates that explains the judgment:

1. **Identity plate** — a large three-quarter or axonometric exterior view of the exact declared model or candidate, with the visible features that establish identity.
2. **Construction plate** — a cutaway, cross-section, or restrained exploded view showing only internals verified by a service manual, parts diagram, teardown, patent, or direct inspection.
3. **Operation plate** — three to five frames showing the action that matters: adjustment, disassembly, cleaning, sharpening, replacement, packing, or repair.
4. **Comparison plate** — matched silhouettes, sections, or detail crops that make a decisive difference visible at the same scale.
5. **Ownership plate** — the parts, tools, consumables, intervals, and failure points a reader will encounter over time.
6. **Accessory plate** — compatible parts and attachments that extend useful life, with exact compatibility and availability notes.

Not every product needs all six. A hammer may need an identity plate and a forged-construction section. A drill or appliance may merit identity, construction, operation, and ownership plates.

### Page grammar

- Put one dominant plate near the top of a spread and let it establish the reading order.
- Reserve iron oxide for section words, numerals, arrows, and the single most important distinction. Use basalt ink for body copy and mineral grayscale for illustrations.
- Keep callout leaders short and uncrossed. Number dense diagrams and resolve their labels in a nearby evidence list.
- Place measurements on the illustration when scale changes the verdict; otherwise keep them in a compact specification block.
- Pair every feature claim with its consequence: what it improves, what it prevents, or what it costs the owner.
- Use model, variant, reviewed date, price snapshot, and evidence status as a consistent catalog footer.
- Keep margins, captions, and tables quieter than the plate. The pages may be dense, but the hierarchy must remain obvious at a glance.

### Illustration truth labels

Every created product image carries one of three visible labels:

| Label | Permitted source basis | What the image may claim |
|---|---|---|
| **Observed exterior** | Multiple exact-model photographs or direct photography | Exterior form, controls, proportions, and visible construction only |
| **Verified construction** | Exact-model service manual, parts diagram, teardown, patent, or direct inspection | The documented internal relationship shown in the cited source |
| **Conceptual mechanism** | General engineering evidence without exact-model internal documentation | A principle or failure path; never the exact model's hidden construction |

Do not generate plausible-looking internal components to fill gaps. If the evidence does not support an exploded view, show the exterior, the serviceable modules, or a conceptual mechanism on a separate clearly labeled plate.

### Reference-image workflow

1. Collect at least three exact-model exterior views and record their URLs, owners, dates, variants, and rights status.
2. Add manuals, parts diagrams, patents, and teardown evidence before planning an internal view.
3. Write a visual fact sheet: overall proportions, material boundaries, controls, fasteners, wear parts, safety features, and details that distinguish the variant.
4. Create original line or tonal artwork without logos or borrowed backgrounds. Manufacturer photographs marked `not-for-republish` may establish identity and visible facts, but must not appear in the dossier.
5. Compare the draft against every reference. Correct model drift, mirrored controls, invented fasteners, impossible joints, and inconsistent scale.
6. Attach the truth label, image ledger entry, and supporting source IDs before layout approval.
7. Retain the prompt, references, draft, review notes, and final asset so the illustration has an auditable provenance trail.

## Production rules

- Verify each quotation against the named edition; do not use quote-aggregation sites.
- Do not combine or silently modernize translated passages. Mark omissions and edits.
- Keep quotations short enough to support the dossier's argument rather than substitute for the source text.
- Store the source ledger alongside the manuscript so credits are assembled during writing, not reconstructed before release.
- Export image credits and quotation notes into the final PDF before paid distribution is enabled.
- Do not present image-generated artwork as product photography or mechanical evidence.
- Do not publish an exploded view until every depicted internal relationship has an exact-model source or is visibly labeled conceptual.
