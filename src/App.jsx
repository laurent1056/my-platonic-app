import React, { useState, useEffect } from 'react';
import { 
  Scale, 
  ArrowRight, 
  CheckCircle2, 
  Ban, 
  History, 
  Clock, 
  AlertTriangle,
  ChevronRight,
  ShieldCheck,
  CalendarDays,
  ImageOff,
  Filter,
  Box,
  Sparkles,
  Loader2,
  XCircle,
  ScrollText,
  Gavel,
  Swords
} from 'lucide-react';

/**
 * PLATONIC IDEAL - INTERNAL RULEBOOK
 */
const RULEBOOK_TEXT = `
Internal Rulebook v1.0 — Platonic Products

Mission
We declare one physical product per category as the Platonic Ideal: the object that best embodies the category’s true function with maximum durability, repairability, and long-term integrity. We prefer finality over novelty.

Core Definition
A product is Platonic if it:
1. Ends the search: owning it makes further shopping in the category feel unnecessary.
2. Improves or stays whole with time: performance doesn’t degrade through ordinary use; if it does, it’s reversible.
3. Has reversible failure modes: damage is fixable by maintenance, repair, parts, refinishing, or service.
4. Is stable: the model’s core materials and construction don’t drift silently year-to-year.
5. Is honest: no fragile complexity pretending to be progress; no engineered obsolescence.
6. Is supported: parts/service/manuals are accessible enough that a normal owner can keep it alive.
7. Is form-faithful: it expresses the essential “Form” of the category, not a subcategory or a lifestyle aesthetic.

What Qualifies as Platonic
The Admission Test (must pass all):
A. Form Clarity: We can state the Form in one sentence: “A ___ is ___.”
B. Longevity Reality: The product is built to last by design, not by luck. There is a credible path to 10–20+ years of ownership.
C. Repair Path: If it breaks, there is a known way to restore function (parts, service, refurb, re-season, resole, rebuild).
D. Model Stability: The name doesn’t hide annual internal downgrades.
E. “No Timers”: No consumable coating or sealed component that forces replacement as a normal lifecycle.

What Disqualifies a Product Even if It’s Popular
- The surface is a countdown timer: Nonstick coatings, fragile finishes, bonded layers that fail before the core.
- Sealed-for-life design: No parts, no service path, no access, proprietary tools, glued assemblies.
- Complexity without recoverability: Touchscreens, sensors, “smart” features, firmware dependence, or electronics that brick the object.
- Silent model drift: The same model name now means cheaper internals.
- Luxury masquerading as quality: Paying for brand rather than core longevity.
- Weak link dependency: One critical component fails and cannot be replaced.
- Optimization for novelty: The value proposition is “new,” not “enduring.”
`;

/**
 * PLATONIC IDEAL - MASTER DATASET (68 ITEMS)
 */
