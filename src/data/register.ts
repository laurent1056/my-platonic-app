import fs from 'node:fs'
import path from 'node:path'
import Papa from 'papaparse'

export type SourceStatus =
  | 'DECLARED'
  | 'EMPTY'
  | 'CANDIDATE'
  | 'CONDITIONAL'
  | 'CONSUMABLE'
  | 'SPLIT_REQUIRED'

export type Verdict = 'DECLARED' | 'EMPTY' | 'IN REVIEW'

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
  imageUrl: string
  hasRealImage: boolean
  alternates: string
  admissionTest: string
  failureModes: string
  confidence: number
  lastReviewed: string
  notes: string
  searchText: string
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

function clean(value?: string): string {
  return (value ?? '').trim().replace(/\r\n/g, '\n')
}

function publicVerdict(status: SourceStatus): Verdict {
  if (status === 'DECLARED') return 'DECLARED'
  if (status === 'EMPTY') return 'EMPTY'
  return 'IN REVIEW'
}

function isRealImage(url: string): boolean {
  return Boolean(url) && !url.includes('placehold.co')
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
  const imageUrl = clean(row['Image URL'])
  const entry: RegisterEntry = {
    number,
    reference: `PI-${String(number).padStart(3, '0')}`,
    category,
    slug: slugify(category),
    sourceStatus,
    verdict: publicVerdict(sourceStatus),
    model,
    price: clean(row.Price),
    formDefinition: clean(row['Form Definition']),
    formStatement: clean(row['Form Statement']),
    summary,
    coreReasoning,
    disqualifiers,
    maintenance: clean(row['Maintenance / Replacement Cycle']),
    permanence: clean(row['Permanence Mechanism']),
    imageUrl,
    hasRealImage: isRealImage(imageUrl),
    alternates: clean(row['Alternates (non-declared)']),
    admissionTest: clean(row['Admission Test']),
    failureModes: clean(row['Failure Modes']),
    confidence: Math.max(0, Math.min(5, Number(clean(row.Confidence)) || 0)),
    lastReviewed: clean(row['Last Reviewed']),
    notes: clean(row.Notes),
    searchText: '',
  }

  entry.searchText = [
    entry.category,
    entry.model,
    entry.verdict,
    entry.sourceStatus,
    entry.permanence,
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
