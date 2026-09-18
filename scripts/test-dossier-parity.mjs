import test from 'node:test'
import assert from 'node:assert/strict'
import fs from 'node:fs/promises'
import path from 'node:path'
import Papa from 'papaparse'

const root = path.resolve('.')
const csvPath = path.join(root, 'public', 'platonic_ideal.csv')
const dossierPath = path.join(root, 'tmp', 'pdfs', 'delta-1940', 'platonic-ideal-dossier-declared-1940.html')
const distRoot = path.join(root, 'dist')

const csv = await fs.readFile(csvPath, 'utf8')
const { data: rows, errors } = Papa.parse(csv, { header: true, skipEmptyLines: true })
assert.equal(errors.length, 0, errors.map((error) => error.message).join('; '))
const clean = (value) => String(value ?? '').trim().replace(/\r\n/g, '\n')
const slugify = (value) => clean(value)
  .normalize('NFKD')
  .replace(/[\u0300-\u036f]/g, '')
  .toLowerCase()
  .replace(/&/g, ' and ')
  .replace(/[^a-z0-9]+/g, '-')
  .replace(/^-|-$/g, '')

function decodeHtml(value) {
  return value
    .replace(/&#x([0-9a-f]+);/gi, (_, hex) => String.fromCodePoint(Number.parseInt(hex, 16)))
    .replace(/&#([0-9]+);/g, (_, number) => String.fromCodePoint(Number(number)))
    .replace(/&quot;/g, '"')
    .replace(/&#39;|&apos;/g, "'")
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&nbsp;/g, ' ')
}

function compareText(value) {
  return decodeHtml(String(value ?? ''))
    .replace(/[’‘]/g, "'")
    .replace(/[“”]/g, '"')
    .replace(/[–—]/g, '-')
    .replace(/…/g, '...')
    .replace(/°/g, ' degrees ')
    .replace(/\s+/g, ' ')
    .trim()
    .toLocaleLowerCase()
}

function visibleText(html) {
  return compareText(html
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<[^>]+>/g, ' '))
}

function escapeRegex(value) {
  return String(value).replace(/[.*+?^${}()|[\\]\\\\]/g, '\\$&')
}

function dossierField(html, reference, field) {
  const pattern = new RegExp(`<section[^>]*data-case-reference="${escapeRegex(reference)}"[^>]*data-case-field="${escapeRegex(field)}"[^>]*>([\\s\\S]*?)<\\/section>`)
  const match = html.match(pattern)
  assert.ok(match, `missing dossier field ${reference}/${field}`)
  return visibleText(match[1])
}

const dossier = await fs.readFile(dossierPath, 'utf8')
const declared = rows.filter((row) => clean(row.Status).toUpperCase() === 'DECLARED')

test('the declared edition keeps its compact three-page chapter plan', () => {
  const reviewPages = (dossier.match(/<section class="review-page/g) || []).length
  const expected = 4 + declared.length * 3 + 4 + 3 + 2
  assert.equal(reviewPages, expected)
  assert.doesNotMatch(dossier, /declared-evidence-record/)
})

test('every declared chapter carries the full editorial and comparative case', async () => {
  assert.equal((dossier.match(/class="declared-editorial-analysis"/g) || []).length, declared.length)
  assert.equal((dossier.match(/class="declared-comparative-analysis"/g) || []).length, declared.length)

  for (const entry of declared) {
    const category = clean(entry.Category)
    const categoryHtml = await fs.readFile(path.join(distRoot, 'category', slugify(category), 'index.html'), 'utf8')
    const categoryText = visibleText(categoryHtml)
    const reasoning = compareText(entry.Core_Reasoning || entry['Core Reasoning'])
    const disqualifiers = compareText(entry.Key_Disqualifiers || entry['Key Disqualifiers'])
    const reference = `PI-${String(entry.Number).padStart(3, '0')}`
    const editorial = dossierField(dossier, reference, 'coreReasoning')
    const comparative = dossierField(dossier, reference, 'disqualifiers')

    assert.ok(reasoning, `${category} has editorial analysis in the register`)
    assert.ok(disqualifiers, `${category} has comparative analysis in the register`)
    assert.ok(editorial.includes(reasoning), `full ${category} editorial analysis is in the dossier`)
    assert.ok(comparative.includes(disqualifiers), `full ${category} comparative analysis is in the dossier`)
    assert.ok(categoryText.includes(reasoning), `public ${category} page carries the editorial analysis`)
    assert.ok(categoryText.includes(disqualifiers), `public ${category} page carries the comparative analysis`)
  }
})

test('Boots retains its exact-model and candidate evidence trail', () => {
  assert.match(dossier, /The Original Semi-Dress \(2332HC\)/)
  assert.match(dossier, /https:\/\/whitesboots\.com\/products\/the-original-semi-dress/)
  assert.match(dossier, /Hiking boots/i)
  assert.match(dossier, /EVA foam/i)
  assert.match(dossier, /Red Wing Iron Ranger/i)
})
