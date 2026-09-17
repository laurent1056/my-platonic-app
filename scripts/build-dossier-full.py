#!/usr/bin/env python3
"""Build the full 100-category Platonic Ideal dossier review edition."""

from __future__ import annotations

import csv
import importlib.util
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence
from xml.sax.saxutils import escape

from PIL import Image, ImageEnhance, ImageOps
from reportlab.lib.colors import Color, HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[1]
REVIEW_SCRIPT = ROOT / "scripts" / "build-dossier-review.py"
spec = importlib.util.spec_from_file_location("dossier_review_pdf", REVIEW_SCRIPT)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Could not load shared PDF helpers from {REVIEW_SCRIPT}")
R = importlib.util.module_from_spec(spec)
spec.loader.exec_module(R)

CSV_PATH = ROOT / "public" / "platonic_ideal.csv"
SOURCE_PATH = ROOT / "src" / "data" / "image-source-inventory.json"
PRODUCT_IMAGE_ROOT = ROOT / "public" / "images" / "products"
ASSET_DIR = ROOT / "docs" / "dossier-review" / "assets"
TMP_DIR = ROOT / "tmp" / "pdfs" / "dossier-full"
OUTPUT_DIR = ROOT / "output" / "pdf"
OUTPUT_PATH = OUTPUT_DIR / "platonic-ideal-dossier-full-review.pdf"

PAGE_W, PAGE_H = R.PAGE_W, R.PAGE_H
M = R.M
PAPER, PAPER_DARK, INK = R.PAPER, R.PAPER_DARK, R.INK
MUTED, RULE, RED = R.MUTED, R.RULE, R.RED
RED_PALE, BLUE, BLUE_PALE = R.RED_PALE, R.BLUE, R.BLUE_PALE
TEAL, TEAL_PALE, GREEN, GREEN_PALE = R.TEAL, R.TEAL_PALE, R.GREEN, R.GREEN_PALE
GOLD = R.GOLD


EXTRA_STYLES = {
    "body_tight": ParagraphStyle(
        "full_body_tight",
        fontName="Georgia",
        fontSize=8.25,
        leading=10.6,
        textColor=INK,
    ),
    "body_micro": ParagraphStyle(
        "full_body_micro",
        fontName="Georgia",
        fontSize=7.2,
        leading=9.15,
        textColor=INK,
    ),
    "sans": ParagraphStyle(
        "full_sans",
        fontName="ArialNarrow",
        fontSize=7.6,
        leading=9.3,
        textColor=INK,
    ),
    "sans_bold": ParagraphStyle(
        "full_sans_bold",
        fontName="ArialNarrow-Bold",
        fontSize=7.6,
        leading=9.3,
        textColor=INK,
    ),
    "source": ParagraphStyle(
        "full_source",
        fontName="ArialNarrow",
        fontSize=6.8,
        leading=8.1,
        textColor=INK,
    ),
    "callout": ParagraphStyle(
        "full_callout",
        fontName="ArialNarrow",
        fontSize=8.1,
        leading=10.2,
        textColor=PAPER,
    ),
}


STATUS_LABELS = {
    "DECLARED": "DECLARED",
    "CANDIDATE": "CANDIDATE",
    "EMPTY": "NO QUALIFYING PICK",
    "SPLIT_REQUIRED": "SPLIT REQUIRED",
    "CONDITIONAL": "CONDITIONAL",
    "CONSUMABLE": "RATIONAL RENEWAL",
}

STATUS_PUBLIC = {
    "DECLARED": "One model currently clears the category threshold.",
    "CANDIDATE": "A credible subject exists, but the evidence packet is incomplete.",
    "EMPTY": "No product currently earns a declaration inside this Form.",
    "SPLIT_REQUIRED": "The parent category contains incompatible jobs and must be narrowed.",
    "CONDITIONAL": "The answer changes materially with use, installation, fit, or service context.",
    "CONSUMABLE": "Renewal is intrinsic to the job and should be made rational and explicit.",
}

STATUS_COLORS = {
    "DECLARED": GREEN,
    "CANDIDATE": GOLD,
    "EMPTY": RED,
    "SPLIT_REQUIRED": BLUE,
    "CONDITIONAL": TEAL,
    "CONSUMABLE": HexColor("#775B47"),
}

STATUS_PALES = {
    "DECLARED": GREEN_PALE,
    "CANDIDATE": PAPER_DARK,
    "EMPTY": RED_PALE,
    "SPLIT_REQUIRED": BLUE_PALE,
    "CONDITIONAL": TEAL_PALE,
    "CONSUMABLE": HexColor("#E6D8CC"),
}


DOMAINS = [
    ("kitchen-cooking", "Kitchen & Cooking", "Objects that turn ingredients into meals or keep them ready."),
    ("household-systems", "Household Systems", "Appliances and infrastructure that keep a home working."),
    ("tools-workshop", "Tools & Workshop", "Hand tools, powered tools, and practical equipment for making and maintaining."),
    ("clothing-carry", "Clothing & Carry", "Wearable and carried objects built around daily use and movement."),
    ("outdoor-utility", "Outdoor & Utility", "Field equipment for travel, shelter, weather, and utility."),
    ("furniture-work", "Furniture & Work", "Objects that support sitting, writing, storage, and daily work."),
    ("writing-office", "Writing & Office", "Small instruments and office objects for recording and organizing thought."),
    ("electronics", "Electronics", "Computing and connected objects judged through software, standards, and service life."),
    ("personal-care-misc", "Personal Care & Misc.", "Personal instruments and inherently renewing objects."),
]

DOMAIN_OVERRIDES = {
    "frying pan": "kitchen-cooking", "refrigerator": "household-systems", "hammer": "tools-workshop",
    "smartphone": "electronics", "kitchen knife": "kitchen-cooking", "washing machine": "household-systems",
    "saucepan": "kitchen-cooking", "screwdriver": "tools-workshop", "dutch oven": "kitchen-cooking",
    "laptop": "electronics", "coffee maker": "kitchen-cooking", "drill": "tools-workshop",
    "kettle": "kitchen-cooking", "task chair": "furniture-work", "toaster": "kitchen-cooking",
    "backpack": "outdoor-utility", "mattress": "household-systems", "hand saw": "tools-workshop",
    "desk": "furniture-work", "boots": "clothing-carry", "oven/range": "kitchen-cooking",
    "belt": "clothing-carry", "freezer": "household-systems", "adjustable wrench": "tools-workshop",
    "t-shirt": "clothing-carry", "jeans": "clothing-carry", "jacket/coat": "clothing-carry",
    "chisel": "tools-workshop", "pliers": "tools-workshop", "tape measure": "tools-workshop",
    "tent": "outdoor-utility", "sleeping bag": "outdoor-utility", "water bottle": "outdoor-utility",
    "flashlight": "outdoor-utility", "sweater": "clothing-carry", "cooler": "outdoor-utility",
    "pocket knife": "outdoor-utility", "notebook": "writing-office", "pen": "writing-office",
    "cutting board": "kitchen-cooking", "vacuum cleaner": "household-systems", "bicycle": "outdoor-utility",
    "dining chair": "furniture-work", "printer": "electronics", "socks": "clothing-carry",
    "watch": "personal-care-misc", "shoes": "clothing-carry", "food storage container": "kitchen-cooking",
    "level": "tools-workshop", "drill bits": "tools-workshop", "extension cord": "tools-workshop",
    "camping stove": "outdoor-utility", "mechanical pencil": "writing-office", "umbrella": "personal-care-misc",
    "ladder": "tools-workshop", "wheelbarrow": "outdoor-utility", "wallet": "clothing-carry",
    "briefcase": "clothing-carry", "hat": "clothing-carry", "gloves": "clothing-carry",
    "toothbrush": "personal-care-misc", "razor": "personal-care-misc", "hair dryer": "personal-care-misc",
    "desktop computer": "electronics", "bed frame": "furniture-work", "sofa / couch": "furniture-work",
    "sofa": "furniture-work", "bookshelf": "furniture-work", "coffee table": "furniture-work",
    "dresser / wardrobe": "furniture-work", "dresser": "furniture-work", "wardrobe": "furniture-work",
    "desk lamp": "furniture-work", "floor lamp": "furniture-work", "window blinds": "furniture-work",
    "pillow": "furniture-work", "backpacking pack": "outdoor-utility", "hunting knife": "outdoor-utility",
    "television": "electronics", "router": "electronics", "headphones": "electronics",
    "speakers": "electronics", "camera": "electronics", "smartwatch": "electronics",
    "home thermostat": "household-systems", "dryer": "household-systems", "water heater": "household-systems",
    "furnace": "household-systems", "air conditioner": "household-systems",
}

