import fs from 'node:fs'
import path from 'node:path'
import Papa from 'papaparse'
import { imageSourceFor } from './image-sources'

export type SourceStatus =
  | 'DECLARED'
  | 'EMPTY'
  | 'CANDIDATE'
  | 'CONDITIONAL'
  | 'CONSUMABLE'
  | 'SPLIT_REQUIRED'

export type Verdict = 'DECLARED' | 'EMPTY' | 'IN REVIEW'

/**
 * Public language for the editorial states. The CSV keeps the precise
 * workflow vocabulary; visitors should see the decision in plain English.
 */
export const publicStateLabels = {
  DECLARED: 'Our pick',
  EMPTY: 'No qualifying pick',
  'IN REVIEW': 'Still researching',
  CANDIDATE: 'Possible pick under review',
  CONDITIONAL: 'Depends on the use',
  CONSUMABLE: 'Designed to be replaced',
  SPLIT_REQUIRED: 'Needs a narrower category',
} as const

export const publicStateDescriptions = {
  DECLARED: 'One product met the standard and is named here.',
  EMPTY: 'We looked seriously and did not find one product that earned the pick.',
  'IN REVIEW': 'The evidence is not complete enough for a final recommendation.',
  CANDIDATE: 'A possible product is being investigated, but it is not yet recommended.',
  CONDITIONAL: 'The answer changes materially depending on the job or operating conditions.',
  CONSUMABLE: 'This category has a rational replacement cycle rather than indefinite ownership.',
  SPLIT_REQUIRED: 'This category contains different jobs that should not share one answer.',
} as const

export const publicPermanenceLabels = {
  repairable: 'Repairable',
  warranty: 'Backed by service or warranty',
  'rational-renewal': 'Replaceable by design',
  consumable: 'Designed to be replaced',
  unspecified: 'Not yet classified',
} as const

export const publicPermanenceDescriptions = {
  repairable: 'The product can be repaired, rebuilt, or restored when parts wear out.',
  warranty: 'A durable service or warranty system helps keep the product in use.',
  'rational-renewal': 'Replacing the product is an expected and rational part of ownership.',
  consumable: 'The category is meant to be replaced as part of normal use.',
  unspecified: 'The long-term ownership path has not been classified yet.',
} as const

export type DomainId =
  | 'kitchen-cooking'
  | 'household-systems'
  | 'tools-workshop'
  | 'clothing-carry'
  | 'outdoor-utility'
  | 'furniture-work'
  | 'writing-office'
  | 'electronics'
  | 'personal-care-misc'

export interface DomainDefinition {
  id: DomainId
  name: string
  description: string
}

export type PermanenceKind = 'repairable' | 'warranty' | 'rational-renewal' | 'consumable' | 'unspecified'

export const domains: DomainDefinition[] = [
  { id: 'kitchen-cooking', name: 'Kitchen & Cooking', description: 'Objects that turn ingredients into meals or keep them ready.' },
  { id: 'household-systems', name: 'Household Systems', description: 'Appliances and infrastructure that keep a home working.' },
  { id: 'tools-workshop', name: 'Tools & Workshop', description: 'Hand tools, powered tools, and practical equipment for making and maintaining.' },
  { id: 'clothing-carry', name: 'Clothing & Carry', description: 'Wearable and carried objects built around daily use and personal movement.' },
  { id: 'outdoor-utility', name: 'Outdoor & Utility', description: 'Field equipment for travel, shelter, weather, and utility.' },
  { id: 'furniture-work', name: 'Furniture & Work', description: 'Objects that support sitting, writing, storage, and daily work.' },
  { id: 'writing-office', name: 'Writing & Office', description: 'Small instruments and office objects for recording and organizing thought.' },
  { id: 'electronics', name: 'Electronics', description: 'Computing and connected objects judged with special attention to software and service life.' },
  { id: 'personal-care-misc', name: 'Personal Care & Misc.', description: 'Personal instruments and inherently renewing objects.' },
]

