import fs from 'node:fs'
import path from 'node:path'
import Papa from 'papaparse'

const root = process.cwd()
const registerPath = path.join(root, 'public', 'platonic_ideal.csv')
const source = fs.readFileSync(registerPath, 'utf8')
const parsed = Papa.parse(source, { header: true, skipEmptyLines: true })
const rows = parsed.data
const blockers = []
const warnings = []
const finalStatuses = new Set(['DECLARED', 'EMPTY'])
const declared = rows.filter((row) => String(row.Status || '').trim().toUpperCase() === 'DECLARED')
const unresolved = rows.filter((row) => !finalStatuses.has(String(row.Status || '').trim().toUpperCase()))
const declaredAlternatives = declared.filter((row) => /\s+or\s+|[A-Za-z]\s*\/\s*[A-Za-z]/i.test(String(row.Model || '')))

if (parsed.errors.length) blockers.push(`CSV parse failed: ${parsed.errors[0].message}`)
if (rows.length !== 100) blockers.push(`Expected 100 catalog categories; found ${rows.length}`)
if (unresolved.length) blockers.push(`${unresolved.length} categories still have non-final editorial states: ${unresolved.map((row) => `${row.Number} ${row.Category} (${row.Status})`).join('; ')}`)
if (declaredAlternatives.length) blockers.push(`Declared rows name multiple alternatives: ${declaredAlternatives.map((row) => `${row.Number} ${row.Category}: ${row.Model}`).join('; ')}`)

for (const row of rows) {
  const status = String(row.Status || '').trim().toUpperCase()
  const category = String(row.Category || '').trim() || `row ${row.Number}`
  if (status === 'DECLARED') {
    for (const field of ['Model', 'Form Definition', 'Core Reasoning', 'Key Disqualifiers', 'Permanence Mechanism']) {
      if (!String(row[field] || '').trim()) blockers.push(`${category}: declared entry is missing ${field}`)
    }
    const supportInputs = ['Form Definition', 'Core Reasoning', 'Key Disqualifiers', 'Maintenance / Replacement Cycle', 'Permanence Mechanism', 'Failure Modes']
      .filter((field) => String(row[field] || '').trim())
    if (supportInputs.length < 5) blockers.push(`${category}: declared entry has only ${supportInputs.length}/6 publication support inputs`)
  }
  if (status === 'EMPTY') {
    for (const field of ['Form Definition', 'Core Reasoning', 'Key Disqualifiers', 'Admission Test']) {
      if (!String(row[field] || '').trim()) blockers.push(`${category}: no-pick entry is missing ${field}`)
    }
  }
}

const packageJson = JSON.parse(fs.readFileSync(path.join(root, 'package.json'), 'utf8'))
if (!packageJson.scripts?.build) blockers.push('package.json has no production build script')

const dossier = fs.readFileSync(path.join(root, 'src', 'data', 'dossier.ts'), 'utf8')
if (/purchasing is not live|Design preview/i.test(dossier)) blockers.push('dossier offer is still preview-only')
if (!/priceLabel/.test(dossier)) blockers.push('dossier offer has no published price label')

const commerce = fs.readFileSync(path.join(root, 'src', 'scripts', 'commerce.ts'), 'utf8')
const analytics = fs.readFileSync(path.join(root, 'src', 'scripts', 'analytics.ts'), 'utf8')
const instrumentation = `${commerce}\n${analytics}`
for (const marker of ['page_view', 'checkout_start', 'purchase', 'fulfillment']) {
  if (!instrumentation.includes(`'${marker}'`)) blockers.push(`analytics instrumentation does not emit ${marker}`)
}

if (!fs.existsSync(path.join(root, 'public', 'dossier', 'sandbox-fulfillment.txt'))) blockers.push('sandbox fulfillment artifact is missing')
if (!fs.existsSync(path.join(root, 'src', 'components', 'EmailCapture.astro'))) blockers.push('email capture component is missing')
if (/purchasing is not live|Design preview/i.test(dossier)) blockers.push('payment provider and live fulfillment are not activated')
const sitePages = fs.readFileSync(path.join(root, 'src', 'data', 'site-pages.ts'), 'utf8')
if (/production privacy policy is pending|Binding purchase terms are not yet available|Refund terms have not been finalized/i.test(sitePages)) blockers.push('privacy, terms, and refund disclosures are still preview-only')

const founderPage = fs.readFileSync(path.join(root, 'src', 'data', 'site-pages.ts'), 'utf8')
if (!/Laurent|founder/i.test(founderPage)) blockers.push('founder origin story is not present in published site data')

const checkReport = {
  categories: rows.length,
  declared: declared.length,
  noQualifyingPick: rows.filter((row) => String(row.Status || '').trim().toUpperCase() === 'EMPTY').length,
  unresolved: unresolved.length,
  blockers,
  warnings,
}

console.log(JSON.stringify(checkReport, null, 2))
if (blockers.length) process.exitCode = 1
