import fs from 'node:fs'
import path from 'node:path'
import Papa from 'papaparse'

const repoRoot = path.resolve(new URL('.', import.meta.url).pathname, '..')
const csv = fs.readFileSync(path.join(repoRoot, 'public/platonic_ideal.csv'), 'utf8')
const inventory = JSON.parse(fs.readFileSync(path.join(repoRoot, 'src/data/image-source-inventory.json'), 'utf8'))
const { data, errors: parseErrors } = Papa.parse(csv, { header: true, skipEmptyLines: true })
const errors = [...parseErrors.map((error) => `CSV row ${error.row ?? '?'}: ${error.message}`)]
const warnings = []
const allowed = {
  sourceType: new Set(['manufacturer', 'authorized-retailer', 'retailer', 'catalog-or-manual', 'open-license', 'owned', 'ai-interpretation', 'unlocated']),
  imageAvailability: new Set(['confirmed', 'lead', 'not-found']),
  rightsStatus: new Set(['unknown', 'permission-pending', 'licensed', 'owned', 'not-for-republish']),
  identityStatus: new Set(['exact', 'family', 'ambiguous', 'generic']),
  recommendedUse: new Set(['identity', 'service', 'evidence', 'purchase-link-only']),
}

const declared = data
  .filter((row) => String(row.Status || '').trim().toUpperCase() === 'DECLARED')
  .map((row) => ({ productId: `PI-${String(row.Number || '').trim().padStart(3, '0')}`, category: String(row.Category || '').trim(), model: String(row.Model || '').trim() }))
const records = Array.isArray(inventory.records) ? inventory.records : []
const byProduct = new Map()

if (!inventory.checkedAt) errors.push('Image source inventory must include checkedAt')
if (records.length !== declared.length) errors.push(`Image source inventory has ${records.length} records for ${declared.length} declared products`)

for (const record of records) {
  if (!record.productId) errors.push('Image source record is missing productId')
  if (byProduct.has(record.productId)) errors.push(`Duplicate image source record: ${record.productId}`)
  byProduct.set(record.productId, record)

  for (const [field, values] of Object.entries(allowed)) {
    if (!values.has(record[field])) errors.push(`${record.productId || 'Unknown'}: invalid ${field} ${record[field] || '(blank)'}`)
  }

  if (!record.category || !record.declaredModel || !record.sourcePageTitle || !record.sellerOrManufacturer || !record.exactModel || !record.variant || !record.region || !record.notes) {
    errors.push(`${record.productId || 'Unknown'}: required source identity fields are incomplete`)
  }
  if (record.sourceUrl && !/^https:\/\//.test(record.sourceUrl)) errors.push(`${record.productId}: sourceUrl must use https`)
  if (record.imageAvailability !== 'not-found' && !record.sourceUrl) errors.push(`${record.productId}: ${record.imageAvailability} source requires sourceUrl`)
  if (record.imageAvailability === 'not-found' && record.sourceUrl) warnings.push(`${record.productId}: not-found record has a sourceUrl; confirm it is intentionally a general lead`)
  if (record.imageAvailability === 'confirmed' && record.identityStatus !== 'exact') warnings.push(`${record.productId}: image-bearing source is confirmed, but identity is ${record.identityStatus}`)
  if (record.rightsStatus !== 'licensed' && record.rightsStatus !== 'owned') warnings.push(`${record.productId}: source image is not cleared for republication`)
}

for (const entry of declared) {
  const record = byProduct.get(entry.productId)
  if (!record) {
    errors.push(`${entry.productId} (${entry.category}): missing image source record`)
    continue
  }
  if (record.category !== entry.category) errors.push(`${entry.productId}: inventory category “${record.category}” does not match CSV “${entry.category}”`)
  if (record.declaredModel !== entry.model) errors.push(`${entry.productId}: inventory model does not match CSV model`)
}

for (const record of records) {
  if (!declared.some((entry) => entry.productId === record.productId)) errors.push(`${record.productId}: inventory record is not a current DECLARED product`)
}

const summary = [
  `Image sources: ${records.length} declared products`,
  `${records.filter((record) => record.imageAvailability === 'confirmed').length} confirmed image-bearing leads`,
  `${records.filter((record) => record.imageAvailability === 'lead').length} leads needing exactness work`,
  `${records.filter((record) => record.imageAvailability === 'not-found').length} without a current source`,
  `${records.filter((record) => record.rightsStatus === 'licensed' || record.rightsStatus === 'owned').length} rights-cleared for republication`,
].join(' · ')

console.log(summary)
if (warnings.length) console.log(`Image source warnings: ${warnings.length} (use --verbose to review)`)
if (process.argv.includes('--verbose')) warnings.forEach((warning) => console.warn(`WARN  ${warning}`))

if (errors.length) {
  errors.forEach((error) => console.error(`ERROR ${error}`))
  process.exit(1)
}

console.log('Image source inventory validation passed.')
