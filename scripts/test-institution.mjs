import assert from 'node:assert/strict'
import test from 'node:test'
import { loadInstitution, validateInstitution, validateInstitutionData } from './lib/institution-validator.mjs'

const base = await loadInstitution()

const evidence = (id, evidenceClass, sourceRole, independence, independenceGroup, commercialRelationship = 'NONE') => ({
  id,
  sourceUrl: `https://example.com/evidence/${id.toLowerCase()}`,
  title: `Evidence ${id}`,
  publisher: sourceRole === 'INDEPENDENT_TEST' ? 'Independent Test Lab' : 'Example Manufacturer',
  sourceRole,
  evidenceClass,
  claim: `Verified claim for ${id}.`,
  relationship: 'SUPPORTS',
  retrievedOn: '2026-09-08',
  verificationStatus: 'VERIFIED',
  independenceGroup,
  independence,
  commercialRelationship,
})

const validEvidence = [
  evidence('PI-E-000001', 'EV-01', 'PRIMARY_TECHNICAL', 'MANUFACTURER', 'manufacturer-docs', 'MANUFACTURER'),
  evidence('PI-E-000002', 'EV-02', 'PRIMARY_SERVICE', 'MANUFACTURER', 'service-docs', 'MANUFACTURER'),
  evidence('PI-E-000003', 'EV-04', 'INDEPENDENT_TEST', 'INDEPENDENT', 'independent-lab'),
]

const makeCase = (status = 'DECLARED', evidenceIds = validEvidence.map((item) => item.id)) => {
  const declared = status === 'DECLARED'
  const empty = status === 'EMPTY'
  return {
    id: 'PI-C-0001',
    category: 'Test Category',
    slug: 'test-category',
    status,
    constitutionVersion: base.profile.version,
    form: {
      statement: 'A stable test form.',
      scope: 'Ordinary test use.',
      exclusions: ['Incompatible sub-forms'],
    },
    subject: declared
      ? { manufacturer: 'Example', model: 'Model One', modelIdentifier: 'M1' }
      : { manufacturer: '', model: '', modelIdentifier: '' },
    gates: base.profile.admissionGates.map((gate, index) => ({
      id: gate.id,
      status: empty && index === 0 ? 'FAIL' : 'PASS',
      finding: `${gate.title} finding.`,
      evidenceIds: [validEvidence[index % validEvidence.length].id],
    })),
    hardDisqualifiers: base.profile.hardDisqualifiers.map((disqualifier) => ({
      id: disqualifier.id,
      status: 'ABSENT',
      finding: `${disqualifier.title} is absent.`,
      evidenceIds: [],
    })),
    evidenceIds,
    evidenceGaps: [],
    ...(empty
      ? {
          categorySearch: {
            protocol: 'Examined the serious candidates in the defined market.',
            candidateSet: ['Candidate A', 'Candidate B'],
          },
          futureRequirement: 'A future product must provide a repairable critical core.',
        }
      : {}),
    failureModes: [{ mode: 'Ordinary wear', severity: 'LOW', remedy: 'Replace the serviceable wear part.' }],
    maintenance: 'Routine maintenance is documented and practical.',
    repairEconomics: 'Repair remains rational relative to replacement.',
    counterCase: {
      claim: 'A credible alternative may have a marginal advantage.',
      disposition: 'It does not materially improve the Form for this category.',
    },
    confidence: 4,
    adjudicator: 'Test adjudicator',
    decisionDate: '2026-09-08',
    evidenceReceipt: {
      evidenceIds,
      facts: ['The evidence records the relevant construction and service facts.'],
      inferences: ['The facts support the terminal finding.'],
      gaps: [],
    },
  }
}

function dataWith(overrides = {}) {
  return {
    profile: structuredClone(base.profile),
    constitutionText: base.constitutionText,
    evidenceStore: structuredClone(base.evidenceStore),
    cases: structuredClone(base.cases),
    rulings: structuredClone(base.rulings),
    challenges: structuredClone(base.challenges),
    schemasDir: new URL('../schemas/', import.meta.url).pathname,
    ...overrides,
  }
}

function errorCodes(result) {
  return new Set(result.errors.map((error) => error.code))
}

test('canonical institution fixtures pass and retain a nonterminal Pocket Knife case', async () => {
  const result = await validateInstitution()
  assert.equal(result.ok, true, result.errors.map((error) => error.message).join('\n'))
  assert.equal(result.summary.cases, 1)
  assert.equal(result.summary.nonterminalCases, 1)
  assert.equal(result.summary.terminalCases, 0)
})

test('a draft case may have incomplete evidence and gates without becoming terminal', () => {
  const result = validateInstitutionData(dataWith({
    cases: [structuredClone(base.cases[0])],
  }))
  assert.equal(result.ok, true, result.errors.map((error) => error.message).join('\n'))
})

