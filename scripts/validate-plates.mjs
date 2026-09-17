import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import Papa from 'papaparse'

const scriptDirectory = path.dirname(fileURLToPath(import.meta.url))
const repoRoot = path.resolve(scriptDirectory, '..')
const csvPath = path.join(repoRoot, 'public', 'platonic_ideal.csv')
const { productPlates } = await import(new URL('../src/data/product-plates.ts', import.meta.url))

const csv = fs.readFileSync(csvPath, 'utf8')
const parsed = Papa.parse(csv, { header: true, skipEmptyLines: true })
const errors = parsed.errors.map((error) => `CSV row ${error.row ?? '?'}: ${error.message}`)
const declared = parsed.data
  .filter((row) => String(row.Status || '').trim().toUpperCase() === 'DECLARED')
  .map((row) => `PI-${String(row.Number || '').trim().padStart(3, '0')}`)
const declaredSet = new Set(declared)
const seen = new Set()

if (!Array.isArray(productPlates)) {
  errors.push('Product plate manifest must export an array named productPlates')
} else {
  for (const plate of productPlates) {
    const label = plate.productId || plate.id || 'Unknown plate'
    const required = ['id', 'productId', 'role', 'kind', 'path', 'width', 'height', 'alt', 'caption', 'credit', 'license', 'exactness', 'capturedOrRetrievedAt', 'verifiedAt', 'status']
    for (const field of required) {
      if (!plate[field]) errors.push(`${label}: missing required field ${field}`)
    }

    if (!Number.isInteger(plate.width) || plate.width <= 0) errors.push(`${label}: width must be a positive integer`)
    if (!Number.isInteger(plate.height) || plate.height <= 0) errors.push(`${label}: height must be a positive integer`)

    if (seen.has(plate.productId)) errors.push(`Duplicate product plate: ${plate.productId}`)
    seen.add(plate.productId)

    if (!declaredSet.has(plate.productId)) errors.push(`${label}: plate is not attached to a current DECLARED entry`)
    if (plate.role !== 'hero') errors.push(`${label}: public plate role must be hero`)
    if (plate.kind !== 'editorial-interpretation') errors.push(`${label}: public plate kind must be editorial-interpretation`)
    if (plate.exactness !== 'representative') errors.push(`${label}: public plate exactness must be representative`)
    if (plate.status !== 'approved') errors.push(`${label}: only approved plates may enter the public manifest`)
    if (!String(plate.caption || '').toLowerCase().includes('not product photography')) {
      errors.push(`${label}: caption must say the plate is not product photography`)
    }
    if (!String(plate.credit || '').toLowerCase().includes('openai image generation')) {
      errors.push(`${label}: credit must identify OpenAI image generation`)
    }

    const assetPath = String(plate.path || '')
    if (!assetPath.startsWith('images/products/')) errors.push(`${label}: plate path must be a local product asset`)
    if (/^https?:\/\//i.test(assetPath) || assetPath.includes('..')) errors.push(`${label}: plate path must not be remote or traverse directories`)
    if (assetPath && !fs.existsSync(path.join(repoRoot, 'public', assetPath))) {
      errors.push(`${label}: local plate asset is missing at public/${assetPath}`)
    }
  }
}

if (seen.size > declaredSet.size) {
  errors.push(`Plate manifest contains more products than the ${declaredSet.size} current DECLARED entries`)
}

const plateCount = Array.isArray(productPlates) ? productPlates.length : 0
console.log(`Plates: ${plateCount} approved local interpretive plates · ${Math.max(0, declaredSet.size - plateCount)} declared entries using glyph fallback`)

if (errors.length) {
  errors.forEach((error) => console.error(`ERROR ${error}`))
  process.exit(1)
}

console.log('Plate-only image validation passed.')
