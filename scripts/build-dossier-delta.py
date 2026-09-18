#!/usr/bin/env python3
"""Build the Platonic Ideal dossier in the Delta 1940 editorial system.

The public site is intentionally not touched by this builder. It produces a
print-first HTML book and asks Chrome to print that book to a tagged PDF.
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import os
import re
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote

from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "public" / "platonic_ideal.csv"
SOURCE_PATH = ROOT / "src" / "data" / "image-source-inventory.json"
PRODUCT_IMAGE_ROOT = ROOT / "public" / "images" / "products"
ASSET_DIR = ROOT / "docs" / "dossier-review" / "assets"
TMP_DIR = ROOT / "tmp" / "pdfs" / "delta-1940"
OUTPUT_DIR = ROOT / "output" / "pdf"
DEFAULT_OUTPUT = OUTPUT_DIR / "platonic-ideal-dossier-full-review.pdf"
DECLARED_OUTPUT = OUTPUT_DIR / "platonic-ideal-dossier-declared-1940.pdf"
CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")


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
    "frying pan": "kitchen-cooking", "refrigerator": "household-systems",
    "hammer": "tools-workshop", "smartphone": "electronics",
    "kitchen knife": "kitchen-cooking", "washing machine": "household-systems",
    "saucepan": "kitchen-cooking", "screwdriver": "tools-workshop",
    "dutch oven": "kitchen-cooking", "laptop": "electronics",
    "coffee maker": "kitchen-cooking", "drill": "tools-workshop",
    "kettle": "kitchen-cooking", "task chair": "furniture-work",
    "toaster": "kitchen-cooking", "backpack": "outdoor-utility",
    "mattress": "household-systems", "hand saw": "tools-workshop",
    "desk": "furniture-work", "boots": "clothing-carry",
    "oven/range": "kitchen-cooking", "belt": "clothing-carry",
    "freezer": "household-systems", "adjustable wrench": "tools-workshop",
    "t-shirt": "clothing-carry", "jeans": "clothing-carry",
    "jacket/coat": "clothing-carry", "chisel": "tools-workshop",
    "pliers": "tools-workshop", "tape measure": "tools-workshop",
    "tent": "outdoor-utility", "sleeping bag": "outdoor-utility",
    "water bottle": "outdoor-utility", "flashlight": "outdoor-utility",
    "sweater": "clothing-carry", "cooler": "outdoor-utility",
    "pocket knife": "outdoor-utility", "notebook": "writing-office",
    "pen": "writing-office", "cutting board": "kitchen-cooking",
    "vacuum cleaner": "household-systems", "bicycle": "outdoor-utility",
    "dining chair": "furniture-work", "printer": "electronics",
    "socks": "clothing-carry", "watch": "personal-care-misc",
    "shoes": "clothing-carry", "food storage container": "kitchen-cooking",
    "level": "tools-workshop", "drill bits": "tools-workshop",
    "extension cord": "tools-workshop", "camping stove": "outdoor-utility",
    "mechanical pencil": "writing-office", "umbrella": "personal-care-misc",
    "ladder": "tools-workshop", "wheelbarrow": "outdoor-utility",
    "wallet": "clothing-carry", "briefcase": "clothing-carry",
    "hat": "clothing-carry", "gloves": "clothing-carry",
    "toothbrush": "personal-care-misc", "razor": "personal-care-misc",
    "hair dryer": "personal-care-misc", "desktop computer": "electronics",
    "bed frame": "furniture-work", "sofa / couch": "furniture-work",
    "sofa": "furniture-work", "bookshelf": "furniture-work",
    "coffee table": "furniture-work", "dresser / wardrobe": "furniture-work",
    "dresser": "furniture-work", "wardrobe": "furniture-work",
    "desk lamp": "furniture-work", "floor lamp": "furniture-work",
    "window blinds": "furniture-work", "pillow": "furniture-work",
    "backpacking pack": "outdoor-utility", "hunting knife": "outdoor-utility",
    "television": "electronics", "router": "electronics",
    "headphones": "electronics", "speakers": "electronics",
    "camera": "electronics", "smartwatch": "electronics",
    "home thermostat": "household-systems", "dryer": "household-systems",
    "water heater": "household-systems", "furnace": "household-systems",
    "air conditioner": "household-systems",
}

DOMAIN_PATTERNS = {
    "kitchen-cooking": [
        "Separate the durable vessel from coatings, seals, and handles that renew.",
        "State the heat source and capacity boundary before comparing brands.",
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

STATUS_LABELS = {
    "DECLARED": "DECLARED",
    "CANDIDATE": "CANDIDATE",
    "EMPTY": "NO QUALIFYING PICK",
    "SPLIT_REQUIRED": "SPLIT REQUIRED",
    "CONDITIONAL": "CONDITIONAL",
    "CONSUMABLE": "RATIONAL RENEWAL",
}

STATUS_CODE = {
    "DECLARED": "D",
    "CANDIDATE": "P",
    "EMPTY": "E",
    "SPLIT_REQUIRED": "S",
    "CONDITIONAL": "C",
    "CONSUMABLE": "R",
}

STATUS_PUBLIC = {
    "DECLARED": "One model currently clears the category threshold.",
    "CANDIDATE": "A credible subject exists, but the evidence packet is incomplete.",
    "EMPTY": "No product currently earns a declaration inside this Form.",
    "SPLIT_REQUIRED": "The parent category contains incompatible jobs and must be narrowed.",
    "CONDITIONAL": "The answer changes materially with use, installation, fit, or service context.",
    "CONSUMABLE": "Renewal is intrinsic to the job and should be made rational and explicit.",
}

QUOTES = [
    ("The many, as we say, are seen but not known.", "Republic VI, 507b"),
    ("The beginning is the most important part of any work.", "Republic II, 377b"),
    ("Beauty of style and harmony and grace and good rhythm depend on simplicity.", "Republic III, 400e"),
    ("Knowledge which is acquired under compulsion obtains no hold on the mind.", "Republic VII, 536e"),
    ("The unexamined life is not worth living.", "Apology 38a"),
]

TECHNICAL_ASSETS = {
    "PI-001": ASSET_DIR / "lodge-l10sk3-technical-plate.png",
    "PI-003": ASSET_DIR / "estwing-e3-16c-technical-plate.png",
    "PI-012": ASSET_DIR / "makita-6302h-technical-plate.png",
}

TECHNICAL_LABELS = {
    "PI-001": "Exterior study + side and underside insets",
    "PI-003": "One-piece steel + conceptual grip section",
    "PI-012": "Exterior evidence + accessory system map",
}

# The four review objects use the exact, reference-spread facts and copy from
# the supplied 1940 dossier brief. Keeping these values in one map prevents a
# generic CSV sentence from weakening the proof pages while the full edition
# continues to use the same rendering functions.
PROOF_COPY = {
    "PI-001": {
        "title": "Lodge L10SK3",
        "subtitle": "12-inch seasoned cast-iron skillet",
        "lead": "The default 12-inch cast-iron skillet when utility per dollar matters more than low weight or a machined cooking surface.",
        "metrics": [("18 x 12.56 in", "overall length x width"), ("7.69 lb", "manufacturer weight"), ("9.12 in", "flat-bottom width"), ("$29.90", "sale snapshot / $37.95 regular")],
        "features": [
            ("ONE CAST BODY", "Bowl, long handle, and assist handle are visually continuous. No fastener is required to hold the pan together."),
            ("RECOVERABLE SURFACE", "The cooking surface is seasoned with vegetable oil. Lodge directs owners to hand wash, dry, and oil it. [S01]"),
            ("BROAD HEAT FIT", "The manufacturer lists stovetop, induction, oven, grill, and campfire compatibility. [S01]"),
        ],
        "ownership_heading": "THE PAN IS A MAINTENANCE LOOP",
        "ownership_intro": "Its value comes from a recoverable surface and a body with almost nothing to loosen. The cost is weight, care, and slower response.",
    },
    "PI-008": {
        "title": "Wiha 26547 #2 Phillips",
        "subtitle": "6-inch blade screwdriver",
        "lead": "The plain professional Phillips driver when a fixed steel shaft and exact tip geometry matter more than a bit system.",
        "metrics": [("6 in", "blade length"), ("56 HRC", "shaft hardness"), ("$18", "price snapshot"), ("DURABLE", "ownership mechanism")],
        "features": [
            ("CONTINUOUS SHAFT", "Chrome-vanadium steel runs through the shaft and is through-hardened to 56 HRC."),
            ("DIRECT-MOLDED GRIP", "The injection-molded handle meets the shaft without a separate grip-to-shaft joint."),
            ("HONEST DRIVE", "Phillips #2 is universal in the US, but cam-out is a limitation built into the drive."),
        ],
        "ownership_heading": "THE TIP IS THE WEAR PART",
        "ownership_intro": "A fixed shaft and direct-molded handle keep the tool simple. The driver still depends on correct fit and a tip that can be damaged by torque.",
    },
    "PI-012": {
        "title": "Makita 6302H",
        "subtitle": "1/2-inch low-speed corded drill",
        "lead": "A durable-looking, battery-independent drilling platform with strong official documentation. The ownership verdict stays open until current service-part availability is verified.",
        "metrics": [("6.5 A", "motor"), ("0-550 rpm", "variable speed"), ("4.8 lb", "net weight"), ("11.25 in", "overall length")],
        "features": [
            ("METAL FRONT END", "Makita specifies an industrial metal gear housing and heavy-duty keyed 1/2-inch chuck. [S03]"),
            ("CONTROL HARDWARE", "The official kit includes a side handle and chuck key; the handle can mount on either side. [S03]"),
            ("NO BATTERY LAYER", "Corded power removes battery-pack compatibility from the ownership system. It does not prove internal parts availability."),
        ],
        "ownership_heading": "DOCUMENTATION IS NOT REPAIRABILITY",
        "ownership_intro": "Makita publishes a manual and illustrated parts breakdown. That proves a service structure exists; it does not prove that every meaningful part remains stocked in the buyer's region.",
    },
    "PI-003": {
        "title": "Estwing E3-16C",
        "subtitle": "16-ounce curved-claw solid-steel hammer",
        "lead": "The compact general-purpose claw hammer for buyers who value a continuous steel core and a 13-inch working length.",
        "metrics": [("16 oz", "head weight"), ("13 in", "overall length"), ("1 piece", "head + handle forging"), ("Smooth", "striking face")],
        "features": [
            ("JOINT REMOVED", "Estwing states that the head and handle are forged in one piece. The common head-to-handle joint does not exist. [S04]"),
            ("MOLDED GRIP", "The shock-reduction grip is molded onto the steel handle. Vibration reduction is a manufacturer claim. [S04]"),
            ("GENERAL GEOMETRY", "A smooth face and curved claw suit ordinary driving and pulling. It is not a long framing hammer. [S04]"),
        ],
        "ownership_heading": "THE CORE IS SIMPLE",
        "ownership_intro": "The one-piece steel body removes the most familiar hammer joint. The grip is the ownership question: it improves use, yet the reviewed manufacturer page does not establish a replacement path.",
    },
}

PROOF_OWNERSHIP = {
    "PI-001": {
        "section_label": "FOUR-STEP CARE CYCLE",
        "care": [
            ("01", "COOK", "Preheat gradually. Use enough fat for the food and surface condition."),
            ("02", "WASH", "Hand wash. Remove residue without leaving the pan soaking."),
            ("03", "DRY", "Dry fully; brief stovetop heat can remove residual moisture."),
            ("04", "OIL", "Wipe on a very thin film before dry storage."),
        ],
        "failures": [
            ("SURFACE RUST", "USUALLY RECOVERABLE", "Remove rust, dry, and rebuild seasoning. Severity depends on depth."),
            ("SEASONING LOSS", "RECOVERABLE", "Clean back to a sound layer and reseason. This is maintenance, not end of life."),
            ("CRACK / MAJOR WARP", "TERMINAL FOR NORMAL OWNERSHIP", "Retire damaged cookware. The reviewed source does not quantify likelihood."),
        ],
        "candidate_headers": ["MODEL", "PRICE SNAPSHOT", "WEIGHT", "WORKING DIMENSIONS", "WHY IT REMAINS"],
        "candidates": [
            ("Lodge L10SK3", "$29.90 sale / $37.95 regular", "7.69 lb", "12.56 in overall, 9.12 in flat bottom", "Value baseline; broad heat fit"),
            ("Victoria Traditional 12", "$37.49", "6.7 lb", "13.3 in overall, extra-deep form", "Lower weight near the same price"),
            ("Field No.10", "$215", "6.0 lb", "11.625 in rim, 9.75 in cooking", "Machined surface; lighter premium"),
            ("Stargazer 12", "$175", "6.5 lb", "12 in rim, 9.4 in cooking", "Machined surface; flared rim"),
        ],
        "ruling": "Lodge wins the broad-use value test. Field and Stargazer buy lower weight and a machined surface; Victoria is the closest price competitor. Those are real upgrades, but none make the Lodge unable to do the job. [S01-S04]",
    },
    "PI-008": {
        "section_label": "CONSTRUCTION AND WEAR",
        "care": [
            ("01", "SEAT", "Seat the #2 tip fully before torque. Fit is the first safety and wear check."),
            ("02", "DRIVE", "Keep the shaft aligned with the recess; Phillips geometry will cam out under excess torque."),
            ("03", "INSPECT", "Look for a rounded tip, twisted shaft, or grip damage before the next fastener."),
            ("04", "REPLACE", "A damaged tip is a rational replacement event; the handle and shaft do not need a battery or software path."),
        ],
        "failures": [
            ("CAM-OUT", "RECOVERABLE", "Reset the driver squarely or change the bit standard. Do not add torque to a slipping tip."),
            ("TIP DAMAGE", "REPLACE", "A rounded Phillips tip is a wear threshold. Retire the driver when fit cannot be restored."),
            ("GRIP / SHAFT", "TERMINAL / UNKNOWN", "The direct-molded grip is simple, but a replacement path is not established in the source record."),
        ],
        "candidate_headers": ["MODEL", "PRICE SNAPSHOT", "CORE", "DRIVE / WEAR", "WHY IT REMAINS"],
        "candidates": [
            ("Wiha 26547 #2 Phillips", "$18", "Chrome-vanadium", "Fixed 6 in blade", "Exact fit; simple durable baseline"),
            ("Wera Kraftform 300", "compare", "Alloy steel", "Fixed Phillips blade", "Ergonomic grip alternative"),
            ("Klein 603-6", "compare", "Steel shaft", "Electrician handle", "Field-service familiarity"),
            ("Megapro 13-in-1", "compare", "Bit magazine", "Multi-bit interface", "Carry breadth; added joint"),
        ],
        "ruling": "Wiha remains the plain professional baseline: a fixed shaft, exact tip geometry, and no bit magazine to loosen. Robertson is the better drive where the fastener standard allows it. [S02]",
    },
    "PI-012": {
        "section_label": "CONCEPTUAL SYSTEM MAP",
        "care": [
            ("01", "MAINS POWER", "Corded power removes battery-pack compatibility from the ownership system."),
            ("02", "TRIGGER + REVERSE", "Controls set the low-speed working boundary; inspect the switch before load."),
            ("03", "MOTOR + GEARS", "The brushed motor and metal reduction train are the service-relevant core."),
            ("04", "CHUCK + LOAD", "Key the chuck fully and match the bit, speed, and side-handle control to the job."),
        ],
        "failures": [
            ("CORD / SWITCH", "SERVICE CHECK", "A replaceable cord or accessible switch can keep a sound motor platform in use."),
            ("BRUSH / BEARING", "INSPECT", "Wear parts need regional stock and a safe service procedure before they count as repairable."),
            ("GEAR / ARMATURE", "TERMINAL / UNKNOWN", "Parts structure is documented; current price, stock, and substitution path remain open."),
        ],
        "candidate_headers": ["MODEL", "MOTOR", "SPEED", "WEIGHT / LENGTH", "WHY IT REMAINS"],
        "candidates": [
            ("Makita 6302H", "6.5 A", "0-550 rpm", "4.8 lb / 11.25 in", "Low-speed baseline; provisional"),
            ("Makita DP4000", "7 A", "0-950 rpm", "4.8 lb / 12 in", "Accessible brushes stated; strongest challenger"),
            ("Cordless 18 V platform", "battery system", "variable", "pack-dependent", "Convenience; battery renewal is intrinsic"),
            ("Used corded drill", "inspect", "model-dependent", "condition-dependent", "Value path when service evidence is present"),
        ],
        "ruling": "Makita publishes a manual and illustrated parts breakdown. That proves a service structure exists; it does not prove that every meaningful part remains stocked in the buyer's region. Ask for current regional availability before treating this as final. [S03]",
    },
    "PI-003": {
        "section_label": "CONSTRUCTION AND WEAR",
        "care": [
            ("01", "STRIKE", "Use the smooth face for ordinary driving and match the 16-ounce head to the job."),
            ("02", "PULL", "Seat the curved claw before levering; avoid side loading that can deform the claw."),
            ("03", "INSPECT", "Check face, claw, eye area, and grip for cracks, mushrooming, or unsafe deformation."),
            ("04", "STORE", "Keep the steel dry. Grip degradation affects comfort before it affects the one-piece core."),
        ],
        "failures": [
            ("GRIP DEGRADATION", "FUNCTION REMAINS", "The molded grip can age without separating the steel head from the handle."),
            ("FACE MUSHROOMING", "INSPECT", "Abuse can deform the striking face. Retire an unsafe surface rather than dressing it casually."),
            ("EYE / CLAW CRACK", "TERMINAL / UNKNOWN", "A crack or severe deformation crosses the safe ownership threshold."),
        ],
        "candidate_headers": ["MODEL", "MASS / LENGTH", "CORE", "WEAR STRATEGY", "REASON TO CHOOSE"],
        "candidates": [
            ("Estwing E3-16C", "16 oz / 13 in", "One-piece steel", "Molded grip", "General carpentry baseline"),
            ("DeWalt DWHT51002", "16 oz / standard claw-hammer length", "One-piece steel", "Magnetic start; side puller", "More extraction features"),
            ("Stanley 51-162", "16 oz / 13-1/8 in", "One-piece steel", "Anti-Vibe handle", "Closest direct alternative"),
            ("Stiletto TIB14RMC", "14 oz head / 15.2 in", "All-titanium body", "Replaceable face + grip", "Premium framing system"),
        ],
        "ruling": "Estwing remains a compact, simple, verified general-purpose form. The declaration is about eliminating the head joint, not claiming zero wear. Choose a replaceable premium framing system when that ownership path is worth the price. [S04-S08]",
    },
}

# The declared spreads are meant to close a real buying decision, so the
# comparison row cannot fall back to blank "candidate" placeholders. These are
# the serious alternatives already implied by the register's counter-cases,
# written as short editorial notes for the reader. They are not new rulings;
# the source bundle remains the place to verify current price and availability.
ALTERNATE_CANDIDATES: dict[str, list[tuple[str, str, str, str]]] = {
    "Kitchen Knife": [
        ("Mercer Culinary Millennia 8-in", "price varies", "Lower-cost stainless chef knife", "Less confidence in edge life and finish."),
        ("Wusthof Classic 8-in", "price varies", "Forged German chef knife", "More money for a similar everyday job."),
        ("Shun Classic 8-in", "price varies", "Harder Japanese edge", "More chip-prone and less forgiving to sharpen."),
    ],
    "Saucepan": [
        ("All-Clad D3 3-qt", "price varies", "Similar tri-ply construction", "A higher price without a better ownership path."),
        ("Cuisinart Multiclad Pro 3-qt", "price varies", "Lower-cost tri-ply option", "A credible value, with less confidence in the finish."),
        ("Le Creuset 3-qt enameled", "price varies", "Easy care for acidic foods", "Heavier, and enamel can chip."),
    ],
    "Dutch Oven": [
        ("Le Creuset 5.5-qt", "price varies", "Enameled cast-iron benchmark", "Similar heat retention at a much higher price."),
        ("Staub 5.5-qt", "price varies", "Strong lid and enamel system", "The premium buys a small feature gain."),
        ("Lodge 6-qt bare cast iron", "price varies", "Lower-cost heat retention", "Seasoning care and acidic-food limits remain."),
    ],
    "Kettle": [
        ("Fellow Stagg EKG", "price varies", "Precise electric pouring control", "Sealed electronics add a failure path."),
        ("Breville Soft Top", "price varies", "Fast electric boiling", "The element and switch are sealed."),
        ("Hario Buono", "price varies", "Simple stovetop pouring", "Narrower use and more mineral cleanup."),
    ],
    "Backpack": [
        ("Osprey Farpoint 40", "price varies", "Travel organization and warranty", "More zippers, foam, and proprietary hardware."),
        ("GoRuck GR1 26L", "price varies", "Heavy fabric and strong zippers", "Heavier and more tactical than needed."),
        ("ALICE Pack", "used market", "Repairable military frame", "Crude ergonomics for everyday carry."),
    ],
    "Hand Saw": [
        ("Bahco 244", "price varies", "Affordable replaceable blade", "The blade is a planned consumable."),
        ("Silky Gomboy 240", "price varies", "Clean pull-stroke and replaceable blade", "A specialized tooth pattern limits the job."),
        ("Disston D-8", "used market", "Traditional resharpenable steel", "Good ownership, but sharpening takes skill."),
    ],
    "Desk": [
        ("IKEA Bekant", "price varies", "Ready-to-use adjustable desk", "More mechanisms and particleboard in the load path."),
        ("Boos Block workbench top", "price varies", "Solid hardwood work surface", "The top still needs legs and a larger budget."),
        ("Used HON steel-frame desk", "used market", "Commercial frame and low used price", "Condition and finish vary by listing."),
    ],
    "Boots": [
        ("Red Wing Iron Ranger", "price varies", "Resoleable leather work boot", "Less custom fit; the cork midsole compresses."),
        ("Nicks BuilderPro", "price varies", "Heavy-duty stitchdown construction", "More boot than most daily work requires."),
        ("Danner Mountain Light", "price varies", "Repairable heritage hiking boot", "More sole complexity and a higher price."),
    ],
    "Belt": [
        ("Tanner Goods Standard Belt", "price varies", "Full-grain leather and simple buckle", "More money for the same basic load."),
        ("Arcade Belts", "price varies", "Comfortable stretch webbing", "Stretch is a wear property, not permanence."),
        ("Hermes H Belt", "price varies", "Polished luxury finish", "Brand premium without a stronger working core."),
    ],
    "Adjustable Wrench": [
        ("Crescent 8-in", "price varies", "Widely available adjustable wrench", "Jaw play and quality vary by production year."),
        ("Proto 8-in", "price varies", "Professional forged alternative", "A higher price without a clear daily advantage."),
        ("Knipex Pliers Wrench 10-in", "price varies", "Excellent parallel-jaw grip", "More moving parts and a different hand feel."),
    ],
    "T-Shirt": [
        ("Uniqlo U Crew Neck", "price varies", "Affordable heavier cotton", "Lower price, but less confidence in long wear."),
        ("3sixteen Heavyweight Tee", "price varies", "Dense premium jersey", "The price rises faster than the service life."),
        ("Carhartt K87", "price varies", "Workwear cotton and easy replacement", "Bulkier fit and a less refined fabric."),
    ],
    "Jeans": [
        ("Iron Heart 21 oz 666", "price varies", "Very heavy selvedge denim", "High price and weight reduce everyday utility."),
        ("Pure Blue Japan 019", "price varies", "Premium denim and fade character", "More care and cost for a similar job."),
        ("Carhartt Rugged Flex", "price varies", "Workwear abrasion resistance", "Stretch adds comfort but creates a wear point."),
    ],
    "Jacket/Coat": [
        ("Patagonia Torrentshell 3L", "price varies", "Light waterproof shell", "The membrane still has a finite life."),
        ("Arc'teryx Beta", "price varies", "Refined technical shell", "More money for the same delamination risk."),
        ("M65 Field Jacket", "price varies", "Simple cotton-nylon field layer", "Less weather protection and a harder liner path."),
    ],
    "Chisel": [
        ("Stanley 750 bench chisel", "used market", "Excellent older socket construction", "The good examples are scarce and used."),
        ("Iyoroi Japanese bench chisel", "price varies", "Laminated steel edge", "Flattening and sharpening ask for more skill."),
        ("Lie-Nielsen bench chisel", "price varies", "Premium bench-chisel geometry", "Higher cost for a specialist finish."),
    ],
    "Pliers": [
        ("Knipex Cobra 87 01 250", "price varies", "Fast push-button adjustment", "More complexity than the simpler groove joint."),
        ("Klein D213-9NE", "price varies", "Familiar heavy-duty lineman pliers", "A narrower job and a less flexible grip."),
        ("Irwin Vise-Grip locking pliers", "price varies", "Strong clamp for awkward work", "Locking hardware adds a failure point."),
    ],
    "Tape Measure": [
        ("Milwaukee STUD 25-ft", "price varies", "Strong standout and rugged case", "Incremental features do not change the wear path."),
        ("Tajima G-25BW", "price varies", "Clear blade and smooth return", "The blade is still the terminal wear part."),
        ("Stanley PowerLock 25-ft", "price varies", "Simple, widely available baseline", "Lower-cost construction gives up drop margin."),
    ],
    "Tent": [
        ("MSR Hubba Hubba", "price varies", "Light backpacking shelter", "Coatings, poles, and zippers still age out."),
        ("Big Agnes Copper Spur", "price varies", "Light and roomy for its class", "Low weight accepts a finite service life."),
        ("Kodiak Canvas Flex-Bow", "price varies", "Repairable canvas shelter", "Too heavy for the backpacking Form."),
    ],
    "Sleeping Bag": [
        ("Feathered Friends Egret 20", "price varies", "High-quality down and construction", "Premium price does not stop loft loss."),
        ("Katabatic Gear Flex 22", "price varies", "Flexible down quilt system", "More setup judgment and less blanket familiarity."),
        ("REI Magma 15", "price varies", "Strong value-to-weight ratio", "Lower-cost materials age sooner."),
    ],
    "Water Bottle": [
        ("Nalgene Wide Mouth 32 oz", "price varies", "Simple, light, widely replaceable", "Plastic scratches and holds flavor over time."),
        ("Hydro Flask Standard Mouth", "price varies", "Strong insulation", "A dented vacuum wall cannot be repaired."),
        ("Lifefactory Glass 22 oz", "price varies", "Taste-neutral glass", "Breakage is the terminal failure."),
    ],
    "Flashlight": [
        ("Maglite 3C LED", "price varies", "Simple high-capacity battery format", "Larger and less convenient to carry."),
        ("Fenix PD36R", "price varies", "Bright rechargeable platform", "Battery and electronics become the service path."),
        ("SureFire G2X", "price varies", "Compact, proven light body", "Proprietary cells cost more to keep supplied."),
    ],
    "Sweater": [
        ("Carraig Donn Aran", "price varies", "Traditional wool cable knit", "Similar Form, with less sourcing certainty."),
        ("Icebreaker Merino 200", "price varies", "Light, soft merino layer", "Finer fibers wear sooner at friction points."),
        ("L.L.Bean Irish Fisherman", "price varies", "Accessible traditional knit", "Fit and fiber consistency vary by season."),
    ],
    "Cooler": [
        ("YETI Tundra 45", "price varies", "Well-supported rotomolded cooler", "Similar construction at a higher price."),
        ("Pelican Elite 45", "price varies", "Strong latches and insulation", "Bulkier hardware for the same size job."),
        ("ORCA 40 QT", "price varies", "Rotomolded body with serviceable parts", "Smaller capacity and less price advantage."),
    ],
    "Pocket Knife": [
        ("Opinel No. 8 Carbon", "price varies", "Simple lock and easy sharpening", "Carbon steel asks for rust care."),
        ("Victorinox Pioneer", "price varies", "Useful compact tool set", "More tools add more interfaces."),
        ("Spyderco Delica 4", "price varies", "Excellent one-hand folding knife", "Lock and clip add parts to wear."),
    ],
    "Notebook": [
        ("Rhodia Webnotebook", "price varies", "Good paper and a clean case", "Glue-bound pages remain the weak point."),
        ("Leuchtturm1917 A5", "price varies", "Useful index and page system", "Extra features do not fix the binding."),
        ("Ampad Gold Fibre legal pad", "price varies", "Cheap, flat, easy to replace", "Designed for notes, not a permanent record."),
    ],
    "Pen": [
        ("Pilot Metropolitan", "price varies", "Refillable metal fountain pen", "Needs cleaning and better paper."),
        ("Lamy Safari", "price varies", "Simple refillable writing tool", "Plastic body and nib fit are taste-sensitive."),
        ("BIC Cristal", "price varies", "Extremely cheap and dependable", "The pen is the consumable, not the holder."),
    ],
    "Cutting Board": [
        ("Teakhaus edge-grain board", "price varies", "Dense wood and recoverable surface", "Heavier and still needs oiling."),
        ("Epicurean Kitchen Series", "price varies", "Thin, dishwasher-friendly composite", "Surface wear is not meaningfully reversible."),
        ("OXO utility board", "price varies", "Low-cost dishwasher option", "Deep scores remain a replacement signal."),
    ],
    "Bicycle": [
        ("Trek 520", "price varies", "Touring geometry and rack mounts", "Availability and standards vary by year."),
        ("Surly Disc Trucker", "price varies", "Current steel touring alternative", "Disc standards add parts and tool demands."),
        ("Giant Contend AR", "price varies", "Modern all-road versatility", "More integrated parts reduce easy rebuilding."),
    ],
    "Dining Chair": [
        ("Stickley Mission dining chair", "price varies", "Solid hardwood and repairable joinery", "Premium price for a heavy style."),
        ("IKEA Ingolf", "price varies", "Accessible traditional silhouette", "Particleboard and hardware age sooner."),
        ("Herman Miller molded chair", "price varies", "Easy-clean shell and stable base", "Plastic shell and molded parts limit repair."),
    ],
    "Socks": [
        ("Smartwool Hike Light Cushion", "price varies", "Comfortable merino blend", "Warranty is shorter than the ideal service life."),
        ("Fox River Wick Dry", "price varies", "Lower-cost work sock", "Cotton content holds moisture and wears sooner."),
        ("Wigwam Merino Comfort", "price varies", "Traditional merino construction", "Less confidence in heel and toe longevity."),
    ],
    "Watch": [
        ("Seiko SKX007", "used market", "Simple automatic movement", "Used supply and service condition vary."),
        ("Citizen Eco-Drive BM8180", "price varies", "Solar quartz convenience", "Battery and sealed electronics still age."),
        ("Apple Watch SE", "price varies", "Useful connected features", "Software support and battery life are finite."),
    ],
    "Shoes": [
        ("Allen Edmonds Park Avenue", "price varies", "Resoleable classic dress shoe", "Less distinctive fit and finishing than the pick."),
        ("Grant Stone Diesel", "price varies", "Strong welted leather construction", "More casual shape for a dress-shoe job."),
        ("Blundstone 550", "price varies", "Convenient everyday Chelsea boot", "The polyurethane sole is hard to renew."),
    ],
    "Level": [
        ("Empire True Blue 48-in", "price varies", "Affordable aluminum level", "Less confidence in drop and vial durability."),
        ("Johnson 48-in", "price varies", "Common jobsite alternative", "Accuracy and end-cap protection vary."),
        ("Bosch GLL 3-80 laser", "price varies", "Fast layout over long distances", "Batteries and electronics add failure points."),
    ],
    "Drill Bits": [
        ("Irwin M2 HSS set", "price varies", "Common sizes in quality HSS", "A set encourages buying sizes you do not use."),
        ("Drill America M42 cobalt", "price varies", "Longer life in hard metal", "Higher cost and less general-purpose fit."),
        ("Vermont American general set", "price varies", "Easy hardware-store availability", "Soft edges and poor concentricity are the risk."),
    ],
    "Extension Cord": [
        ("Southwire 12/3 SJTW 50-ft", "price varies", "Common outdoor-rated copper cord", "Similar construction with no clear service edge."),
        ("Woods 12/3 outdoor cord", "price varies", "Accessible heavy-duty alternative", "Jacket and molded ends remain wear points."),
        ("US Wire 10/3 SJTW 50-ft", "price varies", "Lower voltage drop under load", "Heavier and more cord than most jobs need."),
    ],
    "Camping Stove": [
        ("MSR PocketRocket Deluxe", "price varies", "Light, fast canister stove", "Fuel format and cold performance stay limiting."),
        ("Jetboil Flash", "price varies", "Fast integrated boiling system", "More proprietary parts and a narrower job."),
        ("Coleman Classic 2-burner", "price varies", "Commodity propane and broad cooking area", "Bulkier and less field-portable."),
    ],
    "Mechanical Pencil": [
        ("Rotring 600 0.7mm", "price varies", "Durable all-metal body", "The mechanism still wears before the body."),
        ("Pentel P205", "price varies", "Simple, proven drafting pencil", "Plastic body is less drop-resistant."),
        ("BIC Velocity", "price varies", "Cheap and easy to replace", "Disposable mechanism has no recovery path."),
    ],
    "Umbrella": [
        ("Blunt Classic", "price varies", "Better wind-management geometry", "Still has ribs, fabric, and a finite warranty."),
        ("Davek Solo", "price varies", "Strong canopy and long warranty", "Warranty is doing much of the durability work."),
        ("Totes Titan", "price varies", "Low-cost manual stick umbrella", "Accepts replacement as part of the design."),
    ],
    "Ladder": [
        ("Little Giant Select Step", "price varies", "Versatile adjustable platform", "Hinges and locks add failure points."),
        ("Werner 6-ft aluminum step ladder", "price varies", "Lighter and easy to move", "Conductive metal dents and corrodes."),
        ("Louisville fiberglass step ladder", "price varies", "Direct Type IA alternative", "The exact parts and service path vary."),
    ],
    "Wheelbarrow": [
        ("Ames True Temper 6-cu-ft", "price varies", "Common steel-tub alternative", "Hardware and finish vary by production run."),
        ("Gorilla Carts GOR4PS", "price varies", "Stable four-wheel hauling", "More wheels mean more moving parts."),
        ("Poly garden wheelbarrow", "price varies", "Light and rust-free", "Plastic cracks rather than being welded."),
    ],
    "Wallet": [
        ("Bellroy Hide & Seek", "price varies", "Slim organized leather wallet", "More folds and lining mean more wear points."),
        ("Dun Leather Goods bifold", "price varies", "Simple full-grain construction", "Less evidence of long-term repair support."),
        ("Herschel Charlie", "price varies", "Cheap compact card holder", "Thin fabric and coating wear sooner."),
    ],
    "Briefcase": [
        ("Tom Bihn Synik 30", "price varies", "Light bag with strong organization", "More compartments and zippers to wear."),
        ("Saddleback Leather Classic Briefcase", "price varies", "Heavy full-grain leather body", "Very heavy and expensive for the job."),
        ("Vintage Hartmann Executive", "used market", "Hard-sided protection and repair potential", "Heavy, dated, and condition-dependent."),
    ],
    "Hat": [
        ("Carhartt A18 Watch Hat", "price varies", "Cheap, warm knit alternative", "Acrylic pills and has a finite life."),
        ("Filson Tin Cloth Packer", "price varies", "Weather-resistant field hat", "More care and a less universal fit."),
        ("Stetson Open Road", "price varies", "Traditional felt shape", "Shape and finish need careful storage."),
    ],
    "Gloves": [
        ("Tillman 1418 drivers", "price varies", "Affordable heavy leather work glove", "Work gloves still wear through with use."),
        ("Hestra Army Leather Heli Ski", "price varies", "Repairable cold-weather glove system", "More expensive and specialized."),
        ("Kinco 901T", "price varies", "Inexpensive insulated work glove", "Coatings and seams remain consumable."),
    ],
    "Razor": [
        ("Gillette Fusion", "price varies", "Fast, familiar cartridge shave", "The blade system is pure consumption."),
        ("Braun Series 7", "price varies", "Convenient electric shaving", "Battery, foil, and motor all age out."),
        ("Dovo Bismarck straight razor", "price varies", "Indefinitely resharpenable blade", "Steep learning curve and daily stropping."),
    ],
}

TECHNICAL_PROMPTS = {
    "PI-001": """Create a landscape 4:3 editorial technical plate for a premium reference book. Subject: an accurate exterior study of a Lodge-style L10SK3 12-inch seasoned cast-iron skillet, shown without any brand name or logo. The skillet must have a round 12-inch bowl, a long integral cast-iron handle with a hanging hole, a short integral assist handle directly opposite, and two pour spouts at left and right. Show one large three-quarter isometric view and two small inset views: exact side profile and underside/flat-bottom view. Do not invent internal parts and do not show an exploded assembly; it is a single cast form. Style: 1930s-1940s American industrial catalog engraving combined with clean axonometric product illustration, black charcoal linework and subtle halftone shading on warm ivory archival paper, with restrained vermilion-red registration marks and measurement ticks but absolutely no numbers, letters, labels, captions, logos, signatures, or watermark. Object edges and proportions must be clear enough for annotations to be added later. Generous negative space around the object. High-end editorial, mechanically plausible, clean print texture.""",
    "PI-003": """Create a landscape 4:3 editorial technical plate for a premium reference book. Subject: an accurate exterior study of an Estwing E3-16C type 16-ounce curved-claw hammer, shown without brand name or logo. The hammer is exactly 13 inches overall, with the steel head and steel handle forged as one continuous polished piece, a smooth round striking face, a curved nail-pulling claw, and a molded cobalt-blue shock-reduction grip covering the lower handle. Show one large three-quarter isometric view and two small inset views: side silhouette and a conceptual cut section only through the blue molded grip around the steel core. Do not separate the steel head from the handle and do not invent hidden mechanisms. Style: 1930s-1940s American industrial catalog engraving combined with clean axonometric product illustration, black charcoal and steel-gray linework on warm ivory archival paper, restrained cobalt blue only for the grip, and a few vermilion-red registration marks and measurement ticks. Absolutely no numbers, letters, labels, captions, logos, signatures, or watermark. Mechanically plausible, crisp object edges, generous negative space, high-end editorial print texture.""",
    "PI-012": """Create a landscape 4:3 editorial technical plate for a premium reference book. Subject: an accurate exterior study of a Makita 6302H type 1/2-inch corded pistol-grip drill, shown without brand name or logo. Required visible features: teal cylindrical motor housing, black pistol grip with large trigger and lock-on detail, silver industrial metal gear housing at the front, heavy-duty 1/2-inch keyed chuck, removable black side handle attached beside the gear housing, black power cord exiting the grip, and a small belt clip. Show one large three-quarter isometric view plus three smaller separated accessory/system views: keyed chuck and chuck key, removable side handle, and a clean side silhouette. Do not expose or invent motor internals; this is exterior evidence and an accessory system map, not an exploded internal diagram. Style: 1930s-1940s American power-tool catalog engraving combined with precise axonometric product illustration, black charcoal/steel-gray linework on warm ivory archival paper, restrained teal on the motor housing, and a few vermilion-red registration marks and measurement ticks. Absolutely no numbers, letters, labels, captions, logos, signatures, or watermark. Mechanically plausible, crisp edges, generous negative space, high-end editorial print texture.""",
}

CANONICAL_PROMPT = """Use case: product-mockup
Asset type: clean industrial editorial plate for the Platonic Ideal catalog
Declared category and model: [category] - [exact model]
Form quality to show: [construction or permanence quality]
Visual anchors: [silhouette]; [material, finish, and color]; [distinctive
geometry]; [relevant hardware or service feature]
Scene/backdrop: clean warm ivory archival paper; the product plate is a
standalone object study with no Greek icon, laurel, marble slab, halo, or
decorative panel
Style/medium: 1940s American industrial catalog engraving with crisp black
linework, steel-gray hatching, restrained vermilion registration detail, and
subtle raster texture; not a photograph
Composition/framing: spacious landscape 4:3 plate, one dominant three-quarter
view and two or three separated detail/elevation views, generous margins
Lighting/mood: clear workshop light, durable, quiet, useful, easy to inspect
Text (verbatim): none
Constraints: model-informed but not model-identical; no brand identity; no
copied source-photo composition
Avoid: logos, labels, readable text, packaging, serial or model marks,
proprietary graphics, people, lifestyle scene, sale badge, watermark, exact
product photo, Greek icon background, laurel, marble, nimbus, or border
Disclosure: clean raster editorial plate; representative visual only; verify
the exact model, specification, and condition against the cited source bundle."""

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
    candidates = [
        value,
        re.sub(r"\s*\([^)]*\)$", "", value),
        re.sub(r"\s+-\s+.*$", "", value),
    ]
    candidates.append(candidates[-1].split(" / ")[0])
    return next((DOMAIN_OVERRIDES[c] for c in candidates if c in DOMAIN_OVERRIDES), "personal-care-misc")


def load_entries() -> list[Entry]:
    entries: list[Entry] = []
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as stream:
        rows = csv.DictReader(stream)
        for index, row in enumerate(rows, 1):
            def get(*keys: str) -> str:
                for key in keys:
                    value = normalize(row.get(key))
                    if value:
                        return value
                return ""

            number = int(get("Number") or index)
            status = get("Status").upper()
            category = get("Category")
            entries.append(Entry(
                number=number,
                reference=f"PI-{number:03d}",
                category=category,
                status=status,
                model=get("Model"),
                price=get("Price"),
                form=get("Form Definition"),
                form_statement=get("Form Statement"),
                summary=get("Card Snippet (Why this ends the search)") or get("Form Statement") or get("Core_Reasoning", "Core Reasoning"),
                reasoning=get("Core_Reasoning", "Core Reasoning"),
                disqualifiers=get("Key_Disqualifiers", "Key Disqualifiers"),
                maintenance=get("Maintenance / Replacement Cycle"),
                permanence=get("Permanence Mechanism"),
                alternates=get("Alternates (non-declared)"),
                admission=get("Admission Test"),
                failures=get("Failure Modes"),
                confidence=max(0, min(5, int(get("Confidence") or 0))),
                reviewed=get("Last Reviewed"),
                notes=get("Notes"),
                domain=domain_for(category),
            ))
    return entries


ENTRIES = load_entries()
ENTRIES_BY_REF = {entry.reference: entry for entry in ENTRIES}
ENTRIES_BY_DOMAIN: dict[str, list[Entry]] = defaultdict(list)
for entry in ENTRIES:
    ENTRIES_BY_DOMAIN[entry.domain].append(entry)


def category_page_map() -> dict[str, int]:
    """Mirror the full-edition page flow for human-readable index links."""
    page = 17  # five front pages, ten method pages, and the reader intro
    result: dict[str, int] = {}
    for _domain, _, _ in DOMAINS:
        page += 2
    for domain, _, _ in DOMAINS:
        for entry in ENTRIES_BY_DOMAIN[domain]:
            result[entry.reference] = page
            page += 2 if entry.status == "DECLARED" else 1
    return result


CATEGORY_PAGE_MAP = category_page_map()
SOURCE_DATA = json.loads(SOURCE_PATH.read_text(encoding="utf-8"))
SOURCE_RECORDS = SOURCE_DATA.get("records", [])
SOURCES_BY_REF = {record.get("productId"): record for record in SOURCE_RECORDS}
SOURCE_CHECKED_AT = normalize(SOURCE_DATA.get("checkedAt"))

# Source records are deliberately small. They are identity and provenance
# leads, not a substitute for the product pages. These labels let each spread
# say what the record can prove without forcing the reader into the ledger.
SOURCE_ROLE_LABELS = {
    "manufacturer": "maker's page with product details",
    "authorized-retailer": "authorized seller with product details",
    "retailer": "seller page with current price",
    "catalog-or-manual": "catalog or manual with care details",
    "unlocated": "no live source found",
}


def clean_editorial_text(value: str) -> str:
    """Remove internal source shorthand from reader-facing copy.

    The source ledger carries the actual links and dates. Product spreads use
    plain language so the reader sees the consequence of a fact rather than a
    string such as ``[S03]`` that only makes sense to the production team.
    """
    return re.sub(r"\s*\[[A-Z]+\d+(?:-[A-Z]+?\d+)?\]", "", normalize(value)).strip()


def source_role(record: dict) -> str:
    source_type = normalize(record.get("sourceType")).lower()
    return SOURCE_ROLE_LABELS.get(source_type, source_type or "source role not recorded")


def source_identity_line(entry: Entry) -> str:
    record = source_for(entry)
    exact = normalize(record.get("exactModel"))
    variant = normalize(record.get("variant"))
    region = normalize(record.get("region"))
    identity = normalize(record.get("identityStatus")).upper() or "UNRESOLVED"
    model = exact if exact and exact.lower() not in {"not recorded", "model pending", "not sku-normalized"} else (entry.model or "model not normalized")
    parts = [model]
    if variant and variant.lower() not in {"not recorded", "model pending"}:
        parts.append(variant)
    if region:
        parts.append(region)
    return f"{' / '.join(parts)} / {identity}"


def source_fact_block(entry: Entry) -> str:
    """Render the durable facts the source record contributes to the spread."""
    record = source_for(entry)
    title = normalize(record.get("sourcePageTitle")) or "Source page title not recorded"
    status = normalize(record.get("identityStatus")).upper() or "UNRESOLVED"
    recommended = normalize(record.get("recommendedUse"))
    notes = clean_editorial_text(record.get("notes"))
    rights = normalize(record.get("rightsStatus")).replace("-", " ") or "rights state not recorded"
    role = source_role(record)
    publisher = normalize(record.get("sellerOrManufacturer"))
    if publisher:
        role = f"{publisher} / {role}"
    proof_features = PROOF_COPY.get(entry.reference, {}).get("features", [])
    if proof_features:
        source_says = clean_editorial_text(proof_features[0][1])
        source_label = "SOURCE SAYS"
    else:
        source_says = f"{title}. {notes}" if notes else title
        source_label = "SOURCE RECORD"
    owner = first_sentence(
        entry.failures,
        entry.admission,
        entry.maintenance,
        entry.reasoning,
        entry.permanence,
        fallback="Use the recorded Form boundary and confirm the service path before purchase.",
    )
    audit = f"Checked {SOURCE_CHECKED_AT or entry.reviewed or 'date not recorded'}; {rights}."
    if recommended:
        role = f"{role}; use: {recommended}"
    values = [
        ("MODEL RECORD", source_identity_line(entry)),
        ("SOURCE ROLE", role),
        (source_label, source_says),
        ("OWNER CONSEQUENCE", owner),
    ]
    rows = "".join(
        f'<div class="source-fact"><strong>{esc(label)}</strong><span>{esc(value)}</span></div>'
        for label, value in values
    )
    return f'''<div class="source-facts-heading">SOURCE-DERIVED FACTS / OWNER CONSEQUENCE</div>
<div class="source-facts">{rows}</div>
<p class="source-audit-note"><span class="red">AUDIT:</span> {esc(audit)} The linked source remains the update path; the usable implication is carried above.</p>'''


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def shorten(value: str, limit: int = 230) -> str:
    value = normalize(value)
    if len(value) <= limit:
        return value
    cut = value[: max(1, limit - 3)].rsplit(" ", 1)[0]
    return cut.rstrip(" ,;:-") + "..."


def sentences(value: str, limit: int = 4) -> list[str]:
    value = normalize(value)
    if not value:
        return []
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])|\s*;\s*", value)
    return [part.strip() for part in parts if part.strip()][:limit]


def first_sentence(*values: str, fallback: str = "Evidence for this part of the ruling is still being assembled.") -> str:
    for value in values:
        items = sentences(value, 1)
        if items:
            return shorten(items[0], 190)
    return fallback


def uri(path: Path) -> str:
    return path.resolve().as_uri()


def image_for(entry: Entry) -> Path | None:
    if entry.reference in TECHNICAL_ASSETS:
        path = TECHNICAL_ASSETS[entry.reference]
        return path if path.exists() else None
    folders = sorted(PRODUCT_IMAGE_ROOT.glob(f"pi-{entry.number:03d}-*"))
    if not folders:
        return None
    folder = folders[0]
    candidates = sorted(folder.glob("hero-v2.*")) + sorted(folder.glob("hero.*"))
    return candidates[0] if candidates else None


def source_for(entry: Entry) -> dict:
    return SOURCES_BY_REF.get(entry.reference, {})


def short_title(entry: Entry) -> str:
    """Use the exact model token as the display title when we have it."""
    record = source_for(entry)
    exact = normalize(record.get("exactModel"))
    if exact and exact.lower() not in {"not recorded", "model pending"}:
        variant = normalize(record.get("variant"))
        if variant and len(exact) < 22 and entry.category.lower() in {"screwdriver", "drill", "hammer"}:
            return f"{exact} {shorten(variant, 24)}"
        return exact
    value = entry.model or entry.category
    value = re.sub(r"\s*\([^)]*\)", "", value)
    return shorten(value, 40)


def status_badge(entry: Entry) -> str:
    cls = "badge-declared" if entry.status == "DECLARED" else "badge-open"
    return f'<span class="badge {cls}">{esc(STATUS_LABELS.get(entry.status, entry.status))}</span>'


def top_line(left: str, right: str = "") -> str:
    return f"""<div class="topline">
  <span class="topline-left">{esc(left)}</span>
  <span class="topline-right">{esc(right)}</span>