DOMAIN_PATTERNS = {
    "kitchen-cooking": [
        "Separate the durable vessel from coatings, seals, and handles that renew.",
        "State the heat-source and capacity boundary before comparing brands.",
        "Treat cleaning and storage as part of the design, not aftercare.",
        "Show whether surface damage is recoverable, replaceable, or terminal.",
    ],
    "household-systems": [
        "Installation, capacity, codes, and local service are part of product identity.",
        "Distinguish replaceable controls from sealed critical assemblies.",
        "Record parts availability and labor economics, not warranty language alone.",
        "Energy use matters across the whole ownership horizon.",
    ],
    "tools-workshop": [
        "Look for continuous load paths, standard interfaces, and replaceable wear parts.",
        "Accuracy and safety are terminal thresholds; cosmetic wear is not.",
        "A parts diagram proves structure, while stock checks prove serviceability.",
        "Match geometry and capacity to the ordinary job before rewarding features.",
    ],
    "clothing-carry": [
        "Fit and size are part of the product, not preferences added later.",
        "Separate durable structure from soles, zippers, linings, and other wear layers.",
        "Favor repairable seams and renewable surfaces over decorative complexity.",
        "Record care requirements before calling a material permanent.",
    ],
    "outdoor-utility": [
        "The use envelope includes weather, load, packability, fuel, and field repair.",
        "Safety margins and failure boundaries matter more than heroic marketing claims.",
        "Consumables and regional supply belong in the ownership system.",
        "One camping or carry Form rarely answers every field use.",
    ],
    "furniture-work": [
        "Judge spans, load paths, joinery, and racking before style.",
        "Surfaces, cushions, slides, cords, and switches should be separately renewable.",
        "Commodity hardware is valuable when it keeps a sound structure in use.",
        "Dimensions and human fit are constitutional constraints.",
    ],
    "writing-office": [
        "The durable body should accept a standard or stable refill system.",
        "Precision surfaces and mechanisms need a cleaning and replacement path.",
        "Simple tools win when they preserve the task without proprietary dependency.",
        "Paper and ink are rational consumables; the holder should stay legible.",
    ],
    "electronics": [
        "Software support and account dependency are material construction facts.",
        "Battery, display, storage, ports, and thermal parts need separate horizons.",
        "Modularity only matters when modules remain compatible and available.",
        "A narrow use Form prevents one device from pretending to serve every workload.",
    ],
    "personal-care-misc": [
        "Hygiene can require rational renewal even when the handle remains sound.",
        "Standard blades, bands, cords, and simple mechanisms reduce lock-in.",
        "Safety and body contact set stricter retirement thresholds.",
        "Finite wear should be named directly rather than disguised as permanence.",
    ],
}

QUOTES = [
    ("The many, as we say, are seen but not known.", "Republic VI, 507b"),
    ("The beginning is the most important part of any work.", "Republic II, 377b"),
    ("Beauty of style and harmony and grace and good rhythm depend on simplicity.", "Republic III, 400e"),
    ("Knowledge which is acquired under compulsion obtains no hold on the mind.", "Republic VII, 536e"),
    ("The unexamined life is not worth living.", "Apology 38a"),
]


@dataclass
class Entry:
    number: int
    reference: str
    category: str
    status: str
    model: str
    price: str
    form: str
    form_statement: str
    summary: str
    reasoning: str
    disqualifiers: str
    maintenance: str
    permanence: str
    alternates: str
    admission: str
    failures: str
    confidence: int
    reviewed: str
    notes: str
    domain: str


def normalize(value: str | None) -> str:
    value = (value or "").strip().replace("\r\n", "\n")
    replacements = {
        "\u2011": "-", "\u2012": "-", "\u2013": "-", "\u2014": " - ",
        "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
        "\u2026": "...", "\u00a0": " ", "\u00b0": " degrees ",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    return re.sub(r"\s+", " ", value).strip()


def domain_for(category: str) -> str:
    value = normalize(category).lower()
    candidates = [value, re.sub(r"\s*\([^)]*\)$", "", value), re.sub(r"\s+-\s+.*$", "", value)]
    candidates.append(candidates[-1].split(" / ")[0])
    return next((DOMAIN_OVERRIDES[c] for c in candidates if c in DOMAIN_OVERRIDES), "personal-care-misc")


def load_entries() -> list[Entry]:
    rows = list(csv.DictReader(CSV_PATH.open(encoding="utf-8-sig", newline="")))
    entries = []
    for index, row in enumerate(rows, 1):
        number = int(normalize(row.get("Number")) or index)
        category = normalize(row.get("Category"))
        reasoning = normalize(row.get("Core_Reasoning")) or normalize(row.get("Core Reasoning"))
        disqualifiers = normalize(row.get("Key_Disqualifiers")) or normalize(row.get("Key Disqualifiers"))
        entries.append(
            Entry(
                number=number,
                reference=f"PI-{number:03d}",
                category=category,
                status=normalize(row.get("Status")).upper(),
                model=normalize(row.get("Model")),
                price=normalize(row.get("Price")),
                form=normalize(row.get("Form Definition")),
                form_statement=normalize(row.get("Form Statement")),
                summary=normalize(row.get("Card Snippet (Why this ends the search)")),
                reasoning=reasoning,
                disqualifiers=disqualifiers,
                maintenance=normalize(row.get("Maintenance / Replacement Cycle")),
                permanence=normalize(row.get("Permanence Mechanism")),
                alternates=normalize(row.get("Alternates (non-declared)")),
                admission=normalize(row.get("Admission Test")),
                failures=normalize(row.get("Failure Modes")),
                confidence=max(0, min(5, int(normalize(row.get("Confidence")) or 0))),
                reviewed=normalize(row.get("Last Reviewed")),
                notes=normalize(row.get("Notes")),
                domain=domain_for(category),
            )
        )
    return entries


ENTRIES = load_entries()
ENTRIES_BY_REF = {e.reference: e for e in ENTRIES}
SOURCE_RECORDS = json.loads(SOURCE_PATH.read_text())["records"]
SOURCES_BY_REF = {record["productId"]: record for record in SOURCE_RECORDS}
DOMAIN_INFO = {key: (name, description) for key, name, description in DOMAINS}
ENTRIES_BY_DOMAIN: dict[str, list[Entry]] = defaultdict(list)
for entry in ENTRIES:
    ENTRIES_BY_DOMAIN[entry.domain].append(entry)


def page_count(entry: Entry) -> int:
    return 2 if entry.status == "DECLARED" else 1


def build_page_plan() -> tuple[dict[str, int], dict[str, int], int, int]:
    category_pages: dict[str, int] = {}
    domain_pages: dict[str, int] = {}
    page = 17
    for domain, _, _ in DOMAINS:
        domain_pages[domain] = page
        page += 2
        for entry in ENTRIES_BY_DOMAIN[domain]:
            category_pages[entry.reference] = page
            page += page_count(entry)
    end_start = page
    final_page = end_start + 13
    return category_pages, domain_pages, end_start, final_page


CATEGORY_PAGES, DOMAIN_PAGES, END_START, FINAL_PAGE = build_page_plan()


def sentences(value: str, limit: int = 6) -> list[str]:
    value = normalize(value)
    if not value:
        return []
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])|\s*;\s*", value)
    return [p.strip() for p in parts if p.strip()][:limit]


def shorten(value: str, limit: int) -> str:
    value = normalize(value)
    if len(value) <= limit:
        return value
    cut = value[: max(0, limit - 1)].rsplit(" ", 1)[0]
    return cut.rstrip(" ,;:-") + "..."


def plain_para(c: canvas.Canvas, value: str, x: float, y_top: float, width: float, style: str = "body_tight", max_height: float = 1000) -> float:
    style_obj = EXTRA_STYLES.get(style, R.STYLES.get(style, R.STYLES["body_small"]))
    p = Paragraph(escape(normalize(value)), style_obj)
    _, height = p.wrap(width, max_height)
    p.drawOn(c, x, y_top - height)
    return y_top - height


def fit_para(c: canvas.Canvas, value: str, x: float, y_top: float, width: float, height: float, style: str = "body_tight") -> float:
    style_obj = EXTRA_STYLES.get(style, R.STYLES.get(style, R.STYLES["body_small"]))
    candidate = normalize(value)
    while candidate:
        p = Paragraph(escape(candidate), style_obj)
        _, measured = p.wrap(width, height)
        if measured <= height:
            p.drawOn(c, x, y_top - measured)
            return y_top - measured
        candidate = shorten(candidate, max(20, int(len(candidate) * 0.88)))
    return y_top


def fit_title(c: canvas.Canvas, value: str, x: float, y: float, max_width: float, max_size: float = 26, min_size: float = 13, color=INK) -> float:
    size = max_size
    while size > min_size and pdfmetrics.stringWidth(value, "Georgia-Bold", size) > max_width:
        size -= 0.5
    R.text(c, value, x, y, "Georgia-Bold", size, color)
    return size


def card(c: canvas.Canvas, x: float, y_top: float, width: float, height: float, title: str, body: str, fill=PAPER_DARK, accent=RED, style: str = "body_tight") -> None:
    c.setFillColor(fill)
    c.roundRect(x, y_top - height, width, height, 3, fill=1, stroke=0)
    R.text(c, title.upper(), x + 10, y_top - 18, "ArialNarrow-Bold", 7.7, accent)
    fit_para(c, body, x + 10, y_top - 30, width - 20, height - 37, style)


def numbered_list(c: canvas.Canvas, items: Sequence[str], x: float, y_top: float, width: float, max_items: int = 5, color=RED, item_height: float = 37) -> float:
    y = y_top
    for i, item in enumerate(list(items)[:max_items], 1):
        c.setFillColor(color)
        c.circle(x + 10, y - 10, 8.5, fill=1, stroke=0)
        R.text_center(c, str(i), x + 10, y - 13, "ArialNarrow-Bold", 6.8, white)
        fit_para(c, item, x + 26, y, width - 26, item_height - 3, "sans")
        y -= item_height
    return y


def section_rule(c: canvas.Canvas, value: str, y: float, color=RED) -> None:
    R.block_title(c, value, M, y, PAGE_W - 2 * M, color)


def source_url_paragraph(c: canvas.Canvas, label: str, url: str, x: float, y_top: float, width: float, style: str = "source") -> float:
    value = f'<b>{escape(label)}</b><br/><link href="{escape(url)}" color="#244A63"><u>{escape(url)}</u></link>'
    p = Paragraph(value, EXTRA_STYLES[style])
    _, h = p.wrap(width, 1000)
    p.drawOn(c, x, y_top - h)
    return y_top - h