const categoryDomainOverrides: Record<string, DomainId> = {
  'frying pan': 'kitchen-cooking',
  refrigerator: 'household-systems',
  hammer: 'tools-workshop',
  smartphone: 'electronics',
  'kitchen knife': 'kitchen-cooking',
  'washing machine': 'household-systems',
  saucepan: 'kitchen-cooking',
  screwdriver: 'tools-workshop',
  'dutch oven': 'kitchen-cooking',
  laptop: 'electronics',
  'coffee maker': 'kitchen-cooking',
  drill: 'tools-workshop',
  kettle: 'kitchen-cooking',
  'task chair': 'furniture-work',
  toaster: 'kitchen-cooking',
  backpack: 'outdoor-utility',
  mattress: 'household-systems',
  'hand saw': 'tools-workshop',
  desk: 'furniture-work',
  boots: 'clothing-carry',
  'oven/range': 'kitchen-cooking',
  belt: 'clothing-carry',
  freezer: 'household-systems',
  'adjustable wrench': 'tools-workshop',
  't-shirt': 'clothing-carry',
  jeans: 'clothing-carry',
  'jacket/coat': 'clothing-carry',
  chisel: 'tools-workshop',
  pliers: 'tools-workshop',
  'tape measure': 'tools-workshop',
  tent: 'outdoor-utility',
  'sleeping bag': 'outdoor-utility',
  'water bottle': 'outdoor-utility',
  flashlight: 'outdoor-utility',
  sweater: 'clothing-carry',
  cooler: 'outdoor-utility',
  'pocket knife': 'outdoor-utility',
  notebook: 'writing-office',
  pen: 'writing-office',
  'cutting board': 'kitchen-cooking',
  'vacuum cleaner': 'household-systems',
  bicycle: 'outdoor-utility',
  'dining chair': 'furniture-work',
  printer: 'electronics',
  socks: 'clothing-carry',
  watch: 'personal-care-misc',
  shoes: 'clothing-carry',
  'food storage container': 'kitchen-cooking',
  level: 'tools-workshop',
  'drill bits': 'tools-workshop',
  'extension cord': 'tools-workshop',
  'camping stove': 'outdoor-utility',
  'mechanical pencil': 'writing-office',
  umbrella: 'personal-care-misc',
  ladder: 'tools-workshop',
  wheelbarrow: 'outdoor-utility',
  wallet: 'clothing-carry',
  briefcase: 'clothing-carry',
  hat: 'clothing-carry',
  gloves: 'clothing-carry',
  toothbrush: 'personal-care-misc',
  razor: 'personal-care-misc',
  'hair dryer': 'personal-care-misc',
  'desktop computer': 'electronics',
  'bed frame': 'furniture-work',
  'sofa / couch': 'furniture-work',
  sofa: 'furniture-work',
  bookshelf: 'furniture-work',
  'coffee table': 'furniture-work',
  'dresser / wardrobe': 'furniture-work',
  dresser: 'furniture-work',
  wardrobe: 'furniture-work',
  'desk lamp': 'furniture-work',
  'floor lamp': 'furniture-work',
  'window blinds': 'furniture-work',
  pillow: 'furniture-work',
  'backpacking pack': 'outdoor-utility',
  'hunting knife': 'outdoor-utility',
  television: 'electronics',
  router: 'electronics',
  headphones: 'electronics',
  speakers: 'electronics',
  camera: 'electronics',
  smartwatch: 'electronics',
  'home thermostat': 'household-systems',
  dryer: 'household-systems',
  'water heater': 'household-systems',
  furnace: 'household-systems',
  'air conditioner': 'household-systems',
}

function domainForCategory(category: string): DomainDefinition {
  const normalized = category.toLocaleLowerCase()
  const parentName = normalized.replace(/\s+\([^)]*\)$/, '')
  const formName = normalized.replace(/\s+—\s+.*/, '')
  const slashParent = formName.split(' / ')[0] ?? formName
  const candidates = [normalized, parentName, formName, slashParent]
  const id = candidates.map((candidate) => categoryDomainOverrides[candidate]).find(Boolean) ?? 'personal-care-misc'
  return domains.find((domain) => domain.id === id) ?? domains[domains.length - 1]!
}

function permanenceKind(value: string, sourceStatus: SourceStatus): PermanenceKind {
  const normalized = value.toLocaleLowerCase()
  if (sourceStatus === 'CONSUMABLE' || normalized.includes('consumable')) return 'consumable'
  if (normalized.includes('warranty') || normalized.includes('guarantee')) return 'warranty'
  if (normalized.includes('rebuild') || normalized.includes('repair') || normalized.includes('service')) return 'repairable'
  if (normalized.includes('renew') || normalized.includes('replacement') || normalized.includes('replace')) return 'rational-renewal'
  return 'unspecified'
}

export interface RegisterEntry {
  number: number
  reference: string
  category: string
  slug: string
  sourceStatus: SourceStatus
  verdict: Verdict
  model: string
  price: string
  formDefinition: string
  formStatement: string
  summary: string
  coreReasoning: string
  disqualifiers: string
  maintenance: string
  permanence: string
  alternates: string
  admissionTest: string
  failureModes: string
  confidence: number
  lastReviewed: string
  notes: string
  searchText: string
  domain: DomainDefinition
  domainSlug: DomainId
  permanenceKind: PermanenceKind
}

type CsvRow = Record<string, string>

const source = path.resolve(process.cwd(), 'public/platonic_ideal.csv')
const csv = fs.readFileSync(source, 'utf8')
const parsed = Papa.parse<CsvRow>(csv, {
  header: true,
  skipEmptyLines: true,
  transformHeader: (header) => header.trim(),
})

if (parsed.errors.length) {
  throw new Error(`Register CSV could not be parsed: ${parsed.errors[0]?.message}`)
}

export function slugify(value: string): string {
  return value
    .normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/&/g, ' and ')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
}