const CATEGORY_DATA = [
  { id: 'frying-pan', category: 'Frying Pan', status: 'DECLARED', model: 'Lodge 12 in Cast Iron Skillet (L10SK3)', price: '$30-40', formDefinition: '12-inch cast iron with 3-4mm walls.', coreReasoning: 'Inert material. Seasoning improves with use. Rust/cracks repairable.', keyDisqualifiers: 'Non-stick coatings. Stainless steel hot spots.', maintenance: 'REPAIRABLE', lifespan: 'Indefinite', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'refrigerator', category: 'Refrigerator', status: 'EMPTY', formDefinition: 'Cold storage with replaceable mechanical heart.', coreReasoning: 'Sealed compressor systems and electronic control boards fail unpredictably.', keyDisqualifiers: 'Sealed systems. Integrated insulation.', maintenance: 'DISPOSABLE', lifespan: '7-12 years', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'hammer', category: 'Hammer', status: 'DECLARED', model: 'Estwing E3-16C', price: '$35', formDefinition: 'Single-piece drop-forged steel.', coreReasoning: 'Head cannot separate from handle. Face heat-treated 50 HRC.', keyDisqualifiers: 'Wood handles (break). Fiberglass (bond fails).', maintenance: 'REPAIRABLE', lifespan: 'Indefinite', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'smartphone', category: 'Smartphone', status: 'EMPTY', formDefinition: 'Communication device resistant to obsolescence.', coreReasoning: 'Glued batteries and software support windows force replacement.', keyDisqualifiers: 'Sealed construction. Locked bootloaders.', maintenance: 'CONSUMABLE', lifespan: '3-4 years', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'kitchen-knife', category: 'Kitchen Knife', status: 'DECLARED', model: 'Victorinox Fibrox Chef\'s Knife', price: '$45', formDefinition: 'High-carbon stainless steel, full tang.', coreReasoning: 'Utilitarian perfection. Fibrox handle won\'t delaminate. Sharpenable.', keyDisqualifiers: 'Ceramics (brittle). Carbon steel (rusts).', maintenance: 'DURABLE', lifespan: '20+ years', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'washing-machine', category: 'Washing Machine', status: 'EMPTY', formDefinition: 'Laundry device with mechanical controls.', coreReasoning: 'Electronic boards and sealed bearings force disposal over repair.', keyDisqualifiers: 'Electronic controls. Sealed transmissions.', maintenance: 'DISPOSABLE', lifespan: '5-10 years', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'saucepan', category: 'Saucepan', status: 'DECLARED', model: 'Tramontina Tri-Ply Clad', price: '$70', formDefinition: 'Clad stainless steel with welded handles.', coreReasoning: 'Even heating. No rivets. Indefinite thermal cycling.', keyDisqualifiers: 'Non-stick. Single-ply.', maintenance: 'DURABLE', lifespan: 'Indefinite', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'screwdriver', category: 'Screwdriver', status: 'DECLARED', model: 'Wiha SoftFinish Phillips', price: '$18', formDefinition: 'Hardened steel shaft, molded handle.', coreReasoning: 'Handle molded to shaft. Precision tip reduces cam-out.', keyDisqualifiers: 'Soft tips. Multi-bit wobble.', maintenance: 'DURABLE', lifespan: 'Lifetime', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'dutch-oven', category: 'Dutch Oven', status: 'DECLARED', model: 'Lodge Enameled Cast Iron', price: '$80', formDefinition: 'Enameled cast iron vessel.', coreReasoning: '95% performance of Le Creuset at 20% cost.', keyDisqualifiers: 'Bare iron (reactive). Stainless (poor retention).', maintenance: 'DURABLE', lifespan: 'Indefinite', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'laptop', category: 'Laptop', status: 'EMPTY', formDefinition: 'Portable computer with replaceable battery.', coreReasoning: 'Glued batteries and soldered RAM prevent indefinite use.', keyDisqualifiers: 'Soldered RAM. Glued battery.', maintenance: 'OBSOLETE', lifespan: '5 years', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'coffee-maker', category: 'Coffee Maker', status: 'EMPTY', formDefinition: 'Extraction device without sealed elements.', coreReasoning: 'Drip/Espresso machines fail (scale/electronics).', keyDisqualifiers: 'Internal scale. Electronic failure.', maintenance: 'REPAIRABLE', lifespan: 'Varies', confidence: 2, lastReviewed: '2026-01-16' },
  { id: 'drill', category: 'Drill', status: 'DECLARED', model: 'Makita 6302H Corded', price: '$180', formDefinition: 'Grid-powered rotary tool.', coreReasoning: 'Eliminates battery obsolescence. Metal gearbox.', keyDisqualifiers: 'Cordless (battery death).', maintenance: 'WARRANTY', lifespan: '20+ years', confidence: 2, lastReviewed: '2026-01-16' },
  { id: 'kettle', category: 'Kettle', status: 'DECLARED', model: 'OXO Classic Stovetop', price: '$40', formDefinition: 'Welded stainless boiling vessel.', coreReasoning: 'No heating element. Simple physics.', keyDisqualifiers: 'Electric (element failure). Glass (fragile).', maintenance: 'CONSUMABLE', lifespan: 'Indefinite', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'task-chair', category: 'Task Chair', status: 'SPLIT_REQUIRED', formDefinition: 'Ergonomic work seating.', coreReasoning: 'New market irrational; Used market viable.', keyDisqualifiers: 'Bonded leather. Compressed foam.', maintenance: 'UNKNOWN', lifespan: 'N/A', confidence: 3, lastReviewed: '2026-01-16' },
  { id: 'toaster', category: 'Toaster', status: 'EMPTY', formDefinition: 'Resistance heating with replaceable elements.', coreReasoning: 'Nichrome wire oxidizes. Elements non-replaceable.', keyDisqualifiers: 'Sealed chassis. Electronic timers.', maintenance: 'DISPOSABLE', lifespan: '3-7 years', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'backpack', category: 'Backpack', status: 'DECLARED', model: 'Tom Bihn Synik', price: '$325', formDefinition: 'Ballistic nylon container, YKK zippers.', coreReasoning: 'Materials outlast user. Repairable zippers.', keyDisqualifiers: 'Coated fabric delamination.', maintenance: 'WARRANTY', lifespan: '15-20 years', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'mattress', category: 'Mattress', status: 'EMPTY', formDefinition: 'Sleep surface with replaceable components.', coreReasoning: 'Foams compress permanently. Sealed construction.', keyDisqualifiers: 'Memory foam. Sewn covers.', maintenance: 'CONSUMABLE', lifespan: '7-10 years', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'hand-saw', category: 'Hand Saw', status: 'DECLARED', model: 'Gyokucho Razorsaw', price: '$50', formDefinition: 'Pull saw with replaceable blade.', coreReasoning: 'Acknowledges blade as consumable.', keyDisqualifiers: 'Disposable western saws.', maintenance: 'REPAIRABLE', lifespan: 'Blade 2-5 yrs', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'desk', category: 'Desk', status: 'DECLARED', model: 'Solid Wood Block + Legs', price: '$600', formDefinition: 'Solid timber slab on mechanical legs.', coreReasoning: 'Refinishable. No veneer to peel.', keyDisqualifiers: 'Particleboard.', maintenance: 'DURABLE', lifespan: 'Indefinite', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'boots', category: 'Boots', status: 'DECLARED', model: 'White\'s Semi-Dress', price: '$500', formDefinition: 'Goodyear welted full-grain leather.', coreReasoning: 'Stitched sole allows indefinite rebuilding.', keyDisqualifiers: 'Cemented soles. Synthetic liners.', maintenance: 'REPAIRABLE', lifespan: 'Resoling 5-10 yrs', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'oven-range', category: 'Oven/Range', status: 'EMPTY', formDefinition: 'Cooking appliance with mechanical gas.', coreReasoning: 'Electronic control boards fail.', keyDisqualifiers: 'Electronic controls. Sealed burners.', maintenance: 'DISPOSABLE', lifespan: '10-15 years', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'belt', category: 'Belt', status: 'DECLARED', model: 'Full Grain Leather Belt', price: '$70', formDefinition: 'Single strip full-grain leather.', coreReasoning: 'No stitching to fail. Mechanical buckle.', keyDisqualifiers: 'Bonded leather. Stitched edges.', maintenance: 'REPAIRABLE', lifespan: 'Lifetime', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'freezer', category: 'Freezer', status: 'EMPTY', formDefinition: 'Cold storage with serviceable mechanicals.', coreReasoning: 'Sealed systems make repair irrational.', keyDisqualifiers: 'Sealed compressors.', maintenance: 'DISPOSABLE', lifespan: '10-15 years', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'adjustable-wrench', category: 'Adjustable Wrench', status: 'DECLARED', model: 'Bahco Adjustable', price: '$35', formDefinition: 'Forged steel with precision worm gear.', coreReasoning: 'Tight tolerances reduce rounding.', keyDisqualifiers: 'Stamped steel. Loose jaw play.', maintenance: 'DURABLE', lifespan: 'Lifetime', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 't-shirt', category: 'T-Shirt', status: 'DECLARED', model: 'Velva Sheen 2-Pack', price: '$40', formDefinition: 'Tubular knit cotton.', coreReasoning: 'No side seams to twist. Heavyweight cotton.', keyDisqualifiers: 'Thin fabric. Side seams.', maintenance: 'CONSUMABLE', lifespan: '3-5 years', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'jeans', category: 'Jeans', status: 'DECLARED', model: 'Levi\'s 501 STF', price: '$60', formDefinition: '100% cotton denim, button fly.', coreReasoning: 'No elastane to fail. Button fly repairable.', keyDisqualifiers: 'Stretch denim. Zippers.', maintenance: 'DURABLE', lifespan: '5-10 years', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'jacket', category: 'Jacket/Coat', status: 'DECLARED', model: 'Barbour Beaufort', price: '$400', formDefinition: 'Waxed cotton canvas.', coreReasoning: 'Rewaxable. No membrane to delaminate.', keyDisqualifiers: 'Gore-tex (delaminates).', maintenance: 'REPAIRABLE', lifespan: 'Rewax 1-2 yrs', confidence: 2, lastReviewed: '2026-01-16' },
  { id: 'chisel', category: 'Chisel', status: 'DECLARED', model: 'Narex Richter', price: '$70', formDefinition: 'Through-tang high-carbon steel.', coreReasoning: 'Tang prevents handle separation.', keyDisqualifiers: 'Socket chisels. Plastic handles.', maintenance: 'DURABLE', lifespan: 'Lifetime', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'pliers', category: 'Pliers', status: 'DECLARED', model: 'Channellock 430', price: '$25', formDefinition: 'Drop-forged steel tongue-and-groove.', coreReasoning: 'Simple mechanical joint.', keyDisqualifiers: 'Push-button. Soft steel.', maintenance: 'DURABLE', lifespan: 'Lifetime', confidence: 2, lastReviewed: '2026-01-16' },
  { id: 'tape-measure', category: 'Tape Measure', status: 'DECLARED', model: 'Stanley FatMax', price: '$25', formDefinition: '1.25 in blade width, mylar coating.', coreReasoning: 'Wide blade prevents kinking.', keyDisqualifiers: 'Thin blades. Plastic locks.', maintenance: 'REPAIRABLE', lifespan: '5-10 years', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'tent', category: 'Tent', status: 'DECLARED', model: 'Springbar Highline', price: '$700', formDefinition: '100% cotton canvas, steel frame.', coreReasoning: 'Canvas treats with water to seal.', keyDisqualifiers: 'Nylon (PU coatings).', maintenance: 'REPAIRABLE', lifespan: 'Treat 3-5 yrs', confidence: 2, lastReviewed: '2026-01-16' },
  { id: 'sleeping-bag', category: 'Sleeping Bag', status: 'DECLARED', model: 'Western Mountaineering', price: '$650', formDefinition: '850+ down fill, continuous baffles.', coreReasoning: 'Down outlasts synthetic.', keyDisqualifiers: 'Synthetic fill.', maintenance: 'WARRANTY', lifespan: '15-20 years', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'water-bottle', category: 'Water Bottle', status: 'DECLARED', model: 'Klean Kanteen Single-Wall', price: '$30', formDefinition: '18/8 stainless steel, unlined.', coreReasoning: 'Single wall cannot fail.', keyDisqualifiers: 'Vacuum insulated. Plastic.', maintenance: 'REPAIRABLE', lifespan: 'Indefinite', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'flashlight', category: 'Flashlight', status: 'DECLARED', model: 'Maglite 2D LED', price: '$35', formDefinition: 'Aluminum body, alkaline power.', coreReasoning: 'Commodity batteries. Replaceable switch.', keyDisqualifiers: 'Proprietary lithium.', maintenance: 'WARRANTY', lifespan: '7 years', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'sweater', category: 'Sweater', status: 'DECLARED', model: 'Aran Cable Knit', price: '$100', formDefinition: '100% wool, cable knit.', coreReasoning: 'Structure resists stretching.', keyDisqualifiers: 'Acrylic. Cotton.', maintenance: 'REPAIRABLE', lifespan: '15-25 years', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'cooler', category: 'Cooler', status: 'DECLARED', model: 'RTIC 45-Quart', price: '$200', formDefinition: 'Rotomolded polyethylene.', coreReasoning: 'One-piece tub. Replaceable parts.', keyDisqualifiers: 'Blow-molded plastic.', maintenance: 'REPAIRABLE', lifespan: '20-30 years', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'pocket-knife', category: 'Pocket Knife', status: 'DECLARED', model: 'Opinel No. 8', price: '$18', formDefinition: 'Ring-lock folding knife.', coreReasoning: '5 components. Wear-compensating lock.', keyDisqualifiers: 'Springs. Rivets.', maintenance: 'REPAIRABLE', lifespan: '20-30 years', confidence: 2, lastReviewed: '2026-01-16' },
  { id: 'notebook', category: 'Notebook', status: 'DECLARED', model: 'Mead Composition', price: '$3', formDefinition: 'Sewn binding signatures.', coreReasoning: 'Pages cannot fall out.', keyDisqualifiers: 'Spiral. Glued.', maintenance: 'DURABLE', lifespan: 'Archival', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'pen', category: 'Pen', status: 'DECLARED', model: 'Parker Jotter', price: '$15', formDefinition: 'Stainless steel body.', coreReasoning: 'Metal body lasts indefinitely.', keyDisqualifiers: 'Plastic. Disposable.', maintenance: 'REPAIRABLE', lifespan: 'Lifetime', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'cutting-board', category: 'Cutting Board', status: 'DECLARED', model: 'John Boos Maple', price: '$80', formDefinition: 'Hard maple, edge-grain.', coreReasoning: 'Antimicrobial. Sandable.', keyDisqualifiers: 'Plastic. Glass.', maintenance: 'DURABLE', lifespan: 'Oil 3-6 mos', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'vacuum', category: 'Vacuum Cleaner', status: 'EMPTY', formDefinition: 'Suction device with serviceable motor.', coreReasoning: 'Sealed motors fail. Bagless clogs.', keyDisqualifiers: 'Bagless. Sealed motor.', maintenance: 'EMPTY', lifespan: '5-10 years', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'bicycle', category: 'Bicycle', status: 'DECLARED', model: 'Surly Long Haul Trucker', price: '$1500', formDefinition: 'Chromoly steel frame.', coreReasoning: 'Steel frame weldable. Standard parts.', keyDisqualifiers: 'Carbon fiber. Electronic shifting.', maintenance: 'REPAIRABLE', lifespan: 'Indefinite', confidence: 2, lastReviewed: '2026-01-16' },
  { id: 'dining-chair', category: 'Dining Chair', status: 'DECLARED', model: 'Vermont Woods Windsor', price: '$450', formDefinition: 'Solid hardwood, mechanical joinery.', coreReasoning: 'No glue-only joints.', keyDisqualifiers: 'Upholstery. Particleboard.', maintenance: 'CONSUMABLE', lifespan: '15-20 years', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'printer', category: 'Printer', status: 'EMPTY', formDefinition: 'Printing device with non-DRM consumables.', coreReasoning: 'Inkjet clogs. DRM ink.', keyDisqualifiers: 'DRM. Obsolescence.', maintenance: 'EMPTY', lifespan: '3-12 years', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'socks', category: 'Socks', status: 'DECLARED', model: 'Darn Tough Merino', price: '$25', formDefinition: 'Merino wool blend.', coreReasoning: 'Lifetime warranty.', keyDisqualifiers: 'Cotton. No warranty.', maintenance: 'WARRANTY', lifespan: '2-5 years', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'watch', category: 'Watch', status: 'DECLARED', model: 'Seiko SNK809', price: '$100', formDefinition: 'Mechanical automatic.', coreReasoning: 'No battery. Serviceable.', keyDisqualifiers: 'Smartwatch. Quartz.', maintenance: 'REPAIRABLE', lifespan: '10-15 years', confidence: 2, lastReviewed: '2026-01-16' },
  { id: 'shoes', category: 'Shoes', status: 'DECLARED', model: 'Allen Edmonds Park Ave', price: '$400', formDefinition: 'Goodyear welted leather.', coreReasoning: 'Stitched sole.', keyDisqualifiers: 'Cemented. Foam.', maintenance: 'REPAIRABLE', lifespan: '3-7 years', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'food-storage', category: 'Food Storage', status: 'SPLIT_REQUIRED', formDefinition: 'Inert container.', coreReasoning: 'Glass lasts, lids fail.', keyDisqualifiers: 'Plastic.', maintenance: 'UNKNOWN', lifespan: '3-7 years', confidence: 3, lastReviewed: '2026-01-16' },
  { id: 'level', category: 'Level', status: 'DECLARED', model: 'Stabila Type 196', price: '$100', formDefinition: 'Heavy aluminum profile.', coreReasoning: 'Locked vials.', keyDisqualifiers: 'Plastic. Adjustable.', maintenance: 'WARRANTY', lifespan: 'Lifetime', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'drill-bits', category: 'Drill Bits', status: 'DECLARED', model: 'Viking HSS Jobber', price: '$5', formDefinition: 'High Speed Steel.', coreReasoning: 'Sharpenable.', keyDisqualifiers: 'Carbide tipped.', maintenance: 'REPAIRABLE', lifespan: '5-20 years', confidence: 2, lastReviewed: '2026-01-16' },
  { id: 'extension-cord', category: 'Extension Cord', status: 'DECLARED', model: 'US Wire 12/3', price: '$60', formDefinition: '12-gauge copper.', coreReasoning: 'Prevents voltage drop.', keyDisqualifiers: '16-gauge.', maintenance: 'REPAIRABLE', lifespan: '15-25 years', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'camping-stove', category: 'Camping Stove', status: 'DECLARED', model: 'MSR WhisperLite', price: '$110', formDefinition: 'Liquid fuel, pump.', coreReasoning: 'Field maintainable.', keyDisqualifiers: 'Canister. Piezo.', maintenance: 'REPAIRABLE', lifespan: '2-5 years', confidence: 2, lastReviewed: '2026-01-16' },
  { id: 'mechanical-pencil', category: 'Mechanical Pencil', status: 'DECLARED', model: 'Pentel GraphGear 500', price: '$6', formDefinition: 'Metal grip, 0.7mm.', coreReasoning: 'Simple mechanism.', keyDisqualifiers: 'Plastic clutch.', maintenance: 'REPAIRABLE', lifespan: '5-10 years', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'umbrella', category: 'Umbrella', status: 'DECLARED', model: 'GustBuster Classic', price: '$45', formDefinition: 'Double canopy.', coreReasoning: 'Wind release vents.', keyDisqualifiers: 'Aluminum ribs.', maintenance: 'WARRANTY', lifespan: '5-10 years', confidence: 2, lastReviewed: '2026-01-16' },
  { id: 'ladder', category: 'Ladder', status: 'DECLARED', model: 'Werner Fiberglass', price: '$150', formDefinition: 'Fiberglass rails.', coreReasoning: 'Non-conductive.', keyDisqualifiers: 'Aluminum.', maintenance: 'REPAIRABLE', lifespan: '20-30 years', confidence: 2, lastReviewed: '2026-01-16' },
  { id: 'wheelbarrow', category: 'Wheelbarrow', status: 'DECLARED', model: 'Jackson Steel', price: '$130', formDefinition: 'Steel tray.', coreReasoning: 'Doesn\'t crack.', keyDisqualifiers: 'Plastic tray.', maintenance: 'REPAIRABLE', lifespan: '2-3 years', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'wallet', category: 'Wallet', status: 'DECLARED', model: 'Saddleback Leather', price: '$50', formDefinition: 'Full-grain leather.', coreReasoning: 'No tearing.', keyDisqualifiers: 'Bonded leather.', maintenance: 'WARRANTY', lifespan: '2-5 years', confidence: 2, lastReviewed: '2026-01-16' },
  { id: 'briefcase', category: 'Briefcase', status: 'DECLARED', model: 'Filson Original', price: '$325', formDefinition: 'Rugged Twill.', coreReasoning: 'Heavy canvas.', keyDisqualifiers: 'Nylon.', maintenance: 'REPAIRABLE', lifespan: 'Rewax 2-3 yrs', confidence: 2, lastReviewed: '2026-01-16' },
  { id: 'hat', category: 'Hat', status: 'DECLARED', model: 'Tilley T5', price: '$85', formDefinition: 'Cotton duck.', coreReasoning: 'Guaranteed for life.', keyDisqualifiers: 'Straw. Felt.', maintenance: 'WARRANTY', lifespan: '15-25 years', confidence: 2, lastReviewed: '2026-01-16' },
  { id: 'gloves', category: 'Gloves', status: 'DECLARED', model: 'Dachstein Wool', price: '$70', formDefinition: 'Boiled wool.', coreReasoning: 'Windproof.', keyDisqualifiers: 'Synthetic.', maintenance: 'REPAIRABLE', lifespan: '1-3 years', confidence: 2, lastReviewed: '2026-01-16' },
  { id: 'toothbrush', category: 'Toothbrush', status: 'EMPTY', formDefinition: 'Oral hygiene.', coreReasoning: 'Consumable.', keyDisqualifiers: 'Electric.', maintenance: 'REPAIRABLE', lifespan: '3-4 months', confidence: 2, lastReviewed: '2026-01-16' },
  { id: 'razor', category: 'Razor', status: 'DECLARED', model: 'Merkur 34C', price: '$45', formDefinition: 'Brass safety razor.', coreReasoning: 'Solid brass.', keyDisqualifiers: 'Cartridge.', maintenance: 'REPAIRABLE', lifespan: '10-year', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'hair-dryer', category: 'Hair Dryer', status: 'EMPTY', formDefinition: 'Heated blower.', coreReasoning: 'Elements oxidize.', keyDisqualifiers: 'Sealed.', maintenance: 'EMPTY', lifespan: '2-15 years', confidence: 4, lastReviewed: '2026-01-16' },
  { id: 'desktop-computer', category: 'Desktop Computer', status: 'CANDIDATE', model: 'Custom ATX', price: '$1200', formDefinition: 'ATX architecture.', coreReasoning: 'Repairable.', keyDisqualifiers: 'Proprietary.', maintenance: 'REPAIRABLE', lifespan: '5-10 years', confidence: 2, lastReviewed: '2026-01-16' },
  { id: 'task-chair-new', category: 'Task Chair (New)', status: 'CANDIDATE', formDefinition: 'New chair.', coreReasoning: 'Unproven.', keyDisqualifiers: 'Foam.', maintenance: 'UNKNOWN', lifespan: '15+ years', confidence: 3, lastReviewed: '2026-01-16' },
  { id: 'task-chair-used', category: 'Task Chair (Used)', status: 'CANDIDATE', formDefinition: 'Used chair.', coreReasoning: 'Proven.', keyDisqualifiers: 'None.', maintenance: 'UNKNOWN', lifespan: 'Decades', confidence: 3, lastReviewed: '2026-01-16' },
  { id: 'food-storage-glass', category: 'Food Storage (Glass)', status: 'CANDIDATE', formDefinition: 'Glass.', coreReasoning: 'Lids fail.', keyDisqualifiers: 'Plastic.', maintenance: 'UNKNOWN', lifespan: '10+ years', confidence: 3, lastReviewed: '2026-01-16' },
  { id: 'food-storage-dry', category: 'Food Storage (Dry)', status: 'CANDIDATE', formDefinition: 'Dry goods.', coreReasoning: 'Seal.', keyDisqualifiers: 'Integrated.', maintenance: 'UNKNOWN', lifespan: 'Years', confidence: 3, lastReviewed: '2026-01-16' }
];