def prepare_image(path: Path, name: str, max_px: int = 1300) -> Path:
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    target = TMP_DIR / f"{name}.jpg"
    if target.exists() and target.stat().st_mtime >= path.stat().st_mtime:
        return target
    with Image.open(path) as source:
        image = source.convert("RGB")
        image.thumbnail((max_px, max_px), Image.Resampling.LANCZOS)
        image = ImageEnhance.Contrast(image).enhance(1.03)
        image.save(target, quality=84, optimize=True, progressive=True)
    return target


def plate_path(entry: Entry) -> Path | None:
    overrides = {
        "PI-001": ASSET_DIR / "lodge-l10sk3-technical-plate.png",
        "PI-003": ASSET_DIR / "estwing-e3-16c-technical-plate.png",
        "PI-012": ASSET_DIR / "makita-6302h-technical-plate.png",
    }
    if entry.reference in overrides:
        return prepare_image(overrides[entry.reference], entry.reference.lower() + "-technical", 1500)
    folder_matches = sorted(PRODUCT_IMAGE_ROOT.glob(f"pi-{entry.number:03d}-*"))
    if not folder_matches:
        return None
    folder = folder_matches[0]
    candidates = sorted(folder.glob("hero-v2.*")) + sorted(folder.glob("hero.*"))
    return prepare_image(candidates[0], entry.reference.lower() + "-plate") if candidates else None


def related_entries(entry: Entry) -> list[Entry]:
    base = re.split(r"\s+-\s+|\s*/\s*", entry.category.lower())[0]
    matches = []
    for other in ENTRIES:
        if other.reference == entry.reference:
            continue
        other_base = re.split(r"\s+-\s+|\s*/\s*", other.category.lower())[0]
        if base == other_base or other.category.lower().startswith(base + " -"):
            matches.append(other)
    return matches[:5]


class Book:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.c = canvas.Canvas(str(path), pagesize=R.LETTER, pageCompression=1)
        self.c.setTitle("The Platonic Ideal Dossier - Full 100-Category Review Edition")
        self.c.setAuthor("Platonic Ideal")
        self.c.setSubject("A 100-category evidence-led ownership and product research dossier")
        self.c.setKeywords("buying guide, product research, ownership, repair, maintenance, evidence")
        self.page_no = 0

    def start(self, section: str, title: str | None = None, key: str | None = None, level: int = 0) -> None:
        self.page_no += 1
        R.page_base(self.c, self.page_no, section)
        destination = key or f"page-{self.page_no}"
        self.c.bookmarkPage(destination)
        if title:
            try:
                self.c.addOutlineEntry(title, destination, level=level, closed=False)
            except ValueError:
                self.c.addOutlineEntry(title, destination, level=0, closed=False)

    def finish(self) -> None:
        self.c.showPage()

    def save(self) -> None:
        self.c.save()


def draw_cover(book: Book) -> None:
    book.page_no = 1
    c = book.c
    c.bookmarkPage("cover")
    c.addOutlineEntry("Cover", "cover", level=0, closed=False)
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    left_w = 252
    R.draw_cover_crop(c, ROOT / "public" / "images" / "plato-silanion-berlin.webp", 0, 0, left_w, PAGE_H)
    c.setFillColor(Color(0.07, 0.07, 0.06, alpha=0.12))
    c.rect(0, 0, left_w, PAGE_H, fill=1, stroke=0)
    c.setFillColor(RED)
    c.rect(left_w - 8, 0, 8, PAGE_H, fill=1, stroke=0)
    R.text(c, "PLATONIC IDEAL", left_w + 34, PAGE_H - 60, "ArialNarrow-Bold", 10, RED)
    R.text(c, "THE", left_w + 34, PAGE_H - 116, "Georgia-Bold", 21, INK)
    R.text(c, "DOSSIER", left_w + 34, PAGE_H - 155, "Georgia-Bold", 34, INK)
    R.text(c, "FULL REGISTER / REVIEW EDITION", left_w + 34, PAGE_H - 180, "ArialNarrow-Bold", 9.3, MUTED)
    fit_para(c, "One hundred categories. Forty-eight current declarations. Every open question kept visible.", left_w + 34, PAGE_H - 220, PAGE_W - left_w - 66, 60, "body_tight")
    c.setStrokeColor(RULE)
    c.line(left_w + 34, PAGE_H - 295, PAGE_W - 34, PAGE_H - 295)
    metrics = [
        ("100", "CATEGORY RULINGS"),
        ("48", "TWO-PAGE DECLARATIONS"),
        ("52", "OPEN RESEARCH BRIEFS"),
        ("9", "DOMAIN DOSSIERS"),
        (str(FINAL_PAGE), "REVIEW PAGES"),
    ]
    y = PAGE_H - 335
    for value, label in metrics:
        R.text(c, value, left_w + 34, y, "Georgia-Bold", 18, RED)
        R.text(c, label, left_w + 85, y + 3, "ArialNarrow-Bold", 7.6, INK)
        y -= 52
    c.setFillColor(PAPER_DARK)
    c.roundRect(left_w + 34, 106, PAGE_W - left_w - 68, 118, 4, fill=1, stroke=0)
    R.text(c, '"The many, as we say,', left_w + 50, 184, "Georgia-Italic", 11, INK)
    R.text(c, 'are seen but not known."', left_w + 50, 164, "Georgia-Italic", 11, INK)
    R.text(c, "PLATO / REPUBLIC VI.507B / JOWETT (PUBLIC DOMAIN)", left_w + 50, 135, "ArialNarrow-Bold", 6.5, RED)
    R.text(c, "EVIDENCE / JUDGMENT / OWNERSHIP", left_w + 34, 70, "ArialNarrow-Bold", 8.2, INK)
    R.text(c, "Research review / 15 September 2026", left_w + 34, 52, "ArialNarrow", 7.2, MUTED)
    R.text(c, "Plato portrait: Osama Shukir Muhammed Amin / CC BY-SA 4.0", 18, 18, "ArialNarrow", 5.8, PAPER)
    c.linkURL(R.SOURCES["S15"][1], (0, 30, left_w, PAGE_H), relative=0, thickness=0)
    c.linkURL(R.SOURCES["S16"][1], (18, 8, left_w - 12, 28), relative=0, thickness=0)
    c.linkURL(R.SOURCES["S17"][1], (left_w + 34, 106, PAGE_W - 34, 224), relative=0, thickness=0)
    c.showPage()


def colophon_page(book: Book) -> None:
    book.start("Edition note", "Edition note", "edition-note", 0)
    c = book.c
    R.page_title(c, "Full register review", "A book-sized argument, still under audit.", "This PDF is a complete editorial run for review. It is substantial enough to evaluate structure and value, while every unresolved model, candidate, source, and service question remains visibly unresolved.")
    section_rule(c, "What is inside", 623)
    stats = Counter(e.status for e in ENTRIES)
    cards = [
        ("100", "CATEGORY RULINGS", "The entire working register, including honest empty and split findings."),
        ("48", "DECLARED SPREADS", "Two pages each: the judgment, ownership case, source state, and research gaps."),
        ("52", "OPEN BRIEFS", "Candidate, conditional, split, consumable, and no-pick cases receive a full page."),
        ("48", "SOURCE RECORDS", "Current identity leads are linked; model ambiguity is disclosed, not smoothed over."),
    ]
    w = (PAGE_W - 2 * M - 12) / 2
    for i, (value, label, body) in enumerate(cards):
        col, row = i % 2, i // 2
        x = M + col * (w + 12)
        top = 590 - row * 106
        c.setFillColor(PAPER_DARK)
        c.roundRect(x, top - 88, w, 88, 4, fill=1, stroke=0)
        R.text(c, value, x + 12, top - 31, "Georgia-Bold", 19, RED)
        R.text(c, label, x + 62, top - 26, "ArialNarrow-Bold", 7.7, INK)
        fit_para(c, body, x + 62, top - 39, w - 74, 39, "sans")
    section_rule(c, "Five layers beyond a verdict", 381)
    layers = [
        "Form boundary: what job is actually being judged.",
        "Ownership path: maintenance, consumables, service, and storage.",
        "Failure logic: recoverable wear, replaceable modules, and terminal damage.",
        "Comparison pressure: what a rival must improve to overturn the ruling.",
        "Evidence state: exact identity, ambiguity, missing parts proof, and dated sources.",
    ]
    numbered_list(c, layers, M, 350, PAGE_W - 2 * M, 5, RED, 38)
    section_rule(c, "Release boundary", 151)
    card(c, M, 126, PAGE_W - 2 * M, 72, "Not yet the commercial edition", "Prices, availability, independent testing, candidate fields, parts stock, and territory-specific rights still need production research. This edition exists so those gaps can be judged in context instead of discovered after layout.", RED_PALE, RED)
    book.finish()


def contents_page(book: Book) -> None:
    book.start("Contents", "Contents", "contents", 0)
    c = book.c
    R.page_title(c, "Contents", "Nine domains. One standard.", "Entries are grouped by use domain while retaining their PI reference numbers. Page links and PDF bookmarks are active.")
    y = 620
    for index, (domain, name, description) in enumerate(DOMAINS, 1):
        count = len(ENTRIES_BY_DOMAIN[domain])
        states = Counter(e.status for e in ENTRIES_BY_DOMAIN[domain])
        c.setFillColor(PAPER_DARK if index % 2 else R.WHITE_WASH)
        c.roundRect(M, y - 48, PAGE_W - 2 * M, 48, 3, fill=1, stroke=0)
        R.text(c, f"{index:02d}", M + 10, y - 29, "Georgia-Bold", 13, RED)
        R.text(c, name.upper(), M + 47, y - 17, "ArialNarrow-Bold", 8.3, INK)
        R.text(c, shorten(description, 86), M + 47, y - 33, "ArialNarrow", 7.2, MUTED)
        summary = f"{count} entries / {states.get('DECLARED', 0)} declared"
        R.text_right(c, summary, PAGE_W - M - 45, y - 25, "ArialNarrow", 7.2, MUTED)
        R.text_right(c, str(DOMAIN_PAGES[domain]), PAGE_W - M - 10, y - 27, "Georgia-Bold", 10, RED)
        c.linkAbsolute(name, f"domain-{domain}", (M, y - 48, PAGE_W - M, y), thickness=0)
        y -= 55
    book.finish()