test('a complete DECLARED case passes terminal admissibility', () => {
  const result = validateInstitutionData(dataWith({
    evidenceStore: { constitutionVersion: base.profile.version, items: validEvidence },
    cases: [makeCase('DECLARED')],
  }))
  assert.equal(result.ok, true, result.errors.map((error) => error.message).join('\n'))
})

test('a complete EMPTY case passes category coverage and future-requirement checks', () => {
  const result = validateInstitutionData(dataWith({
    evidenceStore: { constitutionVersion: base.profile.version, items: validEvidence },
    cases: [makeCase('EMPTY')],
  }))
  assert.equal(result.ok, true, result.errors.map((error) => error.message).join('\n'))
})

test('terminal DECLARED requires an exact model', () => {
  const invalid = makeCase('DECLARED')
  invalid.subject.modelIdentifier = ''
  const result = validateInstitutionData(dataWith({
    evidenceStore: { constitutionVersion: base.profile.version, items: validEvidence },
    cases: [invalid],
  }))
  assert.equal(result.ok, false)
  assert.ok(errorCodes(result).has('C-TERM-002'))
})

test('terminal DECLARED rejects failed or unknown gates', () => {
  const invalid = makeCase('DECLARED')
  invalid.gates[2].status = 'UNKNOWN'
  const result = validateInstitutionData(dataWith({
    evidenceStore: { constitutionVersion: base.profile.version, items: validEvidence },
    cases: [invalid],
  }))
  assert.equal(result.ok, false)
  assert.ok(errorCodes(result).has('C-TERM-003'))
})

test('terminal DECLARED rejects an evidence packet below the independence floor', () => {
  const invalid = makeCase('DECLARED', ['PI-E-000001'])
  const result = validateInstitutionData(dataWith({
    evidenceStore: { constitutionVersion: base.profile.version, items: [validEvidence[0]] },
    cases: [invalid],
  }))
  assert.equal(result.ok, false)
  assert.ok(errorCodes(result).has('C-TERM-007'))
  assert.ok(errorCodes(result).has('C-TERM-009'))
})

test('duplicate evidence IDs are rejected', () => {
  const result = validateInstitutionData(dataWith({
    evidenceStore: { constitutionVersion: base.profile.version, items: [validEvidence[0], validEvidence[0]] },
  }))
  assert.equal(result.ok, false)
  assert.ok(errorCodes(result).has('C-ID-001'))
})

test('missing evidence references are rejected', () => {
  const invalid = structuredClone(base.cases[0])
  invalid.evidenceIds = ['PI-E-999999']
  const result = validateInstitutionData(dataWith({ cases: [invalid] }))
  assert.equal(result.ok, false)
  assert.ok(errorCodes(result).has('C-REF-001'))
})

test('ruling events must match the referenced case verdict', () => {
  const result = validateInstitutionData(dataWith({
    evidenceStore: { constitutionVersion: base.profile.version, items: validEvidence },
    cases: [makeCase('DECLARED')],
    rulings: {
      constitutionVersion: base.profile.version,
      events: [{
        id: 'PI-RE-000001',
        rulingId: 'PI-R-0001',
        caseId: 'PI-C-0001',
        eventType: 'ISSUED',
        verdict: 'EMPTY',
        constitutionVersion: base.profile.version,
        recordedOn: '2026-09-08',
        summary: 'Intentional mismatch fixture.',
        evidenceIds: validEvidence.map((item) => item.id),
      }],
    },
  }))
  assert.equal(result.ok, false)
  assert.ok(errorCodes(result).has('C-LEDGER-002'))
})

test('challenges must reference an existing ruling and evidence', () => {
  const result = validateInstitutionData(dataWith({
    challenges: {
      constitutionVersion: base.profile.version,
      challenges: [{
        id: 'PI-CH-000001',
        rulingId: 'PI-R-9999',
        caseId: 'PI-C-0001',
        status: 'SUBMITTED',
        groundType: 'MATERIAL_CLAIM',
        objection: 'A falsifiable objection.',
        evidenceIds: ['PI-E-999999'],
        submittedOn: '2026-09-08',
      }],
    },
  }))
  assert.equal(result.ok, false)
  assert.ok(errorCodes(result).has('C-REF-004'))
  assert.ok(errorCodes(result).has('C-REF-006'))
})

test('Constitution digest drift is a release blocker', () => {
  const result = validateInstitutionData(dataWith({
    constitutionText: `${base.constitutionText}\nUnexpected edit.`,
  }))
  assert.equal(result.ok, false)
  assert.ok(errorCodes(result).has('C-PROFILE-002'))
})