</div>"""


def footer(page_number: int) -> str:
    return f"""<div class="footer">
  <div class="footer-main">Platonic Ideal - Editorial and Product Dossier - 1940 Edition</div>
  <div class="footer-tab">{page_number:02d}</div>
</div>"""


def page(inner: str, page_number: int, extra_class: str = "") -> str:
    """Wrap a full-edition page in the same page anatomy as the 20-page proof.

    The earlier full-run builder used a separate ``.page`` frame and footer.  That
    made the 196-page edition look like a different publication even though it was
    meant to be the expanded version of the proof.  Keep the page content functions
    intact, but give them the proof's inset border, folio, footer rule, and page tab.
    """
    return f'''<section class="review-page {extra_class}">
  <div class="page-border" aria-hidden="true"></div>
  <main class="page-content">{inner}</main>
  <div class="footer-rule" aria-hidden="true"></div>
  <footer class="folio"><span>PLATONIC IDEAL</span><i>THE GOOD BUY</i></footer>
  <div class="page-number">{page_number:02d}</div>
</section>'''


def headline(script: str, red_lead: str, black_tail: str, size: str = "32pt") -> str:
    script_html = f'<div class="script">{esc(script)}</div>' if script else ""
    return f"""{script_html}
<h1 class="display" style="font-size:{size};"><span class="red">{esc(red_lead)}</span> {esc(black_tail)}</h1>"""


def section_heading(red_lead: str, black_tail: str, size: str = "18pt") -> str:
    return f'<h2 class="section-heading" style="font-size:{size};"><span class="red">{esc(red_lead)}</span> {esc(black_tail)}</h2>'


def body(text: str, cls: str = "") -> str:
    return f'<p class="body {cls}">{esc(text)}</p>'


def card(label: str, title: str, text: str, dark: bool = False, cls: str = "") -> str:
    classes = f"card {'dark-card' if dark else ''} {cls}".strip()
    return f"""<div class="{classes}">
  <div class="card-number">{esc(label)}</div>
  <div class="card-title">{esc(title)}</div>
  <div class="card-text">{esc(shorten(clean_editorial_text(text), 245))}</div>
</div>"""


def cards_grid(cards: list[str], cls: str = "") -> str:
    return f'<div class="cards-grid {cls}">{"".join(cards)}</div>'


def field_value(value: str, fallback: str) -> str:
    value = normalize(value)
    if not value:
        return fallback
    return shorten(value, 48)


def source_link(entry: Entry, label: str = "Source") -> str:
    record = source_for(entry)
    url = normalize(record.get("sourceUrl"))
    if not url:
        return f'<span class="source-missing">{esc(label)}: not recorded</span>'
    return f'<a href="{esc(url)}">{esc(label)} / {esc(record.get("sourcePageTitle") or record.get("sellerOrManufacturer") or "exact-model source")}</a>'


def source_summary(entry: Entry) -> str:
    record = source_for(entry)
    identity = normalize(record.get("identityStatus")).upper() or "UNRESOLVED"
    rights = normalize(record.get("rightsStatus")).replace("-", " ") or "rights state not recorded"
    checked = SOURCE_CHECKED_AT or entry.reviewed or "date not recorded"
    return (
        f"<div class=\"source-summary\"><span class=\"red\">SOURCE-DERIVED:</span> "
        f"{esc(source_identity_line(entry))} · {esc(source_role(record))} · "
        f"checked {esc(checked)} · {esc(identity.lower())} identity · {esc(rights)}.</div>"
    )


def product_plate(entry: Entry) -> str:
    image = image_for(entry)
    if not image:
        return '<div class="state-panel"><div class="state-code">?</div><div class="state-note">No local plate has cleared the image gate.</div></div>'
    technical = entry.reference in TECHNICAL_ASSETS
    label = "OBSERVED EXTERIOR" if technical else "INTERPRETIVE PLATE"
    second = "CONCEPTUAL DETAIL" if technical else "ORIGINAL EDITORIAL PLATE"
    alt = f"{entry.category} editorial plate"
    caption = TECHNICAL_LABELS.get(entry.reference, "Model-faithful interpretive plate")
    return f"""<figure class="plate">
  <img src="{esc(uri(image))}" alt="{esc(alt)}" />
  <figcaption><span class="red-label">{esc(label)}</span><span class="outline-label">{esc(second)}</span><em>{esc(caption)}</em></figcaption>
</figure>"""


def score_row(entry: Entry) -> str:
    confidence = max(1, min(3, entry.confidence or 2))
    ownership = 3 if entry.maintenance and entry.permanence else (2 if entry.maintenance or entry.permanence else 1)
    fit = 3 if entry.status == "DECLARED" else 2
    def bars(score: int) -> str:
        return f'<span class="bars">{"■" * score}</span><span class="empty-bars">{"■" * (3-score)}</span>'
    return f"""<div class="score-row">
  <span>IDENTITY {bars(confidence)}</span>
  <span>CATEGORY FIT {bars(fit)}</span>
  <span>OWNERSHIP {bars(ownership)}</span>
  <em>{esc("Confidence is scored per axis. Source status remains separate.")}</em>
</div>"""


def feature_cards(entry: Entry) -> str:
    proof = PROOF_COPY.get(entry.reference)
    if proof:
        facts = [(str(i + 1), title, text) for i, (title, text) in enumerate(proof["features"])]
        return cards_grid([card(number, title, text) for number, title, text in facts], "feature-grid")
    facts = [
        ("1", "FORM", first_sentence(entry.form_statement, entry.form, fallback="The declared Form is still being normalized.")),
        ("2", "OWNERSHIP", first_sentence(entry.maintenance, entry.permanence, fallback="The ownership path is the part of the ruling that needs the closest audit.")),
        ("3", "TRADEOFF", first_sentence(entry.disqualifiers, entry.reasoning, fallback="The category tradeoff is recorded in the evidence bundle.")),
    ]
    return cards_grid([card(number, title, text) for number, title, text in facts], "feature-grid")


def metric_grid(entry: Entry) -> str:
    proof = PROOF_COPY.get(entry.reference)
    if proof:
        metrics = proof["metrics"]
        return '<div class="metric-grid">' + "".join(
            f'<div class="metric"><strong>{esc(value)}</strong><em>{esc(label)}</em></div>' for value, label in metrics
        ) + "</div>"
    combined = " ".join([entry.model, entry.form, entry.form_statement])
    measure = re.search(r"\b\d+(?:\.\d+)?(?:-\d+(?:\.\d+)?)?\s*(?:in(?:ch)?|oz|lb|lbs|kg|mm|cm|qt|A|rpm|V|years?|yr)\b", combined, re.I)
    mass = re.search(r"\b\d+(?:\.\d+)?\s*(?:oz|lb|lbs|kg|g)\b", combined, re.I)
    permanence = entry.permanence.lower()
    if "warranty" in permanence or "guarantee" in permanence:
        ownership = "WARRANTY"
    elif "repair" in permanence or "service" in permanence or "rebuild" in permanence:
        ownership = "REPAIRABLE"
    elif "replace" in permanence or "renew" in permanence or entry.status == "CONSUMABLE":
        ownership = "RENEWAL"
    else:
        ownership = "PENDING"
    metrics = [
        (measure.group(0) if measure else "FORM", "form signal"),
        (mass.group(0) if mass else "USE", "working measure"),
        (field_value(entry.price, "price pending"), "price snapshot"),
        (ownership, "ownership mechanism"),
    ]
    return '<div class="metric-grid">' + "".join(
        f'<div class="metric"><strong>{esc(value)}</strong><em>{esc(label)}</em></div>' for value, label in metrics
    ) + "</div>"


def declaration_page(entry: Entry, declared_index: int, page_number: int) -> str:
    proof = PROOF_COPY.get(entry.reference)
    title = proof["title"] if proof else short_title(entry)
    subtitle = proof["subtitle"] if proof else shorten(entry.form or entry.category, 92)
    lead = proof["lead"] if proof else first_sentence(entry.summary, entry.form_statement, entry.reasoning,
                                                       fallback="The declaration is a bounded answer to the ordinary job.")
    ownership_intro = proof["ownership_intro"] if proof else first_sentence(
        entry.maintenance, entry.permanence,
        fallback="The ownership path is recorded here so the purchase remains legible after checkout.",
    )
    header = top_line(
        f"DECLARATION {declared_index:02d}   {entry.category}",
        STATUS_LABELS.get(entry.status, entry.status),
    )
    inner = f"""{header}
<div class="product-layout">
  <div class="product-copy">
    <h3 class="product-title">{esc(shorten(title, 48))}</h3>
    <p class="product-subtitle">{esc(subtitle)}</p>
    <p class="lead">{esc(clean_editorial_text(lead))}</p>
    {metric_grid(entry)}
  </div>
  {product_plate(entry)}
</div>
{feature_cards(entry)}
{score_row(entry)}
{source_summary(entry)}
<div class="ownership-teaser">
  <h2><span class="red">OWNERSHIP BRIEF {declared_index:02d}:</span> {esc(proof["ownership_heading"] if proof else shorten("The " + entry.category.lower() + " after checkout", 68))}</h2>
  <p>{esc(clean_editorial_text(ownership_intro))}</p>
  <div class="mini-rule">FORM - FIRST CARE CYCLE</div>
</div>"""
    return page(inner, page_number, "declared-page")


def alternate_rows(entry: Entry) -> list[tuple[str, str, str, str, str]]:
    rows: list[tuple[str, str, str, str, str]] = []
    main = entry.model or "Model not normalized"
    rows.append((main, field_value(entry.price, "pending"), "declared", "current", "The present ruling"))
    raw = normalize(entry.alternates)
    if raw:
        parts = [part.strip() for part in re.split(r";|\n|\s+\|\s+", raw) if part.strip()]
        if len(parts) == 1:
            parts = [part.strip() for part in re.split(r",(?=[A-Z])", raw) if part.strip()]
        for i, part in enumerate(parts[:3], 1):
            rows.append((shorten(part, 34), "compare", "candidate", "field", "Named alternative"))
    while len(rows) < 4:
        rows.append(("Candidate field open", "not captured", "unresolved", "next proof", "Add an exact rival before release."))
    return rows[:4]


def candidate_table(entry: Entry) -> str:
    proof = PROOF_OWNERSHIP.get(entry.reference)
    if proof:
        rows = proof["candidates"]
        headers = proof["candidate_headers"]
        head = "".join(f"<th>{esc(value)}</th>" for value in headers)
        body_rows = "".join(
            f"<tr><td><strong>{esc(model)}</strong></td><td>{esc(first)}</td><td>{esc(second)}</td><td>{esc(third)}</td><td>{esc(fourth)}</td></tr>"
            for model, first, second, third, fourth in rows
        )
        return f"""<div class="mini-rule">CANDIDATE FIELD</div>
<table class="candidate-table">
  <thead><tr>{head}</tr></thead>
  <tbody>{body_rows}</tbody>
</table>"""
    rows = alternate_rows(entry)
    body_rows = "".join(
        f"""<tr><td><strong>{esc(model)}</strong></td><td>{esc(price)}</td><td>{esc(core)}</td><td>{esc(strategy)}</td><td>{esc(reason)}</td></tr>"""
        for model, price, core, strategy, reason in rows
    )
    return f"""<div class="mini-rule">CANDIDATE FIELD</div>
<table class="candidate-table">
  <thead><tr><th>MODEL</th><th>PRICE SNAPSHOT</th><th>CORE</th><th>EDITORIAL STATUS</th><th>WHY IT REMAINS</th></tr></thead>
  <tbody>{body_rows}</tbody>
</table>"""


def failure_cards(entry: Entry) -> str:
    proof = PROOF_OWNERSHIP.get(entry.reference)
    if proof:
        cards = []
        for index, (title, status, text) in enumerate(proof["failures"], 1):
            dark = index == len(proof["failures"])
            classes = "failure-card dark-failure" if dark else "failure-card"
            status_class = "failure-status dark-status" if dark else "failure-status"
            cards.append(
                f'<div class="{classes}"><div class="failure-title">{esc(title)}</div><div class="{status_class}">{esc(status)}</div><div class="failure-text">{esc(text)}</div></div>'
            )
        return '<div class="failure-grid">' + "".join(cards) + "</div>"
    fail = sentences(entry.failures, 3)
    if not fail:
        fail = ["Failure modes are not yet logged.", "Add symptom, cause, consequence, and safe recovery.", "Define the terminal threshold before commercial release."]
    while len(fail) < 3:
        fail.append("Add an exact-model symptom, recovery path, and terminal threshold.")
    labels = ["RECOVERABLE", "INSPECT", "TERMINAL / UNKNOWN"]
    return cards_grid([
        card(str(i + 1), labels[i], fail[i], dark=(i == 2))
        for i in range(3)
    ], "failure-grid")


def care_cards(entry: Entry) -> str:
    proof = PROOF_OWNERSHIP.get(entry.reference)
    if proof:
        return cards_grid([card(number, title, text) for number, title, text in proof["care"]], "care-grid")
    values = [
        ("01", "FIRST USE", first_sentence(entry.form, fallback="Confirm size, fit, load, and configuration before use.")),
        ("02", "CARE CYCLE", first_sentence(entry.maintenance, fallback="The maintenance interval is not captured yet.")),
        ("03", "SERVICE PATH", first_sentence(entry.permanence, entry.notes, fallback="Parts and service proof remains open.")),
        ("04", "ADMISSION GATE", first_sentence(entry.admission, fallback="The exact admission test needs a recorded source.")),
    ]
    return cards_grid([card(number, title, text) for number, title, text in values], "care-grid")


def ownership_page(entry: Entry, declared_index: int, page_number: int) -> str:
    proof = PROOF_COPY.get(entry.reference)
    ownership = PROOF_OWNERSHIP.get(entry.reference)
    title = proof["ownership_heading"] if proof else first_sentence(entry.maintenance, entry.permanence,
                                                                     fallback="The ownership path is the part of the ruling that must survive use.")
    intro = proof["ownership_intro"] if proof else title
    source = source_for(entry)
    identity = normalize(source.get("identityStatus")).upper() or "UNRESOLVED"
    next_proof = first_sentence(entry.notes, entry.admission,
                                fallback="Add exact-model service, parts, and failure evidence before release.")
    dark_reason = ownership["ruling"] if ownership else first_sentence(entry.reasoning, entry.summary,
                                                                         fallback="The declaration remains useful because the Form and ownership tradeoff are visible.")
    section_label = ownership["section_label"] if ownership else "FOUR-STEP CARE CYCLE"
    inner = f"""{top_line(f"DECLARATION {declared_index:02d}", entry.category)}
{section_heading(f"OWNERSHIP BRIEF {declared_index:02d}:", shorten(title, 72), "18pt")}
{body(clean_editorial_text(intro), "intro")}
{source_fact_block(entry)}
<div class="mini-rule">{esc(section_label)}</div>
{care_cards(entry)}
<div class="mini-rule">FAILURE MAP</div>
{failure_cards(entry)}
{candidate_table(entry)}
<div class="dark-callout"><span>EDITORIAL RULING.</span> {esc(shorten(clean_editorial_text(dark_reason), 430))}</div>
<div class="source-line"><span class="red">UPDATE PATH:</span> {source_link(entry, "Open source")} <span class="source-date">{esc(SOURCE_CHECKED_AT or entry.reviewed or "review date pending")}</span></div>"""
    return page(inner, page_number, "ownership-page")


def open_page(entry: Entry, page_number: int, open_index: int) -> str:
    label = STATUS_LABELS.get(entry.status, entry.status)
    code = STATUS_CODE.get(entry.status, "?")
    form_text = first_sentence(entry.form, entry.form_statement,
                               fallback="The category Form is mapped, but a bounded product answer is not ready.")
    proof = first_sentence(entry.admission, entry.notes,
                           fallback="Lock the exact model, region, primary source, and ownership proof.")
    change = first_sentence(entry.disqualifiers, entry.failures,
                            fallback="A credible exact-model candidate could change this state.")
    source = source_for(entry)
    source_status = normalize(source.get("identityStatus")).upper() or "NO SOURCE"
    source_note = normalize(source.get("notes")) or "No source note is recorded."
    inner = f"""{top_line(f"RESEARCH BRIEF {open_index:02d}", entry.category)}
<div class="open-layout">
  <div>
    <h3 class="product-title">{esc(shorten(entry.category, 48))}</h3>
    <p class="product-subtitle">{esc(label)}</p>
    <p class="lead">{esc(STATUS_PUBLIC.get(entry.status, "The research state is still being defined."))}</p>
    {metric_grid(entry)}
  </div>
  <div class="state-panel large-state">
    <div class="state-code">{esc(code)}</div>
    <div class="state-label">{esc(label)}</div>
    <div class="state-note">{esc(shorten(entry.model or "No product is declared in this Form.", 120))}</div>
  </div>
</div>
{cards_grid([
    card("1", "FORM BOUNDARY", form_text),
    card("2", "NEXT PROOF", proof),
    card("3", "WHAT WOULD CHANGE", change, dark=True),
], "feature-grid")}
<div class="mini-rule">EVIDENCE STATE</div>
<div class="evidence-strip">
  <div><strong>IDENTITY</strong><span>{esc(source_status)}</span></div>
  <div><strong>PRICE</strong><span>{esc(entry.price or "not captured")}</span></div>
  <div><strong>MAINTENANCE</strong><span>{esc(shorten(entry.maintenance or "not recorded", 46))}</span></div>
  <div><strong>LAST REVIEWED</strong><span>{esc(entry.reviewed or "not dated")}</span></div>
