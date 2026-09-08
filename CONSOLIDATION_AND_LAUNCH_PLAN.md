# Platonic Ideal — Consolidation & Launch Plan

_Historical audit + path to launch. Generated 2026-08-04; status updated 2026-09-08._

> This document preserves the original consolidation diagnosis. The repository has
> since been consolidated and the app rebuilt in Astro. Current implementation,
> deployment, and product requirements live in `README.md`, `docs/DEPLOYMENT.md`,
> and `docs/PRD.md`.

---

## 1. What you actually have

There are **two lineages** of this project tangled together on disk, plus a set
of nested duplicate copies. Everything traces back to one of these two:

### Lineage A — "Vision" (older)
- Monolithic App files at top level: `App_original.jsx`, `App_platonic_v2.jsx`,
  `App_platonic_v3.jsx` (1,250–1,490 lines each).
- Oracle uses **Google Gemini** (`ConsultView`), API key from a `VITE_GEMINI_API_KEY`
  env var (client-exposed).
- Data schema: `Slug, One_Liner, Why_Not_Others, Evidence, Where_to_acquire,
  Image_URL_1..4, Parent/Child_Categories` — richer, category-tree oriented.
- CSV name: `platonic_ideal_1-64.csv`.
- The **Google Drive project docs describe THIS lineage** (ARCHITECTURE, ROADMAP,
  master PRD reference `App_platonic_v3.jsx`).
- ⚠️ All three files contain leftover **debug exfiltration** code that POSTs to
  a localhost debug endpoint including a prefix/length of the API key.

### Lineage B — "Shipped / Canonical" (newer, this is the real app)
- Single clean `src/App.jsx` (934 lines), 5 views (Home, Index, Category,
  Methodology, Oracle).
- Oracle uses **Anthropic** (`OracleView`), key in `localStorage` (`PI_ORACLE_KEY`) —
  a local authoring tool, no key bundled, **no exfiltration code**.
- Data schema: `Number, Category, Status, Model, Price, Form Definition,
  Form Statement, Card Snippet, ... Permanence Mechanism, Admission Test,
  Confidence, Last Reviewed`.
- CSV name: `platonic_ideal.csv` (68 categories).
- Git remote: `github.com/laurent1056/my-platonic-app.git`.
- Current deploy target: Vercel (`my-platonic-app.vercel.app`); the former GitHub
  Pages build is retained only as a short-lived rollback target.

**→ Lineage B is the canonical app. Everything else is history or duplication.**

### The nesting mess (the "Russian doll")
```
Platonic-Ideal/                         ← working folder (NOT git)
├── App_original.jsx  App_platonic_v2/v3.jsx   ← Lineage A leftovers (+exfil code)
├── platonic_ideal_v4..v7.csv                  ← 4 stale CSV copies (all ~68 rows)
├── product_image_urls.md, *.docx
│
└── platonic-ideal/                     ← ✅ THE canonical git repo (Lineage B)
    ├── src/App.jsx  public/platonic_ideal.csv  docs/ (14 reconciled MD)
    ├── my-platonic-app/                ← ❌ 2nd git repo, older, SAME remote,
    │                                        holds .env + .env.local with LIVE key
    ├── platonic-ideal/                 ← ❌ non-git copy + source.tar.gz + own docs
    │   └── {src,public}/               ← ❌ literal broken brace-expansion dir
    └── {src,public}/                   ← ❌ another broken brace-expansion dir
```

---

## 2. Security finding — resolved

1. The exposed Gemini API key was revoked. Its value remains redacted here; old
   local exports and repository history must continue to be treated as sensitive.
2. The key is **not** in the current build bundles on disk and **not** in the
   canonical `src/App.jsx`. Good. The exposure is git history + the two `.env`
   files only.
3. When we archive/remove Lineage A, the old localhost exfiltration code goes
   with it. It never made it into the shipped app — but confirm it's gone before
   any redeploy.

---

## 3. Consolidation — collapse to one clean tree

