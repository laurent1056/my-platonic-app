import fs from 'node:fs'
import path from 'node:path'
import Papa from 'papaparse'

const root = process.cwd()
const csvPath = path.join(root, 'public/platonic_ideal.csv')
const casesPath = path.join(root, 'cases')
const csv = fs.readFileSync(csvPath, 'utf8')
const { data, errors } = Papa.parse(csv, { header: true, skipEmptyLines: true })

if (errors.length) throw new Error(`Could not parse register: ${errors[0].message}`)

const terminal = new Set(['DECLARED', 'EMPTY'])
const slugify = (value) => value
  .normalize('NFKD')
  .replace(/[\u0300-\u036f]/g, '')
  .toLowerCase()
  .replace(/&/g, ' and ')
  .replace(/[^a-z0-9]+/g, '-')
  .replace(/^-|-$/g, '')

const clean = (value) => String(value ?? '').trim()
const splitFailureModes = (value) => clean(value)
  ? [{ mode: 'Register failure-mode record', severity: 'MEDIUM', remedy: clean(value) }]
  : []

const nonterminalRows = data.filter((row) => !terminal.has(clean(row.Status).toUpperCase()))
let created = 0

for (const row of nonterminalRows) {
  const number = Number(clean(row.Number))
  const id = `PI-C-${String(number).padStart(4, '0')}`
  const output = path.join(casesPath, `${id}.json`)
  if (fs.existsSync(output)) continue

  const status = clean(row.Status).toUpperCase()
  const category = clean(row.Category)
  const model = clean(row.Model)
  const formStatement = clean(row['Form Statement']) || clean(row['Form Definition']) || `${category} as a bounded product Form.`
  const disqualifiers = clean(row.Key_Disqualifiers) || clean(row['Key Disqualifiers'])
  const failureModes = clean(row['Failure Modes'])

  const caseFile = {
    id,
    category,
    slug: slugify(category),
    status,
    constitutionVersion: '1.1.0',
    form: {
      statement: formStatement,
      scope: `Imported from the 100-record register as a nonterminal ${status} research case. The ordinary use context, jurisdiction, and exact Form boundary remain part of adjudication.`,
      exclusions: disqualifiers ? [disqualifiers] : ['Incompatible sub-Forms not yet adjudicated']
    },
    subject: {
      manufacturer: '',
      model,
      modelIdentifier: '',
      productionLineage: 'Exact model identity and production continuity remain to be verified.'
    },
    gates: [],
    hardDisqualifiers: [],
    evidenceIds: [],
    evidenceGaps: [
      'Attach at least one primary technical or service source.',
      'Attach independent evidence of longevity, failure behavior, or repair economics.',
      'Record the strongest counter-case and the exact model or child Form boundary.'
    ],
    categorySearch: {
      protocol: 'Research disposition imported from the canonical register. The case must record the candidate set, search coverage, and why the chosen Form is coherent before terminal review.',
      candidateSet: [model || 'No exact subject named; Form or category split required']
    },
    failureModes: splitFailureModes(failureModes),
    maintenance: clean(row['Maintenance / Replacement Cycle']) || 'To be established from primary service evidence.',
    repairEconomics: 'Not yet established. Compare parts, labor, access, downtime, and rational replacement cost before terminal review.',
    counterCase: {
      claim: 'A serious alternative or incompatible sub-Form may answer the same broad category differently.',
      disposition: 'Counter-case not yet adjudicated; do not issue a terminal ruling until the strongest alternative is recorded and answered.'
    },
    futureRequirement: 'Complete the evidence packet, five-gate findings, hard-disqualifier review, and human adjudication before promotion to DECLARED or EMPTY.',
    confidence: Math.max(0, Math.min(5, Number(clean(row.Confidence)) || 0)),
    notes: `${clean(row.Notes)} Seeded from the 100-record migration as a formal nonterminal case; this file does not issue a public ruling.`.trim()
  }

  fs.writeFileSync(output, `${JSON.stringify(caseFile, null, 2)}\n`)
  created += 1
}

console.log(`Seeded ${created} nonterminal register case files; existing cases were preserved.`)