</div>
<div class="dark-callout"><span>NEXT PROOF BEFORE DECLARATION.</span> {esc(shorten(proof + " " + source_note, 500))}</div>
<div class="source-line"><span class="red">SOURCE LEDGER:</span> {source_link(entry, "Identity lead")}</div>"""
    return page(inner, page_number, "open-page")


def method_page(kicker: str, script: str, red_lead: str, black_tail: str,
                intro: str, card_data: list[tuple[str, str, str]], bottom: str,
                page_number: int) -> str:
    cards = cards_grid([card(number, title, text, dark=False) for number, title, text in card_data])
    inner = f"""{top_line(kicker, "METHOD")}
{headline(script, red_lead, black_tail, "29pt")}
{body(intro, "intro")}
{cards}
<div class="dark-callout method-bottom">{esc(bottom)}</div>"""
    return page(inner, page_number, "method-page")


def cover_page(page_number: int, proof: bool = False) -> str:
    # The cover is shared visually with the 20-page proof.  Provenance for the
    # reference portrait remains in the source and image ledgers; the cover uses
    # the approved editorial plate so the full run reads as the same publication.
    portrait = ASSET_DIR / "editorial" / "plato-cover-portrait.png"
    quote, cite = QUOTES[0]
    edition_label = "20-PAGE DESIGN PROOF" if proof else "FULL REVIEW EDITION - SEPTEMBER 2026"
    cover_bottom = "FOUR DECLARED OBJECTS" if proof else "100 CATEGORY ENTRIES  ·  48 DECLARED OBJECTS  ·  196 PAGES"
    inner = f"""{top_line("PLATONIC IDEAL", edition_label)}
<div class="cover-copy">
  <p class="cover-brand">PLATONIC IDEAL</p>
  <p class="cover-label">A BUYING GUIDE</p>
  <h1>THE DURABLE<br>OBJECT FILES</h1>
  <p class="cover-deck">A reference book for buying durable, repairable, well-understood objects. The dossier carries the evidence, judgment, and ownership path that a short storefront page cannot.</p>
  <div class="cover-list">{cover_bottom}</div>
</div>
<p class="cover-date">{edition_label}</p>
<img class="cover-art" src="{esc(uri(portrait))}" alt="Editorial portrait of Plato in a classical engraving style" />
<blockquote class="cover-quote">"{esc(quote)}"<span>PLATO / {esc(cite.upper())} / JOWETT</span></blockquote>"""
    return page(inner, page_number, "cover-page cover")


def edition_page(page_number: int) -> str:
    inner = f"""{top_line("FULL REVIEW EDITION", "THE BOOK BEHIND THE STOREFRONT")}
{headline("", "THE DOSSIER:", "A Reference Book For Buying Durable, Repairable, Well-Understood Objects", "26pt")}
{body("The site is the concise, navigable storefront. The dossier is the evidence and ownership layer behind it. A product page can make one recommendation legible; the dossier shows the pressure that recommendation survived.", "intro")}
{section_heading("FIVE LAYERS OF PRESSURE:", "Why The Dossier Has More Value Than The Site", "18pt")}
{cards_grid([
    card("01", "FORM", "Construction, materials, geometry, mechanism, dimensions, finish, and the features that distinguish one model from another."),
    card("02", "OWNERSHIP PATH", "What happens before first use, during routine maintenance, when a part fails, and when service, storage, or a used purchase matters."),
    card("03", "FAILURE AND RECOVERY", "Likely failure modes, first diagnosis, repair or replacement path, parts availability, and terminal thresholds."),
    card("04", "CANDIDATE PRESSURE", "Named runners-up and credible alternatives, with the reason each one loses, wins, or remains conditional."),
    card("05", "EVIDENCE STATE", "Exact-model sources, independent tests, ownership reports, market evidence, open questions, and editorial inferences."),
], "five-layer-grid")}
<div class="dark-callout"><span>THE PROMISE.</span> Stop researching, buy with clear tradeoffs, and keep the object working.</div>"""
    return page(inner, page_number)


def edition_inventory_page(page_number: int) -> str:
    counts = Counter(entry.status for entry in ENTRIES)
    state_rows = "".join(
        f'<tr><td>{esc(STATUS_LABELS[state])}</td><td class="red-number">{counts[state]}</td><td>{esc(STATUS_PUBLIC[state])}</td></tr>'
        for state in ["DECLARED", "CANDIDATE", "EMPTY", "SPLIT_REQUIRED", "CONDITIONAL", "CONSUMABLE"]
    )
    architecture = [
        ("Front and method", "16 pp"),
        ("Domain openers, 9 domains", "18 pp"),
        ("Declared object spreads, 48", "96 pp"),
        ("Open research briefs, 52", "52 pp"),
        ("End matter and ledgers", "14 pp"),
    ]
    arch_rows = "".join(f"<tr><td>{esc(a)}</td><td>{esc(b)}</td></tr>" for a, b in architecture)
    inner = f"""{top_line("THE REGISTER", "100 CATEGORIES / NINE DOMAINS")}
{headline("", "WHAT IS IN THE CURRENT EDITION:", "100 Categories Across Nine Domains", "22pt")}
<div class="two-col">
  <div class="keyline-box"><div class="box-title">REGISTER STATES</div><table class="simple-table"><tbody>{state_rows}</tbody></table></div>
  <div class="keyline-box"><div class="box-title">PAGE ARCHITECTURE</div><table class="simple-table"><tbody>{arch_rows}</tbody></table><p class="tiny-note">Every declared object gets one decision page and one ownership page. Open states remain visibly open.</p></div>
</div>
{section_heading("A PAGE IS A PROMISE:", "Every claim has a job, source, and owner consequence", "18pt")}
{body("The full review edition is intentionally much larger than the site. It includes linked indexes, method pages, domain maps, decision spreads, ownership briefs, source and rights ledgers, image records, and a change log. The book is substantial enough to review as a product and honest enough to show what still blocks a commercial release.", "intro")}
<div class="stat-line"><strong>196</strong><span>PAGES</span><strong>100</strong><span>ENTRIES</span><strong>48</strong><span>DECLARED</span><strong>52</strong><span>OPEN</span></div>"""
    return page(inner, page_number)


def index_page(entries: list[Entry], title: str, page_number: int) -> str:
    rows = []
    for entry in entries:
        state_class = "state-declared" if entry.status == "DECLARED" else "state-open"
        rows.append(
            f'<div class="index-row {state_class}"><span>{esc(str(CATEGORY_PAGE_MAP.get(entry.reference, "-")))}</span><a href="#entry-{esc(entry.reference)}">{esc(shorten(entry.category, 29))}</a><span>{esc(STATUS_LABELS[entry.status])}</span></div>'
        )
    midpoint = (len(rows) + 1) // 2
    cols = "".join(f'<div class="index-col">{"".join(rows[start:end])}</div>' for start, end in [(0, midpoint), (midpoint, len(rows))])
    inner = f"""{top_line("FIND A RULING", "CATEGORY INDEX")}
{headline("", "CATEGORY INDEX:", title, "24pt")}
{body("Category, editorial state, and destination page. State labels keep a research brief from looking like a settled recommendation.", "intro")}
<div class="index-grid">{cols}</div>"""
    return page(inner, page_number)


def reader_intro_page(page_number: int) -> str:
    inner = f"""{top_line("PART TWO", "DECLARED OBJECT PAGES / 48 SPREADS")}
{headline("How", "A DECLARATION READS:", "One Decision Page, One Ownership Page", "26pt")}
{body("Every declared object receives a decision page and an ownership page. The plate makes form legible; the ownership page tests whether the answer survives use. Sources are dated snapshots, not promises.", "intro")}
<div class="declaration-key">
  <div><span class="red">01</span><strong>DECISION PAGE</strong><p>Form, exact model, representative plate, reasons, and the tradeoff that closes the ordinary search.</p></div>
  <div><span class="red">02</span><strong>OWNERSHIP PAGE</strong><p>Care cycle, failure map, candidate pressure, service path, sources, and the trigger that would reopen the ruling.</p></div>
</div>
<div class="dark-callout"><span>READING PATH.</span> State - Form - plate - reasons - ownership - failures - source - reconsideration trigger.</div>"""
    return page(inner, page_number)


def domain_opener(domain_index: int, domain: str, name: str, description: str, page_number: int) -> str:
    entries = ENTRIES_BY_DOMAIN[domain]
    declared = [entry for entry in entries if entry.status == "DECLARED"]
    representative = declared[0] if declared else None
    plate = product_plate(representative) if representative else f'<div class="state-panel domain-state"><div class="state-code">{domain_index:02d}</div><div class="state-note">No declared plate in this domain.</div></div>'
    counts = Counter(entry.status for entry in entries)
    quote, cite = QUOTES[(domain_index - 1) % len(QUOTES)]
    inner = f"""{top_line(f"DOMAIN {domain_index:02d}", name.upper())}
<div class="domain-layout">
  <div class="domain-plate">{plate}</div>
  <div class="domain-copy">
    <div class="kicker red">DOMAIN {domain_index:02d}</div>
    <h1 class="domain-title">{esc(name)}</h1>
    <p class="domain-description">{esc(description)}</p>
    <div class="domain-metrics"><strong>{len(entries)}<em>ENTRIES</em></strong><strong>{counts["DECLARED"]}<em>DECLARED</em></strong><strong>{len(entries) - counts["DECLARED"]}<em>OPEN</em></strong></div>
    <blockquote class="domain-quote">"{esc(quote)}"<span>PLATO / {esc(cite.upper())}</span></blockquote>
    <div class="mini-rule">READING QUESTION</div>
    <p class="body">{esc(DOMAIN_PATTERNS[domain][0])}</p>
  </div>
</div>"""
    return page(inner, page_number, "domain-opener")


def domain_map(domain_index: int, domain: str, name: str, page_number: int) -> str:
    entries = ENTRIES_BY_DOMAIN[domain]
    patterns = DOMAIN_PATTERNS[domain]
    pattern_cards = cards_grid([card(f"{i+1:02d}", "PROOF QUESTION", text) for i, text in enumerate(patterns)])
    rows = []
    for entry in entries:
        rows.append(
            f'<div class="domain-row"><span>{esc(str(CATEGORY_PAGE_MAP.get(entry.reference, "-")))}</span><span>{esc(shorten(entry.category, 34))}</span><span class="domain-status">{esc(STATUS_LABELS[entry.status])}</span></div>'
        )
    midpoint = (len(rows) + 1) // 2
    map_cols = "".join(f'<div class="domain-col">{"".join(rows[start:end])}</div>' for start, end in [(0, midpoint), (midpoint, len(rows))])
    inner = f"""{top_line(f"DOMAIN {domain_index:02d}", "THE FIELD BEFORE THE PICKS")}
{headline("", "THE FIELD:", f"{name} Before The Picks", "24pt")}
{body("These categories share recurring ownership questions, but each still receives a bounded Form and its own evidence state.", "intro")}
<div class="mini-rule">RECURRING PROOF QUESTIONS</div>
{pattern_cards}
<div class="mini-rule">CATEGORY MAP</div>
<div class="domain-map">{map_cols}</div>"""
    return page(inner, page_number, "domain-map-page")


def source_ledger_page(records: list[dict], page_number: int, page_index: int, total_pages: int = 5) -> str:
    chunks = records[(page_index - 1) * 12: page_index * 12]
    if not chunks:
        identity_counts = Counter(normalize(record.get("identityStatus")).upper() or "UNRESOLVED" for record in records)
        role_counts = Counter(source_role(record) for record in records)
        rights_counts = Counter(normalize(record.get("rightsStatus")).replace("-", " ") or "UNRECORDED" for record in records)
        summary_cards = [
            ("01", "IDENTITY STATES", "; ".join(f"{key.title()}: {value}" for key, value in sorted(identity_counts.items()))),
            ("02", "SOURCE ROLES", "; ".join(f"{key.title()}: {value}" for key, value in sorted(role_counts.items()))),
            ("03", "RIGHTS STATES", "; ".join(f"{key.title()}: {value}" for key, value in sorted(rights_counts.items()))),
            ("04", "CHECK DATE", f"Inventory checked {SOURCE_CHECKED_AT or 'date not recorded'}. Recheck live pages before release."),
            ("05", "WHAT THIS TRAIL PROVES", "Publisher, identity status, source role, rights state, and the URL that can reopen a claim."),
            ("06", "WHAT IT DOES NOT PROVE", "Live stock, current price, repair economics, image republication permission, or a guarantee that a product will remain unchanged."),
        ]
        inner = f"""{top_line("SOURCE LEDGER", f"AUDIT TRAIL / {page_index} OF {total_pages}")}
{headline("How", "THE SOURCE PAGES:", "An Audit Trail, Not The Reading Path", "23pt")}
{body("The declared spreads carry the usable specification, care sequence, failure boundary, and owner consequence. This final ledger page explains how to read the dated records behind them and what still needs a fresh check.", "intro")}
{cards_grid([card(number, title, text) for number, title, text in summary_cards])}
<div class="dark-callout"><span>UPDATE RULE.</span> When a source changes, update the affected spread first, then record the old and new URL, access date, claim, and verdict impact here.</div>"""
        return page(inner, page_number, "ledger-page")
    items = []
    for record in chunks:
        url = normalize(record.get("sourceUrl"))
        label = normalize(record.get("category")) or "source record"
        meta = " / ".join(filter(None, [
            normalize(record.get("exactModel")),
            normalize(record.get("variant")),
            normalize(record.get("identityStatus")).upper(),
            source_role(record),
            ("checked " + (SOURCE_CHECKED_AT or "date not recorded")),
            ("spread p. " + str(CATEGORY_PAGE_MAP.get(record.get("productId"), "-"))),
        ]))
        link = f'<a href="{esc(url)}">{esc(url)}</a>' if url else '<span class="source-missing">URL not recorded</span>'
        rights = normalize(record.get("rightsStatus")).replace("-", " ") or "rights state not recorded"
        note = clean_editorial_text(record.get("notes")) or "No audit note recorded."
        items.append(f'<div class="ledger-item"><strong>{esc(label)}</strong><span>{esc(meta)}</span><p><b>Audit note:</b> {esc(shorten(note, 150))}<br /><b>Rights:</b> {esc(rights)}<br />{link}</p></div>')
    inner = f"""{top_line("SOURCE LEDGER", f"PRIMARY SOURCES / {page_index} OF {total_pages}")}
{headline("", "SOURCE LEDGER:", "Primary Sources, Visible And Dated", "23pt")}
{body("These rows are the audit trail for facts already summarized on the declared spreads. Use them to verify publisher, identity status, source role, rights state, and the URL that can reopen a claim. Manufacturer imagery remains an identity lead unless republication permission is documented.", "intro")}
<div class="ledger-grid">{"".join(items)}</div>"""
    return page(inner, page_number, "ledger-page")


def image_ledger_page(entries: list[Entry], page_number: int, page_index: int) -> str:
    chunks = entries[(page_index - 1) * 24: page_index * 24]
    items = []
    for entry in chunks:
        image = image_for(entry)
        path = str(image.relative_to(ROOT)) if image else "No local asset"
        label = "Observed exterior + conceptual detail" if entry.reference in TECHNICAL_ASSETS else "Interpretive / representative"
        items.append(f'<div class="image-row"><span class="ledger-code">p. {esc(str(CATEGORY_PAGE_MAP.get(entry.reference, "-")))}</span><strong>{esc(shorten(entry.category, 26))}</strong><span>{esc(label)}</span><span>{esc(path)}</span><em>OpenAI image generation</em></div>')
    inner = f"""{top_line("IMAGE LEDGER", f"PUBLIC PLATES / {page_index} OF 2")}
{headline("", "IMAGE LEDGER:", "Every Plate Has A Truth Label", "23pt")}
{body("Public product visuals are local original plates. The exact product source is linked for inspection; the plate is not presented as product photography or SKU evidence.", "intro")}
<div class="image-ledger">{"".join(items)}</div>
<div class="dark-callout"><span>RIGHTS RULE.</span> Source pages identify and help acquire a model. They do not automatically grant permission to republish the source photograph.</div>"""
    return page(inner, page_number, "ledger-page")


def prompt_page(title: str, intro: str, prompt_text: str, page_number: int, page_index: int) -> str:
    inner = f"""{top_line("IMAGE PROMPT RECORD", f"PROMPTS / {page_index} OF 3")}
{headline("", "IMAGE PROMPT RECORD:", title, "23pt")}
{body(intro, "intro")}
<pre class="prompt-box">{esc(prompt_text)}</pre>"""
    return page(inner, page_number, "prompt-page")


def release_page(page_number: int) -> str:
    gates = [
        ("01", "EXACT MODEL", "Normalize model, variant, region, price basis, and included parts."),
        ("02", "CANDIDATE PRESSURE", "Name serious rivals or document why a smaller field is honest."),
        ("03", "OWNERSHIP PROOF", "Add admission tests, failure modes, maintenance, permanence, parts, and service."),
        ("04", "INDEPENDENT TEST", "Use measured testing where a specification or visual inspection cannot settle the claim."),
        ("05", "RIGHTS REVIEW", "Clear every sourced image, quote, excerpt, and linked asset for the intended territory."),
        ("06", "ACCESSIBILITY", "Check captions, reading order, link labels, contrast, and tagged PDF structure."),
    ]
    inner = f"""{top_line("COMMERCIAL EDITION", "PRODUCTION GATES")}
{headline("", "COMMERCIAL RELEASE GATES:", "What Every Declared Category Needs First", "23pt")}
{body("The review edition is deliberately useful before it is commercially final. These gates turn a strong visual and editorial system into a defensible paid reference book.", "intro")}
{cards_grid([card(n, title, text) for n, title, text in gates])}
<div class="dark-callout"><span>STATE POLICY.</span> The storefront can sell the dossier before every open category is complete, but the book must keep state labels and update policy visible.</div>"""
    return page(inner, page_number, "method-page")


def rights_page(page_number: int) -> str:
    inner = f"""{top_line("RIGHTS AND SOURCES", "PLATO / DELTA / ORIGINAL ART")}
{headline("", "THE RIGHTS LEDGER:", "A Source Can Inform The Book Without Becoming Its Artwork", "23pt")}
{cards_grid([
    card("P", "PLATO PORTRAIT", "Silanion-type portrait from the Altes Museum, photographed by Osama Shukir Muhammed Amin, CC BY-SA 4.0. The adaptation keeps attribution and license with every full-size use."),
    card("Q", "PLATO QUOTES", "Benjamin Jowett translations from Project Gutenberg are public domain in the United States. Verify territory and edition status before commercial release elsewhere."),
    card("D", "DELTA REFERENCE", "Delta Power Tools 1940 is an information-design reference. Do not reproduce its wording, branding, page layouts, or artwork."),
    card("A", "ORIGINAL PLATES", "OpenAI-generated editorial interpretations are representative visual aids. They contain no logos, labels, packaging, or invented SKU claims."),
    card("S", "SOURCE PAGES", "Manufacturer and retailer pages are linked for identity, specifications, service, and purchase. Image republication requires a separate permission decision."),
    card("U", "UPDATE RECORD", "Every change gets an access date, source role, rights state, and a note explaining whether the ruling changed."),
])}
<div class="dark-callout"><span>RELEASE RULE.</span> If a source or license is uncertain, the uncertainty stays visible beside the claim until it is resolved.</div>"""
    return page(inner, page_number, "method-page")


def update_page(page_number: int) -> str:
    inner = f"""{top_line("MAINTENANCE OF THE BOOK", "CHANGE LOG / UPDATE POLICY")}
{headline("", "A LIVING REFERENCE:", "What Makes A Ruling Reopen", "23pt")}
{body("A durable recommendation is not a frozen slogan. The dossier records the trigger that would make the answer change and keeps the old state legible in the change log.", "intro")}
{cards_grid([
    card("01", "MODEL REVISION", "A new generation, size, voltage, region, or included accessory changes the Form."),
    card("02", "SERVICE CHANGE", "Parts, manuals, warranty, service centers, or repair economics become materially weaker or stronger."),
    card("03", "SAFETY NOTICE", "A recall, hazard, failure pattern, or regulatory change crosses a terminal threshold."),
    card("04", "MARKET SHIFT", "Price, availability, consumables, or used supply changes the value across the ownership horizon."),
    card("05", "BETTER CANDIDATE", "A rival clears the same admission gates and buys a meaningful advantage."),
    card("06", "EVIDENCE CORRECTION", "A source is withdrawn, contradicted, misidentified, or replaced by a stronger exact-model record."),
])}
<div class="dark-callout"><span>UPDATE NOTE.</span> A change log entry names the date, claim, old evidence, new evidence, affected pages, and whether the public verdict changed.</div>"""
    return page(inner, page_number, "method-page")


def navigation_page(page_number: int) -> str:
    inner = f"""{top_line("HOW TO USE THE BOOK", "READING PATH")}
{headline("Remember", "THE INDEX IS A MAP:", "The Spread Is The Argument", "23pt")}
{body("Use the category index to enter a ruling, then read its ownership page before treating the pick as settled. Follow the source link when a specification, service claim, or price matters to the decision.", "intro")}
{cards_grid([
    card("01", "FIND", "Use the alphabetical index or domain map. The page number is printed in the category row."),
    card("02", "READ", "Start with the Form and the truth label on the plate. The image shows what it can show."),
    card("03", "PRESS", "Read the named rival, failure mode, and admission gate. These are the pressure points."),
    card("04", "OWN", "Use the care cycle, parts path, and terminal threshold after purchase."),
    card("05", "VERIFY", "Open the source ledger when an exact model or current policy changes the answer."),
    card("06", "REOPEN", "Use the reconsideration trigger and change log when new evidence arrives."),
])}
<div class="dark-callout"><span>THE BOOK'S JOB.</span> Turn a short recommendation into a complete decision that remains useful after checkout.</div>"""
    return page(inner, page_number, "method-page")


def colophon_page(page_number: int) -> str:
    inner = f"""{top_line("PLATONIC IDEAL", "FULL REVIEW EDITION")}
{headline("", "THE FULL RUN:", "A Delta-Inspired Reference Book For Durable Objects", "25pt")}
<div class="colophon-grid">
  <div>
    <p class="colophon-number">196</p><p class="colophon-label">PAGES IN THIS REVIEW EDITION</p>
    <p class="colophon-number">100</p><p class="colophon-label">CATEGORY ENTRIES</p>
    <p class="colophon-number">48</p><p class="colophon-label">DECLARED OBJECTS</p>
  </div>
  <div class="keyline-box">
    <div class="box-title">EDITORIAL CONTRACT</div>
    <p class="body">The dossier earns its place beside the site when a reader can move from a short recommendation to a complete decision: what the object is, why it wins, what it will cost to own, how it fails, how it can be repaired, and what evidence would change the answer.</p>
    <div class="mini-rule">EVIDENCE - JUDGMENT - OWNERSHIP</div>
    <p class="tiny-note">Generated with scripts/build-dossier-delta.py. Site code and storefront visuals are unchanged by this PDF build.</p>
  </div>
</div>
<div class="dark-callout"><span>PLATO / REPUBLIC VI, 507B.</span> The many, as we say, are seen but not known, and the ideas are known but not seen.</div>"""
    return page(inner, page_number, "colophon-page")


def proof_edition_page(page_number: int) -> str:
    inner = f"""{top_line("20-PAGE DESIGN PROOF", "DELTA 1940 SYSTEM")}
{headline("How", "THE OBJECT PAGES:", "A Decision Page, An Ownership Page", "26pt")}
{body("This proof isolates the four declared spreads that define the new PDF direction. It uses the supplied Delta 1940 design system for typography, color, page anatomy, product plates, feature cards, candidate pressure, and ownership evidence.", "intro")}
<div class="declaration-key">
  <div><span class="red">01</span><strong>DECISION PAGE</strong><p>Form, exact model, representative plate, reasons, and the tradeoff that closes the ordinary search.</p></div>
  <div><span class="red">02</span><strong>OWNERSHIP PAGE</strong><p>Care cycle, failure map, candidate pressure, service path, sources, and the trigger that would reopen the ruling.</p></div>
</div>
{section_heading("FOUR DECLARED OBJECTS:", "The pages this design is built to carry", "18pt")}
{cards_grid([card("01", "FRYING PAN", "Lodge L10SK3. A recoverable cast-iron surface and a broad-use value ruling."), card("02", "SCREWDRIVER", "Wiha 26547. A simple hand-tool Form with a visible wear and replacement path."), card("03", "DRILL", "Makita 6302H. A corded platform whose service evidence must survive the page."), card("04", "HAMMER", "Estwing E3-16C. One-piece steel construction with an explicit grip question.")])}
<div class="dark-callout"><span>REVIEW ORDER.</span> Read the cover and method pages, then compare all four spreads for hierarchy, copy density, image truth labels, and ownership usefulness.</div>"""
    return page(inner, page_number, "method-page")


def proof_colophon_page(page_number: int) -> str:
    inner = f"""{top_line("PLATONIC IDEAL", "20-PAGE DESIGN PROOF")}
{headline("Why", "THIS DIRECTION:", "The Delta System Makes The Judgment Legible", "25pt")}
<div class="colophon-grid">
  <div>
    <p class="colophon-number">20</p><p class="colophon-label">PAGES IN THIS PROOF</p>
    <p class="colophon-number">04</p><p class="colophon-label">DECLARED OBJECT SPREADS</p>
    <p class="colophon-number">01</p><p class="colophon-label">VISUAL SYSTEM</p>
  </div>
  <div class="keyline-box">
    <div class="box-title">WHAT CHANGED</div>
    <p class="body">The PDF now follows the supplied 1940 catalog language: white stock, black and vermilion only, condensed gothic display type, serif body columns, keylined tables, red leader rules, truth-labeled plates, and the red footer bar with black page tab.</p>
    <div class="mini-rule">SITE STATUS</div>
    <p class="tiny-note">The storefront code and public site visual system were not changed by this proof build. This PDF is a separate print artifact.</p>
  </div>
</div>
<div class="dark-callout"><span>PLATO / REPUBLIC VI, 507B.</span> The many, as we say, are seen but not known, and the ideas are known but not seen.</div>"""
    return page(inner, page_number, "colophon-page")


REVIEW_IMAGES = {
    "plato_cover": ASSET_DIR / "editorial" / "plato-cover-portrait.png",
    "plato_quote": ASSET_DIR / "editorial" / "plato-quote-portrait.png",
    "plato_reader": ASSET_DIR / "editorial" / "plato-quote-portrait.png",
    "pan_plate": ASSET_DIR / "lodge-l10sk3-technical-plate.png",
    "pan_use": ASSET_DIR / "editorial" / "skillet-in-use.png",
    "drill_plate": ASSET_DIR / "makita-6302h-technical-plate.png",
    "drill_use": ASSET_DIR / "editorial" / "corded-drill-in-use.png",
    "hammer_plate": ASSET_DIR / "estwing-e3-16c-technical-plate.png",
    "hammer_use": ASSET_DIR / "editorial" / "hammer-in-use.png",
    "driver_plate": ASSET_DIR / "editorial" / "ph2-driver-plate.png",
    "driver_technical_plate": ASSET_DIR / "editorial" / "ph2-driver-technical-plate.png",
    "driver_use": ASSET_DIR / "editorial" / "ph2-driver-in-use.png",
}


def review_link(label: str, url: str, class_name: str = "text-link") -> str:
    return f'<a class="{class_name}" href="{html.escape(url, quote=True)}">{html.escape(label)}</a>'


def review_image(name: str, class_name: str, alt: str) -> str:
    path = REVIEW_IMAGES[name]
    if not path.exists():
        raise FileNotFoundError(f"Review image not found: {path}")
    return f'<img class="{class_name}" src="{path.resolve().as_uri()}" alt="{html.escape(alt, quote=True)}">'


def review_table(headers: list[str], rows: list[list[str]], class_name: str = "") -> str:
    head = "".join(f"<th>{html.escape(header)}</th>" for header in headers)
    body = "".join(
        "<tr>" + "".join(
            f"<td>{cell if cell.startswith('<a ') or cell.startswith('<span ') or '<br>' in cell else html.escape(cell)}</td>"
            for cell in row
        ) + "</tr>"
        for row in rows
    )
    return f'<table class="review-table {class_name}"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>'


def drill_parts_figure() -> str:
    return r'''<figure class="schematic drill-map" aria-label="Makita 6302H service parts map">
<svg viewBox="0 0 1000 250" role="img" aria-labelledby="drill-map-title drill-map-desc">
  <title id="drill-map-title">Makita 6302H service parts map</title>
  <desc id="drill-map-desc">Maker-listed power, motor, drive, and chuck parts, with their part numbers. This is a reading aid, not the maker’s exploded drawing.</desc>
  <defs><marker id="arrow-red" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 Z" fill="#C6231F"/></marker></defs>
  <path d="M73 80 H925" fill="none" stroke="#C6231F" stroke-width="2" marker-end="url(#arrow-red)"/>
  <circle cx="125" cy="80" r="7" fill="#C6231F"/><circle cx="375" cy="80" r="7" fill="#C6231F"/><circle cx="625" cy="80" r="7" fill="#C6231F"/><circle cx="875" cy="80" r="7" fill="#C6231F"/>
  <path d="M250 48 V218 M500 48 V218 M750 48 V218" fill="none" stroke="#aaa59d" stroke-width="1"/>
  <g fill="#191919" font-family="Arial, sans-serif" text-anchor="middle">
    <text x="125" y="35" font-size="19" font-weight="700" letter-spacing="1">POWER</text>
    <text x="125" y="119" font-size="18">Cord · 664064-4</text>
    <text x="125" y="144" font-size="18">Reverse switch · 651478-6</text>
    <text x="125" y="182" font-size="15" fill="#5f5b55">Grip assembly · 122593-8</text>

    <text x="375" y="35" font-size="19" font-weight="700" letter-spacing="1">MOTOR</text>
    <text x="375" y="119" font-size="18">Armature · 511836-7</text>
    <text x="375" y="144" font-size="18">Field · 633361-9</text>
    <text x="375" y="182" font-size="15" fill="#5f5b55">Brush set · 195005-4</text>

    <text x="625" y="35" font-size="19" font-weight="700" letter-spacing="1">DRIVE</text>
    <text x="625" y="119" font-size="18">Spindle · 324197-4</text>
    <text x="625" y="144" font-size="18">Gear housing · 151765-8</text>
    <text x="625" y="182" font-size="15" fill="#5f5b55">Bearings + gears listed</text>

    <text x="875" y="35" font-size="19" font-weight="700" letter-spacing="1">CHUCK</text>
    <text x="875" y="119" font-size="18">Chuck · 763145-2</text>
    <text x="875" y="144" font-size="18">Chuck key · 763434-5</text>
    <text x="875" y="182" font-size="15" fill="#5f5b55">Check the exact version</text>
  </g>
  <text x="500" y="238" text-anchor="middle" fill="#5f5b55" font-family="Arial, sans-serif" font-size="12">MAKER-LISTED PARTS · CONCEPT MAP, NOT AN EXPLODED VIEW</text>
</svg></figure>'''


def hammer_anatomy_figure() -> str:
    parts = [
        ("01", "STRIKING FACE", "Smooth round face drives common nails. Inspect for chips, dents, or mushrooming."),
        ("02", "CURVED CLAW", "The split claw withdraws common nails. A crack or spread is a stop sign."),
        ("03", "ONE-PIECE STEEL", "Head and handle are forged as one body; dents or cracks mean retire it."),
        ("04", "MOLDED GRIP", "The cobalt-blue grip controls the swing. Check for slip, splits, or separation."),
    ]
    key = "".join(
        f'<div class="hammer-anatomy-row"><b>{number}</b><div><strong>{html.escape(label)}</strong><p>{html.escape(copy)}</p></div></div>'
        for number, label, copy in parts
    )
    plate = review_image(
        "hammer_plate",
        "hammer-anatomy-plate",
        "Three exterior views and a grip section of a one-piece curved-claw hammer",
    )
    return f'''<figure class="hammer-anatomy" aria-label="Hammer construction shown in multiple exterior views">
  <div class="hammer-anatomy-art">{plate}<figcaption class="hammer-anatomy-caption">Main view · side elevation · grip section</figcaption></div>
  <div class="hammer-anatomy-key" aria-label="Labeled hammer sections">{key}</div>
</figure>'''


def screwdriver_anatomy_figure() -> str:
    parts = [
        ("01", "PH2 POINT", "Match the cross-point to the mark on the fastener."),
        ("02", "STEEL BLADE", "150 mm of reach; the full driver is 268 mm long."),
        ("03", "SOFTFINISH HANDLE", "36 mm across for controlled hand turning."),
        ("04", "HANDLE END", "A hanging hole for storage; this is a fixed-blade tool."),
    ]
    key = "".join(
        f'<div class="driver-anatomy-row"><b>{number}</b><div><strong>{html.escape(label)}</strong><p>{html.escape(copy)}</p></div></div>'
        for number, label, copy in parts
    )
    plate = review_image(
        "driver_technical_plate",
        "driver-anatomy-plate",
        "Four exterior views of a PH2 screwdriver: three-quarter view, side elevation, point close-up, and handle-end detail",
    )
    return f'''<figure class="driver-anatomy" aria-label="Screwdriver parts shown in four exterior views">
  <div class="driver-anatomy-art">{plate}<figcaption class="driver-anatomy-caption">Main view · side elevation · PH2 point · handle detail</figcaption></div>
  <div class="driver-anatomy-key" aria-label="Labeled screwdriver parts">{key}</div>
</figure>'''