// --- UTILITIES ---

const getStatusColor = (status) => {
  switch (status) {
    case 'DECLARED': return 'bg-emerald-900 text-emerald-50';
    case 'EMPTY': return 'bg-stone-400 text-stone-900';
    case 'CANDIDATE': return 'bg-amber-600 text-amber-50';
    case 'DEPRECATED': return 'bg-red-900 text-red-50';
    case 'SPLIT_REQUIRED': return 'bg-stone-600 text-stone-100';
    case 'REJECTED': return 'bg-rose-900 text-rose-50';
    default: return 'bg-stone-200 text-stone-800';
  }
};

const getStatusBadge = (status, size = 'normal') => {
  const baseClasses = `font-bold tracking-widest uppercase inline-block rounded-sm ${size === 'small' ? 'px-1.5 py-0.5 text-[10px]' : 'px-2 py-1 text-xs'}`;
  switch (status) {
    case 'DECLARED': return <span className={`${baseClasses} bg-emerald-100 text-emerald-900 border border-emerald-200`}>Declared</span>;
    case 'EMPTY': return <span className={`${baseClasses} bg-stone-200 text-stone-600 border border-stone-300`}>Empty</span>;
    case 'CANDIDATE': return <span className={`${baseClasses} bg-amber-100 text-amber-800 border border-amber-200`}>Candidate</span>;
    case 'DEPRECATED': return <span className={`${baseClasses} bg-red-100 text-red-800 border border-red-200`}>Deprecated</span>;
    case 'SPLIT_REQUIRED': return <span className={`${baseClasses} bg-stone-100 text-stone-600 border border-stone-300`}>Split Req</span>;
    case 'REJECTED': return <span className={`${baseClasses} bg-rose-100 text-rose-900 border border-rose-200`}>Rejected</span>;
    default: return null;
  }
};

// --- PLATONIC ASSET GENERATOR ---

