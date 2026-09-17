import type { Verdict } from './register'

export const SITE_NAME = 'Platonic Ideal'
export const DEFAULT_DESCRIPTION = 'Independent product research for durable, repairable things: one product worth choosing per category, or an honest explanation when none qualifies.'
export const DEFAULT_SOCIAL_IMAGE = 'images/plato-silanion-berlin.webp'

const BRAND_SUFFIX = ` · ${SITE_NAME}`

export function normalizeMetaText(value: string): string {
  return value.trim().replace(/\s+/g, ' ')
}

export function truncateAtWord(value: string, maxLength: number): string {
  const normalized = normalizeMetaText(value)
  if (normalized.length <= maxLength) return normalized

  const withoutOverflow = normalized.slice(0, Math.max(1, maxLength - 1)).trimEnd()
  const lastSpace = withoutOverflow.lastIndexOf(' ')
  const readable = lastSpace > 0 ? withoutOverflow.slice(0, lastSpace) : withoutOverflow
  return `${readable.trimEnd()}…`
}

/** Keep the brand suffix visible when a long page title needs shortening. */
export function metaTitle(value: string, maxLength = 60): string {
  const normalized = normalizeMetaText(value)
  if (normalized.length <= maxLength) return normalized

  if (normalized.endsWith(BRAND_SUFFIX)) {
    const subject = normalized.slice(0, -BRAND_SUFFIX.length).trimEnd()
    const subjectMax = Math.max(1, maxLength - BRAND_SUFFIX.length)
    return `${truncateAtWord(subject, subjectMax)}${BRAND_SUFFIX}`
  }

  return truncateAtWord(normalized, maxLength)
}

export function metaDescription(value?: string, fallback = DEFAULT_DESCRIPTION): string {
  return truncateAtWord(value?.trim() || fallback, 160)
}

function primaryCategoryName(category: string): string {
  return normalizeMetaText(category) || 'Product'
}

function compactModelName(model: string): string {
  return normalizeMetaText(model)
    .replace(/\s*\([^)]*\)/g, '')
    .replace(/\s+\b(?:or|versus|vs\.?)\b.*$/i, '')
    .replace(/\s+—\s+.*$/, '')
    .trim()
}

export function categorySeoTitle(category: string, verdict: Verdict, model = ''): string {
  const name = primaryCategoryName(category)

  if (verdict === 'EMPTY') return `${name}: No qualifying pick`
  if (verdict === 'IN REVIEW') return `${name}: Still researching`

  const product = compactModelName(model)
  return truncateAtWord(`${name}: ${product || 'Our pick'}`, 44)
}

export function categorySeoDescription(category: string, verdict: Verdict, source?: string): string {
  const status = verdict === 'DECLARED'
    ? 'Read the evidence, tradeoffs, and ownership notes behind the pick.'
    : verdict === 'EMPTY'
      ? 'See why no product qualifies and what a future pick would need.'
      : 'See what the open research still needs to establish.'

  return metaDescription(`${source?.trim() || `${category}: ${status}`} ${status}`)
}

export function pageSeoDescription(intro?: string, fallback = DEFAULT_DESCRIPTION): string {
  const source = intro?.trim()
  return metaDescription(source ? `${source} Read the independent research at ${SITE_NAME}.` : fallback)
}
