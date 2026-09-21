/** One commercial product. Editorial categories are never cart items. */
export const dossier = {
  id: 'the-dossier',
  editionId: 'platonic-ideal-declared-1940',
  name: 'The Platonic Ideal Dossier — Declared Edition',
  edition: 'Declared Edition',
  version: '1940',
  recommendationCount: 48,
  pageCount: 157,
  fileFormat: 'Tagged PDF',
  price: 24,
  priceLabel: '$24',
  format: '157-page tagged PDF',
  coverage: '48 declared recommendations',
  availability: 'Preview only',
}

export const dossierChapters = [
  ['01', 'The standard', 'The questions to ask before an object earns a place in your life.'],
  ['02', 'The evidence', 'An organized reading path through source material and research notes.'],
  ['03', 'The tradeoffs', 'What fails, what falls short, and which compromises deserve attention.'],
  ['04', 'The ownership plan', 'Maintenance, repair, replacement, and the practical work of keeping things.'],
]

export const faqs = [
  ['What am I buying?', 'A 157-page tagged PDF containing the Declared Edition of the Platonic Ideal dossier: 48 declared recommendations, their reasoning, evidence, tradeoffs, and ownership notes. Physical objects in the catalog are subjects of our research; they are not sold by us.'],
  ['Can I still read the verdict for free?', 'Yes. Category verdicts, decisive reasoning, and the editorial rules stay public. The dossier is intended to add research depth and convenience.'],
  ['Is this a subscription?', 'No. The dossier is a one-time $24 purchase. There are no membership tiers or recurring charges.'],
  ['Does paying change a recommendation?', 'No. Payment cannot influence product selection, placement, or a verdict. A category can still have no qualifying pick.'],
  ['Can I buy it today?', 'Not yet. The public sample is available now; paid checkout and delivery will be enabled once the production payment and fulfillment configuration is complete.'],
  ['What will the dossier include?', 'The Declared Edition includes 48 recommendations in a 157-page tagged PDF, organized around the standard, evidence, tradeoffs, ownership, and the limits of each judgment.'],
]

export function getDossierFaqs(isLive: boolean) {
  return faqs.map(([question, answer]) => question === 'Can I buy it today?'
    ? [question, isLive
      ? 'Yes. Stripe hosts the secure checkout. After payment is confirmed, the dossier is available through the purchase confirmation flow.'
      : 'Not yet. The public sample is available now; paid checkout and delivery will be enabled once the production payment and fulfillment configuration is complete.']
    : [question, answer])
}