Non-destructive approach: **move** cruft into `_archive/` (nothing deleted), leave
one clean canonical repo. Proposed end state:

```
Platonic-Ideal/
├── app/                      ← the canonical repo, flattened (was platonic-ideal/)
│   ├── src/App.jsx
│   ├── public/platonic_ideal.csv   ← single source of truth
│   ├── docs/                 ← reconciled as-built docs + vision docs merged in
│   └── .gitignore            ← ignores node_modules, dist, .env*
├── data/
│   └── platonic_ideal.master.csv   ← the working master (feeds public/ copy)
├── _archive/                 ← everything below moved here, nothing lost
│   ├── lineageA-gemini/      ← App_original/v2/v3.jsx, old CSVs, tar.gz
│   ├── nested-my-platonic-app/
│   ├── nested-platonic-ideal/
│   └── broken-brace-dirs/
└── CONSOLIDATION_AND_LAUNCH_PLAN.md
```

Actions: pick Lineage B as canonical → move the nested repos, brace dirs, old App
files, and stale CSVs into `_archive/` → dedupe the CSV to one file → add a proper
`.gitignore` → remove committed `dist/` from the tree.

---

## 4. Data integrity

- **Schema has duplicate columns** in the canonical CSV: `Core Reasoning` /
  `Core_Reasoning` and `Key Disqualifiers` / `Key_Disqualifiers`. Pick one naming
  per field, drop the dupes. Freeze a documented 1-column-per-field schema.
- **One-declaration rule enforcement:** current statuses are 48 DECLARED, 12 EMPTY,
  4 CANDIDATE, 2 SPLIT_REQUIRED, 1 CONSUMABLE, 1 CONDITIONAL. CANDIDATE and
  SPLIT_REQUIRED violate "one declaration or EMPTY, nothing in between" — resolve
  each to a single Model or to EMPTY before launch.
- **Content gap:** the CSV has ~64–68 categories; your batch analysis in claude.ai
  has reached **73/100**. The batch work (esp. categories 65–73) isn't synced into
  the CSV yet. Need a pipeline: analyze → validate → append to master CSV.
- Add a small **CSV validator** script (required columns present, exactly one
  Model when DECLARED, valid Status enum, no dupe category names). The vision
  ROADMAP already wanted this.

---

## 5. Product gaps for a real launch

- **Crawlable per-category URLs — implemented.** The Astro rebuild emits one
  static route per category with canonical metadata and sitemap coverage.
- **Images.** Many rows have no `Image URL`. Decide sourcing (own photos vs.
  linked) and fill the DECLARED set first.
- **EMPTY pages as first-class.** The "no ideal exists yet" verdict is core to the
  concept — make those real, explained pages, not blanks.

---

## 6. Phased launch plan

| Phase | Goal | Output |
|---|---|---|
| **0. Safety** (today) | Rotate Gemini key; confirm no secrets in bundle | key rotated, verified |
| **1. Consolidate** | One clean repo; archive the rest | `app/` + `_archive/` |
| **2. Data** | Dedupe schema; validator; resolve CANDIDATE/SPLIT | frozen schema + green validator |
| **3. Content → 100** | Sync 73 analyzed rows; finish 74–100 | 100-row master CSV |
| **4. Polish** | Per-category URLs/SEO, images, EMPTY pages | launch-ready UX |
| **5. Deploy** | Vercel Git deployment; verify live | public site |
| **6. Later** | Submissions ("is this the ideal?"), acquisition/commerce links | post-MVP |

---

## 7. Open decisions for you
1. Archive-in-place (recommended, nothing deleted) vs. hard delete the duplicates?
2. Confirm canonical repo = `platonic-ideal/` (Lineage B). Keep the `my-platonic-app`
   GitHub remote, or start a fresh clean repo?
3. Keep the schema as the shipped `Form Definition` model (recommended — it's what
   the live app reads), and treat the Drive/Gemini vision docs as _reference only_?
