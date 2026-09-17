# Platonic Ideal dossier

The current build is the declared edition at
`output/pdf/platonic-ideal-dossier-declared-1940.pdf`. It follows the supplied
Platonic Ideal 1940 twenty-page proof as the visual and editorial baseline, then
extends that rhythm across every declared product.

The public storefront remains unchanged. Its Greek icon treatment belongs to the
site. Dossier product plates are a separate art direction: clean warm-ivory
industrial views with large objects, separated details, and no Greek icon,
laurel, marble slab, halo, or decorative panel behind the product.

## Page sequence

- **1** Cover
- **2** Full-page Plato quote and a large portrait with both eyes visible
- **3** Field index: all declared categories in alphabetical order, with category
  names and spread page numbers only
- **4** Six tests before a declaration, condensed to one page
- **5 onward** Three pages per recommendation: the pick and a large multi-view
  plate; fit/use and serious alternatives; care, parts, service, and stop
  conditions
- **After the recommendations** Quick comparison for every product, product
  sources, an image and rights glossary, and a final reader checklist

There are **48 DECLARED records** in the working CSV. The brief sometimes says
46; the build carries all 48 so no declared item disappears without a decision.
The first four spreads follow the proof order: Drill, Frying Pan, Hammer,
Screwdriver. The remaining spreads are alphabetical.

## Value carried inside the book

Each recommendation puts the useful source-derived facts next to the decision:
model and variant, dimensions or capacity, construction, what ownership asks of
you, care routine, likely wear symptoms, service and parts path, serious
alternatives, and a link to the maker or seller. The source pages at the back
make those references easy to check and update; they are not a substitute for
the information on the product spread.

Every declared product has at least three dossier images:

1. a dominant clean multi-view plate;
2. a dedicated fit or use action scene showing the object doing its primary
   job, with its working surface, load, hands, or setting clearly visible; and
3. a clean detail plate derived from the same approved object study. The care
   page also typesets a four-part **Parts to Watch** callout rail so the reader
   can connect the detail view to inspection and service.

The image and Creative Commons notes live in the glossary at the back. The
product pages keep the reader focused on the object and the decision.

## Build commands

```sh
# Current edition (default)
python3 scripts/build-dossier-delta.py

# Write HTML only while checking layout
python3 scripts/build-dossier-delta.py --html-only

# Supplied 20-page proof for comparison
python3 scripts/build-dossier-delta.py --proof \
  --output output/pdf/platonic-ideal-dossier-1940-20-page-proof.pdf

# Archived full-register comparison (not the current edition)
python3 scripts/build-dossier-delta.py --legacy-full \
  --output output/pdf/platonic-ideal-dossier-full-review.pdf
```

The default output is a 157-page PDF: four front pages, 144 product pages, four
comparison pages, three source pages, an image and rights glossary, and a final
reader checklist.

## Image truth and sources

Product plates are original editorial raster interpretations based on the named
model and the cited identity source. They are not factory photographs, exact
engineering drawings, or safety instructions. Every declared chapter now has a
dedicated action scene showing the object doing its job.

Manufacturer and retailer imagery is used as an identity reference and is not
republished as a product photograph. Exact specifications, care instructions,
stock, price, and regional service should be checked at the linked source before
purchase. `assets/editorial/IMAGE_PROMPTS.txt` records the generated art briefs,
including the clean-plate family and the commissioned Bahco 8071, extension
cord, ladder, and Windsor chair plates.
