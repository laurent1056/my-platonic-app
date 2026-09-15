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

## Production rules

- Verify each quotation against the named edition; do not use quote-aggregation sites.
- Do not combine or silently modernize translated passages. Mark omissions and edits.
- Keep quotations short enough to support the dossier's argument rather than substitute for the source text.
- Store the source ledger alongside the manuscript so credits are assembled during writing, not reconstructed before release.
- Export image credits and quotation notes into the final PDF before paid distribution is enabled.