def screwdriver_profile_figure() -> str:
    return r'''<figure class="schematic profile-match" aria-label="Match Phillips and Pozidriv profiles to the marked fastener">
<svg viewBox="0 0 1000 300" role="img" aria-labelledby="profile-match-title profile-match-desc">
  <title id="profile-match-title">Phillips and Pozidriv are different cross-recess profiles</title>
  <desc id="profile-match-desc">Two simplified top-view cross recess symbols labeled PH2 and PZ2. Read the fastener and driver markings; this drawing is not a size gauge.</desc>
  <g stroke="#191919" stroke-width="2">
    <path d="M166 59 H254 V124 H319 V212 H254 V277 H166 V212 H101 V124 H166 Z" fill="#eeeae3"/>
    <path d="M646 59 H734 V124 H799 V212 H734 V277 H646 V212 H581 V124 H646 Z" fill="#eeeae3"/>
  </g>
  <g stroke="#C6231F" stroke-width="8" stroke-linecap="round">
    <path d="M210 52 V284 M94 168 H326"/>
    <path d="M690 52 V284 M574 168 H806"/>
  </g>
  <g stroke="#C6231F" stroke-width="4" stroke-linecap="round">
    <path d="M614 91 L631 108 M749 91 L766 108 M614 245 L631 228 M749 245 L766 228"/>
  </g>
  <g fill="#191919" font-family="Arial, sans-serif" text-anchor="middle">
    <text x="210" y="27" font-size="19" font-weight="700" letter-spacing="1">PHILLIPS · PH2</text>
    <text x="690" y="27" font-size="19" font-weight="700" letter-spacing="1">POZIDRIV · PZ2</text>
    <text x="210" y="296" font-size="13" fill="#5f5b55">Use the driver marked PH2</text>
    <text x="690" y="296" font-size="13" fill="#5f5b55">Use the driver marked PZ2</text>
  </g>
  <path d="M500 66 V245" stroke="#aaa59d" stroke-width="1.5"/>
</svg></figure>'''


def review_page(page_number: int, left: str, right: str, content: str, class_name: str = "") -> str:
    return f"""<section class="review-page {class_name}">
  <div class="page-border" aria-hidden="true"></div>
  <div class="topline"><span>{left}</span><span>{right}</span></div>
  <main class="page-content">{content}</main>
  <div class="footer-rule" aria-hidden="true"></div>
  <footer class="folio"><span>PLATONIC IDEAL</span><i>THE GOOD BUY</i></footer>
  <div class="page-number">{page_number:02d}</div>
</section>"""


def review_css() -> str:
    return r"""
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=Roboto+Mono:wght@400;500&display=swap');
@page { size: Letter; margin: 0; }
:root { --red:#C6231F; --ink:#191919; --muted:#5f5b55; --line:#8d8983; --paper:#fff; --serif:'Source Serif 4',Georgia,serif; --sans:'Oswald','Arial Narrow',sans-serif; --mono:'Roboto Mono',monospace; }
* { box-sizing:border-box; }
html,body { margin:0; padding:0; color:var(--ink); background:var(--paper); }
body { font-family:var(--serif); -webkit-print-color-adjust:exact; print-color-adjust:exact; }
a { color:var(--ink); text-decoration-color:var(--red); text-decoration-thickness:1px; text-underline-offset:2px; }
.review-page { position:relative; width:8.5in; height:11in; padding:.49in .62in .7in; overflow:hidden; page-break-after:always; break-after:page; background:#fff; }
.review-page:last-child { page-break-after:auto; break-after:auto; }
.page-border { position:absolute; inset:.17in; border:.8pt solid #262626; pointer-events:none; }
.topline { position:relative; z-index:2; height:.28in; display:flex; justify-content:space-between; align-items:center; border-bottom:.8pt solid var(--ink); font:500 8pt var(--sans); letter-spacing:1.1px; text-transform:uppercase; }
.topline span { white-space:nowrap; flex:0 0 auto; }
.page-content { position:relative; z-index:1; height:9.38in; padding-top:.18in; }
.footer-rule { position:absolute; left:.17in; right:.17in; bottom:.17in; height:.105in; background:var(--red); }
.folio { position:absolute; left:.49in; right:.87in; bottom:.31in; height:.17in; display:flex; align-items:center; gap:.1in; font:500 8pt var(--sans); letter-spacing:1.1px; color:var(--ink); }
.folio i { font-style:normal; color:var(--red); }
.page-number { position:absolute; right:.17in; bottom:.17in; display:flex; align-items:center; justify-content:center; width:.48in; height:.37in; background:#171717; color:#fff; font:500 10pt var(--mono); z-index:3; }
.red { color:var(--red); }
.eyebrow { margin:0 0 .07in; font:500 9pt var(--sans); letter-spacing:1.4px; text-transform:uppercase; }
h1,h2,h3,p { margin-top:0; }
h1,h2,h3 { font-family:var(--sans); text-transform:uppercase; font-weight:600; }
h1 { margin:0; font-size:34pt; line-height:1.02; letter-spacing:.2px; }
h2 { margin:0 0 .08in; font-size:21pt; line-height:1.08; letter-spacing:.1px; }
h3 { margin:0 0 .07in; font-size:12pt; line-height:1.1; letter-spacing:.6px; }
.deck { font-size:13pt; line-height:1.32; margin:.12in 0 .13in; }
.small-copy { font-size:10.5pt; line-height:1.34; }
.tiny { font:7.5pt/1.28 var(--serif); color:var(--muted); }
.text-link { display:inline-block; margin:.02in .16in .02in 0; font:500 9pt var(--sans); letter-spacing:.4px; text-transform:uppercase; }
.buy-link { display:inline-block; padding:.08in .13in .07in; border-bottom:2px solid var(--red); font:600 10pt var(--sans); letter-spacing:.7px; text-decoration:none; text-transform:uppercase; }
.open-title { margin:0 0 .02in; }
.open-subtitle { font:500 10pt var(--sans); letter-spacing:1px; text-transform:uppercase; margin:0; color:#393939; }
.object-opener .deck { max-width:6.9in; margin:.1in 0 .08in; font-size:12.4pt; }
.open-art { width:100%; height:4.63in; object-fit:contain; display:block; margin:.01in 0 .06in; }
.open-meta { display:flex; justify-content:space-between; align-items:flex-start; gap:.2in; border-top:1px solid var(--ink); padding-top:.11in; }
.open-meta .buy-group { width:2.18in; padding-top:.04in; }
.fact-grid { flex:1; display:grid; grid-template-columns:repeat(4,1fr); gap:.06in .14in; }
.fact { border-bottom:.45pt solid #aaa; padding:0 .02in .055in; min-height:.46in; }
.fact b { display:block; font:600 15pt/1 var(--sans); margin-bottom:.035in; }
.fact span { display:block; font:8pt/1.18 var(--sans); letter-spacing:.2px; text-transform:uppercase; color:#56524e; }
.fit-layout { display:grid; grid-template-columns:3.52in 1fr; column-gap:.32in; align-items:start; }
.fit-layout.reverse { grid-template-columns:1fr 3.52in; }
.scene { width:100%; height:3.53in; object-fit:cover; display:block; }
.scene-tall { width:100%; height:5.05in; object-fit:cover; display:block; }
.section-label { margin:.11in 0 .055in; font:500 8.5pt var(--sans); color:var(--red); letter-spacing:1px; text-transform:uppercase; }
.ruled-list { margin:.02in 0 0; padding:0; list-style:none; }
.ruled-list li { border-top:.5pt solid #aaa; padding:.07in 0; font-size:10.5pt; line-height:1.27; }
.ruled-list b { font-family:var(--sans); text-transform:uppercase; font-size:9pt; letter-spacing:.35px; }
.review-table { width:100%; border-collapse:collapse; margin:.05in 0 .12in; font-size:9.6pt; line-height:1.26; }
.review-table th { text-align:left; vertical-align:bottom; font:500 8.5pt/1.1 var(--sans); text-transform:uppercase; letter-spacing:.6px; color:var(--red); padding:.06in .07in .06in 0; border-bottom:1.25pt solid var(--ink); }
.review-table td { vertical-align:top; padding:.065in .08in .065in 0; border-bottom:.45pt solid #aaa; }
.review-table td:first-child { font-weight:600; }
.review-table.compact { font-size:9.1pt; }
.review-table.compact td { padding:.055in .06in .055in 0; }
.note-rule { margin:.09in 0 0; padding:.08in 0 .03in .12in; border-left:2px solid var(--red); font-size:10pt; line-height:1.3; }
.cta-row { display:flex; flex-wrap:wrap; gap:.02in .1in; margin-top:.08in; }
.stat-line { display:flex; gap:.18in; align-items:baseline; border-top:.7pt solid var(--ink); margin:.11in 0 .13in; padding-top:.09in; }
.stat-line strong { font:600 15pt var(--sans); }
.stat-line span { font:8.2pt var(--sans); letter-spacing:.5px; text-transform:uppercase; color:#555; }
.split-title { display:flex; justify-content:space-between; align-items:baseline; border-bottom:1pt solid var(--ink); padding-bottom:.07in; margin-bottom:.1in; }
.split-title span { font:500 8pt var(--mono); color:var(--red); }
.tests { display:grid; grid-template-columns:1fr 1fr; column-gap:.28in; }
.test { display:grid; grid-template-columns:.42in 1fr; gap:.08in; border-top:.65pt solid var(--ink); padding:.15in .04in .14in 0; min-height:1.16in; }
.test-number { font:600 20pt/1 var(--sans); color:var(--red); }
.test h3 { margin:0 0 .04in; font-size:11.5pt; }
.test p { margin:0; font-size:10pt; line-height:1.28; }
.reader-path { margin:.26in auto 0; max-width:6.9in; padding:.14in .12in .09in; border-top:1.25pt solid var(--red); border-bottom:1.25pt solid var(--red); text-align:center; font-size:13pt; line-height:1.25; }
.reader-path span { font-family:var(--sans); font-size:16pt; letter-spacing:.6px; text-transform:uppercase; }
.cover .page-content { height:9.48in; padding:0; }
.cover-art { position:absolute; top:.23in; right:.02in; width:4.68in; height:8.85in; object-fit:cover; object-position:68% 50%; }
.cover-copy { position:absolute; z-index:2; left:.2in; top:.78in; width:4.16in; }
.cover-brand { margin:0 0 .52in; color:var(--red); font:600 13pt var(--sans); letter-spacing:2px; }
.cover-label { margin:0 0 .13in; font:500 9.5pt var(--sans); letter-spacing:1.2px; }
.cover h1 { font-size:36pt; line-height:1.05; margin:0; background:#fff; display:table; padding-right:.06in; }
.cover-deck { max-width:3.18in; margin:.23in 0 0; font-size:15pt; line-height:1.25; }
.cover-list { margin-top:.34in; padding-top:.12in; border-top:1pt solid var(--ink); width:3.2in; font:500 9pt/1.75 var(--sans); letter-spacing:.35px; text-transform:uppercase; }
.cover-date { position:absolute; left:.2in; bottom:.26in; z-index:2; font:500 8pt var(--mono); }
.quote-layout { height:8.75in; display:grid; grid-template-columns:3.08in 1fr; gap:.28in; align-items:stretch; }
.quote-photo { height:100%; overflow:hidden; }
.quote-photo img { width:100%; height:100%; object-fit:cover; object-position:33% 45%; filter:grayscale(100%) contrast(1.04); display:block; }
.quote-copy { padding:.18in .02in 0 0; display:flex; flex-direction:column; }
.quote-copy .quote-label { font:500 9pt var(--sans); letter-spacing:1px; text-transform:uppercase; color:var(--red); margin:0 0 .22in; }
.quote-copy blockquote { margin:0; font-size:15.2pt; line-height:1.36; }
.quote-copy .quote-attr { margin-top:auto; border-top:1pt solid var(--ink); padding-top:.09in; font:500 8.7pt var(--sans); letter-spacing:.7px; text-transform:uppercase; }
.index-heading { margin:.08in 0 .25in; font-size:31pt; }
.index-note { margin:0 0 .16in; max-width:5in; font-size:11pt; }
.index-list { margin:.06in 0 0; }
.index-row { display:flex; align-items:baseline; border-top:1pt solid var(--ink); padding:.18in 0 .16in; font:500 21pt var(--sans); text-transform:uppercase; letter-spacing:.5px; }
.index-row span:first-child { flex:1; }
.index-row .dots { flex:1; border-bottom:.7pt dotted #777; margin:0 .12in .1in; }
.index-row span:last-child { font:500 13pt var(--mono); color:var(--red); }
.value-layout { display:grid; grid-template-columns:2.45in 1fr; gap:.25in; height:8.45in; }
.value-image { width:100%; height:100%; object-fit:cover; object-position:62% 50%; display:block; }
.value-rows { margin:.04in 0 0; }
.value-row { display:grid; grid-template-columns:1.55in 1fr; gap:.14in; padding:.12in 0; border-top:.8pt solid var(--ink); }
.value-row strong { font:600 10pt var(--sans); text-transform:uppercase; letter-spacing:.5px; }
.value-row p { margin:0; font-size:10pt; line-height:1.28; }
.source-columns { display:grid; grid-template-columns:1fr 1fr; gap:.26in; }
.source-group { margin:0 0 .12in; padding-top:.055in; border-top:.8pt solid var(--ink); }
.source-group h3 { color:var(--red); margin:.03in 0 .05in; font-size:9.5pt; letter-spacing:.8px; }
.source-group ul { list-style:none; padding:0; margin:0; }
.source-group li { font-size:9.8pt; line-height:1.3; padding:.035in 0; }
.source-group a { font-family:var(--serif); font-size:9.8pt; font-weight:600; }
.glossary-rows { margin:.05in 0 0; }
.glossary-row { display:grid; grid-template-columns:1.58in 1fr; gap:.16in; border-top:.75pt solid var(--ink); padding:.09in 0; }
.glossary-row strong { font:600 9.5pt var(--sans); letter-spacing:.4px; text-transform:uppercase; }
.glossary-row p { margin:0; font-size:10pt; line-height:1.3; }
.correction { margin:.12in 0 0; padding:.09in 0 .06in .13in; border-left:2px solid var(--red); font-size:9.3pt; line-height:1.28; }
.parts-path { display:grid; grid-template-columns:1fr .2in 1fr .2in 1fr .2in 1fr .2in 1fr; align-items:center; gap:.02in; text-align:center; margin:.04in 0 .11in; border-top:.75pt solid var(--ink); border-bottom:.75pt solid var(--ink); padding:.1in 0; }
.parts-path span { font:500 8.5pt/1.12 var(--sans); text-transform:uppercase; letter-spacing:.3px; }
.parts-path small { display:block; font:7.6pt/1.2 var(--serif); text-transform:none; letter-spacing:0; color:var(--muted); margin-top:.035in; }
.parts-path b { color:var(--red); font:500 12pt var(--sans); }
.scene-wide { width:100%; height:4.75in; object-fit:contain; display:block; }
.hammer-copy-grid { display:grid; grid-template-columns:1fr 1fr; gap:.27in; margin-top:.08in; }
.schematic { margin:.08in 0 .13in; }
.schematic svg { width:100%; display:block; overflow:visible; }
.drill-map svg { height:2.15in; }
.profile-match svg { height:1.63in; }
.hammer-anatomy { display:grid; grid-template-columns:4.65in 1fr; gap:.16in; align-items:center; margin:.04in 0 .11in; }
.hammer-anatomy-art { margin:0; min-width:0; }
.hammer-anatomy-plate { width:100%; aspect-ratio:4 / 3; object-fit:contain; display:block; }
.hammer-anatomy-caption { margin:.035in 0 0; border-top:.7pt solid var(--ink); padding-top:.045in; color:var(--muted); font:500 7.5pt var(--sans); letter-spacing:.45px; text-transform:uppercase; }
.hammer-anatomy-key { border-top:.8pt solid var(--ink); }
.hammer-anatomy-row { display:grid; grid-template-columns:.31in 1fr; gap:.07in; align-items:start; border-bottom:.65pt solid #aaa; padding:.08in 0; }
.hammer-anatomy-row b { color:var(--red); font:600 14pt/1 var(--sans); }
.hammer-anatomy-row strong { display:block; font:600 8.3pt/1.1 var(--sans); letter-spacing:.35px; text-transform:uppercase; }
.hammer-anatomy-row p { margin:.025in 0 0; font-size:8.6pt; line-height:1.17; }
.driver-anatomy { display:grid; grid-template-columns:4.55in 1fr; gap:.15in; align-items:center; margin:.04in 0 .08in; }
.driver-anatomy-art { margin:0; min-width:0; }
.driver-anatomy-plate { width:100%; aspect-ratio:4 / 3; object-fit:contain; display:block; }
.driver-anatomy-caption { margin:.035in 0 0; border-top:.7pt solid var(--ink); padding-top:.045in; color:var(--muted); font:500 7.5pt var(--sans); letter-spacing:.45px; text-transform:uppercase; }
.driver-anatomy-key { border-top:.8pt solid var(--ink); }
.driver-anatomy-row { display:grid; grid-template-columns:.31in 1fr; gap:.07in; align-items:start; border-bottom:.65pt solid #aaa; padding:.085in 0; }
.driver-anatomy-row b { color:var(--red); font:600 14pt/1 var(--sans); }
.driver-anatomy-row strong { display:block; font:600 8.4pt/1.1 var(--sans); letter-spacing:.4px; text-transform:uppercase; }
.driver-anatomy-row p { margin:.025in 0 0; font-size:8.7pt; line-height:1.18; }
.object-gallery { display:grid; grid-template-columns:repeat(4,1fr); gap:.16in; margin:.22in 0 0; border-top:1pt solid var(--ink); padding-top:.15in; }
.object-gallery figure { margin:0; }
.object-gallery img { width:100%; height:1.65in; object-fit:contain; display:block; }
.object-gallery figcaption { border-top:.6pt solid #aaa; padding-top:.06in; font:500 9pt var(--sans); letter-spacing:.6px; text-transform:uppercase; }
.source-finish { margin-top:.12in; font-size:9.8pt; line-height:1.32; }
.pan-checks { margin-top:.02in; }
.page-content > .section-label:first-child { margin-top:.08in; }
@media print { html,body { width:8.5in; } .review-page { margin:0; } }
"""


