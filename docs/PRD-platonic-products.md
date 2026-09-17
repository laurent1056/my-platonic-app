# Product Requirements Document: Platonic Products — The Register

**Author:** Laurent (laurent@moonrock.biz)
**Date:** 2026-09-17
**Status:** Draft
**Stakeholders:** Laurent (product, authoring, engineering)

> **A note on assumptions.** Four strategic inputs — audience, primary metric, monetization, and v1 priority — were not yet locked when this draft was written. Rather than block, this PRD commits to a **default position** for each (marked **[ASSUMPTION]**) that is consistent with everything decided so far: the "one ideal or none" thesis, the integrity-first framing, and the already-scoped SEO/crawlable pages. Every one of these is called out in §7 (Open Questions) so you can overturn it with one line and I'll re-cut the affected sections.

---

## 1. Executive Summary

Platonic Products is a public **register** that applies Plato's theory of Forms to consumer goods: for each product category it names the single best **Platonic ideal** — the durable, repairable, rebuildable item that *ends the search* — or it formally declares the category **EMPTY** when no product qualifies. One product per category. Or none. **Nothing in between.** The register's authority comes from a fixed, published **admission test**: a product is only DECLARED when it clears explicit permanence rules, and EMPTY is treated not as a gap but as a *finding*.

---

## 2. Background & Context

**The problem space.** Buying durable goods is broken. Review sites are SEO farms optimized for affiliate volume, not truth; "best of" lists rank 10 products because ranking 10 products sells 10 products; and genuinely buy-it-for-life knowledge is scattered across Reddit threads, forums, and tribal memory. The shopper who wants *the last frying pan they'll ever buy* has no authoritative, opinionated, single-answer source.

**The insight.** Plato's Forms give this a spine. For most categories there is effectively one Form-approximating product — the Lodge cast-iron skillet, the Estwing hammer — and the honest answer is "buy this one, stop looking." For others (refrigerators, washing machines) **no** current product embodies the Form, and the honest answer is "nothing qualifies; here's what it would take." A register that says exactly one of those two things per category is more useful, and more trustworthy, than any ranked list.

**Why now.** (1) Right-to-repair is culturally ascendant; durability and repairability are mainstream buying criteria. (2) The methodology already exists in this project's data — a status taxonomy (DECLARED, EMPTY, CANDIDATE, CONDITIONAL, CONSUMABLE, SPLIT_REQUIRED, DEPRECATED) and per-category admission tests — it needs a home. (3) The project is being rebuilt from scratch on a modern static stack (Astro + Tailwind), so this is the moment to specify it properly rather than port a Gemini export.

**Prior art in this project.** A design language ("The Canon" — Greek stele + Orthodox icon + apophatic negation) and a catalog/spec-sheet visual direction are already built and committed (`docs/design/design.md`, `docs/design/mockup-catalog-spec.html`). Sample register data exists (Frying Pan → Lodge L10SK3 DECLARED; Refrigerator → EMPTY). This PRD covers the *product*, not the visual identity, which is treated as settled input.

---

## 3. Objectives & Success Metrics

**Goals (what success looks like):**

1. **Establish the register as a credible single-answer authority** for durable-goods categories, where every entry is either a DECLARED ideal with evidence or a defensible EMPTY finding.
2. **Ship a fast, crawlable public site** — an index plus one canonical page per category — that a durability seeker can land on from search and trust in under 30 seconds.
3. **Make authoring rigorous and repeatable** via an internal Oracle tool that enforces the admission test, so verdicts are consistent and defensible rather than ad hoc.

**Non-Goals (explicitly out of scope for v1, and why):**

1. **Public submissions / user-generated content.** The register's value is a single authoritative voice; open submissions would dilute it and create moderation burden. *(Explicitly excluded — carried over from locked decisions.)*
2. **Affiliate commerce / monetization.** v1 stays clean to build trust; architected so it *could* be added later without a credibility reset. **[ASSUMPTION — see §7]**
3. **Accounts, personalization, price tracking, or live inventory.** The register states a durable verdict, not a real-time shopping feed.
4. **Exhaustive category coverage.** Depth and rigor per entry beat a thin catalog of 100 shallow ones. Coverage grows after the model is proven.
5. **Native app.** Static web only.

**Success Metrics:**

| Metric | Current | Target (v1, ~90 days post-launch) | Measurement |
|---|---|---|---|
| Fully adjudicated categories (DECLARED or EMPTY, confidence ≥ 4) | ~ (sample only) | **25** high-confidence entries | Count in register data; validator report |
| Unresolved statuses in published set (CANDIDATE/SPLIT/CONDITIONAL) | present in CSV | **0** published | Data validator gate on build |
| Per-category page crawlable & indexed | 0 | **100%** of published categories | Google Search Console coverage |
| Largest Contentful Paint (mobile, static page) | n/a | **< 1.5s** | Lighthouse CI |
| Time-to-verdict on a category page | n/a | Verdict + price visible **above the fold**, no scroll | Manual QA at 3 breakpoints |

