import fs from 'node:fs'
import Papa from 'papaparse'

const file = new URL('../public/platonic_ideal.csv', import.meta.url)
const csv = fs.readFileSync(file, 'utf8')
const required = ['Number', 'Category', 'Status', 'Model', 'Form Definition', 'Core Reasoning', 'Key Disqualifiers', 'Admission Test', 'Failure Modes']
const allowed = new Set(['DECLARED', 'EMPTY', 'CANDIDATE', 'CONDITIONAL', 'CONSUMABLE', 'SPLIT_REQUIRED'])
const { data, errors: parseErrors, meta } = Papa.parse(csv, { header: true, skipEmptyLines: true })
const errors = [...parseErrors.map((error) => `CSV row ${error.row ?? '?'}: ${error.message}`)]
const warnings = []

for (const header of required) {
  if (!meta.fields?.includes(header)) errors.push(`Missing required column: ${header}`)
}

const slugs = new Map()
const statusCounts = {}
const slugify = (value) => value.toLowerCase().replace(/&/g, ' and ').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '')

data.forEach((row, index) => {
  const line = index + 2
  const category = (row.Category || '').trim()
  const status = (row.Status || '').trim().toUpperCase()
  const model = (row.Model || '').trim()
  if (!category) errors.push(`Line ${line}: Category is required`)
  if (!allowed.has(status)) errors.push(`Line ${line} (${category || 'unnamed'}): Unknown status ${status || 'blank'}`)
  if (status === 'DECLARED' && !model) errors.push(`Line ${line} (${category}): DECLARED requires one Model`)
  if (status === 'EMPTY' && model) errors.push(`Line ${line} (${category}): EMPTY must not name a Model`)
  if (model && /\s+or\s+|\s*\/\s*/i.test(model)) warnings.push(`Line ${line} (${category}): Model may contain multiple declarations: ${model}`)

  const slug = slugify(category)
  if (slugs.has(slug)) errors.push(`Line ${line} (${category}): Duplicate generated slug also used by ${slugs.get(slug)}`)
  slugs.set(slug, category)
  statusCounts[status] = (statusCounts[status] || 0) + 1

  const coreA = (row['Core Reasoning'] || '').trim()
  const coreB = (row.Core_Reasoning || '').trim()
  if (coreA && coreB && coreA !== coreB) warnings.push(`Line ${line} (${category}): duplicate Core Reasoning columns differ`)
  const disA = (row['Key Disqualifiers'] || '').trim()
  const disB = (row.Key_Disqualifiers || '').trim()
  if (disA && disB && disA !== disB) warnings.push(`Line ${line} (${category}): duplicate Key Disqualifiers columns differ`)
})

console.log(`Register: ${data.length} entries · ${Object.entries(statusCounts).map(([key, value]) => `${key} ${value}`).join(' · ')}`)
if (warnings.length) console.log(`Register warnings: ${warnings.length} (run the validator directly to review during data cleanup)`)
if (process.argv.includes('--verbose')) warnings.forEach((warning) => console.warn(`WARN  ${warning}`))

if (errors.length) {
  errors.forEach((error) => console.error(`ERROR ${error}`))
  process.exit(1)
}

console.log('Register validation passed.')
