#!/usr/bin/env python3
"""Build the Platonic Ideal three-product dossier review edition."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Sequence
from xml.sax.saxutils import escape

from PIL import Image, ImageEnhance, ImageOps
from reportlab.lib.colors import Color, HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "docs" / "dossier-review" / "assets"
TMP_DIR = ROOT / "tmp" / "pdfs" / "dossier-review"
OUTPUT_DIR = ROOT / "output" / "pdf"
OUTPUT_PATH = OUTPUT_DIR / "platonic-ideal-three-product-review.pdf"

PAGE_W, PAGE_H = LETTER
M = 36

PAPER = HexColor("#F3EBDD")
PAPER_DARK = HexColor("#E4D7C1")
INK = HexColor("#211F1B")
MUTED = HexColor("#6C665D")
RULE = HexColor("#C6B9A5")
RED = HexColor("#B43A2B")
RED_PALE = HexColor("#EAD0C7")
BLUE = HexColor("#244A63")
BLUE_PALE = HexColor("#D4E0E6")
TEAL = HexColor("#286C70")
TEAL_PALE = HexColor("#D3E4E1")
GREEN = HexColor("#536B50")
GREEN_PALE = HexColor("#DAE4D6")
GOLD = HexColor("#9B7431")
WHITE_WASH = Color(1, 1, 1, alpha=0.58)


def register_fonts() -> None:
    font_root = Path("/System/Library/Fonts/Supplemental")
    faces = {
        "Georgia": "Georgia.ttf",
        "Georgia-Bold": "Georgia Bold.ttf",
        "Georgia-Italic": "Georgia Italic.ttf",
        "Georgia-BoldItalic": "Georgia Bold Italic.ttf",
        "Arial": "Arial.ttf",
        "Arial-Bold": "Arial Bold.ttf",
        "Arial-Italic": "Arial Italic.ttf",
        "ArialNarrow": "Arial Narrow.ttf",
        "ArialNarrow-Bold": "Arial Narrow Bold.ttf",
    }
    for name, filename in faces.items():
        pdfmetrics.registerFont(TTFont(name, str(font_root / filename)))


register_fonts()


STYLES = {
    "body": ParagraphStyle(
        "body",
        fontName="Georgia",
        fontSize=9.2,
        leading=12.3,
        textColor=INK,
        spaceAfter=0,
    ),
    "body_small": ParagraphStyle(
        "body_small",
        fontName="Georgia",
        fontSize=7.9,
        leading=10.6,
        textColor=INK,
        spaceAfter=0,
    ),
    "caption": ParagraphStyle(
        "caption",
        fontName="ArialNarrow",
        fontSize=7.2,
        leading=8.8,
        textColor=MUTED,
    ),
    "caption_bold": ParagraphStyle(
        "caption_bold",
        fontName="ArialNarrow-Bold",
        fontSize=7.2,
        leading=8.8,
        textColor=INK,
    ),
    "table": ParagraphStyle(
        "table",
        fontName="ArialNarrow",
        fontSize=7.2,
        leading=8.7,
        textColor=INK,
    ),
    "table_bold": ParagraphStyle(
        "table_bold",
        fontName="ArialNarrow-Bold",
        fontSize=7.2,
        leading=8.7,
        textColor=INK,
    ),
    "table_header": ParagraphStyle(
        "table_header",
        fontName="ArialNarrow-Bold",
        fontSize=7.2,
        leading=8.7,
        textColor=white,
    ),
    "source": ParagraphStyle(
        "source",
        fontName="ArialNarrow",
        fontSize=6.7,
        leading=8.2,
        textColor=INK,
    ),
    "source_link": ParagraphStyle(
        "source_link",
        fontName="ArialNarrow",
        fontSize=6.4,
        leading=7.8,
        textColor=BLUE,
    ),
    "center_small": ParagraphStyle(
        "center_small",
        fontName="ArialNarrow",
        fontSize=7.3,
        leading=9,
        alignment=TA_CENTER,
        textColor=INK,
    ),
}


SOURCES = {
    "S1": (
        "Lodge L10SK3 12-inch skillet: identity, price, dimensions, care, finish, origin",
        "https://www.lodgecastiron.com/products/round-cast-iron-classic-skillet?variant=51685752242548",
    ),
    "S2": (
        "Victoria traditional 12-inch skillet: price, dimensions, weight, finish, origin",
        "https://victoriacookware.com/products/12-skillet",
    ),
    "S3": (
        "Field Company No.10 skillet: price, dimensions, weight, surface, origin",
        "https://fieldcompany.com/products/no-10-cast-iron-skillet",
    ),
    "S4": (
        "Stargazer 12-inch skillet: price, dimensions, weight, surface, origin",
        "https://stargazercastiron.com/products/12-inch-cast-iron-skillet",
    ),
    "S5": (
        "Estwing E3-16C: forged one-piece construction, molded grip, length, head weight, origin",
        "https://www.estwing.com/product/claw-hammer/",
    ),
    "S6": (
        "DeWalt DWHT51002: 16-ounce curved claw, one-piece steel construction, feature set",
        "https://www.dewalt.com/en-us/product/dwht51002/16-oz-curved-claw-steel-hammer",
    ),
    "S7": (
        "Stanley 51-162: forged one-piece steel, Anti-Vibe handle, length, curved claw",
        "https://www.stanleytools.com/product/51-162/16-oz-xtreme-claw-hammer",
    ),
    "S8": (
        "Stiletto TIB14RMC: titanium construction, replaceable grip and face, dimensions, warranty",
        "https://www.stiletto.com/14oz-tibone-milled-curved-titanium",
    ),
    "S9": (
        "Makita 6302H: current model page, specifications, included accessories, warranty",
        "https://makitatools.com/products/details/6302H",
    ),
    "S10": (
        "Makita 6302H instruction manual: operation and safety documentation",
        "https://cdn.makitatools.com/apps/cms/doc/prod/630/754466c3-a9fa-4c16-9a99-014d3dfc2fdf_6302H_IM.pdf",
    ),
    "S11": (
        "Makita 6302H illustrated parts breakdown: service structure reference",
        "https://cdn.makitatools.com/apps/cms/doc/prod/630/a0fea8d2-c31f-4810-ab22-a2ff5e3ecc98_6302H_PB.pdf",
    ),
    "S12": (
        "Makita DP4000: specifications, accessible brushes, bearing construction",
        "https://makitatools.com/products/details/DP4000",
    ),
    "S13": (
        "DeWalt DWD210G: specifications, metal gear housing, warranty",
        "https://www.dewalt.com/en-us/product/dwd210g/12-13mm-vsr-pistol-grip-drill",
    ),
    "S14": (
        "Milwaukee 0299-20: specifications and discontinued status",
        "https://www.milwaukeetool.com/products/details/1-2-magnum-drill-0-850-rpm/0299-20",
    ),
    "S15": (
        "Plato portrait, Altes Museum, Berlin, photograph by Osama Shukir Muhammed Amin",
        "https://commons.wikimedia.org/wiki/File:Marble_bust_of_the_Greek_philosopher_Plato._Roman_copy_(1st_century_CE)_of_an_original_(350-340_BCE)._Altes_Museum,_Berlin.jpg",
    ),
    "S16": (
        "Creative Commons Attribution-ShareAlike 4.0 license",
        "https://creativecommons.org/licenses/by-sa/4.0/",
    ),
    "S17": (
        "Plato, The Republic, Benjamin Jowett translation, Project Gutenberg eBook 55201",
        "https://www.gutenberg.org/ebooks/55201",
    ),
}


def set_fill(c: canvas.Canvas, color) -> None:
    c.setFillColor(color)


def set_stroke(c: canvas.Canvas, color, width: float = 1) -> None:
    c.setStrokeColor(color)
    c.setLineWidth(width)


def text(c: canvas.Canvas, value: str, x: float, y: float, font: str, size: float, color=INK) -> None:
    c.setFont(font, size)
    c.setFillColor(color)
    c.drawString(x, y, value)


def text_right(c: canvas.Canvas, value: str, x: float, y: float, font: str, size: float, color=INK) -> None:
    c.setFont(font, size)
    c.setFillColor(color)
    c.drawRightString(x, y, value)


def text_center(c: canvas.Canvas, value: str, x: float, y: float, font: str, size: float, color=INK) -> None:
    c.setFont(font, size)
    c.setFillColor(color)
    c.drawCentredString(x, y, value)


def paragraph(
    c: canvas.Canvas,
    value: str,
    x: float,
    y_top: float,
    width: float,
    style: str = "body",
    max_height: float = 1000,
) -> float:
    p = Paragraph(value, STYLES[style])
    _, h = p.wrap(width, max_height)
    p.drawOn(c, x, y_top - h)
    return y_top - h


def block_title(c: canvas.Canvas, label: str, x: float, y: float, width: float, color=RED) -> None:
    text(c, label.upper(), x, y, "ArialNarrow-Bold", 9, color)
    set_stroke(c, color, 1.2)
    c.line(x, y - 5, x + width, y - 5)


def tag(c: canvas.Canvas, value: str, x: float, y: float, fill=RED, fg=white, width: float | None = None) -> float:
    c.setFont("ArialNarrow-Bold", 8)
    w = width or max(54, c.stringWidth(value.upper(), "ArialNarrow-Bold", 8) + 18)
    c.setFillColor(fill)
    c.roundRect(x, y - 13, w, 17, 2.5, fill=1, stroke=0)
    text_center(c, value.upper(), x + w / 2, y - 8.5, "ArialNarrow-Bold", 8, fg)
    return w


def page_base(c: canvas.Canvas, page_no: int, section: str) -> None:
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    text(c, "THE PLATONIC IDEAL", M, PAGE_H - 26, "ArialNarrow-Bold", 8.2, INK)
    text_right(c, section.upper(), PAGE_W - M, PAGE_H - 26, "ArialNarrow", 8.2, MUTED)
    set_stroke(c, RULE, 0.8)
    c.line(M, PAGE_H - 32, PAGE_W - M, PAGE_H - 32)
    text(c, "REVIEW EDITION 01 / 15 SEP 2026", M, 19, "ArialNarrow", 6.8, MUTED)
    text_right(c, f"{page_no:02d}", PAGE_W - M, 19, "ArialNarrow-Bold", 7.2, INK)
    c.line(M, 28, PAGE_W - M, 28)


def page_title(c: canvas.Canvas, kicker: str, title: str, deck: str | None = None) -> float:
    text(c, kicker.upper(), M, PAGE_H - 59, "ArialNarrow-Bold", 9, RED)
    text(c, title, M, PAGE_H - 91, "Georgia-Bold", 27, INK)
    y = PAGE_H - 112
    if deck:
        y = paragraph(c, deck, M, y, PAGE_W - 2 * M, "body_small")
    return y


def metric(c: canvas.Canvas, x: float, y: float, width: float, value: str, label: str, fill=PAPER_DARK) -> None:
    c.setFillColor(fill)
    c.roundRect(x, y - 49, width, 49, 3, fill=1, stroke=0)
    text(c, value, x + 9, y - 22, "Georgia-Bold", 13, INK)
    text(c, label.upper(), x + 9, y - 38, "ArialNarrow", 6.8, MUTED)


def score_bar(c: canvas.Canvas, x: float, y: float, label: str, score: int, color=RED, width: float = 132) -> None:
    text(c, label.upper(), x, y + 3, "ArialNarrow-Bold", 7.2, INK)
    bar_x = x + 59
    seg_w = (width - 59 - 8) / 3
    for i in range(3):
        c.setFillColor(color if i < score else RULE)
        c.rect(bar_x + i * (seg_w + 4), y, seg_w, 7, fill=1, stroke=0)
    text_right(c, f"{score}/3", x + width, y + 1, "ArialNarrow-Bold", 6.8, color)


def callout_card(
    c: canvas.Canvas,
    number: str,
    title_value: str,
    body: str,
    x: float,
    y_top: float,
    width: float,
    height: float,
    color=RED,
) -> None:
    c.setFillColor(WHITE_WASH)
    c.setStrokeColor(RULE)
    c.setLineWidth(0.6)
    c.roundRect(x, y_top - height, width, height, 3, fill=1, stroke=1)
    c.setFillColor(color)
    c.circle(x + 15, y_top - 17, 9, fill=1, stroke=0)
    text_center(c, number, x + 15, y_top - 20.2, "ArialNarrow-Bold", 7.5, white)
    text(c, title_value.upper(), x + 29, y_top - 18.5, "ArialNarrow-Bold", 7.6, color)
    paragraph(c, body, x + 10, y_top - 31, width - 20, "caption")


def draw_contain(c: canvas.Canvas, path: Path, x: float, y: float, width: float, height: float) -> None:
    with Image.open(path) as im:
        iw, ih = im.size
    scale = min(width / iw, height / ih)
    dw, dh = iw * scale, ih * scale
    c.drawImage(ImageReader(str(path)), x + (width - dw) / 2, y + (height - dh) / 2, dw, dh, mask="auto")


def draw_cover_crop(c: canvas.Canvas, path: Path, x: float, y: float, width: float, height: float) -> None:
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    temp_path = TMP_DIR / "plato-cover-tinted.jpg"
    if not temp_path.exists():
        with Image.open(path) as source:
            image = ImageOps.fit(source.convert("RGB"), (1100, 1600), method=Image.Resampling.LANCZOS, centering=(0.48, 0.42))
            gray = ImageOps.grayscale(image)
            gray = ImageEnhance.Contrast(gray).enhance(1.18)
            tinted = ImageOps.colorize(gray, black="#1E211F", white="#DCCAA8")
            tinted.save(temp_path, quality=92, optimize=True)
    c.drawImage(ImageReader(str(temp_path)), x, y, width, height, mask="auto")


def draw_table(
    c: canvas.Canvas,
    x: float,
    y_top: float,
    widths: Sequence[float],
    headers: Sequence[str],
    rows: Sequence[Sequence[str]],
    row_heights: Sequence[float] | None = None,
    header_height: float = 24,
    accent=RED,
) -> float:
    total_width = sum(widths)
    c.setFillColor(accent)
    c.rect(x, y_top - header_height, total_width, header_height, fill=1, stroke=0)
    current_x = x
    for width, header in zip(widths, headers):
        paragraph(c, f"<b>{escape(header.upper())}</b>", current_x + 6, y_top - 7, width - 12, "table_header", 20)
        current_x += width
    y = y_top - header_height
    heights = list(row_heights) if row_heights else [38] * len(rows)
    for row_index, (row, height) in enumerate(zip(rows, heights)):
        c.setFillColor(WHITE_WASH if row_index % 2 == 0 else PAPER_DARK)
        c.rect(x, y - height, total_width, height, fill=1, stroke=0)
        current_x = x
        for column_index, (width, cell) in enumerate(zip(widths, row)):
            style = "table_bold" if column_index == 0 else "table"
            paragraph(c, cell, current_x + 6, y - 7, width - 12, style, height - 10)
            if column_index:
                set_stroke(c, RULE, 0.45)
                c.line(current_x, y, current_x, y - height)
            current_x += width
        set_stroke(c, RULE, 0.45)
        c.line(x, y - height, x + total_width, y - height)
        y -= height
    c.setStrokeColor(RULE)
    c.setLineWidth(0.55)
    c.rect(x, y, total_width, y_top - y, fill=0, stroke=1)
    return y


def source_note(c: canvas.Canvas, refs: str, x: float, y: float, width: float) -> None:
    paragraph(c, f"<b>Evidence:</b> {escape(refs)}. Prices and availability are snapshots accessed 15 Sep 2026.", x, y, width, "caption")


def cover_page(c: canvas.Canvas) -> None:
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    left_w = 248
    draw_cover_crop(c, ROOT / "public" / "images" / "plato-silanion-berlin.webp", 0, 0, left_w, PAGE_H)
    c.setFillColor(Color(0.08, 0.08, 0.07, alpha=0.13))
    c.rect(0, 0, left_w, PAGE_H, fill=1, stroke=0)
    c.setFillColor(RED)
    c.rect(left_w - 8, 0, 8, PAGE_H, fill=1, stroke=0)

    text(c, "PLATONIC IDEAL", left_w + 34, PAGE_H - 62, "ArialNarrow-Bold", 10.5, RED)
    text(c, "THE", left_w + 34, PAGE_H - 120, "Georgia-Bold", 22, INK)
    text(c, "DOSSIER", left_w + 34, PAGE_H - 159, "Georgia-Bold", 34, INK)
    text(c, "REVIEW EDITION 01", left_w + 34, PAGE_H - 184, "ArialNarrow-Bold", 10, MUTED)

    paragraph(
        c,
        "<b>Three declarations under test.</b><br/>A cast-iron skillet, a forged-steel hammer, and a corded drill examined as products, ownership systems, and decisions that should end a search.",
        left_w + 34,
        PAGE_H - 229,
        PAGE_W - left_w - 66,
        "body",
    )

    set_stroke(c, RULE, 0.9)
    c.line(left_w + 34, PAGE_H - 329, PAGE_W - 34, PAGE_H - 329)
    items = [
        ("01", "FRYING PAN", "Lodge L10SK3"),
        ("02", "CLAW HAMMER", "Estwing E3-16C"),
        ("03", "CORDED DRILL", "Makita 6302H"),
    ]
    y = PAGE_H - 370
    for num, category, model in items:
        text(c, num, left_w + 34, y, "Georgia-Bold", 15, RED)
        text(c, category, left_w + 72, y + 2, "ArialNarrow-Bold", 8.2, MUTED)
        text(c, model, left_w + 72, y - 15, "Georgia-Bold", 11.6, INK)
        y -= 67

    c.setFillColor(PAPER_DARK)
    c.roundRect(left_w + 34, 91, PAGE_W - left_w - 68, 106, 4, fill=1, stroke=0)
    text(c, '"The many, as we say,', left_w + 49, 161, "Georgia-Italic", 11, INK)
    text(c, 'are seen but not known."', left_w + 49, 142, "Georgia-Italic", 11, INK)
    text(c, "PLATO / THE REPUBLIC / VI.507B [S17]", left_w + 49, 116, "ArialNarrow-Bold", 7.3, RED)

    text(c, "EVIDENCE-LED BUYING GUIDE", left_w + 34, 52, "ArialNarrow-Bold", 8.4, INK)
    text(c, "Prototype spreads / 15 September 2026", left_w + 34, 36, "ArialNarrow", 7.5, MUTED)
    text(c, "Plato portrait: CC BY-SA 4.0 [S15-S16]", 20, 18, "ArialNarrow", 6.5, PAPER)
    c.showPage()


def method_page(c: canvas.Canvas) -> None:
    page_base(c, 2, "How to read the dossier")
    page_title(
        c,
        "Reader's key",
        "A ruling you can audit.",
        "Each spread separates what a source proves, what the editor infers, and what still needs testing. The labels are part of the product, not legal residue.",
    )

    block_title(c, "Ruling states", M, 640, PAGE_W - 2 * M)
    states = [
        ("DECLARED", "The model clears the category threshold with current identity and fit evidence.", GREEN, GREEN_PALE),
        ("PROVISIONAL", "The model fits the job, but a material evidence or ownership question remains open.", GOLD, PAPER_DARK),
        ("HOLD", "The category or model is too ambiguous to close the search responsibly.", RED, RED_PALE),
    ]
    card_w = (PAGE_W - 2 * M - 20) / 3
    for i, (name, body, color, pale) in enumerate(states):
        x = M + i * (card_w + 10)
        c.setFillColor(pale)
        c.roundRect(x, 516, card_w, 98, 4, fill=1, stroke=0)
        tag(c, name, x + 11, 596, fill=color, width=78)
        paragraph(c, body, x + 11, 565, card_w - 22, "body_small")

    block_title(c, "Six tests before a declaration", M, 486, PAGE_W - 2 * M)
    tests = [
        ("01", "FIT", "Does it solve the normal job without a specialist exception?"),
        ("02", "FORM", "Does the construction remove avoidable joints, coatings, or dependencies?"),
        ("03", "RECOVERY", "Can ordinary wear be cleaned, sharpened, reseasoned, or replaced?"),
        ("04", "SUPPLY", "Are the model, consumables, service, and documentation still obtainable?"),
        ("05", "OWNERSHIP", "Are maintenance, storage, and failure modes legible before purchase?"),
        ("06", "VALUE", "Does the extra cost buy a useful property instead of ornament or churn?"),
    ]
    grid_y = 456
    for i, (num, name, body) in enumerate(tests):
        col = i % 2
        row = i // 2
        x = M + col * 274
        y = grid_y - row * 66
        c.setFillColor(RED)
        c.circle(x + 12, y - 9, 10, fill=1, stroke=0)
        text_center(c, num, x + 12, y - 12, "ArialNarrow-Bold", 7, white)
        text(c, name, x + 30, y - 4, "ArialNarrow-Bold", 8.2, INK)
        paragraph(c, body, x + 30, y - 15, 225, "caption")

    block_title(c, "Image truth", M, 250, PAGE_W - 2 * M)
    truths = [
        ("OBSERVED EXTERIOR", "Visible geometry checked against a manufacturer identity page."),
        ("VERIFIED CONSTRUCTION", "A cited source directly states the material or construction."),
        ("CONCEPTUAL MECHANISM", "The illustration explains a relationship and is not an engineering drawing."),
    ]
    for i, (label, body) in enumerate(truths):
        x = M + i * (card_w + 10)
        c.setStrokeColor(RULE)
        c.setLineWidth(0.65)
        c.roundRect(x, 145, card_w, 79, 3, fill=0, stroke=1)
        text(c, label, x + 9, 204, "ArialNarrow-Bold", 7.5, RED)
        paragraph(c, body, x + 9, 188, card_w - 18, "caption")

    c.setFillColor(INK)
    c.rect(M, 53, PAGE_W - 2 * M, 62, fill=1, stroke=0)
    paragraph(
        c,
        '<font color="#F3EBDD"><b>Confidence is specific.</b> Identity can be 3/3 while serviceability is 1/3. A low score is not hidden by a single aggregate number.</font>',
        M + 15,
        96,
        PAGE_W - 2 * M - 30,
        "body_small",
    )
    c.showPage()


def lodge_identity_page(c: canvas.Canvas) -> None:
    page_base(c, 3, "01 / Frying pan")
    text(c, "DECLARATION 01", M, PAGE_H - 59, "ArialNarrow-Bold", 9, RED)
    text(c, "Lodge L10SK3", M, PAGE_H - 91, "Georgia-Bold", 28, INK)
    text(c, "12-inch seasoned cast-iron skillet", M, PAGE_H - 113, "Georgia-Italic", 11.5, MUTED)
    tag(c, "Declared", PAGE_W - M - 77, PAGE_H - 67, fill=GREEN, width=77)

    c.setFillColor(PAPER_DARK)
    c.roundRect(M, 608, PAGE_W - 2 * M, 48, 3, fill=1, stroke=0)
    paragraph(
        c,
        "<b>The default 12-inch cast-iron skillet when utility per dollar matters more than low weight or a machined cooking surface.</b>",
        M + 13,
        643,
        PAGE_W - 2 * M - 26,
        "body",
    )

    c.setFillColor(WHITE_WASH)
    c.roundRect(M, 289, PAGE_W - 2 * M, 300, 4, fill=1, stroke=0)
    draw_contain(c, ASSET_DIR / "lodge-l10sk3-technical-plate.png", M + 8, 297, PAGE_W - 2 * M - 16, 284)
    tag(c, "Observed exterior", M + 10, 578, fill=RED, width=96)
    text_right(c, "ORIGINAL EDITORIAL PLATE / NOT PRODUCT PHOTOGRAPHY", PAGE_W - M - 10, 571, "ArialNarrow", 6.5, MUTED)

    gap = 8
    metrics_y = 270
    mw = (PAGE_W - 2 * M - gap * 3) / 4
    metric(c, M, metrics_y, mw, "18 x 12.56 in", "overall length x width")
    metric(c, M + (mw + gap), metrics_y, mw, "7.69 lb", "manufacturer weight")
    metric(c, M + 2 * (mw + gap), metrics_y, mw, "9.12 in", "flat-bottom width")
    metric(c, M + 3 * (mw + gap), metrics_y, mw, "$29.90", "sale snapshot / $37.95 regular", GREEN_PALE)

    card_w = (PAGE_W - 2 * M - 16) / 3
    callout_card(c, "1", "One cast body", "Bowl, long handle, and assist handle are visually continuous. No fastener is required to hold the pan together.", M, 204, card_w, 77)
    callout_card(c, "2", "Recoverable surface", "The cooking surface is seasoned with vegetable oil. Lodge directs owners to hand wash, dry, and oil it. [S1]", M + card_w + 8, 204, card_w, 77)
    callout_card(c, "3", "Broad heat fit", "The manufacturer lists stovetop, induction, oven, grill, and campfire compatibility. [S1]", M + 2 * (card_w + 8), 204, card_w, 77)

    score_bar(c, M, 98, "Identity", 3, GREEN, 138)
    score_bar(c, M + 170, 98, "Category fit", 3, GREEN, 138)
    score_bar(c, M + 340, 98, "Ownership", 3, GREEN, 138)
    source_note(c, "[S1]", M, 77, PAGE_W - 2 * M)
    c.showPage()


def lodge_ownership_page(c: canvas.Canvas) -> None:
    page_base(c, 4, "01 / Ownership brief")
    page_title(c, "Lodge L10SK3", "The pan is a maintenance loop.", "Its value comes from a recoverable surface and a body with almost nothing to loosen. The cost is weight, care, and slower response.")

    block_title(c, "Four-step care cycle", M, 632, PAGE_W - 2 * M)
    steps = [
        ("01", "COOK", "Preheat gradually. Use enough fat for the food and surface condition."),
        ("02", "WASH", "Hand wash. Remove residue without leaving the pan soaking."),
        ("03", "DRY", "Dry fully; brief stovetop heat can remove residual moisture."),
        ("04", "OIL", "Wipe on a very thin film before dry storage."),
    ]
    step_w = (PAGE_W - 2 * M - 24) / 4
    for i, (num, name, body) in enumerate(steps):
        x = M + i * (step_w + 8)
        c.setFillColor(WHITE_WASH)
        c.roundRect(x, 514, step_w, 92, 4, fill=1, stroke=0)
        text(c, num, x + 9, 584, "Georgia-Bold", 14, RED)
        text(c, name, x + 38, 586, "ArialNarrow-Bold", 7.8, INK)
        paragraph(c, body, x + 9, 566, step_w - 18, "caption")

    block_title(c, "Failure map", M, 486, PAGE_W - 2 * M)
    failures = [
        ("SURFACE RUST", "Usually recoverable", "Remove rust, dry, and rebuild seasoning. Severity depends on depth."),
        ("SEASONING LOSS", "Recoverable", "Clean back to a sound layer and reseason. This is maintenance, not end of life."),
        ("CRACK / MAJOR WARP", "Terminal for normal ownership", "Retire damaged cookware. The reviewed source does not quantify likelihood."),
    ]
    for i, (name, status, body) in enumerate(failures):
        x = M + i * (card_w := (PAGE_W - 2 * M - 16) / 3) + i * 8
        c.setFillColor(RED_PALE if i == 2 else PAPER_DARK)
        c.roundRect(x, 393, card_w, 66, 3, fill=1, stroke=0)
        text(c, name, x + 9, 441, "ArialNarrow-Bold", 7.6, RED if i == 2 else INK)
        text(c, status, x + 9, 427, "Georgia-Bold", 8.4, INK)
        paragraph(c, body, x + 9, 414, card_w - 18, "caption")

    block_title(c, "Candidate field", M, 365, PAGE_W - 2 * M)
    rows = [
        ["Lodge L10SK3", "$29.90 sale<br/>$37.95 regular", "7.69 lb", "12.56 in overall<br/>9.12 in flat bottom", "Value baseline; broad heat fit"],
        ["Victoria Traditional 12", "$37.49", "6.7 lb", "13.3 in overall<br/>extra-deep form", "Lower weight near the same price"],
        ["Field No.10", "$215", "6.0 lb", "11.625 in rim<br/>9.75 in cooking", "Machined surface; lighter premium"],
        ["Stargazer 12", "$175", "6.5 lb", "12 in rim<br/>9.4 in cooking", "Machined surface; flared rim"],
    ]
    y = draw_table(
        c,
        M,
        344,
        [104, 74, 54, 112, 196],
        ["Model", "Price snapshot", "Weight", "Working dimensions", "Why it remains"],
        rows,
        [42, 42, 42, 42],
        accent=RED,
    )

    c.setFillColor(INK)
    c.roundRect(M, y - 83, PAGE_W - 2 * M, 68, 3, fill=1, stroke=0)
    paragraph(
        c,
        '<font color="#F3EBDD"><b>Editorial ruling:</b> Lodge wins the broad-use value test. Field and Stargazer buy lower weight and a machined surface; Victoria is the closest price competitor. Those are real upgrades, but none make the Lodge unable to do the job.</font>',
        M + 13,
        y - 31,
        PAGE_W - 2 * M - 26,
        "body_small",
    )
    source_note(c, "[S1-S4]", M, 46, PAGE_W - 2 * M)
    c.showPage()


def hammer_identity_page(c: canvas.Canvas) -> None:
    page_base(c, 5, "02 / Claw hammer")
    text(c, "DECLARATION 02", M, PAGE_H - 59, "ArialNarrow-Bold", 9, RED)
    text(c, "Estwing E3-16C", M, PAGE_H - 91, "Georgia-Bold", 28, INK)
    text(c, "16-ounce curved-claw solid-steel hammer", M, PAGE_H - 113, "Georgia-Italic", 11.5, MUTED)
    tag(c, "Declared", PAGE_W - M - 77, PAGE_H - 67, fill=GREEN, width=77)

    c.setFillColor(BLUE_PALE)
    c.roundRect(M, 608, PAGE_W - 2 * M, 48, 3, fill=1, stroke=0)
    paragraph(
        c,
        "<b>The compact general-purpose claw hammer for buyers who value a continuous steel core and a 13-inch working length.</b>",
        M + 13,
        643,
        PAGE_W - 2 * M - 26,
        "body",
    )

    c.setFillColor(WHITE_WASH)
    c.roundRect(M, 289, PAGE_W - 2 * M, 300, 4, fill=1, stroke=0)
    draw_contain(c, ASSET_DIR / "estwing-e3-16c-technical-plate.png", M + 8, 297, PAGE_W - 2 * M - 16, 284)
    tag(c, "Observed exterior", M + 10, 578, fill=RED, width=96)
    tag(c, "Conceptual grip section", M + 114, 578, fill=BLUE, width=118)
    text_right(c, "ORIGINAL EDITORIAL PLATE / NOT PRODUCT PHOTOGRAPHY", PAGE_W - M - 10, 571, "ArialNarrow", 6.5, MUTED)

    gap = 8
    mw = (PAGE_W - 2 * M - gap * 3) / 4
    metric(c, M, 270, mw, "16 oz", "head weight")
    metric(c, M + (mw + gap), 270, mw, "13 in", "overall length")
    metric(c, M + 2 * (mw + gap), 270, mw, "1 piece", "head + handle forging")
    metric(c, M + 3 * (mw + gap), 270, mw, "Smooth", "striking face", BLUE_PALE)

    card_w = (PAGE_W - 2 * M - 16) / 3
    callout_card(c, "1", "Joint removed", "Estwing states that the head and handle are forged in one piece. The common head-to-handle joint does not exist. [S5]", M, 204, card_w, 77, BLUE)
    callout_card(c, "2", "Molded grip", "The blue shock-reduction grip is molded onto the steel handle. Vibration reduction is a manufacturer claim. [S5]", M + card_w + 8, 204, card_w, 77, BLUE)
    callout_card(c, "3", "General geometry", "A smooth face and curved claw suit ordinary driving and pulling. It is not a long framing hammer. [S5]", M + 2 * (card_w + 8), 204, card_w, 77, BLUE)

    score_bar(c, M, 98, "Identity", 3, GREEN, 138)
    score_bar(c, M + 170, 98, "Category fit", 3, GREEN, 138)
    score_bar(c, M + 340, 98, "Ownership", 2, GOLD, 138)
    source_note(c, "[S5]", M, 77, PAGE_W - 2 * M)
    c.showPage()


def hammer_ownership_page(c: canvas.Canvas) -> None:
    page_base(c, 6, "02 / Ownership brief")
    page_title(c, "Estwing E3-16C", "The core is simple.", "The one-piece steel body removes the most familiar hammer joint. The grip is the ownership question: it improves use, yet the reviewed manufacturer page does not establish a replacement path.")

    block_title(c, "Construction and wear", M, 628, PAGE_W - 2 * M)
    path_items = [
        ("FORGED STEEL CORE", "Verified", "Head and handle are one continuous forging. [S5]", GREEN_PALE),
        ("MOLDED BLUE GRIP", "Verified", "The grip is molded on. Replacement availability was not established in this review. [S5]", BLUE_PALE),
        ("FACE / CLAW DAMAGE", "Inspect", "Retire a tool with cracks, severe deformation, or unsafe striking surfaces." , RED_PALE),
    ]
    for i, (name, status, body, fill) in enumerate(path_items):
        x = M + i * (card_w := (PAGE_W - 2 * M - 16) / 3) + i * 8
        c.setFillColor(fill)
        c.roundRect(x, 509, card_w, 91, 4, fill=1, stroke=0)
        text(c, name, x + 10, 579, "ArialNarrow-Bold", 7.6, BLUE if i < 2 else RED)
        text(c, status, x + 10, 560, "Georgia-Bold", 9.2, INK)
        paragraph(c, body, x + 10, 545, card_w - 20, "caption")

    block_title(c, "Candidate field", M, 478, PAGE_W - 2 * M)
    rows = [
        ["Estwing E3-16C", "16 oz / 13 in", "One-piece steel", "Molded grip", "General carpentry baseline"],
        ["DeWalt DWHT51002", "16 oz / length not captured", "One-piece steel", "Magnetic start; side puller", "More extraction features"],
        ["Stanley 51-162", "16 oz / 13-1/8 in", "One-piece steel", "Anti-Vibe handle", "Closest direct alternative"],
        ["Stiletto TIB14RMC", "14 oz head / 15.2 in", "All-titanium body", "Replaceable face + grip", "Premium framing system"],
    ]
    y = draw_table(
        c,
        M,
        457,
        [104, 93, 92, 119, 132],
        ["Model", "Mass / length", "Core", "Wear strategy", "Reason to choose"],
        rows,
        [42, 45, 42, 45],
        accent=BLUE,
    )

    half = (PAGE_W - 2 * M - 10) / 2
    c.setFillColor(BLUE_PALE)
    c.roundRect(M, y - 92, half, 78, 3, fill=1, stroke=0)
    text(c, "WHY ESTWING REMAINS", M + 11, y - 34, "ArialNarrow-Bold", 8, BLUE)
    paragraph(c, "It is a compact, simple, verified general-purpose form. The declaration is about eliminating the head joint, not claiming zero wear.", M + 11, y - 46, half - 22, "body_small")

    c.setFillColor(PAPER_DARK)
    c.roundRect(M + half + 10, y - 92, half, 78, 3, fill=1, stroke=0)
    text(c, "WHEN TO PICK ANOTHER", M + half + 21, y - 34, "ArialNarrow-Bold", 8, RED)
    paragraph(c, "Choose Stiletto for a replaceable premium framing system. Choose a direct steel alternative when magnetic starting or a different grip matters more.", M + half + 21, y - 46, half - 22, "body_small")

    source_note(c, "[S5-S8]", M, 46, PAGE_W - 2 * M)
    c.showPage()


def drill_identity_page(c: canvas.Canvas) -> None:
    page_base(c, 7, "03 / Corded drill")
    text(c, "DECLARATION 03", M, PAGE_H - 59, "ArialNarrow-Bold", 9, RED)
    text(c, "Makita 6302H", M, PAGE_H - 91, "Georgia-Bold", 28, INK)
    text(c, "1/2-inch low-speed corded drill", M, PAGE_H - 113, "Georgia-Italic", 11.5, MUTED)
    tag(c, "Provisional", PAGE_W - M - 85, PAGE_H - 67, fill=GOLD, width=85)

    c.setFillColor(TEAL_PALE)
    c.roundRect(M, 608, PAGE_W - 2 * M, 48, 3, fill=1, stroke=0)
    paragraph(
        c,
        "<b>A durable-looking, battery-independent drilling platform with strong official documentation. The ownership verdict stays open until current service-part availability is verified.</b>",
        M + 13,
        643,
        PAGE_W - 2 * M - 26,
        "body",
    )

    c.setFillColor(WHITE_WASH)
    c.roundRect(M, 289, PAGE_W - 2 * M, 300, 4, fill=1, stroke=0)
    draw_contain(c, ASSET_DIR / "makita-6302h-technical-plate.png", M + 8, 297, PAGE_W - 2 * M - 16, 284)
    tag(c, "Observed exterior", M + 10, 578, fill=RED, width=96)
    tag(c, "Accessory system map", M + 114, 578, fill=TEAL, width=106)
    text_right(c, "ORIGINAL EDITORIAL PLATE / NOT PRODUCT PHOTOGRAPHY", PAGE_W - M - 10, 571, "ArialNarrow", 6.5, MUTED)

    gap = 8
    mw = (PAGE_W - 2 * M - gap * 3) / 4
    metric(c, M, 270, mw, "6.5 A", "motor")
    metric(c, M + (mw + gap), 270, mw, "0-550 rpm", "variable speed")
    metric(c, M + 2 * (mw + gap), 270, mw, "4.8 lb", "net weight")
    metric(c, M + 3 * (mw + gap), 270, mw, "11.25 in", "overall length", TEAL_PALE)

    card_w = (PAGE_W - 2 * M - 16) / 3
    callout_card(c, "1", "Metal front end", "Makita specifies an industrial metal gear housing and heavy-duty keyed 1/2-inch chuck. [S9]", M, 204, card_w, 77, TEAL)
    callout_card(c, "2", "Control hardware", "The official kit includes a side handle and chuck key; the handle can mount on either side. [S9]", M + card_w + 8, 204, card_w, 77, TEAL)
    callout_card(c, "3", "No battery layer", "Corded power removes battery-pack compatibility from the ownership system. It does not prove internal parts availability.", M + 2 * (card_w + 8), 204, card_w, 77, TEAL)

    score_bar(c, M, 98, "Identity", 3, GREEN, 138)
    score_bar(c, M + 170, 98, "Category fit", 2, GOLD, 138)
    score_bar(c, M + 340, 98, "Service proof", 1, RED, 138)
    source_note(c, "[S9-S11]", M, 77, PAGE_W - 2 * M)
    c.showPage()


def drill_ownership_page(c: canvas.Canvas) -> None:
    page_base(c, 8, "03 / Ownership brief")
    page_title(c, "Makita 6302H", "Documentation is not repairability.", "Makita publishes a manual and illustrated parts breakdown. That proves a service structure exists; it does not prove that every meaningful part remains stocked in the buyer's region.")

    block_title(c, "Conceptual system map", M, 625, PAGE_W - 2 * M)
    nodes = ["Mains power", "Trigger + reverse", "Motor", "Gear reduction", "Keyed chuck", "Bit + load"]
    node_w = 76
    gap = (PAGE_W - 2 * M - node_w * len(nodes)) / (len(nodes) - 1)
    x = M
    for i, node in enumerate(nodes):
        fill = TEAL_PALE if i not in (0, 5) else PAPER_DARK
        c.setFillColor(fill)
        c.roundRect(x, 557, node_w, 42, 3, fill=1, stroke=0)
        paragraph(c, node, x + 5, 585, node_w - 10, "center_small")
        if i < len(nodes) - 1:
            set_stroke(c, TEAL, 1.2)
            c.line(x + node_w + 3, 578, x + node_w + gap - 3, 578)
            c.line(x + node_w + gap - 7, 582, x + node_w + gap - 3, 578)
            c.line(x + node_w + gap - 7, 574, x + node_w + gap - 3, 578)
        x += node_w + gap
    text(c, "CONCEPTUAL MECHANISM / NOT AN ENGINEERING DRAWING", M, 545, "ArialNarrow", 6.5, MUTED)

    block_title(c, "Evidence gate", M, 516, PAGE_W - 2 * M)
    gates = [
        ("PASS", "Identity + specifications", "Exact model page, manual, capacities, speed, dimensions, weight, accessories. [S9-S10]", GREEN, GREEN_PALE),
        ("PASS", "Parts structure", "Makita publishes a two-page illustrated parts breakdown for model 6302H. [S11]", GREEN, GREEN_PALE),
        ("OPEN", "Parts availability", "Stock, substitutions, prices, and service-center support were not verified part by part.", RED, RED_PALE),
    ]
    for i, (state, label, body, color, pale) in enumerate(gates):
        x = M + i * (card_w := (PAGE_W - 2 * M - 16) / 3) + i * 8
        c.setFillColor(pale)
        c.roundRect(x, 421, card_w, 69, 3, fill=1, stroke=0)
        tag(c, state, x + 8, 480, fill=color, width=42)
        text(c, label.upper(), x + 57, 471, "ArialNarrow-Bold", 7.2, color)
        paragraph(c, body, x + 9, 454, card_w - 18, "caption")

    block_title(c, "Candidate field", M, 394, PAGE_W - 2 * M)
    rows = [
        ["Makita 6302H", "6.5 A", "0-550", "4.8 lb / 11.25 in", "Low-speed baseline; provisional"],
        ["Makita DP4000", "7 A", "0-950", "4.8 lb / 12 in", "Accessible brushes stated; strongest challenger"],
        ["DeWalt DWD210G", "10 A", "0-1250", "Not captured", "Higher-speed, higher-power alternative"],
        ["Milwaukee 0299-20", "8 A", "0-850", "Not captured", "Documented but discontinued"],
    ]
    y = draw_table(
        c,
        M,
        373,
        [108, 52, 63, 112, 205],
        ["Model", "Motor", "RPM", "Weight / length", "Editorial status"],
        rows,
        [39, 42, 42, 39],
        accent=TEAL,
    )

    c.setFillColor(INK)
    c.roundRect(M, y - 94, PAGE_W - 2 * M, 78, 3, fill=1, stroke=0)
    paragraph(
        c,
        '<font color="#F3EBDD"><b>Next proof before declaration:</b> Ask Makita to confirm current regional availability and substitution paths for the switch, cord, brush set, armature, field, gears, bearings, and chuck. Record price and lead time. If that evidence is weak, the DP4000 becomes the stronger candidate because its official page explicitly calls out accessible brushes.</font>',
        M + 13,
        y - 32,
        PAGE_W - 2 * M - 26,
        "body_small",
    )
    source_note(c, "[S9-S14]", M, 46, PAGE_W - 2 * M)
    c.showPage()


def source_entry(c: canvas.Canvas, key: str, x: float, y_top: float, width: float) -> float:
    title_value, url = SOURCES[key]
    text(c, key, x, y_top - 9, "ArialNarrow-Bold", 7.2, RED)
    y = paragraph(c, escape(title_value), x + 24, y_top, width - 24, "source")
    link_text = f'<link href="{escape(url)}" color="#244A63"><u>{escape(url)}</u></link>'
    y = paragraph(c, link_text, x + 24, y - 2, width - 24, "source_link")
    return y - 10


def sources_page(c: canvas.Canvas) -> None:
    page_base(c, 9, "Source ledger")
    page_title(c, "Evidence", "Primary sources, visible and dated.", "Every factual specification and price in this review edition resolves to the source below. Manufacturer marketing claims are identified as such in the spreads.")

    column_gap = 20
    column_w = (PAGE_W - 2 * M - column_gap) / 2
    left_keys = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S17"]
    right_keys = ["S9", "S10", "S11", "S12", "S13", "S14", "S15", "S16"]
    y_left = 625
    for key in left_keys:
        y_left = source_entry(c, key, M, y_left, column_w)
    y_right = 625
    for key in right_keys:
        y_right = source_entry(c, key, M + column_w + column_gap, y_right, column_w)

    c.setFillColor(PAPER_DARK)
    c.roundRect(M, 46, PAGE_W - 2 * M, 72, 3, fill=1, stroke=0)
    text(c, "SOURCE POLICY", M + 12, 97, "ArialNarrow-Bold", 8, RED)
    paragraph(
        c,
        "Accessed 15 Sep 2026. Prices are snapshots, not promises. Manufacturer product photos informed identity but are not reproduced. Exact-model service claims require documentation plus current availability evidence. The three technical plates are original AI-generated interpretations and are labeled accordingly.",
        M + 12,
        84,
        PAGE_W - 2 * M - 24,
        "body_small",
    )
    c.showPage()


def review_page(c: canvas.Canvas) -> None:
    page_base(c, 10, "Review sheet")
    page_title(c, "Editorial review", "Tell us what deserves another page.", "This prototype tests whether the final dossier feels authoritative, useful, and honest before the full catalog is expanded.")

    block_title(c, "Score the sample", M, 627, PAGE_W - 2 * M)
    criteria = [
        ("Decision clarity", "Can you explain why the winner won after one read?"),
        ("Evidence visibility", "Can you tell a source fact from an editorial inference?"),
        ("Ownership value", "Do care, failure, and service notes change the purchase decision?"),
        ("Comparison depth", "Are the alternatives specific enough to prevent another search?"),
        ("Visual truth", "Do the plates add understanding without pretending to be exact engineering drawings?"),
        ("Page density", "Does the spread feel rich without becoming tiring or cramped?"),
    ]
    y = 594
    for i, (label, question) in enumerate(criteria):
        c.setFillColor(WHITE_WASH if i % 2 == 0 else PAPER_DARK)
        c.rect(M, y - 44, PAGE_W - 2 * M, 44, fill=1, stroke=0)
        text(c, f"{i + 1:02d}", M + 10, y - 26, "Georgia-Bold", 11, RED)
        text(c, label.upper(), M + 40, y - 18, "ArialNarrow-Bold", 7.8, INK)
        text(c, question, M + 40, y - 33, "ArialNarrow", 7.4, MUTED)
        for score in range(4):
            cx = PAGE_W - M - 122 + score * 31
            c.setStrokeColor(RED)
            c.setLineWidth(0.8)
            c.circle(cx, y - 22, 8, fill=0, stroke=1)
            text_center(c, str(score), cx, y - 25, "ArialNarrow-Bold", 6.8, RED)
        y -= 47

    block_title(c, "Decisions this prototype exposes", M, 286, PAGE_W - 2 * M)
    decisions = [
        ("A", "PRICES", "Use exact dated snapshots, broader ranges, or both?"),
        ("B", "POWERED GOODS", "Require verified service parts before any final declaration?"),
        ("C", "SPREAD LENGTH", "Keep two pages per product or allow a third page for test data?"),
        ("D", "ALTERNATIVES", "Show three serious candidates or a wider field of six?"),
    ]
    half = (PAGE_W - 2 * M - 10) / 2
    for i, (letter, label, body) in enumerate(decisions):
        col, row = i % 2, i // 2
        x = M + col * (half + 10)
        top = 254 - row * 74
        c.setFillColor(PAPER_DARK)
        c.roundRect(x, top - 58, half, 58, 3, fill=1, stroke=0)
        c.setFillColor(RED)
        c.circle(x + 17, top - 19, 10, fill=1, stroke=0)
        text_center(c, letter, x + 17, top - 22.5, "ArialNarrow-Bold", 8, white)
        text(c, label, x + 35, top - 17, "ArialNarrow-Bold", 7.8, RED)
        paragraph(c, body, x + 35, top - 27, half - 45, "caption")

    c.setFillColor(INK)
    c.roundRect(M, 50, PAGE_W - 2 * M, 60, 3, fill=1, stroke=0)
    paragraph(
        c,
        '<font color="#F3EBDD"><b>Next production pass:</b> incorporate review notes, verify powered-tool service parts, add test protocols, then expand the design system across the first ten declarations.</font>',
        M + 14,
        91,
        PAGE_W - 2 * M - 28,
        "body_small",
    )
    c.showPage()


def build() -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUTPUT_PATH), pagesize=LETTER, pageCompression=1)
    c.setTitle("The Platonic Ideal - Three-Product Dossier Review Edition")
    c.setAuthor("Platonic Ideal")
    c.setSubject("Evidence-led review spreads for Lodge L10SK3, Estwing E3-16C, and Makita 6302H")
    c.setKeywords("buying guide, product dossier, cast iron skillet, claw hammer, corded drill")
    cover_page(c)
    method_page(c)
    lodge_identity_page(c)
    lodge_ownership_page(c)
    hammer_identity_page(c)
    hammer_ownership_page(c)
    drill_identity_page(c)
    drill_ownership_page(c)
    sources_page(c)
    review_page(c)
    c.save()
    return OUTPUT_PATH


if __name__ == "__main__":
    output = build()
    print(output)