> **[ASSUMPTION]** Primary v1 metric is **coverage + rigor** (depth), with SEO indexation as the secondary. If the real goal is traffic or audience capture, the metric table changes.

---

## 4. Target Users & Segments

Markets are defined by the job-to-be-done, not demographics.

**Primary — the Durability Seeker.** *"I want to buy this thing once, correctly, and never think about it again."* Actively searching "best [X] buy it for life," distrusts ranked affiliate lists, willing to pay more upfront for permanence. Current workaround: hours across Reddit, forums, and YouTube. The register's job: give them one answer, fast, with the reasoning shown. **[ASSUMPTION: this is the primary segment.]**

**Secondary — the Methodology Enthusiast.** BIFL / right-to-repair hobbyists who value *why* a verdict holds — the admission test, the disqualifiers, the EMPTY findings. They stress-test verdicts and become word-of-mouth advocates. Job: give them rigor they can argue with.

**Tertiary — the Author (Laurent).** The one person adjudicating categories. Not an end-user of the public site but the primary user of the **Oracle** authoring tool. Job: research a category, apply the rules, and publish a defensible entry without hand-maintaining HTML or fighting inconsistent data.

**Constraints:** single author (throughput is the real bottleneck, not tech); verdicts must survive public scrutiny (evidence and disqualifiers are load-bearing); the "one or none" rule must never be quietly broken to fill a category.

---

## 5. User Stories & Requirements

### P0 — Must Have (v1)

| # | User Story | Acceptance Criteria |
|---|---|---|
| P0-1 | As a seeker, I land on a category page and see the verdict instantly. | Category page shows status (DECLARED/EMPTY), the product (or "No product qualifies"), and price above the fold on mobile; no interaction required. |
| P0-2 | As a seeker, I understand *why* this is the ideal. | Page renders Form definition, "why it ends the search," permanence mechanism, and key disqualifiers from register data. |
| P0-3 | As a seeker, I trust an EMPTY verdict as much as a DECLARED one. | EMPTY pages render the apophatic treatment: "why the search stays open" + "what the category would require" (the admission checklist, unmet). |
| P0-4 | As a seeker arriving from search, I hit a fast, crawlable page. | Static HTML per category; unique `<title>`/meta/canonical; JSON-LD; sitemap; LCP < 1.5s mobile; stable URL `/[category-slug]`. |
| P0-5 | As a seeker, I browse the whole register. | Index page lists every published category with No., name, verdict chip, the model, price, confidence; sortable/scannable; links to each page. |
| P0-6 | As the author, I never publish an unresolved verdict. | Build fails if any published entry has status CANDIDATE/SPLIT_REQUIRED/CONDITIONAL or confidence below threshold, or missing required fields. |
| P0-7 | As the author, my data is the single source of truth. | One canonical, de-duplicated dataset (no duplicate columns); site generates entirely from it; schema documented. |
| P0-8 | As a seeker, I see the product. | Each DECLARED entry shows a product image (or a deliberate line-art placeholder) with correct licensing/attribution. |

### P1 — Should Have

| # | User Story | Acceptance Criteria |
|---|---|---|
| P1-1 | As the author, I adjudicate a category through a guided tool (the **Oracle**). | Internal tool walks the admission test, captures required fields, enforces one-or-none, and outputs a valid register entry. |
| P1-2 | As a seeker, I filter the index by verdict. | Index filters by DECLARED / EMPTY (and shows counts) client-side, no page reload. |
| P1-3 | As a seeker, I trust the freshness. | Each entry shows "last reviewed" date and a confidence indicator. |
| P1-4 | As the author, I keep the register honest over time. | Entries carry a review date; a report flags entries past a staleness threshold. |
| P1-5 | As a maintainer, the design system is applied consistently. | Live site matches "The Canon" tokens/flourishes; gold rationed to canonization moments; EMPTY never gilded. |

### P2 — Nice to Have / Future

| # | User Story | Acceptance Criteria |
|---|---|---|
| P2-1 | As a seeker, I subscribe to new/updated verdicts. | Email capture + RSS of register changes. |
| P2-2 | As a seeker, I see category splits handled well. | SPLIT_REQUIRED categories render as sub-categories, each with its own verdict. |
| P2-3 | As the business, declared ideals carry affiliate links. | Disclosed, integrity-guarded affiliate links — only if §7 monetization resolves to "yes." |
| P2-4 | As a seeker, I grasp the methodology. | A standalone "How the register works" page explaining Forms, the admission test, and the status taxonomy. |