def build_proof_html(entries: list[Entry]) -> str:
    """Build the 20-page illustrated review edition of the four selected objects."""
    link = review_link
    img = review_image
    table = review_table
    pages: list[str] = []

    pages.append(review_page(1, "PLATONIC IDEAL", "THE DURABLE OBJECT FILES", f"""
<div class="cover-copy">
  <p class="cover-brand">PLATONIC IDEAL</p>
  <p class="cover-label">A BUYING GUIDE</p>
  <h1>THE DURABLE<br>OBJECT FILES</h1>
  <p class="cover-deck">Four everyday objects. Clear picks. The details you need before you buy—and after.</p>
  <div class="cover-list">DRILL&nbsp;&nbsp; / &nbsp;&nbsp;FRYING PAN<br>HAMMER&nbsp;&nbsp; / &nbsp;&nbsp;SCREWDRIVER</div>
</div>
<p class="cover-date">REVIEW EDITION&nbsp;&nbsp; • &nbsp;&nbsp;SEPTEMBER 2026</p>
{img("plato_cover", "cover-art", "Original editorial portrait of Plato") }
""", "cover"))

    pages.append(review_page(2, "PLATO", "REPUBLIC • BOOK VI", f"""
<div class="quote-layout">
  <div class="quote-photo">{img("plato_quote", "", "Original editorial portrait of Plato, showing both eyes")}</div>
  <div class="quote-copy">
    <p class="quote-label">A THING IS MORE THAN ITS APPEARANCE</p>
    <blockquote>“The old story, that there is a many beautiful and a many good, and so of other things which we describe and define; to all of them the term ‘many’ is applied.<br><br>‘True,’ he said.<br><br>‘And there is an absolute beauty and an absolute good, and of other things to which the term “many” is applied there is an absolute; for they may be brought under a single idea, which is called the essence of each.’<br><br>‘Very true.’<br><br>‘The many, as we say, are seen but not known, and the ideas are known but not seen.’<br><br>‘Exactly.’”</blockquote>
    <p class="quote-attr">PLATO&nbsp;&nbsp; / &nbsp;&nbsp;REPUBLIC VI, 507B</p>
  </div>
</div>
""", "quote-page"))

    pages.append(review_page(3, "INDEX", "FOUR OBJECTS", """
<p class="eyebrow red">START HERE</p>
<h1 class="index-heading">The field index</h1>
<p class="index-note">Each chapter gives you the pick, the tradeoffs, the care routine, and the links to check before purchase.</p>
<div class="index-list">
  <div class="index-row"><span>Drill</span><i class="dots"></i><span>05</span></div>
  <div class="index-row"><span>Frying Pan</span><i class="dots"></i><span>08</span></div>
  <div class="index-row"><span>Hammer</span><i class="dots"></i><span>11</span></div>
  <div class="index-row"><span>Screwdriver</span><i class="dots"></i><span>14</span></div>
</div>
""", "index-page"))

    tests = [
        ("FIT", "Will it do your everyday job?", "Name the size, material, load, reach, and setting before comparing brands."),
        ("FORM", "What is holding it together?", "Count the working joints, wear layers, coatings, and parts that can loosen or age."),
        ("RECOVERY", "What can you fix?", "Check which wear is routine, which damage can be restored, and which means replacement."),
        ("SUPPLY", "Can you get the important parts?", "A parts drawing helps. Current stock, service, and regional support decide whether repair is real."),
        ("OWNERSHIP", "What will it ask of you?", "Care, safe handling, storage, and consumables are part of the purchase price."),
        ("VALUE", "What does the upgrade buy?", "Pay more only when the lighter weight, better fit, extra control, or longer service matters to you."),
    ]
    tests_html = "".join(
        f'<article class="test"><span class="test-number">{i:02d}</span><div><h3>{html.escape(title)}</h3><p>{html.escape(copy)}</p></div></article>'
        for i, (title, _, copy) in enumerate(tests, 1)
    )
    pages.append(review_page(4, "THE DECISION", "SIX TESTS", f"""
<p class="eyebrow red">READ THIS BEFORE THE PICKS</p>
<h1 style="margin-bottom:.12in">Six tests before a declaration</h1>
<p class="deck" style="max-width:6.7in">A good product makes the job easier. A great buy still makes sense when it wears, needs care, or has to be repaired.</p>
<div class="tests">{tests_html}</div>
<p class="note-rule">Use the chapter pages in order: what it is, what changes the decision, then what ownership looks like.</p>
""", "tests-page"))

    pages.append(review_page(5, "DRILL", "DECISION • EXACT MODEL", f"""
<div class="object-opener">
  <p class="eyebrow red">THE PICK</p>
  <h1 class="open-title">Drill</h1>
  <p class="open-subtitle">Makita 6302H&nbsp; / &nbsp;1/2-inch low-speed corded drill</p>
  <p class="deck">Choose it when controlled speed and wall power matter more than cordless convenience. The 0–550 rpm ceiling is the point—not a spec to overlook.</p>
</div>
{img("drill_plate", "open-art", "Editorial technical study of a low-speed corded drill and its supplied accessories")}
<div class="open-meta">
  <div class="fact-grid">
    <div class="fact"><b>0–550</b><span>rpm, variable</span></div>
    <div class="fact"><b>6.5 A</b><span>motor</span></div>
    <div class="fact"><b>1/2 in</b><span>steel capacity</span></div>
    <div class="fact"><b>1⅜ in</b><span>wood capacity</span></div>
    <div class="fact"><b>4.8 lb</b><span>net weight</span></div>
    <div class="fact"><b>11¼ in</b><span>overall length</span></div>
    <div class="fact"><b>Keyed</b><span>1/2 in chuck</span></div>
    <div class="fact"><b>1 year</b><span>limited warranty</span></div>
  </div>
  <div class="buy-group">
    <p class="small-copy">Side handle, chuck, and key are included. Maker rates it for steel to 1/2 inch and wood to 1⅜ inches.</p>
    <div class="cta-row">{link("Makita product page", "https://makitatools.com/products/details/6302H", "buy-link")}</div>
  </div>
</div>
""", "object-page"))

    pages.append(review_page(6, "DRILL", "FIT • SPEED • ALTERNATIVES", f"""
<div class="split-title"><h2>When slow is the feature</h2><span>MAKITA 6302H</span></div>
<div class="fit-layout">
  <div>{img("drill_use", "scene", "Illustrative scene of a corded drill boring wood with a side handle")}</div>
  <div>
    <p class="deck" style="margin-top:0">The 6302H tops out at 550 rpm. That gives you a controlled pace for work that benefits from lower speed; it will feel slow when the job rewards fast, repeated holes.</p>
    <p class="small-copy">The listed wood and steel capacities set the boundary. The large keyed chuck grips standard round-shank bits; use the side handle when the work calls for added control.</p>
    <p class="note-rule">If your holes are mostly small and repetitive, buy for the speed you will use every day. A lower top speed cannot be added later.</p>
  </div>
</div>
<p class="section-label">Same family, more speed</p>
{table(["MODEL", "SPEED", "MOTOR", "CAPACITY", "WHAT CHANGES"], [
  ["Makita 6302H", "0–550 rpm", "6.5 A", "Steel 1/2 in<br>Wood 1⅜ in", "Shorter, lower-speed tool; metal gear housing"],
  ["Makita DP4000", "0–950 rpm", "7 A", "Steel 1/2 in<br>Wood 1½ in", "More speed and slightly more wood capacity; aluminum gear housing"],
], "compact")}
<div class="cta-row">{link("6302H maker specs", "https://makitatools.com/products/details/6302H", "text-link")} {link("DP4000 maker specs", "https://makitatools.com/products/details/DP4000", "text-link")}</div>
""", "object-page"))

    pages.append(review_page(7, "DRILL", "CARE • PARTS • SERVICE", f"""
<p class="eyebrow red">A REPAIR LEAD, NOT A PROMISE</p>
<h2>Makita publishes the parts.<br>Confirm the version and the bill.</h2>
<p class="deck">The 6302H breakdown lists the motor, gear train, spindle, chuck, switches, cord, and handle. These IDs come from Makita’s 2022 sheet; check the tool’s nameplate and current stock before ordering.</p>
{drill_parts_figure()}
<p class="section-label">If something changes, start here</p>
{table(["WHAT HAPPENS", "NEXT STEP", "MAKER-LISTED PARTS"], [
  ["The cord is damaged or power cuts in and out.", "Stop using it. Ask a service center to inspect the cord and switch.", "Cord 664064-4 · reversing switch 651478-6"],
  ["The chuck slips or will not hold the bit.", "Check the manual, then verify the model version before ordering.", "Chuck 763145-2 · chuck key 763434-5"],
  ["It runs hot, grinds, or loses power.", "Unplug it. Get a repair estimate before the next job.", "Brush set 195005-4 · bearings and gears listed separately"],
], "compact")}
<p class="note-rule">The parts drawing tells you what Makita names. It does not confirm live stock or make a repair economical. Makita lists parts through dealers and offers factory service; ask for the total before you decide.</p>
<div class="cta-row">{link("6302H manual", "https://cdn.makitatools.com/apps/cms/doc/prod/630/754466c3-a9fa-4c16-9a99-014d3dfc2fdf_6302H_IM.pdf", "text-link")} {link("Makita parts breakdown", "https://cdn.makitatools.com/apps/cms/doc/prod/630/a0fea8d2-c31f-4810-ab22-a2ff5e3ecc98_6302H_PB.pdf", "text-link")} {link("Find service or order parts", "https://makitatools.com/service/faq", "text-link")} {link("Direct Repair", "https://makitatools.com/service/directrepair", "text-link")}</div>
""", "object-page"))

    pages.append(review_page(8, "FRYING PAN", "DECISION • EXACT MODEL", f"""
<div class="object-opener">
  <p class="eyebrow red">THE PICK</p>
  <h1 class="open-title">Frying Pan</h1>
  <p class="open-subtitle">Lodge L10SK3&nbsp; / &nbsp;12-inch seasoned cast iron</p>
  <p class="deck">The value pick for a kitchen that wants one pan for stovetop, oven, grill, or campfire. It is simple, widely available, and heavy enough to make lifting part of the decision.</p>
</div>
{img("pan_plate", "open-art", "Editorial technical study of a cast-iron skillet with side and underside views")}
<div class="open-meta">
  <div class="fact-grid">
    <div class="fact"><b>$29.90</b><span>sale price snapshot</span></div>
    <div class="fact"><b>$37.95</b><span>regular price</span></div>
    <div class="fact"><b>7.69 lb</b><span>manufacturer weight</span></div>
    <div class="fact"><b>18 in</b><span>full length</span></div>
    <div class="fact"><b>12.56 in</b><span>overall width</span></div>
    <div class="fact"><b>9.12 in</b><span>flat bottom</span></div>
    <div class="fact"><b>Seasoned</b><span>vegetable oil surface</span></div>
    <div class="fact"><b>Any heat</b><span>stove, oven, grill, fire</span></div>
  </div>
  <div class="buy-group">
    <p class="small-copy">Price checked 15 Sep 2026; sale pricing can change. Lodge lists induction compatibility and a ready-to-cook seasoned surface.</p>
    <div class="cta-row">{link("Shop Lodge L10SK3", "https://www.lodgecastiron.com/products/round-cast-iron-classic-skillet?variant=51685752242548", "buy-link")}</div>
  </div>
</div>
""", "object-page"))

    pages.append(review_page(9, "FRYING PAN", "FIT • HEAT • HANDLING", f"""
<div class="split-title"><h2>Measure the part that touches the stove</h2><span>9.12 IN FLAT BOTTOM</span></div>
{img("pan_use", "scene-tall", "Illustrative cast-iron skillet cooking a meal on a home stove")}
<div class="fit-layout reverse" style="margin-top:.12in">
  <div>
    <p class="deck" style="margin-top:0">“12 inch” describes the pan’s nominal size. The flat bottom is 9.12 inches; the full width is 12.56 inches and the handle brings the length to 18 inches.</p>
    <p class="small-copy">Check your largest burner and storage space against those three measurements. At 7.69 pounds before food, the helper handle is functional, not decorative.</p>
  </div>
  <div>
    <p class="section-label" style="margin-top:0">It is a strong fit when…</p>
    <ul class="ruled-list">
      <li>You want one pan that moves from stove to oven or open fire.</li>
      <li>You will preheat gradually and clean, dry, and oil it after cooking.</li>
      <li>You can lift the full pan safely while it is hot and loaded.</li>
    </ul>
  </div>
</div>
<div class="cta-row">{link("Lodge dimensions and product page", "https://www.lodgecastiron.com/products/round-cast-iron-classic-skillet?variant=51685752242548", "text-link")} {link("Lodge cleaning guide", "https://www.lodgecastiron.com/pages/how-to-clean", "text-link")}</div>
""", "object-page"))

    pages.append(review_page(10, "FRYING PAN", "CARE • SHORTLIST", f"""
<p class="eyebrow red">CARE THAT TAKES A FEW MINUTES</p>
<h2>Wash. Dry. Wipe on a little oil.</h2>
{table(["WASH", "DRY", "OIL"], [
  ["Warm, soapy water and a brush. Skip soaking and the dishwasher.", "Towel-dry. Use low heat if water remains.", "Rub on a very thin film over the whole pan. Extra oil turns tacky."],
], "compact")}
<p class="section-label">Fix the surface; keep the pan</p>
{table(["WHAT YOU SEE", "WHAT IT MEANS", "HOW TO RECOVER"], [
  ["Rust spots", "Moisture reached the iron.", "Scour with steel wool or a rust eraser; wash, dry, and add a thin coat of oil. Reseason if rust is extensive."],
  ["Sticky, gummy finish", "Too much oil is sitting on the surface, or it has not baked fully.", "Bake the pan upside down at 450–500°F for one hour; let it cool in the oven."],
  ["Black flakes or a dull finish", "The seasoning is breaking down, or cooking burned off the oil.", "Wash and scrub; dry, apply a thin coat of oil, and bake for one hour. Lodge says the flakes are carbonized oil, not harmful to the pan or you."],
], "compact pan-checks")}
<p class="section-label">Four credible 12-inch choices</p>
{table(["MODEL", "WEIGHT / FOOTPRINT", "BUY IT FOR"], [
  [link("Lodge L10SK3", "https://www.lodgecastiron.com/products/round-cast-iron-classic-skillet?variant=51685752242548", "row-link"), "7.69 lb<br>12.56 in wide<br>9.12 in base", "Lowest entry price; broad heat compatibility."],
  [link("Victoria Traditional 12", "https://victoriacookware.com/products/12-skillet", "row-link"), "6.7 lb<br>20.5 × 13.3 in<br>2.8 in deep", "A little lighter and deeper; similar entry price."],
  [link("Field No. 10", "https://fieldcompany.com/products/no-10-cast-iron-skillet", "row-link"), "6.0 lb<br>11⅝ in rim<br>9¾ in cooking", "Lighter with a machined-smooth cooking surface."],
  [link("Stargazer 12", "https://stargazercastiron.com/products/12-inch-cast-iron-skillet", "row-link"), "6.5 lb<br>12 in rim<br>9.4 in cooking", "Flared rim and stay-cool handle; premium price, marked sold out on the check date."],
], "compact")}
<p class="tiny">Price snapshots for Lodge, Victoria, and Stargazer were checked 15 Sep 2026. Field’s current price is on its linked product page. Measure your burner against the flat base before choosing.</p>
<div class="cta-row">{link("Lodge care and restoration", "https://www.lodgecastiron.com/pages/how-to-clean", "text-link")} {link("Fix rust, flakes, and sticky seasoning", "https://www.lodgecastiron.com/pages/cleaning-and-care-cast-iron-troubleshooting", "text-link")} {link("Compare pan sizes", "https://www.lodgecastiron.com/blogs/story/what-size-cast-iron-skillet-do-i-need", "text-link")}</div>
""", "object-page"))

    pages.append(review_page(11, "HAMMER", "DECISION • EXACT MODEL", f"""
<div class="object-opener">
  <p class="eyebrow red">THE PICK</p>
  <h1 class="open-title">Hammer</h1>
  <p class="open-subtitle">Estwing E3-16C&nbsp; / &nbsp;16-ounce curved-claw steel</p>
  <p class="deck">A compact everyday hammer with a head and handle forged as one piece. The steel core is straightforward; the molded grip is the part to watch over time.</p>
</div>
{img("hammer_plate", "open-art", "Editorial technical study of a one-piece curved-claw hammer with grip detail")}
<div class="open-meta">
  <div class="fact-grid">
    <div class="fact"><b>16 oz</b><span>head weight</span></div>
    <div class="fact"><b>13 in</b><span>overall length</span></div>
    <div class="fact"><b>1 piece</b><span>forged head + handle</span></div>
    <div class="fact"><b>Smooth</b><span>striking face</span></div>
  </div>
  <div class="buy-group">
    <p class="small-copy">Estwing specifies a polished, one-piece steel body and a blue molded grip. The maker’s vibration-reduction wording is a manufacturer claim, not an independent test result.</p>
    <div class="cta-row">{link("Estwing E3-16C product page", "https://www.estwing.com/product/claw-hammer/", "buy-link")}</div>
  </div>
</div>
""", "object-page"))

    pages.append(review_page(12, "HAMMER", "FIT • CONTROL • USE", f"""
<div class="split-title"><h2>Good for controlled hand work</h2><span>16 OZ • 13 IN</span></div>
{img("hammer_use", "scene-wide", "Illustrative hammer use driving and pulling a nail at a workbench")}
<div class="hammer-copy-grid">
  <div>
    <p class="deck" style="margin-top:0">The 16-ounce head, smooth face, and curved claw cover ordinary nailing and nail pulling. The 13-inch length keeps the tool compact and close to the work.</p>
    <p class="small-copy">That compact feel is the trade. If framing or heavy demolition is your daily work, compare a longer, heavier hammer built for that job before you buy.</p>
  </div>
  <div>
    <p class="section-label" style="margin-top:0">Three things to check in your hand</p>
    <ul class="ruled-list">
      <li><b>Grip:</b> it should feel secure, with no slip or separation.</li>
      <li><b>Face:</b> keep it clean, smooth, and square to the nail.</li>
      <li><b>Claw:</b> choose the curved form for pulling common nails, not demolition leverage.</li>
    </ul>
  </div>
</div>
<div class="cta-row">{link("Estwing exact model and dimensions", "https://www.estwing.com/product/claw-hammer/", "text-link")}</div>
""", "object-page"))

    pages.append(review_page(13, "HAMMER", "CARE • ALTERNATIVES", f"""
<p class="eyebrow red">USE IT AS A NAIL HAMMER</p>
<h2>Know when to stop using it.</h2>
<p class="deck">Estwing says its nail hammers are for driving and withdrawing common nails. Wear safety glasses; bystanders should wear them too. Never strike hardened tools or objects with this hammer.</p>
{hammer_anatomy_figure()}
{table(["CHECK", "KEEP USING IT WHEN…", "RETIRE IT WHEN…"], [
  ["Face and claw", "The face is smooth; the claw has no cracks.", "The face is chipped, dented, or mushroomed; the claw is cracked."],
  ["Steel handle", "The handle has no dents or cracks.", "You find a dent or crack in the handle."],
  ["Molded grip", "It stays secure and comfortable in your hand.", "It slips, splits, or separates from the steel."],
], "compact")}
<p class="section-label">At the same weight, other features may fit better</p>
{table(["MODEL", "WHAT CHANGES", "A BETTER FIT IF…"], [
  [link("Estwing E3-16C", "https://www.estwing.com/product/claw-hammer/", "row-link"), "Forged steel body; molded blue grip; 13 in.", "You want a one-piece steel hammer for common nails."],
  [link("DEWALT DWHT51002", "https://www.dewalt.com/en-us/product/dwht51002/16-oz-curved-claw-steel-hammer", "row-link"), "One-piece steel; side nail puller and magnetic nail starter.", "Those nail-handling features save time in your work."],
  [link("Estwing SSCF16C", "https://www.estwing.com/product/curved-claw-hammer-carbon-fiber/", "row-link"), "Carbon-fiber handle; 16 oz; 13.25 in.", "You prefer a different handle material."],
], "compact")}
<div class="cta-row">{link("Estwing safety and care", "https://www.estwing.com/resources/safety-and-product-care/", "text-link")} {link("Estwing warranty", "https://www.estwing.com/resources/warranty/", "text-link")} {link("DEWALT specifications", "https://www.dewalt.com/en-us/product/dwht51002/16-oz-curved-claw-steel-hammer", "text-link")}</div>
""", "object-page"))

    pages.append(review_page(14, "SCREWDRIVER", "DECISION • EXACT MODEL", f"""
<div class="object-opener">
  <p class="eyebrow red">THE PICK</p>
  <h1 class="open-title">Screwdriver</h1>
  <p class="open-subtitle">Wiha SoftFinish 27758&nbsp; / &nbsp;PH2 × 150 mm</p>
  <p class="deck">A fixed Phillips driver for the common PH2 screw when you want a full-size handle and a longer blade. Match the tip to the screw; the wrong cross-point still slips.</p>
</div>
{img("driver_plate", "open-art", "Editorial product illustration of a PH2 screwdriver and its cross-point tip")}
<div class="open-meta">
  <div class="fact-grid">
    <div class="fact"><b>PH2</b><span>Phillips tip</span></div>
    <div class="fact"><b>150 mm</b><span>visible blade</span></div>
    <div class="fact"><b>268 mm</b><span>overall length</span></div>
    <div class="fact"><b>6 mm</b><span>blade diameter</span></div>
    <div class="fact"><b>36 mm</b><span>handle diameter</span></div>
    <div class="fact"><b>103 g</b><span>maker-listed weight</span></div>
    <div class="fact"><b>Chrome</b><span>vanadium-molybdenum steel</span></div>
    <div class="fact"><b>$12.09</b><span>TME price snapshot</span></div>
  </div>
  <div class="buy-group">
    <p class="small-copy">Wiha lists DIN ISO 8764-PH and marks this model for dry applications. TME price and stock checked 15 Sep 2026.</p>
    <div class="cta-row">{link("Wiha exact model", "https://wiha.com/tools/screwdrivers/mechanic-s-screwdrivers/softfinish/phillips/screwdriver-softfinish/27758", "buy-link")}</div>
    <div class="cta-row">{link("Check TME price and stock", "https://www.tme.com/us/en-us/details/wiha.27758/standard-screwdrivers/wiha/27758/", "text-link")}</div>
  </div>
</div>
""", "object-page"))

    pages.append(review_page(15, "SCREWDRIVER", "FIT • LENGTH • ALTERNATIVES", f"""
<div class="split-title"><h2>Know the point. Check the reach.</h2><span>PH2 IS NOT EVERY CROSS-POINT</span></div>
<p class="deck">Wiha 27758 pairs a PH2 tip with a 150 mm blade and a 36 mm handle. It reaches farther than a 100 mm driver; leave room to turn, and use a PZ tip for Pozidriv screws.</p>
{screwdriver_anatomy_figure()}
{table(["MODEL", "TIP / BLADE", "OVERALL SIZE", "WHAT IT BUYS"], [
  [link("Wiha 27758", "https://wiha.com/tools/screwdrivers/mechanic-s-screwdrivers/softfinish/phillips/screwdriver-softfinish/27758", "row-link"), "PH2<br>150 mm", "268 mm", "Selected longer reach; 6 mm round blade."],
  [link("Wiha 00759", "https://wiha.com/tools/screwdrivers/mechanic-s-screwdrivers/softfinish/phillips/screwdriver-softfinish/00759", "row-link"), "PH2<br>100 mm", "218 mm", "Same family; shorter reach for tighter clearance."],
  [link("Wera 350 PH", "https://www.wera.de/en/05008723001", "row-link"), "PH2<br>150 mm", "255 mm", "Same blade length; laser-tip and Kraftform handle."],
  [link("Klein 603-4", "https://www.kleintools.com/catalog/fixed-blade-screwdrivers/2-phillips-screwdriver-4-inch-round-shank", "row-link"), "#2 Phillips<br>4 in / 101.6 mm", "8.25 in / 210 mm", "Shorter shaft; cushion grip and U.S.-made listing."],
], "compact")}
<p class="note-rule">Before you turn: seat the tip fully, keep the shaft in line, and stop if it rocks or climbs out. Tip fit saves screws, time, and your hand.</p>
<div class="cta-row">{link("Wiha PH2 dimensions", "https://wiha.com/tools/screwdrivers/mechanic-s-screwdrivers/softfinish/phillips/screwdriver-softfinish/27758", "text-link")} {link("Wera 150 mm product sheet", "https://hybris-media.wera.de/download/pdfgenerator-datasheets/en/05008723001.pdf", "text-link")} {link("Klein #2 Phillips specs", "https://www.kleintools.com/catalog/fixed-blade-screwdrivers/2-phillips-screwdriver-4-inch-round-shank", "text-link")}</div>
""", "object-page"))

    pages.append(review_page(16, "SCREWDRIVER", "CARE • WEAR • REPLACEMENT", f"""
<p class="eyebrow red">MATCH THE SCREW BEFORE YOU TURN</p>
<h2>A cross is not a size. Read the mark.</h2>
{table(["DO THIS", "WHY IT PAYS"], [
  ["Seat the point fully, then push in line with the shaft.", "A close fit is less likely to slip out and damage the screw head."],
  ["Stop if the point rocks, rides up, or will not seat.", "Cross-head screws can look alike while calling for a different driver."],
  ["Do not pry, chisel, or strike the handle.", "A fixed screwdriver is for turning screws; side loads can bend or break it."],
  ["Replace it when the point is rounded, twisted, or will not fit.", "This model has a fixed tip. There is no bit to replace."],
], "compact")}
<p class="section-label">Two cross-head profiles. Use the one on the screw.</p>
{screwdriver_profile_figure()}
<p class="small-copy">Read the letters and number on the fastener or packaging: PH2 matches Phillips; PZ2 matches Pozidriv. Do not force one into the other.</p>
<div class="cta-row">{link("Wiha PH2 × 150 mm", "https://wiha.com/tools/screwdrivers/mechanic-s-screwdrivers/softfinish/phillips/screwdriver-softfinish/27758", "buy-link")} {link("Wiha PZ2 × 100 mm", "https://wiha.com/tools/screwdrivers/mechanic-s-screwdrivers/softfinish/pozidriv/screwdriver-softfinish/00772", "text-link")} {link("Check TME price and stock", "https://www.tme.com/us/en-us/details/wiha.27758/standard-screwdrivers/wiha/27758/", "text-link")}</div>
""", "object-page"))

    pages.append(review_page(17, "AT A GLANCE", "FOUR PICKS • FOUR TRADEOFFS", f"""
<p class="eyebrow red">THE QUICK COMPARISON</p>
<h1 style="margin-bottom:.1in">Pick for the job.<br>Know the trade.</h1>
{table(["JOB", "SELECTED MODEL", "THE WIN", "THE TRADE"], [
  ["Controlled, corded drilling", link("Makita 6302H", "https://makitatools.com/products/details/6302H", "row-link"), "0–550 rpm, keyed chuck, documented parts list.", "Cord and low top speed limit where it fits."],
  ["One pan for stove and oven", link("Lodge L10SK3", "https://www.lodgecastiron.com/products/round-cast-iron-classic-skillet?variant=51685752242548", "row-link"), "Low entry price, broad heat fit, recoverable seasoned surface.", "7.69 lb; care is part of the deal."],
  ["Compact everyday nailing", link("Estwing E3-16C", "https://www.estwing.com/product/claw-hammer/", "row-link"), "16 oz, 13 in, one-piece steel head and handle.", "Grip is molded on; replacement path is unclear."],
  ["Long PH2 hand driving", link("Wiha 27758", "https://wiha.com/tools/screwdrivers/mechanic-s-screwdrivers/softfinish/phillips/screwdriver-softfinish/27758", "row-link"), "PH2, 150 mm blade, full-size SoftFinish handle.", "One fixed tip; wrong profile or worn point means stop."],
], "quick-compare")}
<p class="section-label">The decision in one line</p>
<p class="deck">Match the tool to your real workload. A lighter pan, faster drill, different hammer handle, or shorter driver can be the better buy when that trade matters to you.</p>
<div class="object-gallery">
  <figure><a href="https://makitatools.com/products/details/6302H">{img("drill_plate", "", "Makita 6302H drill technical illustration")}</a><figcaption>Drill · Makita 6302H</figcaption></figure>
  <figure><a href="https://www.lodgecastiron.com/products/round-cast-iron-classic-skillet?variant=51685752242548">{img("pan_plate", "", "Lodge 12-inch skillet technical illustration")}</a><figcaption>Frying Pan · Lodge L10SK3</figcaption></figure>
  <figure><a href="https://www.estwing.com/product/claw-hammer/">{img("hammer_plate", "", "Estwing E3-16C hammer technical illustration")}</a><figcaption>Hammer · Estwing E3-16C</figcaption></figure>
  <figure><a href="https://wiha.com/tools/screwdrivers/mechanic-s-screwdrivers/softfinish/phillips/screwdriver-softfinish/27758">{img("driver_plate", "", "Wiha PH2 screwdriver editorial illustration")}</a><figcaption>Screwdriver · Wiha 27758</figcaption></figure>
</div>
""", "compare-page"))

    value_rows = [
        ("Fit the job", "Exact size, capacity, reach, and weight—so you know whether the pick fits your work and storage."),
        ("Spend where it counts", "Side-by-side alternatives show what changes and when the extra cost buys something useful."),
        ("Avoid easy damage", "A care routine, clear limits, and signs that tell you when to stop using the tool."),
        ("Find the repair path", "Manuals, named parts, and service routes, with a live stock or price check where it matters."),
        ("Buy with evidence", "Maker claims, product measurements, price snapshots, and source links are easy to check."),
    ]
    value_html = "".join(f'<div class="value-row"><strong>{html.escape(title)}</strong><p>{html.escape(copy)}</p></div>' for title, copy in value_rows)
    pages.append(review_page(18, "WHY THE BOOK", "MORE THAN THE STORE PAGE", f"""
<div class="value-layout">
  {img("plato_reader", "value-image", "Original editorial portrait of Plato beside the guide's added value")}
  <div>
    <p class="eyebrow red">THE EXTRA WORK</p>
    <h2>Choose well.<br>Keep it useful longer.</h2>
    <p class="deck">The product page gives you the specs. The dossier helps you decide if the object fits, whether the upgrade is worth it, and what to do when it needs care or repair.</p>
    <div class="value-rows">{value_html}</div>
  </div>
</div>
""", "value-page"))

    sources_left = [
        ("DRILL", [
            ("Makita 6302H: specifications and warranty", "https://makitatools.com/products/details/6302H"),
            ("Makita DP4000: specifications", "https://makitatools.com/products/details/DP4000"),
            ("6302H instruction manual", "https://cdn.makitatools.com/apps/cms/doc/prod/630/754466c3-a9fa-4c16-9a99-014d3dfc2fdf_6302H_IM.pdf"),
            ("6302H parts breakdown", "https://cdn.makitatools.com/apps/cms/doc/prod/630/a0fea8d2-c31f-4810-ab22-a2ff5e3ecc98_6302H_PB.pdf"),
            ("Makita parts and service FAQ", "https://makitatools.com/service/faq"),
            ("Makita Direct Repair", "https://makitatools.com/service/directrepair"),
        ]),
        ("FRYING PAN", [
            ("Lodge L10SK3: product, dimensions, price", "https://www.lodgecastiron.com/products/round-cast-iron-classic-skillet?variant=51685752242548"),
            ("Lodge cleaning and restoration", "https://www.lodgecastiron.com/pages/how-to-clean"),
            ("Lodge rust, flakes, and sticky seasoning help", "https://www.lodgecastiron.com/pages/cleaning-and-care-cast-iron-troubleshooting"),
            ("Lodge skillet size guide", "https://www.lodgecastiron.com/blogs/story/what-size-cast-iron-skillet-do-i-need"),
            ("Victoria Traditional 12-inch", "https://victoriacookware.com/products/12-skillet"),
            ("Field No. 10", "https://fieldcompany.com/products/no-10-cast-iron-skillet"),
            ("Stargazer 12-inch", "https://stargazercastiron.com/products/12-inch-cast-iron-skillet"),
        ]),
    ]
    sources_right = [
        ("HAMMER", [
            ("Estwing E3-16C", "https://www.estwing.com/product/claw-hammer/"),
            ("Estwing safety and product care", "https://www.estwing.com/resources/safety-and-product-care/"),
            ("Estwing warranty and discard conditions", "https://www.estwing.com/resources/warranty/"),
            ("DEWALT DWHT51002", "https://www.dewalt.com/en-us/product/dwht51002/16-oz-curved-claw-steel-hammer"),
            ("Estwing SSCF16C", "https://www.estwing.com/product/curved-claw-hammer-carbon-fiber/"),
        ]),
        ("SCREWDRIVER", [
            ("Wiha SoftFinish 27758", "https://wiha.com/tools/screwdrivers/mechanic-s-screwdrivers/softfinish/phillips/screwdriver-softfinish/27758"),
            ("TME: current Wiha 27758 price and stock", "https://www.tme.com/us/en-us/details/wiha.27758/standard-screwdrivers/wiha/27758/"),
            ("Wiha SoftFinish 00759 PH2 × 100 mm", "https://wiha.com/tools/screwdrivers/mechanic-s-screwdrivers/softfinish/phillips/screwdriver-softfinish/00759"),
            ("Wiha SoftFinish 00772 PZ2 × 100 mm", "https://wiha.com/tools/screwdrivers/mechanic-s-screwdrivers/softfinish/pozidriv/screwdriver-softfinish/00772"),
            ("Wera 350 PH, PH2 × 150 mm", "https://www.wera.de/en/05008723001"),
            ("Klein 603-4, #2 × 4-inch shank", "https://www.kleintools.com/catalog/fixed-blade-screwdrivers/2-phillips-screwdriver-4-inch-round-shank"),
        ]),
        ("PLATO", [
            ("Republic, Book VI, 507b; Benjamin Jowett translation", "https://www.gutenberg.org/cache/epub/1497/pg1497-images.html"),
        ]),
    ]
    def source_groups(groups: list[tuple[str, list[tuple[str, str]]]]) -> str:
        output = []
        for title, items in groups:
            rows = "".join(f"<li>{link(label, url, 'source-link')}</li>" for label, url in items)
            output.append(f'<section class="source-group"><h3>{html.escape(title)}</h3><ul>{rows}</ul></section>')
        return "".join(output)

    pages.append(review_page(19, "SOURCES", "SPECS • MANUALS • CARE", f"""
<p class="eyebrow red">GO STRAIGHT TO THE EVIDENCE</p>
<h2 style="margin-bottom:.12in">Product pages, manuals, care, repair</h2>
<div class="source-columns"><div>{source_groups(sources_left)}</div><div>{source_groups(sources_right)}</div></div>
<p class="source-finish">The maker’s page confirms what the model is and what the company claims. Manuals explain operation. Retailer pages show a price and stock snapshot; check again before ordering because availability changes.</p>
""", "sources-page"))

    pages.append(review_page(20, "IMAGE NOTES", "GLOSSARY • IMAGE NOTES", f"""
<p class="eyebrow red">HOW TO READ THE IMAGES</p>
<h2 style="margin-bottom:.1in">The images clarify the idea.<br>The source links prove the product.</h2>
<div class="glossary-rows">
  <div class="glossary-row"><strong>Product plates</strong><p>Original generated editorial illustrations based on the named model and published dimensions. They are not factory photographs or proof of exact construction.</p></div>
  <div class="glossary-row"><strong>Use scenes</strong><p>Illustrated examples of the job. They are not product tests or safety instructions; follow the maker’s manual.</p></div>
  <div class="glossary-row"><strong>Technical diagrams</strong><p>Custom explanatory drawings made from published specs and parts lists. For exact part order, use the linked manufacturer drawing.</p></div>
  <div class="glossary-row"><strong>Plato portraits</strong><p>All Plato portraits are original editorial interpretations created for this proof; they are not photographs or copies of a specific museum statue.</p></div>
  <div class="glossary-row"><strong>PH2 / PZ2</strong><p>Phillips and Pozidriv are different screw profiles. Match the letters and number on the fastener to the driver.</p></div>
  <div class="glossary-row"><strong>Pan dimensions</strong><p>“12 inch” is the nominal size. The Lodge rim, flat base, and total length are different measurements; compare each with your stove and storage.</p></div>
  <div class="glossary-row"><strong>Price snapshot</strong><p>Prices dated in these pages were checked on 15 September 2026. Recheck the linked seller before ordering.</p></div>
  <div class="glossary-row"><strong>Quote</strong><p>Plato, <i>Republic</i> VI, 507b, translated by Benjamin Jowett (1871). The linked Project Gutenberg text is a public-domain U.S. edition.</p></div>
</div>
<p class="tiny" style="margin-top:.04in">The companion file <b>IMAGE_PROMPTS.txt</b> records the prompts used for generated editorial art.</p>
""", "glossary-page"))

    if len(pages) != 20:
        raise RuntimeError(f"Review edition produced {len(pages)} pages; expected 20")
    for name, path in REVIEW_IMAGES.items():
        if not path.exists():
            raise FileNotFoundError(f"Missing review image '{name}': {path}")
    return "<!doctype html><html><head><meta charset='utf-8'><title>Platonic Ideal — The Durable Object Files</title><style>" + review_css() + "</style></head><body>" + "".join(pages) + "</body></html>"


PRIMARY_DECLARED_ASSETS = {
    "PI-001": REVIEW_IMAGES["pan_plate"],
    "PI-003": REVIEW_IMAGES["hammer_plate"],
    "PI-008": REVIEW_IMAGES["driver_plate"],
    "PI-012": REVIEW_IMAGES["drill_plate"],
    # Commissioned in the same clean-plate pass as the other declared objects.
    # This is a source-faithful Bahco 8071 study, with the Greek icon treatment
    # removed from the dossier art while the storefront keeps its own visual.
    "PI-024": ASSET_DIR / "editorial" / "bahco-8071-technical-plate.png",
    "PI-043": ASSET_DIR / "editorial" / "vermont-windsor-chair-technical-plate.png",
    "PI-051": ASSET_DIR / "editorial" / "us-wire-12-3-sjtw-technical-plate.png",
    "PI-055": ASSET_DIR / "editorial" / "werner-fiberglass-step-ladder-technical-plate.png",
}

DECLARED_CLEAN_ASSET_DIR = ASSET_DIR / "editorial" / "clean"
DECLARED_ACTION_ASSET_DIR = ASSET_DIR / "editorial" / "action"

ACTION_DECLARED_ASSETS = {
    "PI-001": REVIEW_IMAGES["pan_use"],
    "PI-003": REVIEW_IMAGES["hammer_use"],
    "PI-008": REVIEW_IMAGES["driver_use"],
    "PI-012": REVIEW_IMAGES["drill_use"],
}

PROOF_ACTION_COPY = {
    "PI-012": {
        "heading": "When slow is the feature",
        "intro": "The 6302H tops out at 550 rpm. That gives you a controlled pace for work that benefits from lower speed; it will feel slow when the job rewards fast, repeated holes.",
        "detail": "The listed wood and steel capacities set the boundary. The large keyed chuck grips standard round-shank bits; use the side handle when the work calls for added control.",
        "trade": "If your holes are mostly small and repetitive, buy for the speed you will use every day. A lower top speed cannot be added later.",
        "checks": [("CAPACITY", "Keep the listed steel and wood limits in view."), ("CONTROL", "Use the side handle when the work calls for it."), ("SPEED", "Choose a faster platform when repeated small holes dominate.")],
    },
    "PI-001": {
        "heading": "Measure the part that touches the stove",
        "intro": "“12 inch” describes the pan’s nominal size. The flat bottom is 9.12 inches; the full width is 12.56 inches and the handle brings the length to 18 inches.",
        "detail": "Check your largest burner and storage space against those three measurements. At 7.69 pounds before food, the helper handle is functional, not decorative.",
        "trade": "Choose it when you want one pan that moves from stove to oven or open fire and you can lift the full pan safely while it is hot and loaded.",
        "checks": [("FOOTPRINT", "Measure the 9.12-inch flat base against your burner."), ("HEAT", "Use the pan across stove, oven, grill, or fire."), ("WEIGHT", "Treat the helper handle as working hardware.")],
    },
    "PI-003": {
        "heading": "Good for controlled hand work",
        "intro": "The 16-ounce head, smooth face, and curved claw cover ordinary nailing and nail pulling. The 13-inch length keeps the tool compact and close to the work.",
        "detail": "That compact feel is the trade. If framing or heavy demolition is your daily work, compare a longer, heavier hammer built for that job before you buy.",
        "trade": "Pick the one-piece steel core for common nails; choose a longer framing hammer when reach and mass matter more than compact control.",
        "checks": [("GRIP", "It should feel secure, with no slip or separation."), ("FACE", "Keep it clean, smooth, and square to the nail."), ("CLAW", "Use the curved form for pulling common nails.")],
    },
    "PI-008": {
        "heading": "Know the point. Check the reach.",
        "intro": "A fixed PH2 driver earns its place when you want a full-size handle and a longer blade. Match the tip to the screw; the wrong cross-point still slips.",
        "detail": "The selected driver pairs a PH2 tip with a 150 mm blade and a full-size handle. Leave room to turn, and use a PZ tip for Pozidriv screws.",
        "trade": "Seat the tip fully, keep the shaft in line, and stop if it rocks or climbs out. Tip fit saves screws, time, and your hand.",
        "checks": [("TIP", "PH2 is not PZ2; read the mark on the fastener."), ("REACH", "Use 150 mm when clearance gives you room to turn."), ("WEAR", "Replace the fixed driver when its point rounds over.")],
    },
}

ACTION_HEADLINES = {
    "Kitchen Knife": "When the edge earns the prep.",
    "Saucepan": "When even heat matters more than speed.",
    "Dutch Oven": "When one pot needs to carry the whole meal.",
    "Kettle": "When a clean pour beats another appliance.",
    "Backpack": "When the load has to ride close and stay serviceable.",
    "Hand Saw": "When a controlled pull makes the cut.",
    "Desk": "When the work surface has to outlast the room.",
    "Boots": "When wet ground is part of the job.",
    "Belt": "When the buckle is working hardware.",
    "T-Shirt": "When the daily layer should stay simple.",
    "Jeans": "When the five-pocket pattern still earns its keep.",
    "Jacket/Coat": "When weather protection should be renewable.",
    "Chisel": "When a sharp edge does the shaping.",
    "Pliers": "When grip and leverage matter more than reach.",
    "Tape Measure": "When the hook has to tell the truth.",
    "Tent": "When shelter must be inspectable in the field.",
    "Sleeping Bag": "When warmth has to pack down and come back.",
    "Water Bottle": "When the container should be the easy part.",
    "Flashlight": "When a dark corner should not stop the repair.",
    "Sweater": "When warmth should be mendable.",
    "Cooler": "When cold storage has to travel.",
    "Pocket Knife": "When one small blade earns its pocket space.",
    "Notebook": "When the record should survive the meeting.",
    "Pen": "When the refill is cheaper than replacing the tool.",
    "Cutting Board": "When the work surface can take the knife.",
    "Bicycle": "When the frame is the long-term decision.",
    "Dining Chair": "When a chair should be tightened instead of thrown out.",
    "Socks": "When the smallest layer controls the whole fit.",
    "Watch": "When the timepiece should be serviceable.",
    "Shoes": "When the sole and upper can age together.",
    "Level": "When a bubble can prevent a crooked job.",
    "Drill Bits": "When the bit should be matched to the material.",
    "Camping Stove": "When the burner has to work away from the kitchen.",
    "Mechanical Pencil": "When a fine mark is worth keeping the holder.",
    "Umbrella": "When the frame is the thing you are buying.",
    "Wheelbarrow": "When the tray and wheel have to carry the load.",
    "Wallet": "When the fold should age with the leather.",
    "Briefcase": "When the case should keep its shape on the commute.",
    "Hat": "When shade and fit have to survive the day.",
    "Gloves": "When the palm takes the wear first.",
    "Razor": "When the replaceable edge should outlive the handle.",
    "Adjustable Wrench": "When one jaw can cover the common fittings.",
}

DOMAIN_CARE_GUIDANCE = {
    "tools-workshop": [
        ("01", "SET UP", "Confirm the working size, interface, and load before you put torque into it."),
        ("02", "USE", "Keep the load square and inside the maker's capacity; stop when the grip or working edge slips."),
        ("03", "CARE", "Brush away grit, wipe the working surfaces, and add only the lubricant the maker calls for."),
        ("04", "SERVICE", "Replace a damaged working edge or unsafe handle; check parts and labor before the failure is urgent."),
    ],
    "kitchen-cooking": [
        ("01", "SET UP", "Confirm the heat source, working capacity, and storage space before the first use."),
        ("02", "USE", "Bring it up to heat gradually and keep food, load, or temperature inside its useful boundary."),
        ("03", "CARE", "Clean it with the maker's method, dry it fully, and store it where the working surface can breathe."),
        ("04", "SERVICE", "Recover the surface when the maker allows it; retire it when structure or safety is compromised."),
    ],
    "clothing-carry": [
        ("01", "FIT", "Confirm the size, last, or adjustment before you commit to the first wear."),
        ("02", "USE", "Wear it inside the job and weather it was built to handle; do not ask the material to do another job."),
        ("03", "CARE", "Follow the wash, dry, wax, or conditioning cycle before dirt and moisture become damage."),
        ("04", "SERVICE", "Repair the seam, sole, zipper, strap, or buckle while the surrounding structure is still sound."),
    ],
    "outdoor-utility": [
        ("01", "SET UP", "Confirm fit, load, weather, fuel, and field conditions before leaving the trailhead."),
        ("02", "USE", "Keep it inside its rated envelope and make the safety margin visible to the person using it."),
        ("03", "CARE", "Dry it completely, clear grit, and replenish the field consumable the maker specifies."),
        ("04", "SERVICE", "Carry the small repair or replacement part that keeps a field failure from becoming a trip-ending one."),
    ],
    "furniture-work": [
        ("01", "SET UP", "Measure the room, working height, and load path before assembly or installation."),
        ("02", "USE", "Keep fasteners, spans, and moving parts inside the load they were designed to carry."),
        ("03", "CARE", "Wipe the surface, tighten the simple hardware, and address moisture before it reaches the structure."),
        ("04", "SERVICE", "Renew the surface or hardware while the frame and joinery remain sound."),
    ],
    "writing-office": [
        ("01", "SET UP", "Choose the refill, paper, lead, or capacity that matches the way you record work."),
        ("02", "USE", "Keep the precision surface clean and use the mechanism in line with its intended motion."),
        ("03", "CARE", "Wipe dust and residue away before it reaches the tip, feed, hinge, or binding."),
        ("04", "SERVICE", "Replace the rational consumable and keep the holder when the durable body is still sound."),
    ],
    "electronics": [
        ("01", "SET UP", "Confirm power, ports, software support, and the workload before you make it part of the system."),
        ("02", "USE", "Keep heat, moisture, charge, and connection demands inside the maker's stated boundary."),
        ("03", "CARE", "Clear vents and connectors, update while support exists, and keep the data path independent."),
        ("04", "SERVICE", "Check battery, storage, display, and port replacement costs before a sealed failure decides for you."),
    ],
    "personal-care-misc": [
        ("01", "SET UP", "Confirm fit, contact surface, and the renewable part before the first use."),
        ("02", "USE", "Use the instrument only for the body contact or personal job it was designed to make safe."),
        ("03", "CARE", "Clean and dry it after contact; replace the hygienic or cutting consumable on its normal cycle."),
        ("04", "SERVICE", "Retire it when body contact, alignment, or safety can no longer be restored."),
    ],
}