def category_index_page(book: Book, page_index: int, entries: list[Entry]) -> None:
    book.start("Category index", None, f"category-index-{page_index}", 0)
    c = book.c
    title = "Category index A-M" if page_index == 1 else "Category index N-Z"
    R.page_title(c, "Find a ruling", title, "Reference, editorial state, and destination page. State colors match the category briefs.")
    column_gap = 18
    col_w = (PAGE_W - 2 * M - column_gap) / 2
    chunks = [entries[:25], entries[25:50]]
    for col, chunk in enumerate(chunks):
        x = M + col * (col_w + column_gap)
        y = 623
        for entry in chunk:
            color = STATUS_COLORS[entry.status]
            c.setFillColor(PAPER_DARK if entry.number % 2 else R.WHITE_WASH)
            c.rect(x, y - 20, col_w, 20, fill=1, stroke=0)
            c.setFillColor(color)
            c.rect(x, y - 20, 4, 20, fill=1, stroke=0)
            R.text(c, entry.reference, x + 10, y - 13.5, "ArialNarrow-Bold", 6.8, color)
            R.text(c, shorten(entry.category, 29), x + 57, y - 13.5, "ArialNarrow", 7.2, INK)
            R.text_right(c, str(CATEGORY_PAGES[entry.reference]), x + col_w - 8, y - 13.5, "ArialNarrow-Bold", 6.8, INK)
            c.linkAbsolute(entry.category, f"entry-{entry.reference}", (x, y - 20, x + col_w, y), thickness=0)
            y -= 22
    book.finish()


def method_cards_page(book: Book, page_no: int, kicker: str, title: str, deck: str, cards_data: Sequence[tuple[str, str, str]], footer: str) -> None:
    book.start("Method", None, f"method-{page_no}", 0)
    c = book.c
    R.page_title(c, kicker, title, deck)
    card_w = (PAGE_W - 2 * M - 12) / 2
    y_positions = [616, 452, 288]
    for i, (label, heading, body) in enumerate(cards_data[:6]):
        col, row = i % 2, i // 2
        x = M + col * (card_w + 12)
        top = y_positions[row]
        c.setFillColor(PAPER_DARK if i % 2 == 0 else R.WHITE_WASH)
        c.roundRect(x, top - 134, card_w, 134, 4, fill=1, stroke=0)
        R.text(c, label, x + 11, top - 25, "Georgia-Bold", 14, RED)
        R.text(c, heading.upper(), x + 47, top - 21, "ArialNarrow-Bold", 8, INK)
        fit_para(c, body, x + 47, top - 36, card_w - 59, 85, "body_tight")
    c.setFillColor(INK)
    c.roundRect(M, 53, PAGE_W - 2 * M, 63, 3, fill=1, stroke=0)
    footer_text = re.sub(r"<[^>]+>", "", footer)
    fit_para(c, footer_text, M + 14, 96, PAGE_W - 2 * M - 28, 40, "callout")
    book.finish()


def build_front_matter(book: Book) -> None:
    colophon_page(book)
    contents_page(book)
    alphabetical = sorted(ENTRIES, key=lambda e: e.category.lower())
    category_index_page(book, 1, alphabetical[:50])
    category_index_page(book, 2, alphabetical[50:])

    method_cards_page(book, 6, "Reader's key", "Read the ruling, then audit it.", "Each category starts with the job and state. The declaration is only the beginning; the ownership page tests whether the answer survives use.", [
        ("01", "Start with the Form", "The Form is the bounded job. Size, region, installation, fit, load, and use conditions belong here before a model is compared."),
        ("02", "Read the state", "Declared, candidate, empty, split, conditional, and consumable are different conclusions. None should be softened into a generic recommendation."),
        ("03", "Inspect the plate", "A plate may be observed exterior, verified construction, conceptual mechanism, or interpretive. Its label controls what it can prove."),
        ("04", "Follow ownership", "Maintenance, parts, consumables, storage, software, and service are treated as part of the product."),
        ("05", "Pressure-test rivals", "A candidate remains when it buys a real advantage, serves a different Form, or could overturn the decision with new evidence."),
        ("06", "Open the source", "Exact-model identity and service claims resolve to readable source links with an access date and evidence role."),
    ], '<font color="#F3EBDD"><b>Reading path:</b> state -> Form -> plate -> reasons -> ownership -> failures -> source -> reconsideration trigger.</font>')

    method_cards_page(book, 7, "Constitution", "Six tests before a declaration.", "A winner must clear every essential threshold. Prestige, novelty, and feature count cannot compensate for a failed job or an opaque ownership path.", [
        ("01", "Fit", "Does it solve the ordinary job inside the stated use boundary without depending on a specialist exception?"),
        ("02", "Form", "Does its construction remove avoidable joints, coatings, proprietary dependencies, or fragile complexity?"),
        ("03", "Recovery", "Can ordinary wear be cleaned, sharpened, reseasoned, repaired, rebuilt, or replaced rationally?"),
        ("04", "Supply", "Are the model, consumables, service information, and critical parts still obtainable in the intended region?"),
        ("05", "Ownership", "Are care, storage, failure symptoms, service boundaries, and terminal damage legible before purchase?"),
        ("06", "Value", "Does extra cost buy a useful property across the ownership horizon instead of ornament, churn, or lock-in?"),
    ], '<font color="#F3EBDD"><b>A declaration is maintained.</b> New product revisions, discontinued parts, recalls, or better evidence can reopen it.</font>')

    method_cards_page(book, 8, "Constitution", "Ten rules that keep the list honest.", "The dossier is built to resist the pressure to name a product when the category, source, or ownership case is not ready.", [
        ("I", "Define before comparing", "A broad category is split before incompatible jobs are forced into one answer."),
        ("II", "Name exact variants", "Model, generation, size, voltage, region, fit, and configuration are captured whenever they change the verdict."),
        ("III", "Prefer simple failure", "A visible, serviceable wear part is usually better than a sealed assembly whose whole value disappears at one fault."),
        ("IV", "Do not confuse warranty", "A warranty transfers some risk. It does not by itself establish parts, repair, or permanent ownership."),
        ("V", "Preserve honest emptiness", "If no product qualifies, the useful output is the reason and a specification for what would."),
        ("VI-X", "Keep judgment revisable", "Facts are cited, inferences are labeled, uncertainty stays visible, marketing claims stay attributed, and every ruling has a reconsideration trigger."),
    ], '<font color="#F3EBDD">The standard applies equally to an inexpensive pan, a premium coat, a connected device, and an empty category.</font>')

    method_cards_page(book, 9, "Evidence", "A ladder, not a pile of links.", "Sources are ranked by what they can prove. Ten repeated retailer pages do not outweigh one exact service manual.", [
        ("A", "Exact primary", "Exact model page, specification sheet, service manual, parts diagram, warranty, safety notice, certification, or regulatory filing."),
        ("B", "Independent test", "A disclosed method applied to the exact model, with enough detail to understand measurements and limitations."),
        ("C", "Ownership evidence", "Long-term reports, repair records, teardown evidence, parts substitutions, and recurring failure patterns."),
        ("D", "Market evidence", "Current price, regional availability, used supply, consumables, and service-center access. These facts are dated."),
        ("E", "Lead only", "Retailer copy, forums, reviews, and search results can locate evidence. They do not establish the claim by themselves."),
        ("F", "Editorial inference", "A judgment that follows from cited facts. It stays visibly separate from a measurement or manufacturer statement."),
    ], '<font color="#F3EBDD"><b>Source discipline:</b> exact model, evidence role, publisher, region, revision, access date, and claim supported.</font>')

    method_cards_page(book, 10, "Illustration", "A picture can clarify or overclaim.", "The Delta catalog earns attention because its images carry evidence. This dossier borrows that density while making the truth status of every plate explicit.", [
        ("01", "Observed exterior", "Visible geometry checked against exact-model identity views. It can show controls, interfaces, proportions, and visible construction."),
        ("02", "Verified construction", "Hidden relationships shown only when an exact service manual, diagram, teardown, patent, or direct inspection supports them."),
        ("03", "Conceptual mechanism", "A general system or failure path. It must never be mistaken for the exact product's hidden engineering."),
        ("04", "Interpretive plate", "Original editorial art that represents the Form. It is atmosphere and explanation, not SKU identity evidence."),
        ("05", "Comparison plate", "Matched scale, angle, and crop make one decisive difference visible without relying on brand decoration."),
        ("06", "Ownership plate", "Consumables, tools, parts, intervals, and failure points show what the owner will actually encounter."),
    ], '<font color="#F3EBDD">Manufacturer photography remains an identity reference unless republication rights are documented.</font>')

    method_cards_page(book, 11, "Ownership", "The object is only one layer.", "A durable product can still be a poor ownership system when its parts, software, consumables, or service path disappear.", [
        ("01", "Object", "Materials, geometry, interfaces, controls, fasteners, and the load path that performs the job."),
        ("02", "Wear layer", "Seasoning, soles, pads, filters, seals, cords, blades, bearings, batteries, upholstery, and other finite components."),
        ("03", "Care", "Cleaning, lubrication, sharpening, drying, storage, inspection, calibration, updates, and safe operation."),
        ("04", "Service", "Manuals, tools, access, part numbers, substitutions, labor, warranty, and repair economics."),
        ("05", "Supply", "Consumables, standard interfaces, regional availability, software support, and secondhand stock."),
        ("06", "Exit", "The retirement threshold and what can be reused, recycled, rebuilt, sold, or safely discarded."),
    ], '<font color="#F3EBDD">The dossier asks whether all six layers remain intelligible over the likely ownership horizon.</font>')

    method_cards_page(book, 12, "Failure", "Name the recovery path before the failure.", "A useful guide tells the owner what a symptom means, what can be attempted safely, and when the object has crossed a terminal boundary.", [
        ("R1", "Clean or reset", "Contamination, configuration, blocked passages, lost seasoning, or minor corrosion may return through ordinary care."),
        ("R2", "Replace wear part", "A blade, filter, belt, cord, seal, pad, grip, battery, or similar layer renews without discarding the structure."),
        ("R3", "Repair module", "A documented assembly can be serviced with accessible tools, parts, and safe procedures."),
        ("R4", "Rebuild", "The sound frame, body, or chassis justifies major renewal when the parts and economics remain credible."),
        ("T", "Terminal", "Cracks, unsafe deformation, contamination, obsolete security, missing critical parts, or uneconomic core failure can end service."),
        ("?", "Unknown", "When evidence is missing, the dossier records the question instead of inventing a reassuring repair story."),
    ], '<font color="#F3EBDD">Safety-critical electrical, fuel, pressure, structural, and hygiene work may require a qualified professional.</font>')

    method_cards_page(book, 13, "Price and time", "A price is a dated observation.", "The dossier treats price, supply, parts, and policy as changing evidence rather than permanent product specifications.", [
        ("01", "Capture", "Amount or range, currency, seller type, region, configuration, and access date."),
        ("02", "Normalize", "Compare like-for-like size, included accessories, shipping, installation, and necessary consumables."),
        ("03", "Separate", "A premium can buy material, fit, service, lower weight, finish, or warranty. The exact advantage is named."),
        ("04", "Extend", "Five- and ten-year questions include wear parts, consumables, service labor, energy, and forced platform changes."),
        ("05", "Recheck", "Sale price, discontinued status, parts stock, and support policy are revalidated before release."),
        ("06", "Disclose", "Unknown cost remains unknown. A tidy total is never manufactured to fill a table."),
    ], '<font color="#F3EBDD">Prices in this review are historical working notes unless a source and capture date appear beside them.</font>')

    method_cards_page(book, 14, "Editorial states", "A non-declaration can still end a search.", "The open states preserve useful distinctions about what research should happen next.", [
        ("E", "Empty", "No current product clears the Form. The page explains the recurring failure and specifies what a future product must do."),
        ("S", "Split required", "The parent hides incompatible jobs. Child Forms are defined before any model can win."),
        ("C", "Conditional", "A viable answer depends on installation, fit, region, workload, service, or another material condition."),
        ("R", "Consumable", "Wear or hygiene makes replacement intrinsic. The task becomes choosing the safest, simplest renewal cycle."),
        ("P", "Candidate", "A model or construction path deserves serious investigation but is missing decisive proof."),
        ("D", "Declared", "The current evidence closes the ordinary search while keeping tradeoffs and reopening triggers visible."),
    ], '<font color="#F3EBDD">The state describes the research conclusion. It is not a product score.</font>')

    method_cards_page(book, 15, "Testing", "What the next evidence should measure.", "A final commercial edition should add repeatable tests where a specification or visual inspection cannot settle the ownership question.", [
        ("K", "Cookware", "Usable surface, flatness, heat response, handle temperature, pour behavior, cleaning, corrosion, and seasoning recovery."),
        ("T", "Tools", "Accuracy, balance, interface fit, runout, load behavior, wear, service access, and parts substitution."),
        ("C", "Clothing", "Fit stability, seam repair, abrasion, laundering, shrinkage, resoling, and replacement components."),
        ("O", "Outdoor", "Load, weather, pack volume, fuel or power supply, field repair, safety margins, and storage damage."),
        ("E", "Electronics", "Thermals, battery, software horizon, ports, module replacement, security, and compatibility across revisions."),
        ("H", "Home systems", "Capacity, installation, energy, noise, service access, part price, failure frequency, and qualified labor."),
    ], '<font color="#F3EBDD">Every test needs the exact variant, conditions, instruments, repeat count, uncertainty, and failure threshold.</font>')

    method_cards_page(book, 16, "Review edition", "The full run is a map of value and work.", "This book makes the intended paid product concrete: deep enough to review as a whole, explicit enough to reveal what still blocks commercial release.", [
        ("01", "Complete architecture", "Cover, method, nine domains, 100 category rulings, source and image ledgers, maintenance and service indices, and review tools."),
        ("02", "Real editorial states", "All 48 declarations and 52 open findings are present; nothing is promoted merely to make the book feel complete."),
        ("03", "Visible source quality", "Exact, family, ambiguous, and generic identity states remain legible beside declared models."),
        ("04", "Delta-inspired density", "Large plates, reasons-why copy, specification blocks, ownership maps, and tables carry the reading order."),
        ("05", "Plato retained", "The dossier keeps the Plato portrait, sourced passages, mineral palette, and antiquity visual system."),
        ("06", "Next production gates", "Candidate sets, exact-model normalization, parts stock, independent tests, rights review, copy edit, and tagged-PDF accessibility."),
    ], '<font color="#F3EBDD"><b>Review question:</b> does this structure make the dossier worth returning to after the purchase decision?</font>')