const PlatonicAsset = ({ id, className }) => {
  const strokeColor = "#44403C"; 
  const fillColor = "#F5F5F4"; 
  const strokeWidth = "2";

  const renderAsset = () => {
    switch (id) {
      case 'frying-pan':
        return (
          <svg viewBox="0 0 100 100" className="w-full h-full p-6">
            <circle cx="50" cy="50" r="30" fill={fillColor} stroke={strokeColor} strokeWidth={strokeWidth} />
            <path d="M80 50 L110 50" stroke={strokeColor} strokeWidth="6" strokeLinecap="round" />
            <path d="M75 50 L80 50" stroke={fillColor} strokeWidth="6" /> 
          </svg>
        );
      case 'hammer':
        return (
          <svg viewBox="0 0 100 100" className="w-full h-full p-6">
            <path d="M45 20 L55 20 L55 90 L45 90 Z" fill={fillColor} stroke={strokeColor} strokeWidth={strokeWidth} />
            <path d="M30 20 Q50 10 70 20 L70 30 L30 30 Z" fill={strokeColor} stroke="none" />
            <rect x="45" y="60" width="10" height="30" fill={strokeColor} opacity="0.1" />
          </svg>
        );
      case 'kitchen-knife':
        return (
          <svg viewBox="0 0 100 100" className="w-full h-full p-6" transform="rotate(-45 50 50)">
            <path d="M30 45 L80 45 L80 55 L30 55 Q25 50 30 45 Z" fill={strokeColor} />
            <path d="M80 45 L10 60 L80 55 Z" fill={fillColor} stroke={strokeColor} strokeWidth={strokeWidth} />
            <circle cx="35" cy="50" r="1.5" fill="#fff" />
            <circle cx="45" cy="50" r="1.5" fill="#fff" />
            <circle cx="55" cy="50" r="1.5" fill="#fff" />
          </svg>
        );
      case 'saucepan':
        return (
          <svg viewBox="0 0 100 100" className="w-full h-full p-6">
            <rect x="30" y="40" width="40" height="30" rx="2" fill={fillColor} stroke={strokeColor} strokeWidth={strokeWidth} />
            <path d="M30 45 L10 45" stroke={strokeColor} strokeWidth="4" strokeLinecap="round" />
            <ellipse cx="50" cy="40" rx="20" ry="5" fill="#fff" stroke={strokeColor} strokeWidth={strokeWidth} />
          </svg>
        );
      case 'screwdriver':
        return (
          <svg viewBox="0 0 100 100" className="w-full h-full p-6" transform="rotate(45 50 50)">
             <path d="M30 45 L50 45 L50 55 L30 55 Q25 50 30 45 Z" fill={strokeColor} />
             <rect x="50" y="48" width="40" height="4" fill={fillColor} stroke={strokeColor} strokeWidth="1" />
          </svg>
        );
      case 'dutch-oven':
        return (
          <svg viewBox="0 0 100 100" className="w-full h-full p-6">
             <rect x="25" y="40" width="50" height="35" rx="4" fill={fillColor} stroke={strokeColor} strokeWidth={strokeWidth} />
             <path d="M20 45 L25 45 M75 45 L80 45" stroke={strokeColor} strokeWidth="3" strokeLinecap="round" />
             <path d="M25 40 Q50 30 75 40" fill="none" stroke={strokeColor} strokeWidth={strokeWidth} />
             <rect x="45" y="33" width="10" height="4" fill={strokeColor} />
          </svg>
        );
      case 'drill':
        return (
           <svg viewBox="0 0 100 100" className="w-full h-full p-6">
             <path d="M30 30 L70 30 L70 50 L50 50 L50 80 L35 80 L35 50 L30 50 Z" fill={fillColor} stroke={strokeColor} strokeWidth={strokeWidth} />
             <rect x="70" y="35" width="10" height="10" fill={strokeColor} />
             <rect x="80" y="38" width="10" height="4" fill="#ccc" />
           </svg>
        );
      case 'kettle':
        return (
          <svg viewBox="0 0 100 100" className="w-full h-full p-6">
            <circle cx="50" cy="60" r="25" fill={fillColor} stroke={strokeColor} strokeWidth={strokeWidth} />
            <path d="M50 35 L50 25 M30 35 Q50 10 70 35" fill="none" stroke={strokeColor} strokeWidth="3" />
            <path d="M75 50 L90 40" stroke={strokeColor} strokeWidth="4" />
          </svg>
        );
      case 'backpack':
        return (
          <svg viewBox="0 0 100 100" className="w-full h-full p-6">
            <rect x="30" y="20" width="40" height="60" rx="8" fill={fillColor} stroke={strokeColor} strokeWidth={strokeWidth} />
            <path d="M30 40 L70 40" stroke={strokeColor} strokeWidth="1" strokeDasharray="4 2" />
            <rect x="35" y="50" width="30" height="20" rx="2" fill="none" stroke={strokeColor} strokeWidth="1" />
            <path d="M40 20 Q50 10 60 20" fill="none" stroke={strokeColor} strokeWidth="3" />
          </svg>
        );
      case 'hand-saw':
        return (
           <svg viewBox="0 0 100 100" className="w-full h-full p-6" transform="rotate(-15 50 50)">
             <path d="M20 40 L30 40 L30 60 L20 60 Q15 50 20 40 Z" fill={strokeColor} />
             <path d="M30 42 L90 35 L90 65 L30 58 Z" fill={fillColor} stroke={strokeColor} strokeWidth={strokeWidth} />
           </svg>
        );
      case 'desk':
        return (
           <svg viewBox="0 0 100 100" className="w-full h-full p-6">
             <rect x="10" y="35" width="80" height="6" fill={strokeColor} />
             <rect x="20" y="41" width="4" height="40" fill={strokeColor} />
             <rect x="76" y="41" width="4" height="40" fill={strokeColor} />
           </svg>
        );
      case 'boots':
        return (
           <svg viewBox="0 0 100 100" className="w-full h-full p-6">
             <path d="M30 80 L70 80 L75 60 L60 30 L40 30 L30 60 Z" fill={fillColor} stroke={strokeColor} strokeWidth={strokeWidth} strokeLinejoin="round" />
             <line x1="30" y1="75" x2="70" y2="75" stroke={strokeColor} strokeWidth="2" />
             <rect x="30" y="78" width="40" height="4" fill={strokeColor} />
           </svg>
        );
      case 'belt':
        return (
          <svg viewBox="0 0 100 100" className="w-full h-full p-6">
             <circle cx="50" cy="50" r="30" fill="none" stroke={strokeColor} strokeWidth="6" />
             <rect x="15" y="40" width="10" height="20" fill={strokeColor} />
             <line x1="25" y1="50" x2="35" y2="50" stroke={strokeColor} strokeWidth="2" />
          </svg>
        );
      case 'flashlight':
        return (
           <svg viewBox="0 0 100 100" className="w-full h-full p-6" transform="rotate(-45 50 50)">
             <rect x="30" y="42" width="40" height="16" fill={fillColor} stroke={strokeColor} strokeWidth={strokeWidth} />
             <rect x="70" y="35" width="15" height="30" fill={strokeColor} />
             <path d="M85 35 L95 50 L85 65 Z" fill="#fff" opacity="0.5" />
           </svg>
        );
      case 'pocket-knife':
        return (
           <svg viewBox="0 0 100 100" className="w-full h-full p-6" transform="rotate(45 50 50)">
             <path d="M20 45 L60 45 L60 55 L20 55 Q15 50 20 45 Z" fill={strokeColor} />
             <path d="M60 48 L90 50 L60 52 Z" fill={fillColor} stroke={strokeColor} strokeWidth={1} />
           </svg>
        );
       case 'notebook':
        return (
           <svg viewBox="0 0 100 100" className="w-full h-full p-6">
             <rect x="30" y="20" width="40" height="60" fill={strokeColor} />
             <rect x="32" y="20" width="3" height="60" fill="#222" />
             <rect x="40" y="30" width="20" height="10" fill="#fff" opacity="0.8" />
           </svg>
        );
      case 'pen':
        return (
           <svg viewBox="0 0 100 100" className="w-full h-full p-6" transform="rotate(-45 50 50)">
             <rect x="20" y="48" width="60" height="4" fill={fillColor} stroke={strokeColor} strokeWidth={1} />
             <path d="M80 48 L90 50 L80 52 Z" fill={strokeColor} />
             <rect x="15" y="48" width="5" height="4" fill={strokeColor} />
           </svg>
        );
      case 'cutting-board':
        return (
           <svg viewBox="0 0 100 100" className="w-full h-full p-6">
             <rect x="20" y="30" width="60" height="40" fill={fillColor} stroke={strokeColor} strokeWidth={strokeWidth} />
             <circle cx="70" cy="40" r="3" fill="none" stroke={strokeColor} strokeWidth={1} />
           </svg>
        );
      case 'ladder':
        return (
           <svg viewBox="0 0 100 100" className="w-full h-full p-6">
             <line x1="30" y1="10" x2="30" y2="90" stroke={strokeColor} strokeWidth={3} />
             <line x1="70" y1="10" x2="70" y2="90" stroke={strokeColor} strokeWidth={3} />
             <line x1="30" y1="20" x2="70" y2="20" stroke={strokeColor} strokeWidth={2} />
             <line x1="30" y1="40" x2="70" y2="40" stroke={strokeColor} strokeWidth={2} />
             <line x1="30" y1="60" x2="70" y2="60" stroke={strokeColor} strokeWidth={2} />
             <line x1="30" y1="80" x2="70" y2="80" stroke={strokeColor} strokeWidth={2} />
           </svg>
        );
      case 'wheelbarrow':
        return (
           <svg viewBox="0 0 100 100" className="w-full h-full p-6">
             <path d="M20 40 L70 40 L80 60 L30 60 Z" fill={fillColor} stroke={strokeColor} strokeWidth={strokeWidth} />
             <circle cx="60" cy="75" r="10" fill="none" stroke={strokeColor} strokeWidth={2} />
             <line x1="10" y1="50" x2="30" y2="60" stroke={strokeColor} strokeWidth={2} />
             <line x1="10" y1="50" x2="10" y2="60" stroke={strokeColor} strokeWidth={2} />
           </svg>
        );
      case 'bicycle':
        return (
           <svg viewBox="0 0 100 100" className="w-full h-full p-6">
             <circle cx="25" cy="70" r="15" fill="none" stroke={strokeColor} strokeWidth={2} />
             <circle cx="75" cy="70" r="15" fill="none" stroke={strokeColor} strokeWidth={2} />
             <path d="M25 70 L45 35 L75 70 L25 70" fill="none" stroke={strokeColor} strokeWidth={2} />
             <path d="M45 35 L65 35 L75 70" fill="none" stroke={strokeColor} strokeWidth={2} />
             <line x1="65" y1="35" x2="65" y2="25" stroke={strokeColor} strokeWidth={2} />
             <path d="M60 25 L70 25" stroke={strokeColor} strokeWidth={2} />
           </svg>
        );
      default:
        // Generic Platonic Form (Abstract)
        return (
          <svg viewBox="0 0 100 100" className="w-full h-full p-6 opacity-50">
             <circle cx="50" cy="50" r="20" fill="none" stroke={strokeColor} strokeWidth={1} />
             <rect x="30" y="30" width="40" height="40" fill="none" stroke={strokeColor} strokeWidth={1} transform="rotate(45 50 50)" />
             <line x1="10" y1="50" x2="90" y2="50" stroke={strokeColor} strokeWidth={0.5} strokeDasharray="4 4" />
          </svg>
        );
    }
  };

  return (
    <div className={`flex items-center justify-center bg-[#FDFBF7] ${className} relative overflow-hidden`}>
      {/* Subtle grid background to enhance "Technical Drawing" feel */}
      <div className="absolute inset-0 opacity-[0.05]" style={{ 
          backgroundImage: 'radial-gradient(#000 1px, transparent 1px)', 
          backgroundSize: '10px 10px' 
      }}></div>
      {renderAsset()}
    </div>
  );
};