# The ownership page is where the plate earns its keep. These are the parts a
# reader should actually point to before buying, cleaning, repairing, or
# retiring the object. The clean multi-view plates are deliberately unlabeled
# so the labels can stay legible in the page typography instead of being baked
# into generated art.
PART_CALLOUT_LABELS = {
    "Drill": ["CHUCK", "SIDE HANDLE", "CORD / SWITCH", "MOTOR / GEARS"],
    "Frying Pan": ["COOKING SURFACE", "HELPER HANDLE", "POUR SPOUT", "FLAT BASE"],
    "Hammer": ["STRIKING FACE", "CURVED CLAW", "ONE-PIECE EYE", "GRIP"],
    "Screwdriver": ["PH2 TIP", "STEEL SHAFT", "HANDLE", "BUTT"],
    "Kitchen Knife": ["CUTTING EDGE", "HEEL", "FULL TANG", "RIVETS"],
    "Saucepan": ["CLAD BODY", "FLAT BASE", "LONG HANDLE", "LID"],
    "Dutch Oven": ["ENAMEL BODY", "LID RIM", "KNOB", "SIDE HANDLES"],
    "Kettle": ["STEEL BODY", "SPOUT", "LID / CAP", "HANDLE"],
    "Backpack": ["BALLISTIC SHELL", "ZIPPER RUN", "FRAME STAYS", "SHOULDER HARNESS"],
    "Hand Saw": ["TOOTH LINE", "BLADE BACK", "HANDLE", "BLADE FASTENER"],
    "Desk": ["MAPLE TOP", "EDGE / APRON", "LEGS", "LOWER SHELF"],
    "Boots": ["LEATHER UPPER", "LACE EYELETS", "WELT", "HEEL / SOLE"],
    "Belt": ["LEATHER STRAP", "ROLLER BUCKLE", "ADJUSTMENT HOLES", "EDGE"],
    "T-Shirt": ["RIBBED COLLAR", "SHOULDER SEAM", "POCKET", "BOTTOM HEM"],
    "Jeans": ["WAISTBAND", "POCKET / RIVET", "INSEAM", "HEM"],
    "Jacket/Coat": ["WAXED SHELL", "COLLAR", "PATCH POCKET", "CUFF / SNAP"],
    "Chisel": ["BEVEL EDGE", "BLADE", "FERRULE", "WOOD HANDLE"],
    "Pliers": ["SERRATED JAWS", "SLIP JOINT", "PIVOT", "GRIP"],
    "Tape Measure": ["CASE", "STEEL TAPE", "HOOK", "LOCK / CLIP"],
    "Tent": ["CANVAS SHELL", "RIDGE POLE", "GUY LINE", "STOVE JACK / VENT"],
    "Sleeping Bag": ["OUTER SHELL", "BAFFLE", "ZIPPER", "HOOD"],
    "Water Bottle": ["BODY", "THREADED NECK", "CAP / GASKET", "BASE"],
    "Flashlight": ["BEZEL", "LENS", "KNURLED BODY", "TAIL SWITCH"],
    "Sweater": ["CABLE KNIT", "COLLAR", "CUFF", "HEM"],
    "Cooler": ["LID", "GASKET", "LATCH", "DRAIN PLUG"],
    "Pocket Knife": ["BLADE", "PIVOT", "LOCK", "HANDLE SCALES"],
    "Notebook": ["COVER", "STITCHED BINDING", "PAPER BLOCK", "SPINE"],
    "Pen": ["BARREL", "TIP", "CLIP", "REFILL"],
    "Cutting Board": ["EDGE-GRAIN TOP", "WORKING EDGE", "FINGER GRIP", "END GRAIN"],
    "Bicycle": ["FRAME", "FORK / HEADSET", "DRIVE TRAIN", "BRAKES"],
    "Socks": ["RIBBED CUFF", "KNIT BODY", "HEEL", "REINFORCED TOE"],
    "Watch": ["CASE", "CROWN", "DIAL / HANDS", "STRAP"],
    "Shoes": ["LEATHER UPPER", "LACE FACING", "WELT", "SOLE / HEEL"],
    "Level": ["ALUMINUM BODY", "VIAL", "WORKING EDGE", "END CAP"],
    "Drill Bits": ["POINT", "FLUTES", "SHANK", "CASE"],
    "Camping Stove": ["BURNER", "POT SUPPORT", "FUEL LINE", "PUMP"],
    "Mechanical Pencil": ["LEAD SLEEVE", "GRIP", "PUSH BUTTON", "CLIP"],
    "Umbrella": ["CANOPY", "RIBS", "RUNNER", "HANDLE"],
    "Wheelbarrow": ["STEEL TRAY", "FRONT WHEEL", "LEG BRACES", "HANDLES"],
    "Wallet": ["LEATHER BODY", "CARD POCKETS", "BILL FOLD", "STITCHING"],
    "Briefcase": ["STRUCTURED SHELL", "LATCH", "TOP HANDLE", "GUSSET"],
    "Hat": ["CROWN", "BRIM", "CHIN CORD", "VENTILATION"],
    "Gloves": ["KNIT BODY", "PALM", "CUFF", "FINGER SEAMS"],
    "Razor": ["HEAD", "GUARD", "BLADE GAP", "HANDLE"],
    "Dining Chair": ["SEAT", "SPINDLES", "LEGS", "JOINERY"],
    "Extension Cord": ["JACKET", "PLUG", "RECEPTACLE", "STRAIN RELIEF"],
    "Ladder": ["SIDE RAILS", "TREADS", "HINGES", "FEET"],
    "Adjustable Wrench": ["FIXED JAW", "MOVING JAW", "WORM", "HANDLE"],
}

PART_CALLOUT_TEMPLATES = {
    "tools-workshop": "Check alignment, wear, and fit here before applying force.",
    "kitchen-cooking": "This is the working surface or heat interface; keep it clean and inspect it for distortion.",
    "clothing-carry": "This is a load or contact zone; repair it while the surrounding material is still sound.",
    "outdoor-utility": "This is the field interface; dry it, clear grit, and inspect it before storage.",
    "furniture-work": "This carries the load; tighten or renew it while the surrounding structure is sound.",
    "writing-office": "This is the precision interface; keep it clean and replace the rational consumable.",
    "electronics": "This is the system interface; confirm compatibility and service access before failure.",
    "personal-care-misc": "This is the contact or wear interface; clean it and replace it when alignment or safety goes.",
}


def _part_callout_guidance(label: str, domain: str) -> str:
    """Turn a part name into an owner action without putting prose in the art."""
    text = label.upper()
    rules = (
        (("CHUCK",), "Seat the bit fully; inspect jaw grip and the key before torque."),
        (("WORM",), "Keep the adjustment clean and seated; play makes the jaw unsafe."),
        (("JAW",), "Seat the flats squarely; stop when the jaw cocks or slips."),
        (("TIP", "POINT"), "Match the tip to the interface; rounding or mismatch causes slip."),
        (("BLADE", "EDGE", "BEVEL", "TOOTH"), "Keep the working edge true; chips, bends, or rounding change the job."),
        (("HANDLE", "GRIP"), "Check for slip, cracks, and separation before the working load."),
        (("MOTOR", "GEAR", "ARMATURE"), "Listen for rough running and check the service path before heat becomes damage."),
        (("CORD", "JACKET", "STRAIN"), "Flex this section and inspect the strain relief before connecting power."),
        (("SWITCH", "LOCK"), "Run the control unloaded; intermittent response is a service signal."),
        (("JOINT", "PIVOT", "HINGE", "FASTENER", "JOINERY"), "Check movement and fastener tightness before the next load."),
        (("BODY", "SHELL", "TOP", "COVER", "SURFACE"), "Keep the load or contact surface clean; distortion changes fit."),
        (("POCKET", "STORAGE"), "Keep the seam and closure loaded evenly; repair before contents pull it open."),
        (("FRAME", "RAIL", "SPINDLE", "LEG", "BRACE", "RIB"), "Check this load-bearing structure for bends, cracks, or looseness."),
        (("VIAL",), "Check zero and bubble readability; a damaged vial ends the precision claim."),
        (("CAP", "LID", "GASKET", "SEAL"), "Keep the seal clean and seated; a leak changes the job."),
        (("BUCKLE", "LATCH", "CATCH"), "Close it fully and inspect the catch; partial engagement is the failure."),
        (("HEEL", "SOLE", "WELT"), "Watch the contact edge for separation and uneven wear."),
        (("CUFF", "COLLAR", "HEM"), "Check stitching and stretch before wear reaches the main body."),
        (("STRAP", "HARNESS"), "Set the load evenly and inspect stitching at every anchor."),
        (("KNIT", "YARN", "CABLE"), "Keep abrasion and snagging visible; repair before a run spreads."),
        (("CASE",), "Check the shell, hinge, and latch; a crack changes protection."),
        (("PAPER", "BLOCK", "BINDING", "SPINE"), "Keep the binding flat and dry; repair a loose signature before pages disappear."),
        (("REFILL", "LEAD"), "Replace the rational consumable before the durable holder is discarded."),
        (("WHEEL", "TIRE"), "Check roundness, axle play, and tread before carrying the load."),
        (("DIAL", "HANDS", "CROWN"), "Check readability and movement; moisture or crown play is a service signal."),
        (("LENS", "BEZEL"), "Keep the optical edge clean and replace the wear part before output drops."),
        (("BASE", "FEET"), "Keep the base flat and dry; wobble is a stop signal."),
        (("CANOPY", "RUNNER"), "Open it fully and check the tension path before weather puts load on it."),
        (("FUEL", "BURNER", "PUMP"), "Check the seal and flow before lighting; leaks are a stop condition."),
        (("POLE", "RIDGE"), "Seat the joint fully and keep the load path tensioned before weather arrives."),
        (("HEAD", "GUARD"), "Keep the contact face aligned and the removable wear part seated."),
    )
    for tokens, guidance in rules:
        if any(token in text for token in tokens):
            return guidance
    return PART_CALLOUT_TEMPLATES.get(domain, "Inspect this interface before use and keep its wear visible.")


def declared_part_callouts(entry: Entry) -> list[tuple[str, str]]:
    """Return readable part labels and owner consequences for the care plate."""
    labels = PART_CALLOUT_LABELS.get(entry.category)
    if not labels:
        labels = ["BODY", "WORKING EDGE", "JOINT / FIT", "SERVICE PART"]
    details: list[tuple[str, str]] = []
    for label in labels[:4]:
        details.append((label, _part_callout_guidance(label, entry.domain)))
    return details


def declared_order(entries: list[Entry]) -> list[Entry]:
    """Put the four proof objects first, then carry every declaration alphabetically."""
    declared = [entry for entry in entries if entry.status == "DECLARED"]
    preferred = ["PI-012", "PI-001", "PI-003", "PI-008"]
    by_ref = {entry.reference: entry for entry in declared}
    first = [by_ref[ref] for ref in preferred if ref in by_ref]
    rest = sorted((entry for entry in declared if entry.reference not in preferred), key=lambda e: e.category.casefold())
    return first + rest


def declared_page_map(entries: list[Entry], first_product_page: int = 5) -> dict[str, int]:
    return {entry.reference: first_product_page + index * 3 for index, entry in enumerate(entries)}


def declared_primary_asset(entry: Entry) -> Path | None:
    """Return the dossier plate, never the storefront's Greek-background hero.

    The four proof objects keep their approved technical plates and the Bahco
    wrench uses its commissioned source-faithful study. Every other declaration
    has a clean warm-ivory raster plate in ``assets/editorial/clean``. Falling
    back to ``image_for`` would silently reintroduce the Greek icon treatment,
    so a missing clean asset is surfaced as an image gate instead.
    """
    direct = PRIMARY_DECLARED_ASSETS.get(entry.reference)
    if direct and direct.exists():
        return direct
    clean = DECLARED_CLEAN_ASSET_DIR / f"{_declared_asset_stem(entry)}-multi-view.jpg"
    return clean if clean.exists() else None


def _declared_asset_stem(entry: Entry) -> str:
    return re.sub(r"[^a-z0-9]+", "-", f"{entry.reference}-{entry.category}".lower()).strip("-")


def _contained_image(source: Image.Image, size: tuple[int, int]) -> Image.Image:
    return ImageOps.contain(source.convert("RGB"), size, method=Image.Resampling.LANCZOS)