/**
 * Use the source inventory's exact-model page as the shared display identity
 * when it is confirmed. The CSV remains the editorial register of record;
 * this only prevents the storefront and dossier from naming the same model
 * differently.
 */
export function canonicalModelLabel(reference: string, fallback: string): string {
  const source = imageSourceFor(reference)
  const title = source?.sourcePageTitle?.trim()
  const exact = source?.exactModel?.trim()
  const exactIsUsable = exact && !['not recorded', 'model pending', 'not sku-normalized'].includes(exact.toLocaleLowerCase())
  if (!source || source.identityStatus !== 'exact' || !exactIsUsable) return fallback
  const base = title || source.variant?.trim() || exact
  if (!base) return fallback
  return base.toLocaleLowerCase().includes(exact.toLocaleLowerCase()) ? base : `${base} (${exact})`
}

function clean(value?: string): string {
  return (value ?? '').trim().replace(/\r\n/g, '\n')
}

function publicVerdict(status: SourceStatus): Verdict {
  if (status === 'DECLARED') return 'DECLARED'
  if (status === 'EMPTY') return 'EMPTY'
  return 'IN REVIEW'
}

export function publicStateLabel(verdict: Verdict, sourceStatus?: SourceStatus): string {
  void sourceStatus
  if (verdict === 'DECLARED') return publicStateLabels.DECLARED
  if (verdict === 'EMPTY') return publicStateLabels.EMPTY
  return 'Research in progress'
}

export function publicStateDescription(verdict: Verdict, sourceStatus?: SourceStatus): string {
  void sourceStatus
  if (verdict === 'DECLARED') return publicStateDescriptions.DECLARED
  if (verdict === 'EMPTY') return publicStateDescriptions.EMPTY
  return 'The category has a defined research question, but the evidence is not complete enough for a final public outcome.'
}

export const register: RegisterEntry[] = parsed.data.map((row, index) => {
  const number = Number(clean(row.Number)) || index + 1
  const category = clean(row.Category)
  const sourceStatus = (clean(row.Status).toUpperCase() || 'CANDIDATE') as SourceStatus
  const model = clean(row.Model)
  const coreReasoning = clean(row.Core_Reasoning) || clean(row['Core Reasoning'])
  const disqualifiers = clean(row.Key_Disqualifiers) || clean(row['Key Disqualifiers'])
  const summary =
    clean(row['Card Snippet (Why this ends the search)']) ||
    clean(row['Form Statement']) ||
    coreReasoning
  const domain = domainForCategory(category)
  const permanenceValue = clean(row['Permanence Mechanism'])
  const entry: RegisterEntry = {
    number,
    reference: `PI-${String(number).padStart(3, '0')}`,
    category,
    slug: slugify(category),
    sourceStatus,
    verdict: publicVerdict(sourceStatus),
    model: canonicalModelLabel(`PI-${String(number).padStart(3, '0')}`, model),
    price: clean(row.Price),
    formDefinition: clean(row['Form Definition']),
    formStatement: clean(row['Form Statement']),
    summary,
    coreReasoning,
    disqualifiers,
    maintenance: clean(row['Maintenance / Replacement Cycle']),
    permanence: clean(row['Permanence Mechanism']),
    alternates: clean(row['Alternates (non-declared)']),
    admissionTest: clean(row['Admission Test']),
    failureModes: clean(row['Failure Modes']),
    confidence: Math.max(0, Math.min(5, Number(clean(row.Confidence)) || 0)),
    lastReviewed: clean(row['Last Reviewed']),
    notes: clean(row.Notes),
    searchText: '',
    domain,
    domainSlug: domain.id,
    permanenceKind: permanenceKind(permanenceValue, sourceStatus),
  }

  entry.searchText = [
    entry.category,
    entry.model,
    entry.verdict,
    publicStateLabel(entry.verdict, entry.sourceStatus),
    entry.permanence,
    publicPermanenceLabels[entry.permanenceKind],
    entry.domain.name,
    entry.permanenceKind,
    entry.summary,
  ]
    .join(' ')
    .toLocaleLowerCase()

  return entry
})

export const registerStats = {
  total: register.length,
  declared: register.filter((entry) => entry.verdict === 'DECLARED').length,
  empty: register.filter((entry) => entry.verdict === 'EMPTY').length,
  review: register.filter((entry) => entry.verdict === 'IN REVIEW').length,
}

export function withBase(path = ''): string {
  const base = import.meta.env.BASE_URL.endsWith('/')
    ? import.meta.env.BASE_URL
    : `${import.meta.env.BASE_URL}/`
  return `${base}${path.replace(/^\//, '')}`
}

export function categoryUrl(entry: Pick<RegisterEntry, 'slug'>): string {
  return withBase(`category/${entry.slug}/`)
}

export function splitStatements(value: string): string[] {
  if (!value) return []
  return value
    .split(/(?:\n+|(?<=[.!?])\s+(?=[A-Z0-9]))/)
    .map((part) => part.trim())
    .filter(Boolean)
}