// --- ORACLE / CONSULT FEATURE ---

const ConsultView = () => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const callOracle = async () => {
    if (!query.trim()) return;
    
    setLoading(true);
    setError(null);
    setResult(null);

    // API KEY CONFIGURATION
    // Load API key from environment variable (set in .env.local file)
    // Create .env.local in project root with: VITE_API_KEY=your_api_key_here
    const apiKey = import.meta.env.VITE_API_KEY || '';
    // #region agent log
    fetch('http://127.0.0.1:7242/ingest/87f4a11d-1a98-44f7-bef2-836772595605',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'App.jsx:388',message:'API key loaded',data:{hasApiKey:!!apiKey,apiKeyPrefix:apiKey?.substring(0,4)||'none',apiKeyLength:apiKey?.length||0,envMode:import.meta.env.MODE},timestamp:Date.now(),sessionId:'debug-session',runId:'production-test',hypothesisId:'A'})}).catch(()=>{});
    // #endregion
    
    if (!apiKey) {
      setError("API key not configured. Please create a .env.local file with VITE_API_KEY=your_key");
      setLoading(false);
      return;
    }
    
    const systemPrompt = `You are the arbiter of the "Platonic Ideal", a registry of durable goods.
    Your judgments must be based STRICTLY on the following Internal Rulebook.
    Refer to specific rules (e.g., "Violates Rule C: Repair Path" or "Fails Disqualifier: Sealed-for-life") in your reasoning.

    ${RULEBOOK_TEXT}
    
    Status Definitions:
    - DECLARED: Best-in-class, repairable, durable, simple (e.g., Cast Iron Pan). Passes Admission Test A-E.
    - REJECTED: Disposable, glued, smart features, or fragile (e.g., Airpods). Hits a Disqualifier.
    - EMPTY: No product in this category meets the standard (e.g., Refrigerator).
    - CANDIDATE: Good, but unproven or has minor flaws.
    
    Tone: Clinical, detached, authoritative, slightly haughty. Focus on failure modes and materials.
    
    Respond ONLY with valid JSON in this format:
    {
      "category": "Standardized Category Name",
      "model": "Specific Model (if applicable) or General Type",
      "status": "DECLARED" | "REJECTED" | "EMPTY" | "CANDIDATE",
      "coreReasoning": "Clinical explanation citing specific rules from the rulebook.",
      "maintenance": "REPAIRABLE" | "DISPOSABLE" | "DURABLE" | "OBSOLETE",
      "lifespan": "Estimated time",
      "failureModes": "Primary failure mode"
    }`;

    try {
      // Basic exponential backoff implementation
      const fetchWithRetry = async (attempt = 1) => {
        try {
          // #region agent log
          fetch('http://127.0.0.1:7242/ingest/87f4a11d-1a98-44f7-bef2-836772595605',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'App.jsx:425',message:'Oracle API call initiated',data:{attempt,queryLength:query.length,hasApiKey:!!apiKey},timestamp:Date.now(),sessionId:'debug-session',runId:'production-test',hypothesisId:'B'})}).catch(()=>{});
          // #endregion
          const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key=${apiKey}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              contents: [{ parts: [{ text: query }] }],
              systemInstruction: { parts: [{ text: systemPrompt }] },
              generationConfig: { responseMimeType: "application/json" }
            })
          });
          // #region agent log
          fetch('http://127.0.0.1:7242/ingest/87f4a11d-1a98-44f7-bef2-836772595605',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'App.jsx:433',message:'Oracle API response received',data:{status:response.status,statusText:response.statusText,ok:response.ok,attempt},timestamp:Date.now(),sessionId:'debug-session',runId:'production-test',hypothesisId:'C'})}).catch(()=>{});
          // #endregion

          if (!response.ok) {
            let errorDetails = {
              status: response.status,
              statusText: response.statusText,
              message: null,
              code: null,
              details: null
            };
            
            try {
              const errorText = await response.text();
              // Try to parse as JSON (Google API returns structured error objects)
              try {
                const errorJson = JSON.parse(errorText);
                if (errorJson.error) {
                  errorDetails.message = errorJson.error.message || null;
                  errorDetails.code = errorJson.error.code || null;
                  errorDetails.details = errorJson.error.details || null;
                } else {
                  errorDetails.message = errorText.substring(0, 200);
                }
              } catch (parseErr) {
                // Not JSON, use text as is
                errorDetails.message = errorText.substring(0, 200);
              }
              
              // #region agent log
              fetch('http://127.0.0.1:7242/ingest/87f4a11d-1a98-44f7-bef2-836772595605',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'App.jsx:448',message:'Oracle API error response',data:errorDetails,timestamp:Date.now(),sessionId:'debug-session',runId:'production-test',hypothesisId:'D'})}).catch(()=>{});
              // #endregion
              
              // Create error with full details
              const apiError = new Error(`API Error (${errorDetails.status})`);
              apiError.status = errorDetails.status;
              apiError.statusText = errorDetails.statusText;
              apiError.apiMessage = errorDetails.message;
              apiError.apiCode = errorDetails.code;
              throw apiError;
            } catch (textErr) {
              // If reading response text fails, throw with status info
              const apiError = new Error(`API Error (${response.status})`);
              apiError.status = response.status;
              apiError.statusText = response.statusText;
              throw apiError;
            }
          }
          const jsonData = await response.json();
          // #region agent log
          fetch('http://127.0.0.1:7242/ingest/87f4a11d-1a98-44f7-bef2-836772595605',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'App.jsx:445',message:'Oracle API success',data:{hasCandidates:!!jsonData.candidates,hasText:!!jsonData.candidates?.[0]?.content?.parts?.[0]?.text,textLength:jsonData.candidates?.[0]?.content?.parts?.[0]?.text?.length||0},timestamp:Date.now(),sessionId:'debug-session',runId:'production-test',hypothesisId:'E'})}).catch(()=>{});
          // #endregion
          return jsonData;
        } catch (e) {
          if (attempt < 3) {
            await new Promise(r => setTimeout(r, Math.pow(2, attempt) * 1000));
            return fetchWithRetry(attempt + 1);
          }
          throw e;
        }
      };

      const data = await fetchWithRetry();
      const text = data.candidates?.[0]?.content?.parts?.[0]?.text;
      // #region agent log
      fetch('http://127.0.0.1:7242/ingest/87f4a11d-1a98-44f7-bef2-836772595605',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'App.jsx:456',message:'Oracle result processing',data:{hasText:!!text,textLength:text?.length||0},timestamp:Date.now(),sessionId:'debug-session',runId:'production-test',hypothesisId:'F'})}).catch(()=>{});
      // #endregion
      
      if (text) {
        // #region agent log
        fetch('http://127.0.0.1:7242/ingest/87f4a11d-1a98-44f7-bef2-836772595605',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'App.jsx:471',message:'Attempting JSON parse',data:{textPreview:text.substring(0,100),textLength:text.length},timestamp:Date.now(),sessionId:'debug-session',runId:'production-test',hypothesisId:'G1'})}).catch(()=>{});
        // #endregion
        let parsedResult;
        try {
          parsedResult = JSON.parse(text);
        } catch (parseErr) {
          // #region agent log
          fetch('http://127.0.0.1:7242/ingest/87f4a11d-1a98-44f7-bef2-836772595605',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'App.jsx:476',message:'JSON parse error',data:{errorMessage:parseErr.message,textPreview:text.substring(0,200)},timestamp:Date.now(),sessionId:'debug-session',runId:'production-test',hypothesisId:'G2'})}).catch(()=>{});
          // #endregion
          throw new Error(`Failed to parse JSON response: ${parseErr.message}`);
        }
        // #region agent log
        fetch('http://127.0.0.1:7242/ingest/87f4a11d-1a98-44f7-bef2-836772595605',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'App.jsx:481',message:'Oracle result parsed successfully',data:{status:parsedResult.status,category:parsedResult.category,hasReasoning:!!parsedResult.coreReasoning},timestamp:Date.now(),sessionId:'debug-session',runId:'production-test',hypothesisId:'G3'})}).catch(()=>{});
        // #endregion
        setResult(parsedResult);
      } else {
        throw new Error("No verdict returned");
      }
    } catch (err) {
      // Parse error to create user-friendly message
      let userMessage = 'The Oracle is currently silent';
      
      if (err.status) {
        // API error with HTTP status
        const status = err.status;
        const apiMessage = err.apiMessage || '';
        const apiCode = err.apiCode || '';
        
        switch (status) {
          case 401:
            userMessage = `API Key Error (401): Invalid or missing API key. ${apiMessage || 'Please check your API key configuration in .env.local'}`;
            break;
          case 403:
            userMessage = `Access Forbidden (403): ${apiMessage || 'API key may be restricted or service is disabled. Check API key permissions.'}`;
            break;
          case 429:
            userMessage = `Rate Limit Exceeded (429): ${apiMessage || 'Too many requests. Please try again later.'}`;
            break;
          case 400:
            userMessage = `Bad Request (400): ${apiMessage || 'Invalid request format. Please try a different query.'}`;
            break;
          case 404:
            userMessage = `Service Not Found (404): ${apiMessage || 'API endpoint not found. The model may not be available.'}`;
            break;
          case 500:
          case 502:
          case 503:
            userMessage = `Service Error (${status}): ${apiMessage || 'The API service is temporarily unavailable. Please try again later.'}`;
            break;
          default:
            userMessage = `API Error (${status}): ${apiMessage || err.message || 'An unexpected error occurred'}`;
        }
      } else {
        // Network or other error
        userMessage = `The Oracle is currently silent: ${err.message || 'Connection failed. Check your internet connection or try again.'}`;
      }
      
      // #region agent log
      fetch('http://127.0.0.1:7242/ingest/87f4a11d-1a98-44f7-bef2-836772595605',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'App.jsx:525',message:'Oracle error caught',data:{errorMessage:err.message,errorName:err.name,errorStatus:err.status,errorStatusText:err.statusText,apiMessage:err.apiMessage,apiCode:err.apiCode,userMessage,errorStack:err.stack?.substring(0,300)},timestamp:Date.now(),sessionId:'debug-session',runId:'production-test',hypothesisId:'H'})}).catch(()=>{});
      // #endregion
      console.error('Oracle Error:', err);
      setError(userMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto px-4 py-20 min-h-screen bg-[#FDFBF7] animate-in fade-in duration-500">
      <div className="text-center mb-12">
        <div className="w-16 h-16 bg-stone-900 rounded-full flex items-center justify-center mx-auto mb-6">
          <Sparkles className="text-stone-50" size={32} />
        </div>
        <h1 className="font-serif text-4xl text-stone-900 mb-4">Consult the Oracle</h1>
        <p className="text-stone-500 font-sans max-w-md mx-auto">
          Submit an object for judgment. The Oracle evaluates based on structure, material, and time.
        </p>
      </div>

      <div className="relative mb-12">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && callOracle()}
          placeholder="e.g. Nespresso Machine, Herman Miller Aeron, Plastic Spatula..."
          className="w-full bg-white border border-stone-300 p-6 pr-32 text-lg font-serif text-stone-900 placeholder:text-stone-300 focus:outline-none focus:border-stone-500 shadow-sm"
        />
        <button
          onClick={callOracle}
          disabled={loading || !query}
          className="absolute right-2 top-2 bottom-2 bg-stone-900 text-stone-50 px-6 font-bold uppercase tracking-widest text-xs hover:bg-stone-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
        >
          {loading ? <Loader2 className="animate-spin" size={16} /> : 'Judge'} 
          {!loading && <Sparkles size={14} />}
        </button>
      </div>

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 text-red-800 text-sm text-center mb-8">
          {error}
        </div>
      )}

      {result && (
        <div className="animate-in slide-in-from-bottom-4 duration-700">
          <div className="border border-stone-200 bg-white shadow-lg overflow-hidden relative">
            {/* Status Header */}
            <div className={`p-4 border-b border-stone-100 flex justify-between items-center ${
              result.status === 'DECLARED' ? 'bg-emerald-50' : 
              result.status === 'REJECTED' ? 'bg-rose-50' :
              result.status === 'EMPTY' ? 'bg-stone-100' : 'bg-amber-50'
            }`}>
              <span className="font-serif font-bold text-stone-900 text-lg">{result.category}</span>
              {getStatusBadge(result.status)}
            </div>

            <div className="p-8">
              {/* Verdict Icon */}
              <div className="flex justify-center mb-8">
                {result.status === 'DECLARED' && <CheckCircle2 size={64} className="text-emerald-900 opacity-80" />}
                {result.status === 'REJECTED' && <XCircle size={64} className="text-rose-900 opacity-80" />}
                {result.status === 'EMPTY' && <Ban size={64} className="text-stone-400 opacity-80" />}
                {result.status === 'CANDIDATE' && <Clock size={64} className="text-amber-600 opacity-80" />}
              </div>

              {/* Core Content */}
              <h3 className="font-sans font-bold text-xs uppercase tracking-widest text-stone-400 mb-2 text-center">
                Oracle Verdict
              </h3>
              <p className="font-serif text-xl md:text-2xl text-center text-stone-900 mb-8 leading-relaxed">
                "{result.coreReasoning}"
              </p>

              {/* Data Grid */}
              <div className="grid grid-cols-2 gap-4 border-t border-stone-100 pt-6">
                <div>
                  <h4 className="text-[10px] font-bold uppercase tracking-widest text-stone-400 mb-1">Lifespan</h4>
                  <p className="text-stone-900 font-mono text-sm">{result.lifespan}</p>
                </div>
                <div>
                  <h4 className="text-[10px] font-bold uppercase tracking-widest text-stone-400 mb-1">Maintenance</h4>
                  <p className="text-stone-900 font-mono text-sm">{result.maintenance}</p>
                </div>
                <div className="col-span-2">
                  <h4 className="text-[10px] font-bold uppercase tracking-widest text-stone-400 mb-1">Fatal Flaw / Failure Mode</h4>
                  <p className="text-stone-900 font-mono text-sm text-red-900 bg-red-50 p-2 inline-block">
                    {result.failureModes}
                  </p>
                </div>
              </div>
            </div>
            
            {/* Timestamp */}
            <div className="bg-stone-50 p-3 text-center border-t border-stone-200">
              <p className="text-[10px] text-stone-400 uppercase tracking-widest">
                Generated by Gemini • {new Date().toLocaleDateString()}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

const ChallengeWidget = ({ item }) => {
  const [challenger, setChallenger] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const callChallenge = async () => {
    if (!challenger.trim()) return;
    setLoading(true);
    setResult(null);

    // API KEY CONFIGURATION
    // Load API key from environment variable (set in .env.local file)
    const apiKey = import.meta.env.VITE_API_KEY || '';
    
    if (!apiKey) {
      setResult("API key not configured. Please create a .env.local file with VITE_API_KEY=your_key");
      setLoading(false);
      return;
    }
    
    const systemPrompt = `You are the defender of the Platonic Ideal.
    Declared Item: ${item.model || 'None declared'} (${item.category})
    Challenger: ${challenger}
    Rulebook: ${RULEBOOK_TEXT}

    Compare them. Defend the Declared Item using the rulebook (durability, repairability). 
    If the Challenger is truly superior (rare), admit it as a 'Candidate'. 
    If the Challenger is flawed (disposable, complex, fragile), eviscerate it politely but clinically.
    Keep it under 100 words.`;

    try {
        const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key=${apiKey}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              contents: [{ parts: [{ text: "Evaluate this challenger." }] }],
              systemInstruction: { parts: [{ text: systemPrompt }] }
            })
        });
        const data = await response.json();
        setResult(data.candidates?.[0]?.content?.parts?.[0]?.text || "The Oracle remains silent.");
    } catch (e) {
        setResult("Connection to the Oracle failed. Please check your API key configuration in .env.local");
    } finally {
        setLoading(false);
    }
  };

  return (
    <div className="mt-12 border-t-2 border-stone-200 pt-8">
      <h3 className="font-serif text-2xl text-stone-900 mb-4 flex items-center gap-2">
        <Swords size={24} /> Challenge the Verdict
      </h3>
      <p className="text-stone-500 text-sm mb-6 max-w-xl">
        Do you believe another product is superior? Submit a challenger. The Oracle will compare it against the {item.category} standards.
      </p>
      
      <div className="flex gap-2 mb-6">
        <input 
          type="text" 
          value={challenger}
          onChange={(e) => setChallenger(e.target.value)}
          placeholder={`e.g. My ${item.category}...`}
          className="flex-1 bg-stone-50 border border-stone-300 p-3 font-serif focus:outline-none focus:border-stone-500"
        />
        <button 
          onClick={callChallenge}
          disabled={loading || !challenger}
          className="bg-stone-900 text-stone-50 px-6 font-bold uppercase tracking-widest text-xs hover:bg-stone-700 transition-colors disabled:opacity-50"
        >
          {loading ? <Loader2 className="animate-spin" /> : 'Compare'}
        </button>
      </div>

      {result && (
        <div className="bg-stone-100 p-6 border-l-4 border-stone-400 animate-in fade-in slide-in-from-top-2">
          <h4 className="text-xs font-bold uppercase tracking-widest text-stone-500 mb-2">Oracle Comparison</h4>
          <p className="font-serif text-lg text-stone-800 leading-relaxed">{result}</p>
        </div>
      )}
    </div>
  );
};