def declared_raster_variant(entry: Entry, kind: str) -> Path | None:
    """Create warm-paper raster derivatives so every object has three useful plates.

    The derivatives deliberately stay photographic/raster editorial plates. They
    provide a detail and a contextual view when a dedicated use scene has not yet
    been commissioned; they never pretend to be a factory photograph.
    """
    source_path = declared_primary_asset(entry)
    if not source_path:
        return None
    target_dir = TMP_DIR / "declared-assets"
    target_dir.mkdir(parents=True, exist_ok=True)
    # ``clean`` in the filename keeps old Greek-background derivatives from
    # being reused when the book is rebuilt in the same workspace.
    output = target_dir / f"{_declared_asset_stem(entry)}-clean-{kind}.jpg"
    if output.exists() and output.stat().st_mtime >= source_path.stat().st_mtime:
        return output
    source = Image.open(source_path).convert("RGB")
    paper = (249, 245, 236)
    if kind == "detail":
        canvas = Image.new("RGB", (1600, 1000), paper)
        plate = _contained_image(source, (1500, 900))
        x = (canvas.width - plate.width) // 2
        y = (canvas.height - plate.height) // 2
        canvas.paste(plate, (x, y))
        draw = ImageDraw.Draw(canvas)
        draw.rectangle((28, 28, canvas.width - 29, canvas.height - 29), outline=(35, 35, 35), width=2)
        draw.rectangle((42, 42, canvas.width - 43, canvas.height - 43), outline=(198, 35, 31), width=1)
    else:
        canvas = Image.new("RGB", (1600, 1000), paper)
        draw = ImageDraw.Draw(canvas)
        # A restrained grounding shadow gives the staged view a useful object/action
        # relationship without drawing a fake mechanism or adding vector art.
        draw.ellipse((690, 790, 1490, 900), fill=(224, 217, 204))
        full = _contained_image(source, (850, 720))
        canvas.paste(full, (650 + (850 - full.width) // 2, 105 + (720 - full.height) // 2))
        crop_box = (int(source.width * .12), int(source.height * .12), int(source.width * .88), int(source.height * .88))
        crop = source.crop(crop_box)
        inset = ImageOps.fit(crop, (485, 360), centering=(.5, .5), method=Image.Resampling.LANCZOS)
        canvas.paste(inset, (95, 302))
        draw.rectangle((82, 289, 593, 675), outline=(35, 35, 35), width=2)
        draw.rectangle((95, 302, 579, 661), outline=(198, 35, 31), width=1)
    canvas.save(output, quality=94, subsampling=0, optimize=True)
    return output


def declared_action_asset(entry: Entry) -> tuple[Path | None, bool]:
    direct = ACTION_DECLARED_ASSETS.get(entry.reference)
    if direct and direct.exists():
        return direct, True
    generated = DECLARED_ACTION_ASSET_DIR / f"{_declared_asset_stem(entry)}-action.jpg"
    if generated.exists():
        return generated, True
    return declared_raster_variant(entry, "context"), False


def declared_detail_asset(entry: Entry) -> Path | None:
    return declared_raster_variant(entry, "detail")


def declared_img(path: Path | None, class_name: str, alt: str) -> str:
    if not path or not path.exists():
        return f'<div class="declared-image-missing"><span class="red">IMAGE</span> / editorial plate pending</div>'
    return f'<img class="{esc(class_name)}" src="{esc(uri(path))}" alt="{esc(alt)}">'


def declared_model_label(entry: Entry) -> str:
    record = source_for(entry)
    exact = normalize(record.get("exactModel"))
    variant = normalize(record.get("variant"))
    title = normalize(record.get("sourcePageTitle"))
    identity = normalize(record.get("identityStatus")).lower()
    if identity == "exact" and exact and exact.lower() not in {"not recorded", "model pending", "not sku-normalized"}:
        base = title or variant or exact
        if exact.lower() not in base.lower():
            base = f"{base} ({exact})"
        return shorten(base, 96)
    return shorten(entry.model or entry.category, 96)


def declared_lead(entry: Entry) -> str:
    proof = PROOF_COPY.get(entry.reference)
    if proof:
        return clean_editorial_text(proof["lead"])
    job = clean_editorial_text(first_sentence(entry.summary, entry.form_statement, entry.form,
                                              fallback=f"A considered {entry.category.lower()} for the job it is built to do."))
    trade = clean_editorial_text(first_sentence(entry.disqualifiers, entry.reasoning,
                                                fallback="The trade is visible in the ownership and service path."))
    if trade and trade.lower() not in job.lower():
        return shorten(f"The buy: {job.rstrip('.')}. The trade: {trade.rstrip('.') }.", 280)
    return shorten(job, 280)


def declared_trade(entry: Entry) -> str:
    return clean_editorial_text(first_sentence(entry.disqualifiers, entry.reasoning, entry.failures,
                                               fallback="The trade is the care, weight, fit, or service work the job demands."))


def declared_metric_values(entry: Entry) -> list[tuple[str, str]]:
    proof = PROOF_COPY.get(entry.reference)
    metrics: list[tuple[str, str]] = list(proof["metrics"]) if proof else []
    combined = " ".join((entry.model, entry.form, entry.form_statement, entry.summary))
    measure = re.search(r"\b\d+(?:\.\d+)?(?:-\d+(?:\.\d+)?)?\s*(?:in(?:ch)?|oz|lb|lbs|kg|g|mm|cm|qt|A|rpm|V|ft|L|ml|degrees?)\b", combined, re.I)
    material_match = re.search(r"\b(?:stainless steel|cast iron|solid wood|full[- ]grain leather|cotton canvas|ballistic nylon|chrome[- ]vanadium steel|high[- ]carbon stainless steel|100% wool|merino wool|aluminum|chromoly steel|brass|polyethylene|fiberglass|HSS)\b", combined, re.I)
    record = source_for(entry)
    identity = normalize(record.get("identityStatus")).upper() or "UNRESOLVED"
    if not metrics:
        metrics = [
            (shorten(normalize(record.get("exactModel")) or entry.model or entry.category, 26), "model record"),
            (measure.group(0) if measure else "SEE FORM", "working measure"),
            (field_value(entry.price, "price pending"), "price snapshot"),
            (shorten(material_match.group(0) if material_match else first_sentence(entry.form, fallback="material recorded"), 24), "primary material"),
        ]
    labels = {label.lower() for _, label in metrics}
    if "identity" not in " ".join(labels):
        metrics.append((identity, "model identity"))
    if "field state" not in " ".join(labels):
        metrics.append(("DECLARED", "field state"))
    return metrics[:6]


def declared_metric_grid(entry: Entry) -> str:
    return '<div class="declared-fact-grid">' + "".join(
        f'<div class="fact"><b>{esc(value)}</b><span>{esc(label)}</span></div>'
        for value, label in declared_metric_values(entry)
    ) + "</div>"


def declared_feature_rows(entry: Entry) -> list[tuple[str, str]]:
    proof = PROOF_COPY.get(entry.reference)
    if proof:
        return [(title, clean_editorial_text(text)) for title, text in proof["features"]]
    parts = declared_part_callouts(entry)
    admission = first_sentence(entry.admission, entry.summary,
                                fallback="Match the product to the job you actually repeat.")
    form = first_sentence(entry.form, entry.form_statement,
                          fallback="The construction is the part that carries the work.")
    upkeep = first_sentence(entry.maintenance, entry.permanence,
                            fallback="Keep the first wear point visible before it becomes a failure.")
    return [
        ("FIT", clean_editorial_text(admission)),
        ("FORM", clean_editorial_text(form)),
        ("WATCH", clean_editorial_text(f"{parts[0][0]} and {parts[1][0]} are the first ownership checkpoints. {upkeep}")),
    ]


def declared_care_rows(entry: Entry) -> list[tuple[str, str, str]]:
    proof = PROOF_OWNERSHIP.get(entry.reference)
    if proof:
        return [(number, title, clean_editorial_text(text)) for number, title, text in proof["care"]]
    guidance = DOMAIN_CARE_GUIDANCE.get(entry.domain)
    if guidance:
        values = [(number, title, text) for number, title, text in guidance]
        if entry.maintenance:
            values[2] = (values[2][0], values[2][1], first_sentence(entry.maintenance, fallback=values[2][2]))
        if entry.permanence:
            values[3] = (values[3][0], values[3][1], first_sentence(entry.permanence, fallback=values[3][2]))
        return [(number, title, clean_editorial_text(text)) for number, title, text in values]
    values = [
        ("01", "SET UP", first_sentence(entry.form, entry.form_statement,
                                          fallback="Confirm size, fit, load, and configuration before use.")),
        ("02", "USE", first_sentence(entry.summary, fallback="Use it inside the job and capacity it was chosen for.")),
        ("03", "CARE", first_sentence(entry.maintenance, fallback="Follow the maker's cleaning, drying, storage, and inspection interval.")),
        ("04", "SERVICE", first_sentence(entry.permanence, entry.notes,
                                            fallback="Check parts, labor, and replacement options before a failure becomes urgent.")),
    ]
    return [(number, title, clean_editorial_text(text)) for number, title, text in values]


def declared_failure_rows(entry: Entry) -> list[tuple[str, str, str]]:
    proof = PROOF_OWNERSHIP.get(entry.reference)
    if proof:
        return [(clean_editorial_text(title), clean_editorial_text(status), clean_editorial_text(text)) for title, status, text in proof["failures"]]
    raw = sentences(entry.failures, 3)
    if not raw:
        raw = ["A routine wear symptom is not recorded in the current register.", "Inspect it and compare the maker's limits.", "Retire it when safe fit or structure cannot be restored."]
    while len(raw) < 3:
        raw.append("Add the symptom, safe recovery, and terminal threshold to the next review.")
    labels = [("ROUTINE WEAR", "RECOVERABLE"), ("DAMAGE", "INSPECT"), ("STRUCTURE", "STOP / REPLACE")]
    return [(title, status, clean_editorial_text(raw[index])) for index, (title, status) in enumerate(labels)]


def declared_candidate_rows(entry: Entry) -> list[tuple[str, str, str, str, str]]:
    proof = PROOF_OWNERSHIP.get(entry.reference)
    if proof:
        return [
            (
                clean_editorial_text(a),
                clean_editorial_text(b),
                clean_editorial_text(f"{c}; {d}"),
                "THE PICK" if index == 0 else "PASSED",
                clean_editorial_text(e),
            )
            for index, (a, b, c, d, e) in enumerate(proof["candidates"])
        ]

    rows = [(
        declared_model_label(entry),
        field_value(entry.price, "price varies"),
        shorten(first_sentence(entry.form, entry.form_statement, fallback="The defined job and construction."), 72),
        "THE PICK",
        "Best balance for the job this chapter defines.",
    )]

    alternates = ALTERNATE_CANDIDATES.get(entry.category, [])
    if not alternates:
        raw = normalize(entry.alternates)
        if raw:
            parts = [part.strip() for part in re.split(r";|\n|\s+\|\s+", raw) if part.strip()]
            if len(parts) == 1:
                parts = [part.strip() for part in re.split(r",(?=[A-Z])", raw) if part.strip()]
            alternates = [
                (shorten(part, 42), "price varies", "A named alternative in the register.", "The current record gives it less support for this job.")
                for part in parts[:3]
            ]
    for name, price, strength, reason in alternates[:3]:
        rows.append((shorten(name, 42), price, strength, "PASSED", reason))

    # Keep the table honest if a future category is added without a shortlist.
    # This is a readable statement of the gap, not a fake candidate.
    if len(rows) < 4:
        rows.append(("No additional serious option recorded", "not recorded", "The comparison field is still being researched.", "OPEN", "Add a named alternative before release."))
    return rows[:4]


def declared_candidate_table(entry: Entry) -> str:
    rows = declared_candidate_rows(entry)
    body_rows = "".join(
        f"<tr><td><strong>{esc(model)}</strong></td><td>{esc(price)}</td><td>{esc(core)}</td><td>{esc(strategy)}</td><td>{esc(reason)}</td></tr>"
        for model, price, core, strategy, reason in rows
    )
    return f'''<div class="section-label">OTHER OPTIONS WE CONSIDERED</div>
<p class="candidate-note">These are the serious alternatives. The table shows what each one does well, its result, and why it did or did not take the pick.</p>
<table class="review-table compact declared-candidate-table">
  <thead><tr><th>PRODUCT</th><th>PRICE</th><th>WHAT IT DOES WELL</th><th>RESULT</th><th>WHY IT'S HERE</th></tr></thead>
  <tbody>{body_rows}</tbody>
</table>'''


def declared_source_cta(entry: Entry, label: str = "View product details") -> str:
    record = source_for(entry)
    url = normalize(record.get("sourceUrl"))
    if not url:
        return '<span class="source-missing">Product details are still needed for this pick.</span>'
    return review_link(label, url, "text-link")


def declared_source_line(entry: Entry) -> str:
    record = source_for(entry)
    role = source_role(record)
    identity = normalize(record.get("identityStatus")).upper() or "UNRESOLVED"
    checked = SOURCE_CHECKED_AT or entry.reviewed or "date not recorded"
    identity_text = "exact model confirmed" if identity == "EXACT" else f"{identity.lower()} model record"
    return f'<p class="declared-source-line"><span class="red">CHECK THE SOURCE:</span> {esc(role)}; {esc(identity_text)}; last checked {esc(checked)}. {declared_source_cta(entry)}</p>'


def declared_editorial_analysis(entry: Entry) -> str:
    """Give every declared pick's full editorial reasoning visual priority."""
    return f'''<section class="declared-editorial-analysis" data-case-reference="{esc(entry.reference)}" data-case-field="coreReasoning">
  <p class="section-label">EDITORIAL ANALYSIS</p>
  <h3>Why this is the pick</h3>
  <p>{esc(clean_editorial_text(entry.reasoning))}</p>
</section>'''


def declared_comparative_analysis(entry: Entry) -> str:
    """Place every declared pick's full counter-case below its candidate table."""
    return f'''<section class="declared-comparative-analysis" data-case-reference="{esc(entry.reference)}" data-case-field="disqualifiers">
  <div>
    <p class="section-label">COMPARATIVE ANALYSIS</p>
    <h3>Why the field falls short</h3>
  </div>
  <p>{esc(clean_editorial_text(entry.disqualifiers))}</p>
</section>'''


def _declared_index_rows(entries: list[Entry], page_map: dict[str, int]) -> str:
    return "".join(
        f'<div class="declared-index-row"><span>{esc(entry.category)}</span><i class="dots"></i><span>{page_map[entry.reference]:02d}</span></div>'
        for entry in sorted(entries, key=lambda e: e.category.casefold())
    )


def _declared_comparison_rows(entries: list[Entry]) -> list[list[str]]:
    rows: list[list[str]] = []
    for entry in entries:
        proof = PROOF_COPY.get(entry.reference)
        win = clean_editorial_text(proof["lead"] if proof else first_sentence(entry.summary, entry.form,
                                                                              fallback="The selected model clears the declared Form."))
        trade = declared_trade(entry)
        record = source_for(entry)
        source_url = normalize(record.get("sourceUrl"))
        source_cell = review_link("open", source_url, "text-link") if source_url else '<span class="source-missing">pending</span>'
        rows.append([
            entry.category,
            declared_model_label(entry),
            shorten(win, 125),
            shorten(trade, 125),
            source_cell,
        ])
    return rows


def _declared_source_items(entries: list[Entry]) -> str:
    items: list[str] = []
    for entry in entries:
        record = source_for(entry)
        url = normalize(record.get("sourceUrl"))
        title = normalize(record.get("sourcePageTitle")) or normalize(record.get("sellerOrManufacturer")) or "product page still needed"
        model = declared_model_label(entry)
        if url:
            title_html = review_link(title, url, "source-link")
        else:
            title_html = f'<span class="source-missing">{esc(title)}</span>'
        items.append(f'''<section class="declared-source-item">
  <h3>{esc(entry.category)}</h3>
  <p><strong>{esc(model)}</strong><br>{title_html}</p>
  <span class="tiny">{esc(source_role(record))} · {esc("exact model confirmed" if normalize(record.get("identityStatus")).upper() == "EXACT" else "model record needs review")}</span>
</section>''')
    return "".join(items)


def build_declared_html(entries: list[Entry]) -> str:
    """Build the declared-only book in the supplied 1940 proof rhythm.

    Four front pages establish the reading method. Every declaration then gets
    exactly three pages: decision, fit/use, and ownership/service. Every
    declared chapter uses the existing decision and fit pages to carry its
    full editorial and comparative case. The remaining
    pages are a comparison, product sources, an image glossary, and a reader checklist.
    """
    declared = declared_order(entries)
    if not declared:
        raise RuntimeError("No DECLARED entries found")
    page_map = declared_page_map(declared)
    count = len(declared)
    pages: list[str] = []

    cover_items = "CLEAR PICK  /  HONEST TRADEOFF  /  PRACTICAL CARE"
    pages.append(review_page(1, "PLATONIC IDEAL", "THE GOOD BUY", f'''
<div class="cover-copy">
  <p class="cover-brand">PLATONIC IDEAL</p>
  <p class="cover-label">A BUYING GUIDE FOR EVERYDAY THINGS</p>
  <h1>BUY WELL.<br>KEEP IT WORKING.</h1>
  <p class="cover-deck">Clear recommendations for the things you use every day, with the tradeoffs and care that make each choice worth it.</p>
  <div class="cover-list"><span class="red">{cover_items}</span></div>
</div>
<p class="cover-date">DECLARED EDITION&nbsp;&nbsp; • &nbsp;&nbsp;SEPTEMBER 2026</p>
{review_image("plato_cover", "cover-art", "Original editorial portrait of Plato")}
''', "cover declared-cover"))

    pages.append(review_page(2, "PLATO", "REPUBLIC • BOOK VI", f'''
<div class="quote-layout declared-quote-layout">
  <div class="quote-copy">
    <p class="quote-label">A THING IS MORE THAN ITS APPEARANCE</p>
    <blockquote>“The old story, that there is a many beautiful and a many good, and so of other things which we describe and define; to all of them the term ‘many’ is applied.<br><br>‘True,’ he said.<br><br>‘And there is an absolute beauty and an absolute good, and of other things to which the term “many” is applied there is an absolute; for they may be brought under a single idea, which is called the essence of each.’<br><br>‘Very true.’<br><br>‘The many, as we say, are seen but not known, and the ideas are known but not seen.’<br><br>‘Exactly.’”</blockquote>
    <p class="quote-attr">PLATO&nbsp;&nbsp; / &nbsp;&nbsp;REPUBLIC VI, 507B</p>
  </div>
  <div class="quote-photo">{review_image("plato_quote", "", "Original editorial portrait of Plato, both eyes visible")}</div>
</div>
''', "quote-page declared-quote"))

    alpha = sorted(declared, key=lambda e: e.category.casefold())
    split = (len(alpha) + 1) // 2
    pages.append(review_page(3, "INDEX", f"{count} RECOMMENDATIONS", f'''
<p class="eyebrow red">START HERE</p>
<h1 class="index-heading">The field index</h1>
<p class="index-note">Alphabetical by product type. Start at the page number for the recommendation, then keep reading for fit, care, and service.</p>
<div class="declared-index-layout">
  <div class="declared-index-column">{_declared_index_rows(alpha[:split], page_map)}</div>
  <div class="declared-index-column">{_declared_index_rows(alpha[split:], page_map)}</div>
</div>
''', "index-page declared-index"))

    tests = [
        ("FIT", "Will it do your everyday job?", "Name the size, material, load, reach, and setting before comparing brands."),
        ("FORM", "What is holding it together?", "Count the working joints, wear layers, coatings, and parts that can loosen or age."),
        ("RECOVERY", "What can you fix?", "Check which wear is routine, which damage can be restored, and which means replacement."),
        ("SUPPLY", "Can you get the important parts?", "A parts drawing helps. Current stock, service, and regional support decide whether repair is real."),
        ("OWNERSHIP", "What will it ask of you?", "Care, safe handling, storage, and consumables are part of the purchase price."),
        ("VALUE", "What does the upgrade buy?", "Pay more only when the lighter weight, better fit, extra control, or longer service matters to you."),
    ]
    tests_html = "".join(
        f'<article class="test"><span class="test-number">{i:02d}</span><div><h3>{html.escape(title)}</h3><p>{html.escape(copy)}</p></div></article>'
        for i, (title, _, copy) in enumerate(tests, 1)
    )
    pages.append(review_page(4, "THE DECISION", "SIX TESTS", f'''
<p class="eyebrow red">READ THIS BEFORE THE PICKS</p>
<h1 style="margin-bottom:.12in">Six tests before a declaration</h1>
<p class="deck" style="max-width:6.7in">A good product makes the job easier. A great buy still makes sense when it wears, needs care, or has to be repaired.</p>
<div class="tests">{tests_html}</div>
<p class="reader-path">Use each chapter in order:<br><span>what it is / how it fits / how to keep it working.</span></p>
''', "tests-page declared-tests"))

    for index, entry in enumerate(declared):
        decision_page = page_map[entry.reference]
        model = declared_model_label(entry)
        lead = declared_lead(entry)
        primary = declared_primary_asset(entry)
        action, is_real_action = declared_action_asset(entry)
        detail = declared_detail_asset(entry)
        action_right = "FIT • ACTION • TRADEOFF" if is_real_action else "FIT • CONTEXT • TRADEOFF"
        proof_action = PROOF_ACTION_COPY.get(entry.reference)
        action_heading = proof_action["heading"] if proof_action else ACTION_HEADLINES.get(
            entry.category, f"When the {entry.category.lower()} earns its keep.")
        action_intro = proof_action["intro"] if proof_action else first_sentence(
            entry.admission, entry.summary, fallback="Choose it for the job you repeat most.")
        action_detail = proof_action["detail"] if proof_action else first_sentence(
            entry.form, entry.form_statement, fallback="The construction keeps the work legible.")
        action_trade = proof_action["trade"] if proof_action else declared_trade(entry)
        feature_rows = [(label, text) for label, text in proof_action["checks"]] if proof_action else declared_feature_rows(entry)
        feature_html = "".join(f'<li><b>{esc(label)}:</b> {esc(shorten(text, 180))}</li>' for label, text in feature_rows)
        editorial_case = clean_editorial_text(entry.reasoning)
        comparative_case = clean_editorial_text(entry.disqualifiers)
        decision_page_class = "declared-page declared-decision"
        action_page_class = "declared-page declared-action"
        if len(editorial_case) > 590:
            decision_page_class += " declared-decision-compact"
        if len(comparative_case) > 520:
            action_page_class += " declared-action-compact"

        pages.append(review_page(decision_page, entry.category.upper(), "DECISION • EXACT MODEL", f'''
<div class="declared-object-opener">
  <p class="eyebrow red">THE PICK</p>
  <h1 class="open-title">{esc(entry.category)}</h1>
  <p class="open-subtitle">{esc(model)}</p>
  <p class="deck">{esc(lead)}</p>
</div>
{declared_img(primary, "declared-plate-large", f"Large editorial multi-view plate of {entry.category}")}
<div class="declared-decision-bottom">
  {declared_metric_grid(entry)}
  <div class="declared-verdict"><p class="section-label">THE DECISION</p><p>{esc(shorten(declared_trade(entry), 230))}</p><div class="cta-row">{declared_source_cta(entry, "View product details")}</div></div>
</div>
{declared_editorial_analysis(entry)}
''', decision_page_class))

        pages.append(review_page(decision_page + 1, entry.category.upper(), action_right, f'''
<div class="split-title"><h2>{esc(action_heading)}</h2><span>{esc(shorten(model, 34))}</span></div>
<div class="declared-action-layout">
  <div class="declared-action-figure">{declared_img(action, "declared-action-image", f"{entry.category} shown in a work context")}</div>
  <div class="declared-action-copy">
    <p class="eyebrow red">BUY IT WHEN</p>
    <h2>{esc(shorten(action_heading, 115))}</h2>
    <p class="small-copy">{esc(shorten(action_intro + " " + action_detail, 260))}</p>
    <p class="note-rule"><b>THE TRADE:</b> {esc(shorten(action_trade, 280))}</p>
    <p class="section-label">THREE FIT CHECKS</p>
    <ul class="ruled-list">{feature_html}</ul>
  </div>
</div>
{declared_candidate_table(entry)}
{declared_comparative_analysis(entry)}
<div class="cta-row">{declared_source_cta(entry, "View specs and fit")}</div>
''', action_page_class))

        care_rows = declared_care_rows(entry)
        care_html = "".join(f'<tr><td>{esc(number)}</td><td><strong>{esc(title)}</strong></td><td>{esc(text)}</td></tr>' for number, title, text in care_rows)
        callout_rows = declared_part_callouts(entry)
        callout_html = "".join(
            f'<div class="declared-part-callout"><span class="part-callout-number">{index + 1:02d}</span><div><strong>{esc(label)}</strong><p>{esc(text)}</p></div></div>'
            for index, (label, text) in enumerate(callout_rows)
        )
        failure_rows = declared_failure_rows(entry)
        failure_html = "".join(f'<tr><td><strong>{esc(title)}</strong></td><td>{esc(status)}</td><td>{esc(text)}</td></tr>' for title, status, text in failure_rows)
        pages.append(review_page(decision_page + 2, entry.category.upper(), "CARE • PARTS • SERVICE", f'''
<p class="eyebrow red">AFTER YOU BUY</p>
<h2>Keep it useful longer.</h2>
<p class="deck">The useful part starts here: care, service, and the point where you should repair or replace it.</p>
<div class="declared-care-layout">
  <div class="declared-detail-column">
    <div class="declared-detail-figure">{declared_img(detail, "declared-detail-image", f"Detail plate of {entry.category}")}</div>
  </div>
  <div>
    <p class="section-label">CARE ROUTINE</p>
    <table class="review-table compact declared-care-table"><thead><tr><th>#</th><th>MOVE</th><th>DO THIS</th></tr></thead><tbody>{care_html}</tbody></table>
  </div>
</div>
<div class="declared-part-callouts"><p class="section-label">PARTS TO WATCH</p><div class="declared-part-callout-grid">{callout_html}</div></div>
<p class="section-label">WHEN TO REPAIR OR REPLACE</p>
<table class="review-table compact declared-failure-table"><thead><tr><th>SYMPTOM</th><th>STATUS</th><th>OWNER MOVE</th></tr></thead><tbody>{failure_html}</tbody></table>
<p class="note-rule"><b>CARE AND SERVICE:</b> {esc(shorten(first_sentence(entry.permanence, entry.maintenance, entry.notes, fallback="Verify current parts, labor, warranty, and replacement options with the maker."), 320))}</p>
<div class="cta-row">{declared_source_cta(entry, "View manual and service details")}</div>
{declared_source_line(entry)}
''', "declared-page declared-care"))

    # All declared picks are kept in the comparison. Split into two readable
    # pages so the table can stay generous instead of becoming a tiny index.
    comparison_rows = _declared_comparison_rows(declared)
    comparison_chunk_size = 12
    for chunk_index in range(0, len(comparison_rows), comparison_chunk_size):
        chunk = comparison_rows[chunk_index:chunk_index + comparison_chunk_size]
        page_number = 5 + count * 3 + chunk_index // comparison_chunk_size
        pages.append(review_page(page_number, "AT A GLANCE", f"RECOMMENDATIONS {chunk_index + 1:02d}–{chunk_index + len(chunk):02d}", f'''
<p class="eyebrow red">THE QUICK COMPARISON</p>
<h1 style="margin-bottom:.1in">Pick for the job.<br>Know the trade.</h1>
{review_table(["CATEGORY", "SELECTED MODEL", "THE WIN", "THE TRADE", "SOURCE"], chunk, "declared-comparison-table")}
<p class="note-rule">Every row opens the same three-page chapter: decision, fit/use, then care and service.</p>
''', "comparison-page declared-comparison"))

    comparison_page_count = (len(comparison_rows) + comparison_chunk_size - 1) // comparison_chunk_size
    source_chunk_size = 16
    source_start = 5 + count * 3 + comparison_page_count
    for chunk_index in range(0, len(declared), source_chunk_size):
        chunk = declared[chunk_index:chunk_index + source_chunk_size]
        half = (len(chunk) + 1) // 2
        page_number = source_start + chunk_index // source_chunk_size
        pages.append(review_page(page_number, "PRODUCT SOURCES", f"RECOMMENDATIONS {chunk_index + 1:02d}–{chunk_index + len(chunk):02d}", f'''
<p class="eyebrow red">GO STRAIGHT TO THE EVIDENCE</p>
<h2 style="margin-bottom:.12in">Specs, manuals, care, service</h2>
<p class="small-copy">The source page proves the model and the maker's claims. Retail and market pages are snapshots; check them again before ordering.</p>
<div class="declared-source-columns"><div>{_declared_source_items(chunk[:half])}</div><div>{_declared_source_items(chunk[half:])}</div></div>
''', "sources-page declared-sources"))

    source_page_count = (len(declared) + source_chunk_size - 1) // source_chunk_size
    glossary_page_no = source_start + source_page_count
    pages.append(review_page(glossary_page_no, "IMAGE NOTES", "GLOSSARY • RIGHTS", f'''
<p class="eyebrow red">HOW TO READ THE IMAGES</p>
<h2>The images make the judgment easier to see.</h2>
<div class="glossary-rows">
  <div class="glossary-row"><strong>Multi-view illustrations</strong><p>These editorial views show the product from more than one useful angle. The named source remains the authority for exact dimensions and construction.</p></div>
  <div class="glossary-row"><strong>Action illustrations</strong><p>Each chapter includes a scene showing the product doing its job. It clarifies fit, handling, and the working interface; it is not independent product testing and does not replace the maker's safety instructions.</p></div>
  <div class="glossary-row"><strong>Detail illustrations</strong><p>These warm-ivory views enlarge the same source-faithful product to clarify silhouette, finish, and service-relevant geometry. They are not exploded views.</p></div>
  <div class="glossary-row"><strong>Product sources</strong><p>Maker pages, seller pages, manuals, care notes, and the date we checked them are collected here and repeated on each recommendation.</p></div>
  <div class="glossary-row"><strong>Plato reference</strong><p>The reference photograph is the Silanion-type portrait of Plato at the Altes Museum, Berlin, by Osama Shukir Muhammed Amin, Wikimedia Commons, CC BY-SA 4.0. The portraits in this book are original editorial interpretations.</p></div>
  <div class="glossary-row"><strong>Quote</strong><p>Plato, <i>Republic</i> VI, 507b, Benjamin Jowett translation. The linked Project Gutenberg text is a public-domain U.S. edition.</p></div>
  <div class="glossary-row"><strong>Reader labels</strong><p>Internal production codes are omitted. Pages use the category name and page number so the index reads like a magazine contents page.</p></div>
</div>
<p class="tiny" style="margin-top:.08in">Image rights and quotation notes live here, at the back of the book, rather than interrupting the buying advice.</p>
''', "glossary-page declared-glossary"))

    colophon_page_no = glossary_page_no + 1
    pages.append(review_page(colophon_page_no, "PLATONIC IDEAL", "KEEP THIS GUIDE HANDY", f'''
<p class="eyebrow red">WHEN YOU ARE READY TO BUY</p>
<h1 style="font-size:31pt">Start with the job.<br>See the trade.<br>Keep it working.</h1>
<p class="deck" style="max-width:6.6in">The point of this guide is simple: spend less time comparing and more time using the right thing. Choose the version that fits the work you actually have, then keep the care and service notes close.</p>
<div class="colophon-grid declared-colophon-grid">
  <div class="quick-start-list">
    <div><p class="colophon-number">01</p><p class="colophon-label">NAME THE JOB</p><p class="tiny-note">Start with size, fit, load, reach, and setting.</p></div>
    <div><p class="colophon-number">02</p><p class="colophon-label">READ THE TRADE</p><p class="tiny-note">Know what the pick gives up before you spend.</p></div>
    <div><p class="colophon-number">03</p><p class="colophon-label">CHECK THE CARE</p><p class="tiny-note">Before checkout, look at parts, service, and the stop condition.</p></div>
  </div>
  <div class="keyline-box"><div class="box-title">BEFORE CHECKOUT</div><p class="body">Confirm the exact model, current price, fit, and regional availability. The product page is the place to buy; these pages are the shortcut to a decision you can explain.</p><div class="mini-rule">ONE LAST QUESTION</div><p class="tiny-note">Will this still be a good choice after the first wear, the first repair, and the first change in the market?</p></div>
</div>
''', "colophon-page declared-colophon"))

    for name, path in REVIEW_IMAGES.items():
        if not path.exists():
            raise FileNotFoundError(f"Missing review image '{name}': {path}")
    title = "Platonic Ideal — The Good Buy — Declared Edition"
    return "<!doctype html><html><head><meta charset='utf-8'><title>" + html.escape(title) + "</title><style>" + declared_css() + "</style></head><body>" + "".join(pages) + "</body></html>"


def declared_css() -> str:
    return review_css() + r"""
.declared-cover .cover-deck { max-width:3.35in; }
.declared-cover .cover-list { width:3.55in; }
.declared-quote-layout { grid-template-columns:1fr 3.28in; }
.declared-quote-layout .quote-photo { order:2; }
.declared-quote-layout .quote-copy { order:1; padding-left:.02in; padding-right:.14in; }
.declared-quote-layout .quote-photo img { object-position:50% 42%; }
.declared-index { overflow:hidden; }
.declared-index .index-heading { margin-bottom:.13in; }
.declared-index .index-note { max-width:6.5in; margin-bottom:.11in; }
.declared-index-layout { display:grid; grid-template-columns:1fr 1fr; gap:.3in; }
.declared-index-row { display:flex; align-items:baseline; border-top:.7pt solid var(--ink); padding:.045in 0 .038in; font:500 8.85pt/1.02 var(--sans); text-transform:uppercase; letter-spacing:.5px; }
.declared-index-row span:first-child { flex:0 1 auto; }
.declared-index-row .dots { flex:1; border-bottom:.55pt dotted #777; margin:0 .1in .08in; }
.declared-index-row span:last-child { font:500 9.2pt var(--mono); color:var(--red); }
.declared-object-opener .deck { max-width:7.05in; margin:.09in 0 .07in; font-size:11.8pt; line-height:1.28; }
.declared-plate-large { width:100%; height:4.55in; object-fit:contain; display:block; margin:.01in 0 .07in; }
.declared-decision-bottom { display:grid; grid-template-columns:1fr 2.08in; gap:.22in; border-top:1pt solid var(--ink); padding-top:.09in; }
.declared-fact-grid { display:grid; grid-template-columns:repeat(3, 1fr); gap:.045in .15in; }
.declared-fact-grid .fact { min-height:.42in; padding-bottom:.04in; }
.declared-fact-grid .fact b { font-size:12.2pt; }
.declared-fact-grid .fact span { font-size:7.2pt; line-height:1.1; }
.declared-verdict { border-left:1.4pt solid var(--red); padding-left:.14in; font-size:9.3pt; line-height:1.25; }
.declared-verdict p { margin:0 0 .06in; }
.declared-verdict .section-label { margin:0 0 .035in; }
.declared-action-layout { display:grid; grid-template-columns:3.72in 1fr; column-gap:.28in; align-items:start; }
.declared-action-image { width:100%; height:3.75in; object-fit:contain; display:block; }
.declared-action-copy .eyebrow { margin-bottom:.05in; }
.declared-action-copy h2 { font-size:15pt; line-height:1.08; margin-bottom:.07in; }
.declared-action-copy .small-copy { font-size:9.3pt; line-height:1.27; }
.declared-action-copy .note-rule { font-size:9.1pt; line-height:1.24; margin:.08in 0; }
.declared-action-copy .ruled-list li { font-size:8.8pt; line-height:1.17; padding:.047in 0; }
.declared-action-copy .ruled-list b { font-size:7.9pt; }
.declared-action .declared-candidate-table { margin-top:.09in; }
.candidate-note { margin:-.01in 0 .04in; font-size:8.4pt; line-height:1.18; color:var(--muted); }
.declared-candidate-table { font-size:7.35pt; line-height:1.14; }
.declared-candidate-table th { font-size:7.1pt; padding:.04in .045in .04in 0; }
.declared-candidate-table td { padding:.042in .045in .042in 0; }
.declared-candidate-table td:first-child { width:1.55in; }
.declared-decision-compact .declared-plate-large { height:4.02in; }
.declared-decision-compact .declared-editorial-analysis p:last-child { font-size:8.4pt; line-height:1.15; }
.declared-action-compact .declared-action-copy .small-copy { font-size:8.9pt; line-height:1.2; }
.declared-action-compact .declared-action-copy .note-rule { font-size:8.7pt; line-height:1.17; margin:.06in 0; }
.declared-action-compact .declared-action-copy .ruled-list li { font-size:8.3pt; line-height:1.1; padding:.035in 0; }
.declared-action-compact .declared-action-copy .ruled-list b { font-size:7.6pt; }
.declared-action-compact .candidate-note { font-size:8pt; line-height:1.1; margin:-.01in 0 .03in; }
.declared-action-compact .declared-candidate-table { font-size:7.1pt; line-height:1.08; margin-bottom:.08in; }
.declared-action-compact .declared-candidate-table th { padding:.03in .04in .03in 0; }
.declared-action-compact .declared-candidate-table td { padding:.03in .04in .03in 0; }
.declared-action-compact .declared-comparative-analysis { grid-template-columns:1.45in 1fr; gap:.12in; margin-top:.06in; padding-top:.04in; }
.declared-action-compact .declared-comparative-analysis > p { font-size:7.95pt; line-height:1.12; }
.declared-action-compact .cta-row { margin-top:.04in; }
.declared-care .deck { max-width:6.9in; margin:.06in 0 .08in; font-size:10.8pt; }
.declared-care-layout { display:grid; grid-template-columns:2.72in 1fr; gap:.22in; align-items:start; }
.declared-detail-image { width:100%; height:3.02in; object-fit:contain; display:block; }
.declared-detail-figure { margin-top:.03in; }
.declared-detail-column { min-width:0; }
.declared-part-callouts { margin-top:.08in; border-top:.85pt solid var(--ink); padding-top:.045in; }
.declared-part-callouts .section-label { margin:0 0 .05in; }
.declared-part-callout-grid { display:grid; grid-template-columns:repeat(4, 1fr); column-gap:.2in; row-gap:0; }
.declared-part-callout { display:grid; grid-template-columns:.28in 1fr; column-gap:.06in; border-top:.55pt solid #bdb8ae; padding:.06in 0 .055in; min-width:0; }
.declared-part-callout .part-callout-number { color:var(--red); font:600 9.2pt var(--mono); line-height:1.18; }
.declared-part-callout strong { display:block; font:600 8.1pt/1.05 var(--sans); letter-spacing:.55px; text-transform:uppercase; }
.declared-part-callout p { margin:.025in 0 0; font:8.8pt/1.16 var(--serif); }
.declared-care-table { margin:0; font-size:8.2pt; line-height:1.18; }
.declared-care-table th { font-size:7.3pt; padding:.04in .045in .04in 0; }
.declared-care-table td { padding:.044in .05in .044in 0; }
.declared-care-table td:first-child { width:.2in; color:var(--red); font-family:var(--mono); }
.declared-care-table td:nth-child(2) { width:.68in; }
.declared-failure-table { margin:.02in 0 .06in; font-size:8.15pt; line-height:1.17; }
.declared-failure-table th { font-size:7.4pt; padding:.04in .05in .04in 0; }
.declared-failure-table td { padding:.045in .05in .045in 0; }
.declared-failure-table td:nth-child(1) { width:1.3in; }
.declared-failure-table td:nth-child(2) { width:1.18in; color:var(--red); font-family:var(--sans); font-size:7.2pt; text-transform:uppercase; }
.declared-care .note-rule { font-size:8.9pt; line-height:1.2; margin:.04in 0 .04in; }
.declared-source-line { margin:.04in 0 0; font-size:7.2pt; line-height:1.18; color:var(--muted); }
.declared-source-line .text-link { font-size:7.2pt; margin:0 0 0 .08in; }
.declared-source-line .source-missing { font:7.2pt var(--sans); color:var(--red); }
.declared-editorial-analysis { margin-top:.08in; padding-top:.06in; border-top:1pt solid var(--ink); break-inside:avoid; }
.declared-editorial-analysis .section-label { margin:0 0 .025in; }
.declared-editorial-analysis h3 { margin:0 0 .025in; font-size:10.5pt; line-height:1.05; }
.declared-editorial-analysis p:last-child { margin:0; font-size:8.65pt; line-height:1.19; }
.declared-comparative-analysis { display:grid; grid-template-columns:1.65in 1fr; gap:.16in; align-items:start; margin-top:.1in; padding-top:.06in; border-top:1pt solid var(--ink); break-inside:avoid; }
.declared-comparative-analysis .section-label { margin:0 0 .025in; }
.declared-comparative-analysis h3 { margin:0; font-size:10.2pt; line-height:1.05; }
.declared-comparative-analysis > p { margin:0; font-size:8.35pt; line-height:1.2; }
.declared-image-missing { height:2.8in; display:flex; align-items:center; justify-content:center; border-top:1pt solid var(--ink); border-bottom:1pt solid var(--ink); font:8pt var(--sans); letter-spacing:.7px; text-transform:uppercase; }
.colophon-number { margin:0; color:var(--red); font:600 31pt/.86 var(--sans); }
.colophon-label { margin:.035in 0 .13in; font:600 8pt var(--sans); letter-spacing:1px; text-transform:uppercase; }
.quick-start-list { display:grid; align-content:start; gap:.12in; }
.quick-start-list > div { border-top:.85pt solid var(--ink); padding-top:.08in; }
.quick-start-list .tiny-note { margin:.04in 0 0; font-size:9.2pt; line-height:1.22; }
.declared-colophon-grid .keyline-box { height:max-content; }
.declared-comparison h1 { font-size:27pt; }
.declared-comparison-table { margin-top:.04in; font-size:7.25pt; line-height:1.16; }
.declared-comparison-table th { font-size:7.15pt; padding:.04in .04in .04in 0; }
.declared-comparison-table td { padding:.043in .045in .043in 0; }
.declared-comparison-table td:nth-child(1) { width:1.02in; }
.declared-comparison-table td:nth-child(2) { width:1.45in; }
.declared-comparison-table td:nth-child(5) { width:.47in; }
.declared-comparison-table .text-link { font-size:7pt; margin:0; }
.declared-source-columns { display:grid; grid-template-columns:1fr 1fr; gap:.26in; margin-top:.09in; }
.declared-source-item { border-top:.75pt solid var(--ink); padding:.047in 0 .055in; margin:0 0 .055in; }
.declared-source-item h3 { color:var(--red); margin:0 0 .03in; font-size:8.5pt; letter-spacing:.7px; }
.declared-source-item p { margin:0 0 .02in; font-size:7.95pt; line-height:1.16; }
.declared-source-item p strong { font-size:8.2pt; }
.declared-source-item .source-link { font-size:7.7pt; line-height:1.12; }
.declared-source-item .tiny { font-size:6.8pt; }
.declared-glossary .glossary-row { padding:.078in 0; }
.declared-glossary .glossary-row p { font-size:9.1pt; line-height:1.22; }
.prompt-record { margin:.06in 0 0; white-space:pre-wrap; font:7.55pt/1.22 var(--mono); max-height:7.85in; overflow:hidden; }
.declared-colophon-grid { height:4.55in; }
@media print { .declared-index-row { break-inside:avoid; } .declared-source-item { break-inside:avoid; } }
"""


def css() -> str:
    return r"""
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=Yellowtail&family=Roboto+Mono:wght@400;500&display=swap');

:root {
  --paper: #FFFFFF;
  --red: #C6231F;
  --black: #1A1A1A;
  --gray-paper: #F0EEE9;
  --gray-ink: #5B5750;
  --rule: rgba(26,26,26,.45);
}

* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; background: #3A3733; }
body { color: var(--black); font-family: 'Source Serif 4', Georgia, serif; font-size: 10pt; line-height: 1.38; }
a { color: var(--red); text-decoration: none; }
a:hover { color: var(--black); text-decoration: underline; }

@page { size: Letter; margin: 0; }
.page {
  width: 8.5in;
  height: 11in;
  padding: .70in .70in .78in;
  margin: 0 auto;
  position: relative;
  overflow: hidden;
  background: var(--paper);
  border: 1px solid var(--black);
  page-break-after: always;
}
.page:last-child { page-break-after: auto; }
.page::before {
  content: "";
  position: absolute;
  left: .70in; right: .70in; top: .43in;
  border-top: 1px solid rgba(26,26,26,.18);
  pointer-events: none;
}
.footer {
  position: absolute; left: .70in; right: .70in; bottom: .30in;
  height: 19px; display: flex; align-items: stretch;
  font-family: Oswald, 'Arial Narrow', sans-serif;
  font-size: 7pt; letter-spacing: .13em; text-transform: uppercase;
  color: var(--paper);
}
.footer-main { flex: 1; background: var(--red); padding: 4px 8px 2px; white-space: nowrap; }
.footer-tab { width: 23px; background: var(--black); color: var(--paper); text-align: center; padding-top: 4px; font-weight: 700; }
.topline {
  display: flex; justify-content: space-between; align-items: baseline;
  border-bottom: 1px solid var(--black); padding-bottom: 6px;
  font-family: Oswald, 'Arial Narrow', sans-serif;
  font-size: 8pt; font-weight: 500; letter-spacing: .18em; text-transform: uppercase;
}
.topline-left { color: var(--red); }
.topline-right { color: var(--black); }
.red { color: var(--red); }
.script { margin-top: 12px; color: var(--red); font-family: Yellowtail, cursive; font-size: 29pt; line-height: .88; }
.display {
  margin: 4px 0 12px; color: var(--black);
  font-family: Oswald, 'Arial Narrow', sans-serif; font-weight: 700;
  text-transform: uppercase; line-height: .96; letter-spacing: -.01em;
}
.body { margin: 0 0 9px; }
.body.intro { max-width: 47em; font-size: 11pt; line-height: 1.42; }
.section-heading {
  margin: 18px 0 9px; padding-top: 7px; border-top: 3px solid var(--black);
  font-family: Oswald, 'Arial Narrow', sans-serif; font-weight: 700;
  text-transform: uppercase; line-height: 1.01;
}
.cards-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }
.card {
  min-height: 86px; padding: 8px 10px 9px; border: 1px solid var(--black);
  background: var(--gray-paper); break-inside: avoid;
}
.card:nth-child(even) { background: #F7F2E6; }
.card-number { color: var(--red); font-family: Oswald, sans-serif; font-size: 12pt; font-weight: 700; line-height: 1; }
.card-title { margin: 4px 0 4px; font-family: Oswald, 'Arial Narrow', sans-serif; font-size: 8.5pt; font-weight: 700; letter-spacing: .11em; text-transform: uppercase; }
.card-text { font-size: 8.6pt; line-height: 1.35; }
.dark-card { color: var(--paper); background: var(--black) !important; border-color: var(--black); }
.dark-card .card-number, .dark-card .card-title { color: var(--paper); }
.dark-callout {
  margin-top: 10px; padding: 10px 13px; color: var(--paper); background: var(--black);
  font-size: 9.2pt; line-height: 1.37; break-inside: avoid;
}
.dark-callout > span { font-family: Oswald, sans-serif; font-size: 8.5pt; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; }
.dark-callout small { font-family: Oswald, sans-serif; letter-spacing: .08em; }
.method-bottom { margin-top: 18px; }
.five-layer-grid { margin-top: 12px; }
.five-layer-grid .card:last-child { grid-column: 1 / -1; }
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; align-items: start; }
.keyline-box { border: 1px solid var(--black); padding: 10px 12px; break-inside: avoid; }
.box-title, .mini-rule {
  font-family: Oswald, 'Arial Narrow', sans-serif; font-size: 8.5pt; font-weight: 700;
  letter-spacing: .16em; text-transform: uppercase;
}
.mini-rule { margin: 14px 0 8px; padding-bottom: 4px; border-bottom: 1px solid var(--black); }
.simple-table, .candidate-table { width: 100%; border-collapse: collapse; }
.simple-table td { padding: 3px 0; border-bottom: 1px solid rgba(26,26,26,.22); font-size: 8.7pt; vertical-align: top; }
.simple-table tr:last-child td { border-bottom: 0; }
.simple-table td:nth-child(2) { text-align: right; font-family: Oswald, sans-serif; font-weight: 700; }
.simple-table td:last-child { padding-left: 9px; }
.red-number { color: var(--red); font-family: Oswald, sans-serif; font-weight: 700; }
.tiny-note { margin: 8px 0 0; font-size: 8.2pt; font-style: italic; line-height: 1.32; }
.stat-line {
  display: flex; align-items: baseline; gap: 8px; margin-top: 16px; padding: 8px 0;
  border-top: 1px solid var(--black); border-bottom: 1px solid var(--black);
  font-family: Oswald, sans-serif; letter-spacing: .12em; text-transform: uppercase;
}
.stat-line strong { color: var(--red); font-size: 17pt; letter-spacing: 0; }
.stat-line span { font-size: 7.5pt; margin-right: 14px; }
.index-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 17px; margin-top: 12px; }
.index-row {
  display: grid; grid-template-columns: 30px 1fr 86px; align-items: center;
  min-height: 22px; padding: 3px 5px; border-bottom: 1px solid rgba(26,26,26,.18);
  font-family: Oswald, sans-serif; font-size: 7pt; letter-spacing: .04em;
}
.index-row:nth-child(odd) { background: var(--gray-paper); }
.index-row span:first-child { color: var(--red); font-weight: 700; }
.index-row a { color: var(--black); font-size: 7.2pt; }
.index-row span:nth-child(3) { color: var(--gray-ink); font-size: 6.2pt; text-transform: uppercase; }
.index-row span:first-child { text-align: right; padding-right: 4px; }
.declaration-key { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 17px; }
.declaration-key > div { border-top: 3px solid var(--black); padding-top: 8px; }
.declaration-key span { float: left; margin-right: 10px; color: var(--red); font-family: Oswald, sans-serif; font-size: 18pt; font-weight: 700; }
.declaration-key strong { font-family: Oswald, sans-serif; font-size: 9pt; letter-spacing: .13em; text-transform: uppercase; }
.declaration-key p { margin: 5px 0 0 34px; font-size: 9pt; }
.product-layout, .open-layout { display: grid; grid-template-columns: 1.07fr .93fr; gap: 24px; align-items: start; margin-top: 12px; }
.product-copy { min-width: 0; }
.product-title { margin: 0; font-family: Oswald, 'Arial Narrow', sans-serif; font-size: 27pt; font-weight: 700; line-height: .94; text-transform: uppercase; overflow-wrap: anywhere; }
.product-subtitle { margin: 5px 0 12px; font-size: 10.5pt; font-style: italic; line-height: 1.25; }
.lead { margin: 0 0 10px; padding-left: 11px; border-left: 3px solid var(--red); font-size: 10.7pt; font-weight: 600; line-height: 1.31; }
.metric-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0 11px; margin-top: 10px; }
.metric { min-height: 45px; padding: 5px 0 6px; border-top: 1px solid var(--black); }
.metric strong { display: block; font-family: Oswald, 'Arial Narrow', sans-serif; font-size: 13pt; line-height: 1.04; }
.metric em { display: block; font-size: 7.6pt; font-style: italic; line-height: 1.15; }
.plate { margin: 0; padding: 7px; border: 1px solid var(--black); background: #F7F2E6; break-inside: avoid; }
.plate img { width: 100%; height: 218px; display: block; object-fit: contain; }
.plate figcaption { display: flex; align-items: baseline; flex-wrap: wrap; gap: 5px; margin-top: 5px; font-size: 7.5pt; line-height: 1.2; }
.plate figcaption em { margin-left: auto; font-style: italic; }
.red-label, .outline-label, .badge {
  display: inline-block; padding: 2px 6px; font-family: Oswald, sans-serif;
  font-size: 7.2pt; letter-spacing: .13em; line-height: 1.1; text-transform: uppercase;
}
.red-label { color: var(--paper); background: var(--red); }
.outline-label { border: 1px solid var(--black); }
.badge { padding: 3px 8px; }
.badge-declared { color: var(--paper); background: var(--black); }
.badge-open { color: var(--red); border: 1px solid var(--black); }
.feature-grid { margin-top: 12px; grid-template-columns: repeat(3, 1fr); }
.feature-grid .card { min-height: 103px; }
.score-row {
  display: flex; gap: 21px; align-items: baseline; flex-wrap: wrap;
  margin-top: 10px; padding: 7px 0 6px; border-top: 1px solid var(--black);
  font-family: Oswald, sans-serif; font-size: 7.2pt; letter-spacing: .13em;
}
.score-row em { margin-left: auto; font-family: 'Source Serif 4', serif; font-size: 7.2pt; letter-spacing: 0; }
.bars { color: var(--red); letter-spacing: 1px; }
.empty-bars { color: rgba(26,26,26,.28); letter-spacing: 1px; }
.ownership-teaser { margin-top: 10px; border-top: 3px solid var(--black); padding-top: 7px; }
.ownership-teaser h2 { margin: 0 0 5px; font-family: Oswald, sans-serif; font-size: 16pt; line-height: 1; text-transform: uppercase; }
.ownership-teaser p { margin: 0; font-size: 9.3pt; }
.ownership-teaser .mini-rule { margin-top: 10px; }
.source-summary { margin-top: 7px; padding: 6px 0; border-top: 1px solid var(--black); border-bottom: 1px solid rgba(26,26,26,.25); font-size: 7.5pt; line-height: 1.28; }
.source-summary .red { font-family: Oswald, sans-serif; font-weight: 700; letter-spacing: .11em; }
.ownership-page .section-heading { margin-top: 9px; }
.ownership-page .body.intro { font-size: 10.5pt; }
.source-facts-heading { margin: 8px 0 5px; padding-bottom: 4px; border-bottom: 1px solid var(--black); font-family: Oswald, 'Arial Narrow', sans-serif; font-size: 8.5pt; font-weight: 700; letter-spacing: .16em; text-transform: uppercase; }
.source-facts { display: grid; grid-template-columns: 1fr 1fr; gap: 0 18px; border-bottom: 1px solid rgba(26,26,26,.25); }
.source-fact { min-height: 47px; padding: 5px 0 6px; border-top: 1px solid rgba(26,26,26,.25); }
.source-fact strong { display: block; color: var(--red); font-family: Oswald, sans-serif; font-size: 7.2pt; letter-spacing: .11em; }
.source-fact span { display: block; margin-top: 2px; font-size: 7.7pt; line-height: 1.22; }
.source-audit-note { margin: 5px 0 7px; color: var(--gray-ink); font-size: 7.3pt; line-height: 1.25; }
.source-audit-note .red { font-family: Oswald, sans-serif; font-weight: 700; letter-spacing: .11em; }
.care-grid { grid-template-columns: repeat(4, 1fr); gap: 10px; }
.care-grid .card { min-height: 95px; padding-left: 8px; padding-right: 8px; }
.failure-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
.failure-card { min-height: 91px; padding: 8px 10px 9px; border: 1px solid var(--black); background: var(--gray-paper); break-inside: avoid; }
.failure-card:nth-child(2) { background: #F7F2E6; }
.dark-failure { color: var(--paper); background: var(--black) !important; border-color: var(--black); }
.failure-title { font-family: Oswald, 'Arial Narrow', sans-serif; font-size: 8.5pt; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; }
.failure-status { margin: 3px 0 4px; color: var(--red); font-family: Oswald, sans-serif; font-size: 8pt; line-height: 1.1; text-transform: uppercase; }
.dark-status { color: var(--paper); }
.failure-text { font-size: 8.2pt; line-height: 1.28; }
.candidate-table { margin-top: 7px; border: 1px solid var(--black); font-size: 7.6pt; }
.candidate-table th { padding: 5px 6px; border-bottom: 1px solid var(--black); text-align: left; font-family: Oswald, sans-serif; font-size: 7pt; letter-spacing: .11em; text-transform: uppercase; }
.candidate-table td { padding: 5px 6px; border-bottom: 1px solid rgba(26,26,26,.25); vertical-align: top; line-height: 1.25; }
.candidate-table tr:last-child td { border-bottom: 0; }
.dark-callout + .source-line { margin-top: 7px; }
.source-line { font-size: 7.5pt; line-height: 1.3; }
.source-line .red { font-family: Oswald, sans-serif; font-weight: 700; letter-spacing: .12em; }
.source-date { float: right; font-style: italic; }
.source-missing { color: var(--gray-ink); font-style: italic; }
.open-layout { grid-template-columns: 1.1fr .9fr; }
.open-layout .metric-grid { margin-top: 16px; }
.state-panel {
  min-height: 190px; padding: 18px; color: var(--paper); background: var(--black);
  display: flex; flex-direction: column; justify-content: center; align-items: center;
  text-align: center; border: 1px solid var(--black);
}
.large-state { min-height: 215px; }
.state-code { color: var(--red); font-family: Oswald, sans-serif; font-size: 72pt; font-weight: 700; line-height: .9; }
.state-label { margin-top: 10px; font-family: Oswald, sans-serif; font-size: 11pt; letter-spacing: .12em; text-transform: uppercase; }
.state-note { max-width: 23em; margin-top: 9px; font-size: 8.7pt; line-height: 1.3; }
.evidence-strip { display: grid; grid-template-columns: repeat(4, 1fr); border: 1px solid var(--black); }
.evidence-strip > div { min-height: 57px; padding: 7px; border-right: 1px solid var(--black); }
.evidence-strip > div:last-child { border-right: 0; }
.evidence-strip strong { display: block; color: var(--red); font-family: Oswald, sans-serif; font-size: 7.4pt; letter-spacing: .12em; }
.evidence-strip span { display: block; margin-top: 3px; font-size: 7.8pt; line-height: 1.2; }
.domain-layout { display: grid; grid-template-columns: 270px 1fr; gap: 25px; margin-top: 18px; }
.domain-plate { height: 570px; padding: 8px; background: #F7F2E6; border: 1px solid var(--black); }
.domain-plate .plate { border: 0; padding: 0; height: 100%; }
.domain-plate .plate img { height: 510px; }
.domain-plate .plate figcaption { display: none; }
.domain-copy { padding-top: 20px; }
.kicker { font-family: Oswald, sans-serif; font-size: 8.5pt; letter-spacing: .17em; text-transform: uppercase; }
.domain-title { margin: 8px 0 10px; font-family: Oswald, sans-serif; font-size: 30pt; line-height: .95; text-transform: uppercase; }
.domain-description { font-size: 11pt; line-height: 1.35; }
.domain-metrics { display: grid; gap: 18px; margin-top: 35px; }
.domain-metrics strong { color: var(--red); font-family: Oswald, sans-serif; font-size: 21pt; line-height: 1; }
.domain-metrics em { margin-left: 10px; color: var(--black); font-size: 7.5pt; font-style: normal; letter-spacing: .16em; }
.domain-quote { margin: 36px 0 20px; padding: 11px 12px; border-left: 3px solid var(--red); background: var(--gray-paper); font-size: 11pt; line-height: 1.32; }
.domain-quote span, .cover-quote span { display: block; margin-top: 8px; font-family: Oswald, sans-serif; font-size: 7.4pt; letter-spacing: .13em; text-transform: uppercase; }
.domain-map { display: grid; grid-template-columns: 1fr 1fr; gap: 17px; }
.domain-row { display: grid; grid-template-columns: 30px 1fr 92px; min-height: 23px; align-items: center; padding: 3px 5px; border-bottom: 1px solid rgba(26,26,26,.18); font-family: Oswald, sans-serif; font-size: 6.9pt; }
.domain-row:nth-child(odd) { background: var(--gray-paper); }
.domain-row > span:first-child { color: var(--red); font-weight: 700; }
.domain-row > span:nth-child(2) { font-size: 7pt; }
.domain-status { color: var(--gray-ink); font-size: 5.9pt; text-transform: uppercase; }
.domain-row > span:first-child { text-align: right; padding-right: 4px; }
.ledger-grid { columns: 2; column-gap: 22px; margin-top: 10px; }
.ledger-item { break-inside: avoid; margin-bottom: 6px; font-size: 7.3pt; line-height: 1.20; }
.ledger-code { display: inline-block; min-width: 28px; color: var(--red); font-family: Oswald, sans-serif; font-size: 8pt; font-weight: 700; letter-spacing: .08em; }
.ledger-item strong { margin-right: 4px; font-family: Oswald, sans-serif; font-size: 7.3pt; letter-spacing: .05em; text-transform: uppercase; }
.ledger-item > span:nth-of-type(2) { display: inline; color: var(--gray-ink); font-size: 6.9pt; }
.ledger-item p { margin: 2px 0 0; font-size: 7.0pt; line-height: 1.15; }
.image-ledger { margin-top: 10px; border-top: 1px solid var(--black); }
.image-row { display: grid; grid-template-columns: 52px 125px 118px 1fr; gap: 7px; align-items: baseline; padding: 5px 4px; border-bottom: 1px solid rgba(26,26,26,.24); font-size: 7.2pt; }
.image-row:nth-child(odd) { background: var(--gray-paper); }
.image-row strong { font-family: Oswald, sans-serif; font-size: 7.3pt; text-transform: uppercase; }
.image-row span:nth-of-type(2) { font-size: 6.8pt; }
.image-row span:nth-of-type(3) { color: var(--gray-ink); overflow-wrap: anywhere; font-size: 6.5pt; }
.image-row em { grid-column: 4; font-size: 6.6pt; }
.prompt-box {
  margin: 12px 0 0; padding: 13px; min-height: 480px; white-space: pre-wrap;
  border: 1px solid var(--black); background: #F7F2E6;
  font-family: 'Roboto Mono', 'Courier New', monospace; font-size: 7.5pt; line-height: 1.42;
}
.cover-page::before { display: none; }
.cover-top { display: flex; justify-content: space-between; border-bottom: 3px solid var(--black); padding-bottom: 7px; font-family: Oswald, sans-serif; font-size: 7.5pt; letter-spacing: .18em; text-transform: uppercase; }
.cover-top .red { font-weight: 700; }
.cover-layout { display: grid; grid-template-columns: 1fr 196px; gap: 24px; align-items: start; margin-top: 24px; }
.cover-title { font-family: Oswald, sans-serif; font-size: 35pt; font-weight: 700; line-height: .9; text-transform: uppercase; letter-spacing: -.01em; }
.cover-deck { margin: 14px 0 0; font-size: 9.6pt; line-height: 1.36; }
.cover-rule { display: flex; gap: 10px; margin-top: 17px; padding: 7px 0; border-top: 1px solid var(--black); border-bottom: 1px solid var(--black); font-family: Oswald, sans-serif; font-size: 7.5pt; letter-spacing: .16em; }
.cover-rule b { color: var(--red); }
.cover-portrait { margin: 0; }
.cover-portrait img { width: 100%; height: 218px; display: block; object-fit: cover; filter: grayscale(1) contrast(1.08); border: 1px solid var(--black); }
.cover-portrait figcaption { margin-top: 5px; font-size: 7.3pt; line-height: 1.25; font-style: italic; }
.cover-portrait strong { font-family: Oswald, sans-serif; letter-spacing: .12em; font-style: normal; }
.cover-portrait span { font-size: 6.8pt; }
.cover-quote { margin: 23px 0 0; padding: 8px 0 8px 13px; border-left: 3px solid var(--red); font-size: 11.5pt; line-height: 1.3; }
.cover-bottom { margin-top: 18px; padding-top: 8px; border-top: 1px solid var(--black); font-family: Oswald, sans-serif; font-size: 8pt; letter-spacing: .14em; }
.colophon-grid { display: grid; grid-template-columns: .75fr 1.25fr; gap: 25px; margin-top: 25px; }
.colophon-number { margin: 0; color: var(--red); font-family: Oswald, sans-serif; font-size: 42pt; font-weight: 700; line-height: .85; }
.colophon-label { margin: 4px 0 21px; font-family: Oswald, sans-serif; font-size: 7.8pt; letter-spacing: .13em; text-transform: uppercase; }
@media print {
  html, body { background: var(--paper); }
  .page { margin: 0; }
}

/*
 * Delta 1940 proof system
 * -----------------------
 * The full run uses the same page frame and editorial grammar as the proof.
 * These rules intentionally come last so the legacy full-run component rules
 * cannot reintroduce the old cream canvas, outer page border, or footer bar.
 */
html, body { width: 8.5in; background: #fff; }
body { color: var(--black); font-family: 'Source Serif 4', Georgia, serif; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.review-page { position: relative; width: 8.5in; height: 11in; padding: .49in .62in .7in; margin: 0; overflow: hidden; background: #fff; page-break-after: always; break-after: page; }
.review-page:last-child { page-break-after: auto; break-after: auto; }
.page-border { position: absolute; inset: .17in; border: .8pt solid #262626; pointer-events: none; }
.review-page .page-content { position: relative; z-index: 1; height: 9.38in; padding-top: .18in; }
.review-page .topline { position: relative; z-index: 2; height: .28in; display: flex; justify-content: space-between; align-items: center; border-bottom: .8pt solid var(--black); padding: 0; font: 500 8pt Oswald, 'Arial Narrow', sans-serif; letter-spacing: 1.1px; text-transform: uppercase; }
.review-page .topline span { white-space: nowrap; flex: 0 0 auto; }
.review-page .topline-left { color: var(--red); }
.review-page .topline-right { color: var(--black); }
.footer-rule { position: absolute; left: .17in; right: .17in; bottom: .17in; height: .105in; background: var(--red); }
.folio { position: absolute; left: .49in; right: .87in; bottom: .31in; height: .17in; display: flex; align-items: center; gap: .1in; font: 500 8pt Oswald, 'Arial Narrow', sans-serif; letter-spacing: 1.1px; color: var(--black); }
.folio i { font-style: normal; color: var(--red); }
.page-number { position: absolute; right: .17in; bottom: .17in; display: flex; align-items: center; justify-content: center; width: .48in; height: .37in; background: #171717; color: #fff; font: 500 10pt 'Roboto Mono', monospace; z-index: 3; }
.review-page .display { margin: 4px 0 12px; font-family: Oswald, 'Arial Narrow', sans-serif; font-weight: 600; text-transform: uppercase; line-height: 1.02; letter-spacing: .2px; }
.review-page .script { margin-top: 8px; color: var(--red); font-family: Yellowtail, cursive; font-size: 24pt; line-height: .9; }
.review-page .body { margin: 0 0 9px; font-size: 10pt; line-height: 1.34; }
.review-page .body.intro { max-width: 47em; font-size: 11pt; line-height: 1.38; }
.review-page .section-heading { margin: 18px 0 9px; padding-top: 7px; border-top: 2px solid var(--black); font-family: Oswald, 'Arial Narrow', sans-serif; font-weight: 600; text-transform: uppercase; line-height: 1.04; }
.review-page .cards-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 0 18px; }
.review-page .card { min-height: 78px; padding: 10px 4px 11px 0; border: 0; border-top: .65pt solid var(--black); background: transparent; break-inside: avoid; }
.review-page .card:nth-child(even) { background: transparent; }
.review-page .card-number { color: var(--red); font-family: Oswald, sans-serif; font-size: 12pt; font-weight: 600; line-height: 1; }
.review-page .card-title { margin: 4px 0 4px; font-family: Oswald, 'Arial Narrow', sans-serif; font-size: 8.5pt; font-weight: 600; letter-spacing: .11em; text-transform: uppercase; }
.review-page .card-text { font-size: 8.6pt; line-height: 1.34; }
.review-page .dark-card { color: var(--black); background: transparent !important; border-color: var(--black); }
.review-page .dark-card .card-number, .review-page .dark-card .card-title { color: var(--red); }
.review-page .dark-callout { margin-top: 10px; padding: 8px 0 4px 12px; color: var(--black); background: transparent; border-left: 2px solid var(--red); border-top: 0; font-size: 9.2pt; line-height: 1.37; break-inside: avoid; }
.review-page .dark-callout > span { color: var(--red); font-family: Oswald, sans-serif; font-size: 8.5pt; font-weight: 600; letter-spacing: .12em; text-transform: uppercase; }
.review-page .keyline-box { border: 0; border-top: 1px solid var(--black); border-bottom: 1px solid var(--black); padding: 10px 0; break-inside: avoid; }
.review-page .product-layout, .review-page .open-layout { margin-top: 12px; }
.review-page .product-title { font-family: Oswald, 'Arial Narrow', sans-serif; font-size: 30pt; font-weight: 600; line-height: 1.02; text-transform: uppercase; }
.review-page .plate { margin: 0; padding: 0; border: 0; background: transparent; break-inside: avoid; }
.review-page .plate img { width: 100%; height: 2.85in; display: block; object-fit: contain; }
.review-page .plate figcaption { display: flex; align-items: baseline; flex-wrap: wrap; gap: 5px; margin-top: 5px; border-top: .6pt solid #aaa; padding-top: 5px; font-size: 7.5pt; line-height: 1.2; }
.review-page .feature-grid { margin-top: 12px; grid-template-columns: repeat(3, 1fr); gap: 0 14px; }
.review-page .feature-grid .card { min-height: 93px; }
.review-page .source-summary { margin-top: 7px; padding: 6px 0; border-top: 1px solid var(--black); border-bottom: 1px solid rgba(26,26,26,.25); font-size: 7.5pt; line-height: 1.28; }
.review-page .candidate-table { border: 0; border-top: 1px solid var(--black); border-bottom: 1px solid var(--black); }
.review-page .candidate-table th { border-bottom: 1px solid var(--black); }
.review-page .candidate-table td { border-bottom: .5px solid rgba(26,26,26,.25); }
.review-page .index-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0 28px; margin-top: 12px; }
.review-page .index-row { display: grid; grid-template-columns: .45in 1fr 1.25in; align-items: baseline; min-height: 25px; padding: 7px 0 6px; border-top: .7pt solid var(--black); border-bottom: 0; background: transparent; font: 500 9.5pt Oswald, sans-serif; letter-spacing: .04em; }
.review-page .index-row:nth-child(odd) { background: transparent; }
.review-page .index-row span:first-child { color: var(--red); font-weight: 600; text-align: right; padding-right: 8px; }
.review-page .index-row a { color: var(--black); font: 500 9.5pt Oswald, sans-serif; text-transform: uppercase; }
.review-page .index-row span:nth-child(3) { color: var(--gray-ink); font-size: 7.2pt; text-transform: uppercase; text-align: right; }
.review-page .domain-plate { border: 0; border-top: 1px solid var(--black); padding: 8px 0 0; background: transparent; }
.review-page .domain-row:nth-child(odd) { background: transparent; }
.review-page .ledger-grid { margin-top: 10px; }

/* Cover: same left-copy / right-Plato composition as the proof. */
.review-page.cover-page .page-content { height: 9.48in; padding-top: .18in; }
.cover-page .cover-copy { position: absolute; z-index: 2; left: .2in; top: .78in; width: 4.16in; }
.cover-page .cover-brand { margin: 0 0 .52in; color: var(--red); font: 600 13pt Oswald, sans-serif; letter-spacing: 2px; }
.cover-page .cover-label { margin: 0 0 .13in; font: 500 9.5pt Oswald, sans-serif; letter-spacing: 1.2px; }
.cover-page .cover-copy h1 { margin: 0; color: var(--black); font: 700 36pt/1.05 Oswald, sans-serif; text-transform: uppercase; }
.cover-page .cover-deck { max-width: 3.18in; margin: .23in 0 0; font-size: 15pt; line-height: 1.25; }
.cover-page .cover-list { margin-top: .34in; padding-top: .12in; border-top: 1pt solid var(--black); width: 3.2in; font: 500 9pt/1.75 Oswald, sans-serif; letter-spacing: .35px; text-transform: uppercase; }
.cover-page .cover-date { position: absolute; left: .2in; bottom: .26in; z-index: 2; font: 500 8pt 'Roboto Mono', monospace; }
.cover-page .cover-art { position: absolute; top: .23in; right: .02in; width: 4.68in; height: 8.85in; object-fit: cover; object-position: 68% 50%; }
.cover-page .cover-quote { position: absolute; left: .2in; bottom: .72in; width: 3.35in; margin: 0; padding: 8px 0 8px 13px; border-left: 3px solid var(--red); background: transparent; font-size: 10.5pt; line-height: 1.3; }
.cover-page .cover-quote span { display: block; margin-top: 8px; font: 500 7.4pt Oswald, sans-serif; letter-spacing: .13em; text-transform: uppercase; }

@media print { html, body { width: 8.5in; background: #fff; } .review-page { margin: 0; } }
"""

def build_html(entries: list[Entry]) -> str:
    pages: list[str] = []
    page_number = 1
    pages.append(cover_page(page_number)); page_number += 1
    pages.append(edition_page(page_number)); page_number += 1
    pages.append(edition_inventory_page(page_number)); page_number += 1
    alphabetical = sorted(entries, key=lambda entry: entry.category.lower())
    pages.append(index_page(alphabetical[:50], "A - M", page_number)); page_number += 1
    pages.append(index_page(alphabetical[50:], "N - Z", page_number)); page_number += 1

    methods = [
        ("READER'S KEY", "Read", "READ THE RULING:", "Then Audit It",
         "Each category starts with the job and state. The declaration is only the beginning; the ownership page tests whether the answer survives use.",
         [("01", "START WITH THE FORM", "Size, region, installation, fit, load, and use conditions belong here before a model is compared."),
          ("02", "READ THE STATE", "Declared, candidate, empty, split, conditional, and consumable are different conclusions."),
          ("03", "INSPECT THE PLATE", "The truth label says whether the image is observed exterior, verified construction, conceptual, or interpretive."),
          ("04", "FOLLOW OWNERSHIP", "Maintenance, parts, consumables, storage, software, and service are part of the product."),
          ("05", "PRESSURE-TEST RIVALS", "A candidate remains when it buys a real advantage or could overturn the decision with new evidence."),
          ("06", "OPEN THE SOURCE", "Exact-model identity and service claims resolve to readable source links.")],
         "Reading path: state - Form - plate - reasons - ownership - failures - source - reconsideration trigger."),
        ("CONSTITUTION", "How", "SIX TESTS BEFORE", "A Declaration",
         "A winner must clear every essential threshold. Prestige, novelty, and feature count cannot compensate for a failed job or opaque ownership path.",
         [("01", "FIT", "Does it solve the ordinary job inside the stated use boundary?"),
          ("02", "FORM", "Does construction remove avoidable joints, coatings, proprietary dependencies, or fragile complexity?"),
          ("03", "RECOVERY", "Can ordinary wear be cleaned, sharpened, reseasoned, repaired, rebuilt, or replaced rationally?"),
          ("04", "SUPPLY", "Are the model, consumables, service information, and critical parts obtainable in the intended region?"),
          ("05", "OWNERSHIP", "Are care, storage, failure symptoms, service boundaries, and terminal damage legible?"),
          ("06", "VALUE", "Does extra cost buy a useful property across the ownership horizon?")],
         "A declaration is maintained. New evidence, discontinued parts, recalls, or a better candidate can reopen it."),
        ("CONSTITUTION", "Why", "TEN RULES THAT KEEP", "The List Honest",
         "The dossier resists the pressure to name a product when the category, source, or ownership case is not ready.",
         [("I", "DEFINE BEFORE COMPARING", "A broad category is split before incompatible jobs are forced into one answer."),
          ("II", "NAME EXACT VARIANTS", "Model, generation, size, voltage, region, fit, and configuration are captured whenever they change the verdict."),
          ("III", "PREFER SIMPLE FAILURE", "A visible, serviceable wear part is usually better than a sealed assembly."),
          ("IV", "DO NOT CONFUSE WARRANTY", "A warranty transfers some risk. It does not establish parts, repair, or permanent ownership."),
          ("V", "PRESERVE HONEST EMPTINESS", "If no product qualifies, the useful output is the reason and a specification for what would."),
          ("VI-X", "KEEP JUDGMENT REVISABLE", "Facts are cited, inferences labeled, uncertainty visible, and every ruling has a trigger.")],
         "The standard applies equally to an inexpensive pan, a premium coat, a connected device, and an empty category."),
        ("EVIDENCE", "What", "A SOURCE CAN", "Actually Prove",
         "Sources are ranked by what they can prove. Ten repeated retailer pages do not outweigh one exact service manual.",
         [("A", "EXACT PRIMARY", "Model page, specification, service manual, parts diagram, warranty, safety notice, or filing."),
          ("B", "INDEPENDENT TEST", "A disclosed method applied to the exact model with measurable limitations."),
          ("C", "OWNERSHIP EVIDENCE", "Long-term reports, repair records, teardown evidence, substitutions, and recurring failure patterns."),
          ("D", "MARKET EVIDENCE", "Current price, regional availability, used supply, consumables, and service-center access."),
          ("E", "LEAD ONLY", "Retailer copy, forums, reviews, and search results can locate evidence."),
          ("F", "EDITORIAL INFERENCE", "A judgment that follows from cited facts stays separate from a measurement.")],
         "Source discipline: exact model, evidence role, publisher, region, revision, access date, and claim supported."),
        ("ILLUSTRATION", "Why", "A PICTURE CAN", "Clarify Or Overclaim",
         "The Delta catalog earns attention because its images carry evidence. This dossier borrows that density while making every plate's truth status explicit.",
         [("01", "OBSERVED EXTERIOR", "Visible geometry checked against exact-model identity views."),
          ("02", "VERIFIED CONSTRUCTION", "Hidden relationships shown only when a source or inspection supports them."),
          ("03", "CONCEPTUAL MECHANISM", "A general system or failure path, never the exact hidden engineering."),
          ("04", "INTERPRETIVE PLATE", "Original editorial art that represents the Form, not SKU identity evidence."),
          ("05", "COMPARISON PLATE", "Matched scale and crop make one decisive difference visible."),
          ("06", "OWNERSHIP PLATE", "Consumables, tools, parts, intervals, and failure points show the real owner path.")],
         "Manufacturer photography remains an identity reference unless republication rights are documented."),
        ("OWNERSHIP", "What", "THE OBJECT IS", "Only One Layer",
         "A durable product can still be a poor ownership system when its parts, software, consumables, or service path disappear.",
         [("01", "OBJECT", "Materials, geometry, interfaces, controls, fasteners, and the load path."),
          ("02", "WEAR LAYER", "Seasoning, soles, pads, filters, seals, cords, blades, bearings, batteries, and upholstery."),
          ("03", "CARE", "Cleaning, lubrication, sharpening, drying, storage, inspection, calibration, and updates."),
          ("04", "SERVICE", "Manuals, tools, access, part numbers, substitutions, labor, warranty, and repair economics."),
          ("05", "SUPPLY", "Consumables, standard interfaces, regional availability, software support, and secondhand stock."),
          ("06", "EXIT", "The retirement threshold and what can be reused, rebuilt, sold, or safely discarded.")],
         "The dossier asks whether all six layers remain intelligible over the likely ownership horizon."),
        ("FAILURE", "When", "NAME THE", "Recovery Path",
         "A useful guide tells the owner what a symptom means, what can be attempted safely, and when the object has crossed a terminal boundary.",
         [("R1", "CLEAN OR RESET", "Contamination, configuration, blocked passages, lost seasoning, or minor corrosion may recover."),
          ("R2", "REPLACE WEAR PART", "A blade, filter, belt, cord, seal, pad, grip, battery, or similar layer renews."),
          ("R3", "REPAIR MODULE", "A documented assembly can be serviced with accessible tools and parts."),
          ("R4", "REBUILD", "The sound frame, body, or chassis justifies major renewal."),
          ("T", "TERMINAL", "Cracks, unsafe deformation, obsolete security, missing critical parts, or uneconomic failure can end service."),
          ("?", "UNKNOWN", "When evidence is missing, the dossier records the question.")],
         "Safety-critical electrical, fuel, pressure, structural, and hygiene work may require a qualified professional."),
        ("PRICE AND TIME", "Why", "A PRICE IS A", "Dated Observation",
         "Price, supply, parts, and policy are changing evidence rather than permanent product specifications.",
         [("01", "CAPTURE", "Amount, currency, seller type, region, configuration, and access date."),
          ("02", "NORMALIZE", "Compare like-for-like size, accessories, shipping, installation, and consumables."),
          ("03", "SEPARATE", "A premium can buy material, fit, service, lower weight, finish, or warranty."),
          ("04", "EXTEND", "Five- and ten-year questions include wear parts, energy, labor, and forced changes."),
          ("05", "RECHECK", "Sale price, discontinued status, parts stock, and support policy are revalidated."),
          ("06", "DISCLOSE", "Unknown cost remains unknown. A tidy total is never manufactured.")],
         "Prices in this review are historical working notes unless a source and capture date appear beside them."),
        ("EDITORIAL STATES", "How", "A NON-DECLARATION", "Can Still End A Search",
         "Open states preserve useful distinctions about what research should happen next.",
         [("E", "EMPTY", "No current product clears the Form. The page explains the recurring failure."),
          ("S", "SPLIT REQUIRED", "The parent hides incompatible jobs. Child Forms are defined first."),
          ("C", "CONDITIONAL", "A viable answer depends on installation, fit, region, workload, or service."),
          ("R", "CONSUMABLE", "Wear or hygiene makes replacement intrinsic."),
          ("P", "CANDIDATE", "A model deserves investigation but is missing decisive proof."),
          ("D", "DECLARED", "The current evidence closes the ordinary search while keeping tradeoffs visible.")],
         "The state describes the research conclusion. It is not a product score."),
        ("TESTING", "What", "THE NEXT EVIDENCE", "Should Measure",
         "A final commercial edition should add repeatable tests where a specification or visual inspection cannot settle the ownership question.",
         [("K", "COOKWARE", "Usable surface, flatness, heat response, handle temperature, cleaning, corrosion, and seasoning recovery."),
          ("T", "TOOLS", "Accuracy, balance, interface fit, runout, load behavior, wear, service access, and parts substitution."),
          ("C", "CLOTHING", "Fit stability, seam repair, abrasion, laundering, shrinkage, resoling, and replacement components."),
          ("O", "OUTDOOR", "Load, weather, pack volume, fuel or power supply, field repair, and safety margins."),
          ("E", "ELECTRONICS", "Thermals, battery, software horizon, ports, modules, security, and compatibility."),
          ("H", "HOME SYSTEMS", "Capacity, installation, energy, noise, service access, part price, and qualified labor.")],
         "Every test needs the exact variant, conditions, instruments, repeat count, uncertainty, and failure threshold."),
        ("REVIEW EDITION", "Why", "THE FULL RUN", "Is A Map Of Value",
         "This book makes the intended paid product concrete: deep enough to review as a whole, explicit enough to reveal what still blocks release.",
         [("01", "COMPLETE ARCHITECTURE", "Cover, method, nine domains, 100 category entries, ledgers, and review tools."),
          ("02", "REAL EDITORIAL STATES", "All 48 declarations and 52 open findings are present."),
          ("03", "VISIBLE SOURCE QUALITY", "Exact, family, ambiguous, and generic identity states remain legible."),
          ("04", "DELTA-INSPIRED DENSITY", "Large plates, reasons-why copy, specification blocks, maps, and tables carry the reading order."),
          ("05", "PLATO RETAINED", "The dossier keeps the Plato portrait, sourced passages, mineral palette, and antiquity thread."),
          ("06", "NEXT PRODUCTION GATES", "Candidate sets, model normalization, parts stock, independent tests, rights, copy, and tagged PDF.")],
         "Review question: does this structure make the dossier worth returning to after the purchase decision?"),
    ]
    # The review-edition summary is carried by the cover, edition pages, and
    # colophon; the ten method pages keep the front matter at the designed 16pp.
    for method in methods[:-1]:
        pages.append(method_page(*method, page_number)); page_number += 1

    pages.append(reader_intro_page(page_number)); page_number += 1

    domain_page_map: dict[str, int] = {}
    for domain_index, (domain, name, description) in enumerate(DOMAINS, 1):
        domain_page_map[domain] = page_number
        pages.append(domain_opener(domain_index, domain, name, description, page_number)); page_number += 1
        pages.append(domain_map(domain_index, domain, name, page_number)); page_number += 1

    declared = [entry for entry in entries if entry.status == "DECLARED"]
    declared_index = 0
    open_index = 0
    for domain, _, _ in DOMAINS:
        for entry in ENTRIES_BY_DOMAIN[domain]:
            if entry.status == "DECLARED":
                declared_index += 1
                pages.append(declaration_page(entry, declared_index, page_number)); page_number += 1
                pages.append(ownership_page(entry, declared_index, page_number)); page_number += 1
            else:
                open_index += 1
                pages.append(open_page(entry, page_number, open_index)); page_number += 1

    records = sorted(SOURCE_RECORDS, key=lambda record: record.get("productId", ""))
    for page_index in range(1, 6):
        pages.append(source_ledger_page(records, page_number, page_index)); page_number += 1
    for page_index in range(1, 3):
        pages.append(image_ledger_page(declared[(page_index - 1) * 24: page_index * 24], page_number, page_index)); page_number += 1

    cover_prompt = """EDITORIAL COVER PLATE - GENERATED FROM A SOURCE REFERENCE
Asset: docs/dossier-review/assets/editorial/plato-cover-portrait.png
Reference: public/images/plato-silanion-berlin.webp, a Wikimedia Commons photograph
of a Silanion-type portrait of Plato at the Altes Museum, Berlin.
Reference photographer: Osama Shukir Muhammed Amin FRCP(Glasg.).
Reference license: CC BY-SA 4.0.
Treatment: original editorial engraving-style plate with Plato's eyes visible,
classical architectural context, and a warm paper ground. It is not a museum
photograph and must not be described as one."""
    pages.append(prompt_page("Editorial Cover Portrait", "The full edition uses the approved editorial Plato plate so its cover shares the 20-page proof composition. The source photograph remains in the audit record as the reference and provenance trail.", cover_prompt + "\n\n" + CANONICAL_PROMPT, page_number, 1)); page_number += 1

    technical_text = "\n\n".join(f"{ref}\n{prompt}" for ref, prompt in TECHNICAL_PROMPTS.items())
    pages.append(prompt_page("Three Technical Plates", "These prompts were used for the Lodge, Estwing, and Makita technical plates. They specify the visible construction while prohibiting logos, labels, readable text, and invented hidden mechanisms.", technical_text, page_number, 2)); page_number += 1

    legacy_prompt = """LEGACY INTERPRETIVE PLATES
The raw per-file prompt was not retained for every existing plate. The canonical
prompt family below is the reproducible prompt record; it must be completed with
the category's exact model, Form quality, and three to five physical anchors.

""" + CANONICAL_PROMPT + """

FRYING PAN INTENT
A solemn museum-like specimen plate for a heavy single-piece cast-iron frying
pan. Greek red-figure vessel sensibility with a restrained Byzantine icon panel:
terracotta and black iron mineral pigments, deep curved sidewalls, long handle,
helper handle, pour spouts, and one quiet aureole. No logos, labels, packaging,
readable text, or exact product-photo recreation.

HAMMER INTENT
Preserve the frying-pan plate's terracotta mineral ground, aureole, aged panel,
and solemn composition while expressing a continuous forged-steel curved-claw
hammer. Cobalt grip as the only strong color accent. No logos, labels,
packaging, readable text, or exact product-photo recreation."""
    pages.append(prompt_page("Existing Plate Family", "The public product plates are model-faithful editorial interpretations. Where a legacy raw prompt is unavailable, the record says so and gives the canonical family used for review and regeneration.", legacy_prompt, page_number, 3)); page_number += 1

    pages.append(release_page(page_number)); page_number += 1
    pages.append(update_page(page_number)); page_number += 1
    pages.append(navigation_page(page_number)); page_number += 1
    pages.append(colophon_page(page_number)); page_number += 1

    expected = 196
    if len(pages) != expected:
        raise RuntimeError(f"Page plan produced {len(pages)} pages; expected {expected}")
    return "<!doctype html><html><head><meta charset='utf-8'><title>Platonic Ideal Dossier - 1940 Edition</title><style>" + css() + "</style></head><body>" + "".join(pages) + "</body></html>"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DECLARED_OUTPUT)
    parser.add_argument("--html-only", action="store_true")
    parser.add_argument("--proof", action="store_true", help="build the 20-page four-object design proof")
    parser.add_argument("--legacy-full", action="store_true", help="build the archived category/research edition")
    args = parser.parse_args()

    TMP_DIR.mkdir(parents=True, exist_ok=True)
    if args.proof and args.legacy_full:
        parser.error("--proof and --legacy-full are mutually exclusive")
    if args.proof and args.output == DECLARED_OUTPUT:
        args.output = OUTPUT_DIR / "platonic-ideal-dossier-1940-20-page-proof.pdf"
    if args.legacy_full and args.output == DECLARED_OUTPUT:
        args.output = DEFAULT_OUTPUT
    if args.proof:
        html_path = TMP_DIR / "platonic-ideal-dossier-1940-proof.html"
        document = build_proof_html(ENTRIES)
    elif args.legacy_full:
        html_path = TMP_DIR / "platonic-ideal-dossier-1940-legacy.html"
        document = build_html(ENTRIES)
    else:
        html_path = TMP_DIR / "platonic-ideal-dossier-declared-1940.html"
        document = build_declared_html(ENTRIES)
    html_path.write_text(document, encoding="utf-8")
    print(f"wrote {html_path} ({len(document):,} bytes)")

    if args.html_only:
        return
    if not CHROME.exists():
        raise SystemExit(f"Chrome not found at {CHROME}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    profile = TMP_DIR / f"chrome-profile-{os.getpid()}"
    command = [
        str(CHROME),
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        "--disable-extensions",
        "--no-first-run",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=20000",
        f"--user-data-dir={profile}",
        f"--print-to-pdf={args.output}",
        html_path.resolve().as_uri(),
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        raise SystemExit(result.returncode)
    print(result.stdout[-1000:])
    print(result.stderr[-1000:])
    print(f"wrote {args.output} ({args.output.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