def domain_opener_pages(book: Book, domain_index: int, domain: str, name: str, description: str) -> None:
    entries = ENTRIES_BY_DOMAIN[domain]
    declared = [e for e in entries if e.status == "DECLARED"]
    representative = declared[0] if declared else entries[0]
    book.start(name, name, f"domain-{domain}", 0)
    c = book.c
    image = plate_path(representative)
    if image:
        c.setFillColor(R.WHITE_WASH)
        c.roundRect(M, 108, 270, 620, 4, fill=1, stroke=0)
        R.draw_contain(c, image, M + 10, 118, 250, 600)
        R.tag(c, "Interpretive plate", M + 12, 708, fill=RED, width=96)
    else:
        c.setFillColor(INK)
        c.rect(M, 108, 270, 620, fill=1, stroke=0)
        R.text_center(c, f"{domain_index:02d}", M + 135, 405, "Georgia-Bold", 72, PAPER)
    x = M + 300
    R.text(c, f"DOMAIN {domain_index:02d}", x, 698, "ArialNarrow-Bold", 9, RED)
    fit_title(c, name, x, 646, PAGE_W - M - x, 29, 16)
    fit_para(c, description, x, 606, PAGE_W - M - x, 58, "body_tight")
    states = Counter(e.status for e in entries)
    metrics = [(str(len(entries)), "ENTRIES"), (str(states.get("DECLARED", 0)), "DECLARED"), (str(len(entries) - states.get("DECLARED", 0)), "OPEN")]
    y = 510
    for value, label in metrics:
        R.text(c, value, x, y, "Georgia-Bold", 19, RED)
        R.text(c, label, x + 48, y + 4, "ArialNarrow-Bold", 7.4, MUTED)
        y -= 46
    quote, cite = QUOTES[(domain_index - 1) % len(QUOTES)]
    c.setFillColor(PAPER_DARK)
    c.roundRect(x, 222, PAGE_W - M - x, 128, 4, fill=1, stroke=0)
    fit_para(c, f'"{quote}"', x + 14, 322, PAGE_W - M - x - 28, 68, "body_tight")
    R.text(c, f"PLATO / {cite.upper()}", x + 14, 242, "ArialNarrow-Bold", 7.2, RED)
    R.text(c, "READING QUESTION", x, 185, "ArialNarrow-Bold", 7.7, RED)
    question = DOMAIN_PATTERNS[domain][0]
    fit_para(c, question, x, 169, PAGE_W - M - x, 55, "body_tight")
    book.finish()

    book.start(name, None, f"domain-map-{domain}", 0)
    c = book.c
    R.page_title(c, f"Domain {domain_index:02d}", "The field before the picks.", "These categories share recurring ownership questions, but each still receives a bounded Form and its own evidence state.")
    section_rule(c, "Recurring proof questions", 622)
    pattern_w = (PAGE_W - 2 * M - 12) / 2
    for i, pattern in enumerate(DOMAIN_PATTERNS[domain]):
        x = M + (i % 2) * (pattern_w + 12)
        top = 592 - (i // 2) * 82
        card(c, x, top, pattern_w, 66, f"{i + 1:02d}", pattern, R.WHITE_WASH if i % 2 else PAPER_DARK, RED, "sans")
    section_rule(c, "Category map", 411)
    col_gap = 16
    col_w = (PAGE_W - 2 * M - col_gap) / 2
    split_at = (len(entries) + 1) // 2
    for col, chunk in enumerate([entries[:split_at], entries[split_at:]]):
        x = M + col * (col_w + col_gap)
        y = 384
        for entry in chunk:
            color = STATUS_COLORS[entry.status]
            c.setFillColor(PAPER_DARK if entry.number % 2 else R.WHITE_WASH)
            c.rect(x, y - 27, col_w, 27, fill=1, stroke=0)
            c.setFillColor(color)
            c.rect(x, y - 27, 4, 27, fill=1, stroke=0)
            R.text(c, entry.reference, x + 10, y - 12, "ArialNarrow-Bold", 6.7, color)
            R.text(c, shorten(entry.category, 30), x + 55, y - 12, "ArialNarrow", 7.2, INK)
            R.text(c, STATUS_LABELS[entry.status], x + 55, y - 22, "ArialNarrow", 5.8, MUTED)
            R.text_right(c, str(CATEGORY_PAGES[entry.reference]), x + col_w - 8, y - 17, "ArialNarrow-Bold", 6.7, INK)
            c.linkAbsolute(entry.category, f"entry-{entry.reference}", (x, y - 27, x + col_w, y), thickness=0)
            y -= 30
    book.finish()


def source_state(entry: Entry) -> tuple[str, str, str]:
    source = SOURCES_BY_REF.get(entry.reference)
    if not source:
        return ("No source record", "No exact identity source is logged.", "")
    identity = normalize(source.get("identityStatus")).upper()
    note = normalize(source.get("notes"))
    url = normalize(source.get("sourceUrl"))
    return (identity, note, url)


def verdict_title(entry: Entry) -> str:
    if entry.status == "DECLARED":
        return "Why this ends the search"
    if entry.status == "EMPTY":
        return "Why no product qualifies"
    if entry.status == "SPLIT_REQUIRED":
        return "Why the parent must split"
    if entry.status == "CONSUMABLE":
        return "Why renewal is intrinsic"
    return "Why the decision stays open"


def declared_judgment_page(book: Book, entry: Entry) -> None:
    domain_name = DOMAIN_INFO[entry.domain][0]
    book.start(f"{entry.reference} / {domain_name}", entry.category, f"entry-{entry.reference}", 1)
    c = book.c
    color = STATUS_COLORS[entry.status]
    R.text(c, entry.reference, M, PAGE_H - 61, "ArialNarrow-Bold", 8.5, RED)
    fit_title(c, entry.category, M, PAGE_H - 96, PAGE_W - 2 * M - 105, 27, 16)
    R.tag(c, STATUS_LABELS[entry.status], PAGE_W - M - 94, PAGE_H - 67, fill=color, width=94)
    if entry.model:
        fit_para(c, entry.model, M, PAGE_H - 116, PAGE_W - 2 * M, 33, "body_tight")
    image = plate_path(entry)
    image_x, image_y, image_w, image_h = M, 316, 326, 352
    c.setFillColor(R.WHITE_WASH)
    c.roundRect(image_x, image_y, image_w, image_h, 4, fill=1, stroke=0)
    if image:
        R.draw_contain(c, image, image_x + 8, image_y + 8, image_w - 16, image_h - 16)
    plate_label = "Observed exterior + conceptual detail" if entry.reference in {"PI-001", "PI-003", "PI-012"} else "Interpretive plate / not SKU evidence"
    R.tag(c, plate_label, image_x + 10, image_y + image_h - 14, fill=RED, width=156 if entry.reference in {"PI-001", "PI-003", "PI-012"} else 151)
    R.text(c, "ORIGINAL EDITORIAL ART", image_x + 10, image_y + 12, "ArialNarrow-Bold", 6.2, MUTED)

    right_x = M + image_w + 14
    right_w = PAGE_W - M - right_x
    card(c, right_x, 668, right_w, 119, "The ruling", entry.summary or entry.reasoning, STATUS_PALES[entry.status], color)
    card(c, right_x, 538, right_w, 123, "The Form", entry.form, R.WHITE_WASH, RED)
    identity, identity_note, _ = source_state(entry)
    meta = [
        ("PRICE NOTE", entry.price or "Not captured"),
        ("REVIEWED", entry.reviewed or "Not recorded"),
        ("PERMANENCE", entry.permanence or "Not classified"),
        ("IDENTITY", identity),
    ]
    meta_y = 403
    for label, value in meta:
        c.setFillColor(PAPER_DARK)
        c.roundRect(right_x, meta_y - 38, right_w, 34, 3, fill=1, stroke=0)
        R.text(c, label, right_x + 8, meta_y - 17, "ArialNarrow-Bold", 6.3, MUTED)
        R.text_right(c, shorten(value, 31), right_x + right_w - 8, meta_y - 18, "ArialNarrow-Bold", 6.8, INK)
        meta_y -= 42

    section_rule(c, verdict_title(entry), 289, color)
    fit_para(c, entry.reasoning or entry.summary, M, 261, PAGE_W - 2 * M, 91, "body_tight")
    section_rule(c, "Decisive facts and consequences", 154, color)
    facts = sentences(entry.reasoning, 4)
    if not facts:
        facts = sentences(entry.form, 4)
    fact_w = (PAGE_W - 2 * M - 18) / 4
    for i in range(4):
        fact = facts[i] if i < len(facts) else "Additional exact-model evidence is still required for this part of the ruling."
        x = M + i * (fact_w + 6)
        c.setFillColor(R.WHITE_WASH if i % 2 else PAPER_DARK)
        c.roundRect(x, 59, fact_w, 70, 3, fill=1, stroke=0)
        R.text(c, f"{i + 1:02d}", x + 8, 111, "Georgia-Bold", 10, color)
        fit_para(c, fact, x + 8, 98, fact_w - 16, 34, "sans")
    book.finish()


def ownership_checklist(entry: Entry) -> list[str]:
    items = [
        f"Confirm the exact variant, size, configuration, and region for {entry.model or entry.category}.",
        "Open the current manual, warranty, and service information before purchase.",
        "Price the first expected wear part or consumable, including tools and labor.",
        "Record serial, receipt, configuration, and source links while the pages are current.",
    ]
    if entry.maintenance:
        items[2] = f"Plan for the recorded maintenance boundary: {entry.maintenance}."
    return items


def change_trigger(entry: Entry) -> str:
    if entry.notes:
        return "Reopen the ruling when the noted identity or evidence issue is resolved: " + entry.notes
    if entry.disqualifiers:
        first = sentences(entry.disqualifiers, 1)
        return "Reopen the ruling when a credible rival clears the Form without this failure: " + (first[0] if first else entry.disqualifiers)
    return "Reopen the ruling when a credible exact model improves the ownership path without failing the defined Form."


def declared_ownership_page(book: Book, entry: Entry) -> None:
    domain_name = DOMAIN_INFO[entry.domain][0]
    book.start(f"{entry.reference} / Ownership", None, f"ownership-{entry.reference}", 1)
    c = book.c
    color = STATUS_COLORS[entry.status]
    R.text(c, entry.reference, M, PAGE_H - 61, "ArialNarrow-Bold", 8.5, RED)
    fit_title(c, "Ownership brief", M, PAGE_H - 96, PAGE_W - 2 * M, 26, 16)
    fit_para(c, entry.category + " / " + (entry.model or "model not normalized"), M, PAGE_H - 116, PAGE_W - 2 * M, 26, "sans_bold")

    section_rule(c, "Admission test", 637, color)
    admission = entry.admission or entry.form
    admission_items = sentences(admission, 4)
    if not admission_items:
        admission_items = [entry.form]
    w = (PAGE_W - 2 * M - 18) / 4
    for i in range(4):
        body = admission_items[i] if i < len(admission_items) else "Criterion not yet decomposed into a cited pass/fail check."
        x = M + i * (w + 6)
        card(c, x, 611, w, 84, f"Gate {i + 1}", body, GREEN_PALE if i < len(admission_items) else RED_PALE, GREEN if i < len(admission_items) else RED, "sans")

    section_rule(c, "Failure and recovery", 506, color)
    failure_body = entry.failures or "Exact-model failure modes are not yet logged. Commercial release gate: add symptom, cause, consequence, safe recovery, parts path, and terminal threshold."
    card(c, M, 480, 346, 110, "Known or required failure map", failure_body, R.WHITE_WASH, RED)
    maintenance_body = entry.maintenance or "No maintenance cycle is recorded. Establish cleaning, inspection, consumables, storage, and service intervals."
    card(c, M + 358, 480, PAGE_W - M - (M + 358), 110, "Maintenance path", maintenance_body, PAPER_DARK, color)

    section_rule(c, "Why alternatives lose", 345, color)
    left_w = 340
    disq = sentences(entry.disqualifiers, 5)
    if not disq:
        disq = ["A named, evidence-backed disqualifier set has not yet been recorded."]
    numbered_list(c, disq, M, 320, left_w, 5, color, 31)
    right_x = M + left_w + 16
    right_w = PAGE_W - M - right_x
    alt_body = entry.alternates or "No named runners-up are logged. Add at least three serious candidates, their decisive advantage, decisive loss, price, evidence state, and reconsideration trigger."
    card(c, right_x, 320, right_w, 89, "Candidate field", alt_body, STATUS_PALES["CANDIDATE"], GOLD)
    identity, identity_note, url = source_state(entry)
    source_body = f"Identity status: {identity}. {identity_note or 'No source note recorded.'}"
    card(c, right_x, 219, right_w, 94, "Source audit", source_body, BLUE_PALE, BLUE)

    section_rule(c, "Before you buy", 144, color)
    checks = ownership_checklist(entry)
    check_w = (PAGE_W - 2 * M - 8) / 2
    for i, check in enumerate(checks):
        col, row = i % 2, i // 2
        x = M + col * (check_w + 8)
        top = 119 - row * 34
        c.setFillColor(PAPER_DARK if i % 2 == 0 else R.WHITE_WASH)
        c.roundRect(x, top - 28, check_w, 28, 2, fill=1, stroke=0)
        R.text(c, f"{i + 1:02d}", x + 8, top - 18, "ArialNarrow-Bold", 6.6, color)
        fit_para(c, check, x + 30, top - 7, check_w - 38, 18, "sans")
    if url:
        c.linkURL(url, (right_x, 125, right_x + right_w, 219), relative=0, thickness=0)
    book.finish()


def open_brief_page(book: Book, entry: Entry) -> None:
    domain_name = DOMAIN_INFO[entry.domain][0]
    book.start(f"{entry.reference} / {domain_name}", entry.category, f"entry-{entry.reference}", 1)
    c = book.c
    color = STATUS_COLORS[entry.status]
    pale = STATUS_PALES[entry.status]
    R.text(c, entry.reference, M, PAGE_H - 61, "ArialNarrow-Bold", 8.5, RED)
    fit_title(c, entry.category, M, PAGE_H - 96, PAGE_W - 2 * M - 112, 25, 13)
    R.tag(c, STATUS_LABELS[entry.status], PAGE_W - M - 108, PAGE_H - 67, fill=color, width=108)
    if entry.model:
        R.text(c, shorten(entry.model, 102), M, PAGE_H - 116, "ArialNarrow", 7.4, MUTED)

    c.setFillColor(pale)
    c.roundRect(M, 592, PAGE_W - 2 * M, 66, 4, fill=1, stroke=0)
    R.text(c, "CURRENT RULING", M + 12, 636, "ArialNarrow-Bold", 7.6, color)
    fit_para(c, entry.summary or STATUS_PUBLIC[entry.status], M + 12, 622, PAGE_W - 2 * M - 24, 34, "body_tight")

    section_rule(c, "The bounded Form", 574, color)
    card(c, M, 548, PAGE_W - 2 * M, 78, "What must be true", entry.form, R.WHITE_WASH, color)

    section_rule(c, verdict_title(entry), 442, color)
    left_w = 330
    card(c, M, 416, left_w, 139, "Current case", entry.reasoning or entry.summary, PAPER_DARK, color)
    disq_body = entry.disqualifiers or "No exact disqualifier set has been recorded. Define the evidence that would fail this Form."
    card(c, M + left_w + 12, 416, PAGE_W - 2 * M - left_w - 12, 139, "Blocking conditions", disq_body, RED_PALE if entry.status == "EMPTY" else R.WHITE_WASH, RED)

    section_rule(c, "Ownership and next evidence", 247, color)
    box_w = (PAGE_W - 2 * M - 16) / 3
    card(c, M, 221, box_w, 105, "Maintenance boundary", entry.maintenance or "Not yet recorded.", PAPER_DARK, color)
    card(c, M + box_w + 8, 221, box_w, 105, "Permanence", entry.permanence or "Unresolved.", R.WHITE_WASH, color)
    next_evidence = entry.notes or "Normalize the exact model and variant, add primary sources, compare serious rivals, and define the reconsideration trigger."
    card(c, M + 2 * (box_w + 8), 221, box_w, 105, "Release gate", next_evidence, BLUE_PALE, BLUE)

    related = related_entries(entry)
    section_rule(c, "Related child Forms or cases", 89, color)
    if related:
        x = M
        for related_entry in related[:4]:
            w = (PAGE_W - 2 * M - 18) / min(4, len(related))
            c.setFillColor(STATUS_PALES[related_entry.status])
            c.roundRect(x, 46, w, 29, 2, fill=1, stroke=0)
            R.text(c, related_entry.reference, x + 7, 64, "ArialNarrow-Bold", 6.2, STATUS_COLORS[related_entry.status])
            R.text(c, shorten(related_entry.category, 20), x + 43, 64, "ArialNarrow", 6.5, INK)
            c.linkAbsolute(related_entry.category, f"entry-{related_entry.reference}", (x, 46, x + w, 75), thickness=0)
            x += w + 6
    else:
        R.text(c, "No linked child case is currently recorded.", M, 59, "ArialNarrow", 7.2, MUTED)
    book.finish()


def build_domain_content(book: Book) -> None:
    for index, (domain, name, description) in enumerate(DOMAINS, 1):
        domain_opener_pages(book, index, domain, name, description)
        for entry in ENTRIES_BY_DOMAIN[domain]:
            if entry.status == "DECLARED":
                declared_judgment_page(book, entry)
                declared_ownership_page(book, entry)
            else:
                open_brief_page(book, entry)


def maintenance_index_pages(book: Book) -> None:
    declared = [e for e in ENTRIES if e.status == "DECLARED"]
    for page_index, chunk in enumerate([declared[:24], declared[24:]], 1):
        book.start("Ownership index", "Maintenance index" if page_index == 1 else None, f"maintenance-index-{page_index}", 0)
        c = book.c
        R.page_title(c, "Ownership index", f"Maintenance map {page_index}/2", "The current register's recorded care or replacement cycle. Short legacy values are preserved and flagged for expansion in production research.")
        y = 620
        widths = [52, 110, 138, 174, 66]
        headers = ["Ref", "Category", "Declared model", "Recorded cycle", "Page"]
        c.setFillColor(RED)
        c.rect(M, y - 22, sum(widths), 22, fill=1, stroke=0)
        x = M
        for w, header in zip(widths, headers):
            R.text(c, header.upper(), x + 6, y - 15, "ArialNarrow-Bold", 6.5, white)
            x += w
        y -= 22
        for i, entry in enumerate(chunk):
            h = 23
            c.setFillColor(R.WHITE_WASH if i % 2 == 0 else PAPER_DARK)
            c.rect(M, y - h, sum(widths), h, fill=1, stroke=0)
            values = [entry.reference, entry.category, entry.model, entry.maintenance or "Not recorded", str(CATEGORY_PAGES[entry.reference])]
            x = M
            for j, (w, value) in enumerate(zip(widths, values)):
                R.text(c, shorten(value, [8, 24, 34, 46, 5][j]), x + 6, y - 15, "ArialNarrow-Bold" if j in (0, 4) else "ArialNarrow", 6.4, RED if j == 0 else INK)
                x += w
            c.linkAbsolute(entry.category, f"entry-{entry.reference}", (M, y - h, M + sum(widths), y), thickness=0)
            y -= h
        book.finish()


def service_audit_pages(book: Book) -> None:
    declared = [e for e in ENTRIES if e.status == "DECLARED"]
    for page_index, chunk in enumerate([declared[:24], declared[24:]], 1):
        book.start("Evidence index", "Serviceability audit" if page_index == 1 else None, f"service-audit-{page_index}", 0)
        c = book.c
        R.page_title(c, "Evidence index", f"Serviceability audit {page_index}/2", "A declaration can have strong category fit and weak exact-model service proof. This index keeps those dimensions separate.")
        y = 620
        widths = [52, 112, 75, 104, 197]
        headers = ["Ref", "Category", "Identity", "Permanence", "Evidence gap or note"]
        c.setFillColor(BLUE)
        c.rect(M, y - 22, sum(widths), 22, fill=1, stroke=0)
        x = M
        for w, header in zip(widths, headers):
            R.text(c, header.upper(), x + 6, y - 15, "ArialNarrow-Bold", 6.5, white)
            x += w
        y -= 22
        for i, entry in enumerate(chunk):
            identity, note, _ = source_state(entry)
            h = 23
            c.setFillColor(R.WHITE_WASH if i % 2 == 0 else PAPER_DARK)
            c.rect(M, y - h, sum(widths), h, fill=1, stroke=0)
            values = [entry.reference, entry.category, identity, entry.permanence or "Unresolved", note or "No source note"]
            limits = [8, 24, 13, 19, 58]
            x = M
            for j, (w, value) in enumerate(zip(widths, values)):
                R.text(c, shorten(value, limits[j]), x + 6, y - 15, "ArialNarrow-Bold" if j in (0, 2) else "ArialNarrow", 6.2, RED if j == 0 else INK)
                x += w
            c.linkAbsolute(entry.category, f"entry-{entry.reference}", (M, y - h, M + sum(widths), y), thickness=0)
            y -= h
        book.finish()


def source_ledger_pages(book: Book) -> None:
    records = sorted(SOURCE_RECORDS, key=lambda r: r["productId"])
    chunks = [records[i:i + 10] for i in range(0, 50, 10)]
    for page_index, chunk in enumerate(chunks, 1):
        book.start("Source ledger", "Source ledger" if page_index == 1 else None, f"source-ledger-{page_index}", 0)
        c = book.c
        R.page_title(c, "Evidence ledger", f"Identity sources {page_index}/5", "Manufacturer and comparable identity leads for the 48 declared records. Rights status controls image use; identity status controls factual confidence.")
        y = 620
        for record in chunk:
            ref = normalize(record.get("productId"))
            entry = ENTRIES_BY_REF.get(ref)
            color = GREEN if normalize(record.get("identityStatus")) == "exact" else GOLD
            c.setFillColor(R.WHITE_WASH if int(ref[-3:]) % 2 else PAPER_DARK)
            c.roundRect(M, y - 50, PAGE_W - 2 * M, 50, 3, fill=1, stroke=0)
            R.text(c, ref, M + 9, y - 17, "ArialNarrow-Bold", 7, RED)
            R.text(c, shorten(record.get("sourcePageTitle", "Untitled source"), 54), M + 58, y - 16, "ArialNarrow-Bold", 7, INK)
            R.tag(c, normalize(record.get("identityStatus")) or "unknown", PAGE_W - M - 74, y - 7, fill=color, width=68)
            url = normalize(record.get("sourceUrl"))
            if url:
                link = f'<link href="{escape(url)}" color="#244A63"><u>{escape(shorten(url, 118))}</u></link>'
                p = Paragraph(link, EXTRA_STYLES["source"])
                _, h = p.wrap(PAGE_W - 2 * M - 67, 20)
                p.drawOn(c, M + 58, y - 31 - h)
                c.linkURL(url, (M, y - 50, PAGE_W - M, y), relative=0, thickness=0)
            else:
                R.text(c, "No public source URL recorded.", M + 58, y - 37, "ArialNarrow", 6.5, MUTED)
            y -= 55
        book.finish()


def image_ledger_pages(book: Book) -> None:
    declared = [e for e in ENTRIES if e.status == "DECLARED"]
    for page_index, chunk in enumerate([declared[:24], declared[24:]], 1):
        book.start("Image ledger", "Image ledger" if page_index == 1 else None, f"image-ledger-{page_index}", 0)
        c = book.c
        R.page_title(c, "Image ledger", f"Original product plates {page_index}/2", "Every product image is original editorial artwork. Three featured plates use exterior references and conceptual detail; the remaining plates represent the Form and do not prove SKU identity.")
        y = 620
        widths = [52, 116, 180, 126, 66]
        headers = ["Ref", "Category", "Local asset", "Truth label", "Credit"]
        c.setFillColor(RED)
        c.rect(M, y - 22, sum(widths), 22, fill=1, stroke=0)
        x = M
        for w, header in zip(widths, headers):
            R.text(c, header.upper(), x + 6, y - 15, "ArialNarrow-Bold", 6.5, white)
            x += w
        y -= 22
        for i, entry in enumerate(chunk):
            h = 23
            path = plate_path(entry)
            label = "Observed exterior + conceptual detail" if entry.reference in {"PI-001", "PI-003", "PI-012"} else "Interpretive / representative"
            values = [entry.reference, entry.category, str(path.relative_to(ROOT)) if path else "No local asset", label, "OpenAI image generation"]
            limits = [8, 25, 50, 31, 20]
            c.setFillColor(R.WHITE_WASH if i % 2 == 0 else PAPER_DARK)
            c.rect(M, y - h, sum(widths), h, fill=1, stroke=0)
            x = M
            for j, (w, value) in enumerate(zip(widths, values)):
                R.text(c, shorten(value, limits[j]), x + 6, y - 15, "ArialNarrow-Bold" if j == 0 else "ArialNarrow", 6.2, RED if j == 0 else INK)
                x += w
            y -= h
        book.finish()


def research_queue_page(book: Book) -> None:
    book.start("Research queue", "Research queue", "research-queue", 0)
    c = book.c
    R.page_title(c, "Release planning", "The gaps with the highest editorial leverage.", "The full run reveals where another source, named candidate, or exact variant would add the most reader value before commercial release.")
    section_rule(c, "Register state", 622)
    stats = Counter(e.status for e in ENTRIES)
    x = M
    w = (PAGE_W - 2 * M - 25) / 6
    for status in ["DECLARED", "CANDIDATE", "EMPTY", "SPLIT_REQUIRED", "CONDITIONAL", "CONSUMABLE"]:
        c.setFillColor(STATUS_PALES[status])
        c.roundRect(x, 537, w, 62, 3, fill=1, stroke=0)
        R.text_center(c, str(stats[status]), x + w / 2, 569, "Georgia-Bold", 15, STATUS_COLORS[status])
        R.text_center(c, STATUS_LABELS[status], x + w / 2, 550, "ArialNarrow-Bold", 5.8, INK)
        x += w + 5
    section_rule(c, "Priority queue", 511)
    queue = []
    for entry in ENTRIES:
        identity, note, _ = source_state(entry)
        if entry.status == "DECLARED" and identity != "EXACT":
            queue.append(("P1", entry, f"Normalize declared identity: {identity.lower()}. {note}"))
        elif entry.status == "DECLARED" and not entry.alternates:
            queue.append(("P1", entry, "Add three named candidate records with decisive loss reasons."))
        elif entry.status in {"CANDIDATE", "CONDITIONAL"} and entry.model.lower().startswith("model pending"):
            queue.append(("P1", entry, "Lock exact model, variant, region, and primary source bundle."))
        elif entry.status in {"EMPTY", "SPLIT_REQUIRED"}:
            queue.append(("P2", entry, "Complete rescue pass or child-Form case before terminal publication."))
    queue = queue[:16]
    y = 482
    for i, (priority, entry, action) in enumerate(queue):
        c.setFillColor(R.WHITE_WASH if i % 2 == 0 else PAPER_DARK)
        c.rect(M, y - 25, PAGE_W - 2 * M, 25, fill=1, stroke=0)
        R.tag(c, priority, M + 6, y - 4, fill=RED if priority == "P1" else GOLD, width=32)
        R.text(c, entry.reference, M + 46, y - 16, "ArialNarrow-Bold", 6.6, STATUS_COLORS[entry.status])
        R.text(c, shorten(entry.category, 24), M + 90, y - 16, "ArialNarrow-Bold", 6.8, INK)
        R.text(c, shorten(action, 90), M + 218, y - 16, "ArialNarrow", 6.5, MUTED)
        c.linkAbsolute(entry.category, f"entry-{entry.reference}", (M, y - 25, PAGE_W - M, y), thickness=0)
        y -= 27
    book.finish()


def change_log_page(book: Book) -> None:
    book.start("Change log", "Change log", "change-log", 0)
    c = book.c
    R.page_title(c, "Production record", "What this full run adds.", "The book is reviewable as a complete product while still exposing every major evidence and production gate.")
    section_rule(c, "Added in this edition", 622)
    added = [
        "Complete 100-category pagination with all six editorial states.",
        "Nine two-page domain openers and linked category maps.",
        "Two-page spreads for all 48 declarations and one-page briefs for 52 open cases.",
        "Ownership, failure, maintenance, candidate, evidence, and reconsideration modules.",
        "Clickable category index, PDF bookmarks, and direct external identity-source links.",
        "Cross-category maintenance, serviceability, source, image, and research-queue ledgers.",
        "Large Plato cover plus Delta-catalog-inspired plate, table, and reasons-why grammar.",
    ]
    numbered_list(c, added, M, 592, PAGE_W - 2 * M, 7, GREEN, 42)
    section_rule(c, "Still required for commercial release", 268)
    gates = [
        ("CANDIDATE DEPTH", "At least three serious named products or near-misses per category where the field supports them."),
        ("MODEL NORMALIZATION", "Resolve family, ambiguous, generic, voltage, size, generation, and exact-SKU identity records."),
        ("SERVICE PROOF", "Parts stock, substitutions, prices, labor, and safe procedures for claims that depend on repair."),
        ("INDEPENDENT TESTS", "Repeatable methods for performance and durability claims that primary sources cannot settle."),
        ("RIGHTS + ACCESSIBILITY", "Image and quotation territory review, copy edit, tagged PDF, reading order, and alt text."),
    ]
    y = 236
    for label, body in gates:
        c.setFillColor(PAPER_DARK)
        c.roundRect(M, y - 34, PAGE_W - 2 * M, 34, 2, fill=1, stroke=0)
        R.text(c, label, M + 10, y - 20, "ArialNarrow-Bold", 7, RED)
        fit_para(c, body, M + 142, y - 8, PAGE_W - 2 * M - 152, 22, "sans")
        y -= 39
    book.finish()


def full_review_page(book: Book) -> None:
    book.start("Review sheet", "Review sheet", "review-sheet", 0)
    c = book.c
    R.page_title(c, "Editorial review", "Does this feel five layers deeper?", "Score the book as a durable research product. The next pass should concentrate on the dimensions that still feel like a reformatted website instead of a reference work.")
    criteria = [
        ("Decision clarity", "The verdict and its boundary are clear after one spread."),
        ("Ownership value", "Maintenance, service, failure, and retirement change the decision."),
        ("Candidate pressure", "Alternatives are serious enough to make the winner credible."),
        ("Evidence visibility", "Facts, claims, inferences, gaps, and dates are easy to distinguish."),
        ("Delta influence", "Plates, sections, tables, and reasons-why copy carry useful information."),
        ("Platonic identity", "Plato, antiquity, restraint, and judgment feel integral to the book."),
        ("Density", "The page is rich enough to revisit without becoming exhausting."),
        ("Commercial value", "The dossier gives meaningfully more help than the public category page."),
    ]
    y = 620
    for i, (label, question) in enumerate(criteria, 1):
        c.setFillColor(R.WHITE_WASH if i % 2 else PAPER_DARK)
        c.rect(M, y - 48, PAGE_W - 2 * M, 48, fill=1, stroke=0)
        R.text(c, f"{i:02d}", M + 10, y - 29, "Georgia-Bold", 10, RED)
        R.text(c, label.upper(), M + 46, y - 20, "ArialNarrow-Bold", 7.6, INK)
        R.text(c, question, M + 46, y - 36, "ArialNarrow", 7, MUTED)
        for score in range(4):
            cx = PAGE_W - M - 124 + score * 31
            c.setStrokeColor(RED)
            c.setLineWidth(0.8)
            c.circle(cx, y - 24, 8, fill=0, stroke=1)
            R.text_center(c, str(score), cx, y - 27, "ArialNarrow-Bold", 6.6, RED)
        y -= 51
    section_rule(c, "Three decisions for the next pass", 185)
    decisions = [
        ("1", "DEPTH", "Which categories deserve a third page for tests, parts, or an expanded candidate field?"),
        ("2", "ART", "Which product families most need new observed-exterior or verified-construction plates?"),
        ("3", "SCOPE", "Should the commercial first edition include all 100 cases or a smaller fully verified volume?"),
    ]
    w = (PAGE_W - 2 * M - 16) / 3
    for i, (num, label, body) in enumerate(decisions):
        x = M + i * (w + 8)
        card(c, x, 156, w, 93, f"{num} / {label}", body, PAPER_DARK, RED)
    book.finish()


def build_end_matter(book: Book) -> None:
    maintenance_index_pages(book)
    service_audit_pages(book)
    source_ledger_pages(book)
    image_ledger_pages(book)
    research_queue_page(book)
    change_log_page(book)
    full_review_page(book)


def build() -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    book = Book(OUTPUT_PATH)
    draw_cover(book)
    build_front_matter(book)
    build_domain_content(book)
    build_end_matter(book)
    if book.page_no != FINAL_PAGE:
        raise RuntimeError(f"Page-plan mismatch: built {book.page_no}, expected {FINAL_PAGE}")
    book.save()
    print(OUTPUT_PATH)
    print(f"pages={book.page_no}")
    return OUTPUT_PATH


if __name__ == "__main__":
    build()