// --- COMPONENTS ---

const Navigation = ({ setView, currentView }) => (
  <nav className="w-full border-b border-stone-300 bg-[#FDFBF7] sticky top-0 z-50 shadow-sm">
    <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
      <div 
        className="font-serif text-xl md:text-2xl font-bold tracking-tight cursor-pointer text-stone-900 flex items-center gap-2"
        onClick={() => setView('home')}
      >
        <Scale size={24} className="text-stone-800" />
        PLATONIC IDEAL
      </div>
      <div className="flex gap-6 text-sm font-medium uppercase tracking-wider text-stone-500">
        <button 
          onClick={() => setView('index')}
          className={`hover:text-stone-900 transition-colors ${currentView === 'index' ? 'text-stone-900 underline underline-offset-4' : ''}`}
        >
          Index
        </button>
        <button 
          onClick={() => setView('consult')}
          className={`hover:text-stone-900 transition-colors flex items-center gap-1 ${currentView === 'consult' ? 'text-stone-900 underline underline-offset-4' : ''}`}
        >
          <Sparkles size={14} className="mb-0.5" />
          Oracle
        </button>
        <button 
          onClick={() => setView('about')}
          className={`hover:text-stone-900 transition-colors ${currentView === 'about' ? 'text-stone-900 underline underline-offset-4' : ''}`}
        >
          Method
        </button>
      </div>
    </div>
  </nav>
);