---

## 6. Solution Overview

**Approach.** A statically generated site (**Astro + Tailwind**, deployed to **GitHub Pages** via GitHub Actions) built from a single canonical dataset. Two surfaces: (1) the **public register** — index + one page per category, catalog/spec-sheet aesthetic per "The Canon"; (2) the **Oracle** — an internal authoring tool that enforces the admission test and emits valid entries.

**Key design decisions:**

- **Data is the product.** A single, validated, de-duplicated dataset is the source of truth; pages are a pure function of it. A **build-time validator** is the trust mechanism — it refuses to ship unresolved or malformed verdicts (P0-6).
- **Two states, one grammar.** DECLARED and EMPTY share a page template but diverge in treatment: DECLARED = canonization (framed, confident, the gilded rule, the nimbus); EMPTY = apophatic negation (struck, ungilded, "what it would require"). This contrast *is* the product's voice.
- **Static-first for trust and speed.** No client accounts, no server, no runtime data fetching. Crawlability and sub-1.5s loads are structural, not optimizations.
- **The rules are explicit and published.** The admission test and status taxonomy are documented and, ideally, surfaced on-site (P2-4) so verdicts are auditable.

**Technology (already decided):** Astro + Tailwind; GitHub Pages + Actions; register data in a structured file (CSV/JSON/frontmatter — schema to be finalized in build); design tokens as CSS custom properties, theme-aware.

**Assumptions (flagged for validation):**

- The current sample verdicts (Lodge skillet DECLARED; Refrigerator EMPTY) are representative of the adjudication quality bar.
- A single author can reach ~25 high-confidence entries in the v1 window.
- Line-art/product imagery can be sourced with clean licensing at the pace of authoring.
- Static generation is sufficient for v1 (no dynamic feature forces a server).

---

## 7. Open Questions

| # | Question | Why it matters | Default if unanswered |
|---|---|---|---|
| Q1 | **Primary audience** — public durability seekers, a niche community, personal reference, or enthusiast researchers? | Drives tone, SEO investment, and whether email/community features rise in priority. | **[ASSUMPTION]** Public durability seekers (SEO-discoverable), enthusiasts secondary. |
| Q2 | **Primary success metric** — coverage/rigor vs. organic traffic vs. audience capture vs. authoring throughput? | Determines the metric table in §3 and what v1 optimizes for. | **[ASSUMPTION]** Coverage + rigor; SEO indexation secondary. |
| Q3 | **Monetization** — affiliate, none, donations, or keep-open? | Changes trust posture, disclosure requirements, and whether verdicts need bias guards. | **[ASSUMPTION]** No monetization in v1; architect so affiliate is *addable* later. |
| Q4 | **v1 build order** — public site first, Oracle first, data-integrity first, or coupled? | Sequences the roadmap in §8. | **[ASSUMPTION]** Data-integrity gate → public site → Oracle. |
| Q5 | How many categories must be adjudicated before public launch is credible? | Too few looks thin; waiting for many delays launch. | Draft target: **25** (overturnable). |
| Q6 | Exact data schema and format (CSV vs. per-entry markdown frontmatter)? | Affects validator and Oracle output contract. | Resolve during build; JSON/frontmatter favored for per-entry richness. |

---

## 8. Timeline & Phasing

Relative timeframes, single author; sequencing reflects the **[ASSUMPTION]** default for Q4 (data-integrity gate first).

**Phase 0 — Data integrity (foundation).**
Consolidate to one canonical, de-duplicated dataset; finalize schema; build the **validator** (rejects unresolved statuses, missing fields, sub-threshold confidence). *Gate: nothing ships publicly until the current set passes.* Resolve outstanding CANDIDATE/SPLIT/CONDITIONAL rows or hold them out of the published set.

**Phase 1 — Public site (v1 launch).**
Scaffold Astro + Tailwind against "The Canon" tokens. Build the index and the two-state category template (DECLARED / EMPTY). Wire SEO (per-page meta, canonical, JSON-LD, sitemap). Source images for DECLARED entries. GitHub Actions → GitHub Pages. Lighthouse CI gate. **Launch with ~25 high-confidence entries.**

**Phase 2 — The Oracle (authoring leverage).**
Internal tool enforcing the admission test and emitting valid entries; makes throughput repeatable and consistent. Raises the ceiling on how fast the register grows.

**Phase 3 — Growth & durability features.**
Index filtering; staleness/review reporting; "How the register works" page; email/RSS of changes; SPLIT_REQUIRED sub-categories. Revisit monetization (Q3) as an explicit, disclosed decision — not a drift.

**Dependencies:** Phase 1 depends on Phase 0's canonical dataset and validator. Design language is *not* a dependency — it's already built. Image sourcing runs parallel to Phase 1 authoring.

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