const HomeView = ({ setView, setSelectedCategory }) => {
  const stats = {
    declared: CATEGORY_DATA.filter(c => c.status === 'DECLARED').length,
    empty: CATEGORY_DATA.filter(c => c.status === 'EMPTY').length,
    candidate: CATEGORY_DATA.filter(c => c.status === 'CANDIDATE').length,
    deprecated: CATEGORY_DATA.filter(c => c.status === 'DEPRECATED').length,
  };

  return (
    <div className="animate-in fade-in duration-500">
      {/* Hero */}
      <div className="py-20 md:py-32 px-4 border-b border-stone-300 bg-[#FDFBF7]">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="font-serif text-4xl md:text-6xl text-stone-900 leading-tight mb-6">
            An index that names the one product in each category built to last.
          </h1>
          <p className="font-sans text-lg md:text-xl text-stone-500 max-w-2xl mx-auto leading-relaxed">
            One ideal. No alternatives. No rankings. <br/>
            <span className="text-stone-400 text-base mt-2 block">Or the category is left explicitly empty.</span>
          </p>
          <div className="mt-8">
             <button 
                onClick={() => setView('consult')}
                className="px-8 py-3 bg-stone-900 text-stone-50 font-bold uppercase tracking-widest text-xs hover:bg-stone-700 transition-all shadow-lg flex items-center gap-2 mx-auto"
             >
                <Sparkles size={14} /> Consult the Oracle
             </button>
          </div>
        </div>
      </div>

      {/* Stats Bar */}
      <div className="border-b border-stone-300 bg-stone-50">
        <div className="max-w-6xl mx-auto px-4 py-4 flex flex-wrap justify-center gap-8 md:gap-16 text-xs uppercase tracking-widest font-semibold text-stone-500">
          <div className="flex items-center gap-2"><span className="w-2 h-2 rounded-full bg-emerald-800"></span> {stats.declared} Declared</div>
          <div className="flex items-center gap-2"><span className="w-2 h-2 rounded-full bg-stone-400"></span> {stats.empty} Empty</div>
          <div className="flex items-center gap-2"><span className="w-2 h-2 rounded-full bg-amber-600"></span> {stats.candidate} Candidates</div>
          <div className="flex items-center gap-2"><span className="w-2 h-2 rounded-full bg-red-800"></span> {stats.deprecated} Deprecated</div>
        </div>
      </div>

      {/* Grid */}
      <div className="max-w-6xl mx-auto px-4 py-16 bg-[#FDFBF7]">
        <h2 className="font-serif text-2xl text-stone-900 mb-8 border-b border-stone-200 pb-4">Recent Verdicts</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {CATEGORY_DATA.map((item) => (
            <div 
              key={item.id}
              onClick={() => { setSelectedCategory(item); setView('category'); }}
              className="group border border-stone-200 bg-white hover:border-stone-400 transition-all duration-300 cursor-pointer flex flex-col h-72 shadow-sm hover:shadow-md"
            >
              <div className="flex-1 relative overflow-hidden flex items-center justify-center bg-stone-50/50">
                {item.status === 'DECLARED' ? (
                   <PlatonicAsset 
                      id={item.id} 
                      className="w-full h-full p-4 mix-blend-multiply opacity-90 group-hover:scale-105 transition-transform duration-500"
                   />
                ) : (
                  <div className="w-full h-full flex items-center justify-center">
                    {item.status === 'EMPTY' && (
                      <div className="w-24 h-24 border-2 border-stone-200 border-dashed rounded-full flex items-center justify-center">
                        <span className="text-stone-300 font-serif italic text-sm">Void</span>
                      </div>
                    )}
                    {item.status === 'DEPRECATED' && (
                      <div className="w-24 h-24 bg-red-50 rounded-full flex items-center justify-center grayscale opacity-60">
                        <History size={40} className="text-red-900 opacity-50" />
                      </div>
                    )}
                    {item.status === 'CANDIDATE' && (
                      <div className="w-24 h-24 bg-amber-50 rounded-full flex items-center justify-center">
                        <Clock size={40} className="text-amber-600 opacity-60" />
                      </div>
                    )}
                    {item.status === 'SPLIT_REQUIRED' && (
                      <div className="w-24 h-24 bg-stone-100 rounded-full flex items-center justify-center">
                        <ArrowRight size={40} className="text-stone-400 opacity-60" />
                      </div>
                    )}
                  </div>
                )}
                
                <div className="absolute top-4 right-4 z-10">
                  {getStatusBadge(item.status, 'small')}
                </div>
              </div>
              <div className="p-5 border-t border-stone-100 bg-white flex flex-col gap-2">
                <h3 className="font-serif text-lg text-stone-900 leading-tight truncate">{item.category}</h3>
                <p className="text-sm text-stone-500 line-clamp-2">
                  {item.status === 'EMPTY' ? 'No qualified product.' : item.model || item.coreReasoning}
                </p>
                <div className="mt-auto pt-2 flex items-center justify-between text-xs text-stone-400 font-mono">
                  <span>{item.lastReviewed}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

const IndexView = ({ setView, setSelectedCategory }) => {
  const [filter, setFilter] = useState('ALL');

  const filteredData = filter === 'ALL' 
    ? CATEGORY_DATA 
    : CATEGORY_DATA.filter(c => c.status === filter);

  return (
    <div className="max-w-6xl mx-auto px-4 py-12 min-h-screen animate-in fade-in slide-in-from-bottom-4 duration-500 bg-[#FDFBF7]">
      <div className="flex flex-col md:flex-row md:items-end justify-between mb-8 gap-4">
        <div>
          <h1 className="font-serif text-3xl md:text-4xl text-stone-900 mb-2">The Ledger</h1>
          <p className="text-stone-500 font-sans">Complete index of all categories tracked by the system.</p>
        </div>
        <div className="flex flex-wrap gap-2 text-xs font-medium uppercase tracking-wider">
          {['ALL', 'DECLARED', 'EMPTY', 'CANDIDATE', 'DEPRECATED', 'SPLIT_REQUIRED'].map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-3 py-2 border transition-colors rounded-sm ${
                filter === f 
                  ? 'bg-stone-900 text-white border-stone-900' 
                  : 'bg-white text-stone-500 border-stone-200 hover:border-stone-400'
              }`}
            >
              {f.replace('_', ' ')}
            </button>
          ))}
        </div>
      </div>

      <div className="border border-stone-200 bg-white rounded-sm overflow-hidden shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-stone-50 border-b border-stone-200 text-xs uppercase tracking-widest text-stone-500 font-semibold">
                <th className="p-4 w-1/4">Category</th>
                <th className="p-4 w-1/6">Status</th>
                <th className="p-4 w-1/3">Verdict / Model</th>
                <th className="p-4 w-1/6">Confidence</th>
                <th className="p-4 text-right">Last Reviewed</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-stone-100">
              {filteredData.map((item) => (
                <tr 
                  key={item.id} 
                  onClick={() => { setSelectedCategory(item); setView('category'); }}
                  className="hover:bg-stone-50 transition-colors cursor-pointer group"
                >
                  <td className="p-4 font-serif font-medium text-stone-900 group-hover:text-emerald-900 transition-colors">
                    {item.category}
                  </td>
                  <td className="p-4">
                    {getStatusBadge(item.status)}
                  </td>
                  <td className="p-4 text-stone-600 font-sans text-sm">
                    {item.status === 'EMPTY' 
                      ? <span className="text-stone-400 italic">None</span> 
                      : <span className="text-stone-800 line-clamp-1">{item.model || 'Under Review'}</span>}
                  </td>
                  <td className="p-4 text-stone-500 text-xs">
                    {item.confidence && (
                       <div className="flex gap-1">
                         {[...Array(5)].map((_, i) => (
                           <div key={i} className={`w-1.5 h-1.5 rounded-full ${i < item.confidence ? 'bg-stone-800' : 'bg-stone-200'}`} />
                         ))}
                       </div>
                    )}
                  </td>
                  <td className="p-4 text-right text-stone-400 text-sm font-mono">
                    {item.lastReviewed}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {filteredData.length === 0 && (
          <div className="p-12 text-center text-stone-400 font-serif italic">
            No categories found with this status.
          </div>
        )}
      </div>
    </div>
  );
};

const CategoryView = ({ item }) => {
  if (!item) return null;

  const isDeclared = item.status === 'DECLARED';
  const isEmpty = item.status === 'EMPTY';
  const isDeprecated = item.status === 'DEPRECATED';

  return (
    <div className="max-w-4xl mx-auto px-4 py-12 animate-in fade-in slide-in-from-bottom-8 duration-700 bg-[#FDFBF7] min-h-screen">
      
      {/* Breadcrumb */}
      <div className="mb-8 border-b border-stone-200 pb-6">
        <div className="flex items-center gap-3 mb-4">
          <span className="text-stone-400 uppercase tracking-widest text-xs font-bold">Category</span>
          <ChevronRight size={12} className="text-stone-300" />
          <span className="text-stone-900 uppercase tracking-widest text-xs font-bold">{item.category}</span>
        </div>
        <div className="flex flex-col md:flex-row md:items-start justify-between gap-4">
          <div>
            <h1 className="font-serif text-3xl md:text-5xl text-stone-900 mb-2 leading-tight">
              {item.status === 'EMPTY' ? item.category : (item.model || item.category)}
            </h1>
            {item.price && <p className="text-stone-500 font-mono text-sm mt-2">{item.price} • {item.manufacturer || 'Standard Issue'}</p>}
          </div>
          <div className="shrink-0">
             {getStatusBadge(item.status)}
          </div>
        </div>
      </div>

      {/* Verdict Block - The core of the page */}
      <div className={`p-8 mb-12 border-l-4 shadow-sm ${
        isDeclared ? 'bg-emerald-50/50 border-emerald-800' :
        isEmpty ? 'bg-stone-100/50 border-stone-400' :
        isDeprecated ? 'bg-red-50/50 border-red-800' :
        'bg-amber-50/50 border-amber-500'
      }`}>
        <h3 className={`text-xs font-bold uppercase tracking-widest mb-3 flex items-center gap-2 ${
          isDeclared ? 'text-emerald-900' :
          isEmpty ? 'text-stone-600' :
          isDeprecated ? 'text-red-900' : 'text-amber-800'
        }`}>
          {isDeclared && <ShieldCheck size={16} />}
          {isEmpty && <Ban size={16} />}
          {isDeprecated && <History size={16} />}
          {!isDeclared && !isEmpty && !isDeprecated && <Clock size={16} />}
          Official Verdict
        </h3>
        <p className={`font-serif text-xl md:text-2xl leading-relaxed ${
          isDeclared ? 'text-emerald-950' : 'text-stone-800'
        }`}>
          {item.coreReasoning}
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-12">
        {/* Main Content Column */}
        <div className="lg:col-span-8 space-y-12">
          
          {/* Form Statement */}
          <section>
            <h3 className="font-sans font-bold text-sm uppercase tracking-widest text-stone-400 mb-4 border-b border-stone-200 pb-2">Form Definition</h3>
            <p className="font-serif text-lg text-stone-800 leading-relaxed">
              {item.formDefinition}
            </p>
          </section>

          {/* Why Not Others / Market Disqualifiers */}
          {item.keyDisqualifiers && (
             <section>
              <h3 className="font-sans font-bold text-sm uppercase tracking-widest text-stone-400 mb-4 border-b border-stone-200 pb-2">
                {isEmpty ? 'Market Disqualifiers' : 'Why Not Others'}
              </h3>
              <p className="text-stone-600 leading-relaxed">
                {item.keyDisqualifiers}
              </p>
            </section>
          )}

          {/* Failure Modes */}
          {item.failureModes && (
            <section>
               <h3 className="font-sans font-bold text-sm uppercase tracking-widest text-stone-400 mb-4 border-b border-stone-200 pb-2 flex items-center gap-2">
                 <AlertTriangle size={14} /> Known Failure Modes
               </h3>
               <p className="text-stone-600 leading-relaxed bg-stone-50 p-4 border border-stone-200 text-sm">
                 {item.failureModes}
               </p>
            </section>
          )}

           {/* Evidence List */}
           {item.evidence && item.evidence.length > 0 && (
            <section>
               <h3 className="font-sans font-bold text-sm uppercase tracking-widest text-stone-400 mb-4 border-b border-stone-200 pb-2">
                 Evidence of Longevity
               </h3>
               <ul className="grid grid-cols-1 md:grid-cols-2 gap-4">
                 {item.evidence.map((e, i) => (
                   <li key={i} className="flex items-start gap-3 text-stone-700 text-sm">
                     <span className="text-emerald-800 mt-1">●</span>
                     {e}
                   </li>
                 ))}
               </ul>
            </section>
          )}

          {/* CHALLENGE WIDGET INTEGRATION */}
          <ChallengeWidget item={item} />

        </div>

        {/* Sidebar Column */}
        <div className="lg:col-span-4 space-y-8">
           {/* Schematic / Image Placeholder */}
           <div className="aspect-square bg-white border border-stone-200 flex items-center justify-center relative overflow-hidden shadow-sm">
             {/* Platonic Asset (Procedural Wireframe) */}
             {isDeclared ? (
                <PlatonicAsset 
                   id={item.id} 
                   className="w-full h-full p-8"
                />
             ) : (
                <div className="text-center z-10 p-6">
                 {isEmpty ? (
                     <Ban size={80} className="text-stone-300 mx-auto mb-4" />
                 ) : (
                     <Box size={80} className="text-stone-300 mx-auto mb-4" />
                 )}
                 <p className="text-xs uppercase tracking-widest text-stone-400">
                    {isEmpty ? 'Void Category' : 'No Reference'}
                 </p>
               </div>
             )}
          </div>

          {/* Meta Data Box */}
          <div className="bg-stone-50 border border-stone-200 p-6 space-y-6">
             {item.maintenance && (
               <div>
                  <h4 className="text-xs font-bold uppercase tracking-widest text-stone-400 mb-1">Permanence Type</h4>
                  <div className="flex items-center gap-2 text-stone-900 font-medium">
                    <ShieldCheck size={14} className="text-stone-500" />
                    {item.maintenance}
                  </div>
               </div>
             )}
             
             {item.lifespan && (
               <div>
                  <h4 className="text-xs font-bold uppercase tracking-widest text-stone-400 mb-1">Estimated Lifespan</h4>
                  <div className="flex items-center gap-2 text-stone-900 font-medium">
                    <CalendarDays size={14} className="text-stone-500" />
                    {item.lifespan}
                  </div>
               </div>
             )}

             <div>
                <h4 className="text-xs font-bold uppercase tracking-widest text-stone-400 mb-1">Last Reviewed</h4>
                <p className="text-stone-900 font-mono text-sm">{item.lastReviewed}</p>
             </div>

             {item.price && (
                <a href="#" className="block w-full py-3 bg-stone-900 text-stone-50 text-center text-sm font-bold uppercase tracking-widest hover:bg-stone-700 transition-colors">
                  Where to Buy
                </a>
             )}
          </div>
        </div>
      </div>
    </div>
  );
};

const AboutView = () => (
  <div className="max-w-4xl mx-auto px-4 py-20 bg-[#FDFBF7] animate-in fade-in duration-500 min-h-screen">
    <div className="border-b border-stone-300 pb-12 mb-12">
      <div className="w-16 h-16 bg-stone-900 rounded-full flex items-center justify-center mb-6">
        <Gavel className="text-stone-50" size={32} />
      </div>
      <h1 className="font-serif text-4xl md:text-5xl text-stone-900 mb-6">Internal Rulebook v1.0</h1>
      <p className="font-serif text-xl leading-relaxed text-stone-500 max-w-2xl">
        We declare one physical product per category as the Platonic Ideal: the object that best embodies the category’s true function with maximum durability, repairability, and long-term integrity.
      </p>
    </div>
    
    <div className="grid grid-cols-1 md:grid-cols-12 gap-12">
      <div className="md:col-span-8 space-y-16">
        
        {/* Core Definition */}
        <section>
          <h2 className="font-sans font-bold text-sm uppercase tracking-widest text-stone-400 mb-6 flex items-center gap-2">
            <Scale size={16} /> Core Definition
          </h2>
          <p className="font-serif text-lg text-stone-900 mb-6">A product is Platonic if it:</p>
          <ul className="space-y-4">
            {[
              "Ends the search: Owning it makes further shopping unnecessary.",
              "Improves or stays whole with time: Performance doesn't degrade through ordinary use.",
              "Has reversible failure modes: Damage is fixable by maintenance or repair.",
              "Is stable: The model’s core materials don't drift silently year-to-year.",
              "Is honest: No fragile complexity pretending to be progress.",
              "Is supported: Accessible parts/service/manuals.",
              "Is form-faithful: Expresses the essential 'Form' of the category."
            ].map((rule, i) => (
              <li key={i} className="flex gap-4 items-start">
                <span className="font-mono text-stone-300 text-sm">0{i+1}</span>
                <span className="text-stone-700 leading-relaxed">{rule}</span>
              </li>
            ))}
          </ul>
        </section>

        {/* Admission Test */}
        <section className="bg-white border border-stone-200 p-8 shadow-sm">
          <h2 className="font-sans font-bold text-sm uppercase tracking-widest text-emerald-900 mb-6 flex items-center gap-2">
            <CheckCircle2 size={16} /> The Admission Test
          </h2>
          <div className="space-y-6">
            <div>
              <h3 className="font-bold text-stone-900 mb-1">A. Form Clarity</h3>
              <p className="text-stone-600 text-sm">We can state the Form in one sentence: “A ___ is ___.”</p>
            </div>
            <div>
              <h3 className="font-bold text-stone-900 mb-1">B. Longevity Reality</h3>
              <p className="text-stone-600 text-sm">Built to last by design. Credible path to 10–20+ years of ownership.</p>
            </div>
            <div>
              <h3 className="font-bold text-stone-900 mb-1">C. Repair Path</h3>
              <p className="text-stone-600 text-sm">Known way to restore function (parts, service, refurb).</p>
            </div>
            <div>
              <h3 className="font-bold text-stone-900 mb-1">D. Model Stability</h3>
              <p className="text-stone-600 text-sm">The name doesn’t hide annual internal downgrades.</p>
            </div>
            <div>
              <h3 className="font-bold text-stone-900 mb-1">E. “No Timers”</h3>
              <p className="text-stone-600 text-sm">No consumable coating or sealed component that forces replacement.</p>
            </div>
          </div>
        </section>

        {/* Disqualifiers */}
        <section>
          <h2 className="font-sans font-bold text-sm uppercase tracking-widest text-red-900 mb-6 flex items-center gap-2">
            <XCircle size={16} /> Immediate Disqualifiers
          </h2>
          <ul className="grid grid-cols-1 gap-4">
            {[
              { title: "Countdown Timer Surfaces", desc: "Nonstick coatings, fragile finishes." },
              { title: "Sealed-for-life", desc: "No parts, glued assemblies, proprietary tools." },
              { title: "Complexity w/o Recoverability", desc: "Touchscreens, sensors, smart features that brick the object." },
              { title: "Silent Model Drift", desc: "Same name, cheaper internals." },
              { title: "Luxury Masquerade", desc: "Paying for brand, not core longevity." }
            ].map((item, i) => (
              <li key={i} className="border-l-2 border-red-200 pl-4 py-1">
                <span className="font-bold text-stone-900 block">{item.title}</span>
                <span className="text-stone-500 text-sm">{item.desc}</span>
              </li>
            ))}
          </ul>
        </section>

      </div>

      <div className="md:col-span-4 space-y-8">
        <div className="bg-stone-100 p-6 border border-stone-200">
          <h3 className="font-bold text-stone-900 mb-2 flex items-center gap-2">
            <Ban size={16} className="text-stone-400"/> Empty Categories
          </h3>
          <p className="text-sm text-stone-600 mb-4">We leave a category empty when the market is compromised or no product meets the standard.</p>
          <p className="text-xs font-bold uppercase tracking-widest text-stone-400">Empty is integrity.</p>
        </div>

        <div className="bg-stone-50 p-6 border border-stone-200">
          <h3 className="font-bold text-stone-900 mb-2 flex items-center gap-2">
            <History size={16} className="text-stone-400"/> Revocation
          </h3>
          <p className="text-sm text-stone-600 mb-2">A declaration is revoked if:</p>
          <ul className="text-sm text-stone-600 list-disc pl-4 space-y-1">
            <li>Material drift occurs</li>
            <li>Support collapses</li>
            <li>New failure mode emerges</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
);

// --- MAIN APP ---

const App = () => {
  const [view, setView] = useState('home');
  const [selectedCategory, setSelectedCategory] = useState(null);

  // Scroll to top on view change
  React.useEffect(() => {
    window.scrollTo(0, 0);
  }, [view]);

  return (
    <div className="min-h-screen bg-[#FDFBF7] text-stone-900 font-sans selection:bg-stone-200">
      <Navigation setView={setView} currentView={view} />
      
      <main>
        {view === 'home' && <HomeView setView={setView} setSelectedCategory={setSelectedCategory} />}
        {view === 'index' && <IndexView setView={setView} setSelectedCategory={setSelectedCategory} />}
        {view === 'category' && <CategoryView item={selectedCategory} />}
        {view === 'consult' && <ConsultView />}
        {view === 'about' && <AboutView />}
      </main>

      <footer className="bg-stone-100 border-t border-stone-300 py-12">
        <div className="max-w-6xl mx-auto px-4 grid grid-cols-1 md:grid-cols-3 gap-8 text-stone-600 text-sm">
          <div>
            <h4 className="font-serif font-bold text-stone-900 mb-4 flex items-center gap-2"><Scale size={16}/> Platonic Ideal</h4>
            <p className="mb-4 max-w-xs">An independent index of durability.</p>
            <p>© {new Date().getFullYear()} Verdict Systems.</p>
          </div>
          <div>
            <h4 className="font-serif font-bold text-stone-900 mb-4">Principles</h4>
            <ul className="space-y-2">
              <li>Time over Performance</li>
              <li>Repair over Recycle</li>
              <li>Structure over Features</li>
            </ul>
          </div>
          <div className="md:text-right">
            <p className="italic">"Perfection is achieved, not when there is nothing more to add, but when there is nothing left to take away."</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;