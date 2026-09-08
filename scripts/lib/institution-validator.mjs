import fs from 'node:fs'
import { readdir, readFile } from 'node:fs/promises'
import path from 'node:path'
import { createHash } from 'node:crypto'
import { fileURLToPath } from 'node:url'
import Ajv from 'ajv'

const here = path.dirname(fileURLToPath(import.meta.url))
export const repoRoot = path.resolve(here, '../..')

const schemaFiles = {
  constitution: 'constitution.schema.json',
  evidence: 'evidence.schema.json',
  case: 'case.schema.json',
  ruling: 'ruling.schema.json',
  challenge: 'challenge.schema.json',
}

const terminalStatuses = new Set(['DECLARED', 'EMPTY'])
const primarySourceRoles = new Set(['PRIMARY_TECHNICAL', 'PRIMARY_SERVICE'])

function makeError({ code, path: errorPath, id, rule, message, fix }) {
  return { code, path: errorPath, ...(id ? { id } : {}), rule, message, fix }
}

function schemaErrors(validate, label, id) {
  return (validate.errors || []).map((error) => makeError({
    code: 'C-SCHEMA-001',
    path: `${label}${error.instancePath || '/'}`,
    id,
    rule: 'JSON Schema contract',
    message: `${error.message}${error.params?.missingProperty ? `: ${error.params.missingProperty}` : ''}`,
    fix: 'Update the object to match the referenced schema before retrying.',
  }))
}

function uniqueIds(items, label, idKey = 'id') {
  const seen = new Map()
  const errors = []

  for (const item of items) {
    const id = item?.[idKey]
    if (!id) continue
    if (seen.has(id)) {
      errors.push(makeError({
        code: 'C-ID-001',
        path: `${label}.${idKey}`,
        id,
        rule: 'permanent identifiers',
        message: `duplicate identifier ${id}; first seen at ${seen.get(id)}`,
        fix: 'Give each record a unique permanent identifier; identifiers are never reused.',
      }))
    } else {
      seen.set(id, `${label}[${items.indexOf(item)}]`)
    }
  }

  return errors
}

function setEqual(actual, expected) {
  if (actual.size !== expected.size) return false
  for (const item of actual) if (!expected.has(item)) return false
  return true
}

function requiredRuleSet(items, expectedIds, label, id, ruleName) {
  const errors = []
  const actual = new Set(items.map((item) => item.id))
  const expected = new Set(expectedIds)

  for (const missing of expected) {
    if (!actual.has(missing)) {
      errors.push(makeError({
        code: 'C-RULE-001',
        path: label,
        id,
        rule: ruleName,
        message: `missing required ${missing} finding`,
        fix: `Add one ${missing} finding before using terminal status.`,
      }))
    }
  }

  for (const unexpected of actual) {
    if (!expected.has(unexpected)) {
      errors.push(makeError({
        code: 'C-RULE-002',
        path: label,
        id,
        rule: ruleName,
        message: `unknown rule identifier ${unexpected}`,
        fix: 'Use only identifiers from constitution.v1.json.',
      }))
    }
  }

  if (actual.size !== items.length) {
    errors.push(makeError({
      code: 'C-RULE-003',
      path: label,
      id,
      rule: ruleName,
      message: 'rule findings contain duplicate identifiers',
      fix: 'Keep one finding per Constitution gate or hard disqualifier.',
    }))
  }

  return errors
}

function collectEvidenceRefs(caseFile) {
  const refs = [
    ...(caseFile.evidenceIds || []),
    ...(caseFile.evidenceReceipt?.evidenceIds || []),
    ...(caseFile.counterCase?.evidenceIds || []),
  ]

  for (const gate of caseFile.gates || []) refs.push(...(gate.evidenceIds || []))
  for (const disqualifier of caseFile.hardDisqualifiers || []) refs.push(...(disqualifier.evidenceIds || []))

  return [...new Set(refs)]
}

function validateEvidenceReferences(caseFile, evidenceById, errors) {
  for (const evidenceId of collectEvidenceRefs(caseFile)) {
    if (!evidenceById.has(evidenceId)) {
      errors.push(makeError({
        code: 'C-REF-001',
        path: `cases/${caseFile.id}.json`,
        id: caseFile.id,
        rule: 'evidence references',
        message: `references missing evidence item ${evidenceId}`,
        fix: 'Add the evidence item to institution/evidence.json or remove the reference.',
      }))
    }
  }
}

function validateTerminalCase(caseFile, profile, evidenceById, errors) {
  const casePath = `cases/${caseFile.id}.json`
  const id = caseFile.id

  if (caseFile.constitutionVersion !== profile.version) {
    errors.push(makeError({
      code: 'C-TERM-001',
      path: `${casePath}.constitutionVersion`,
      id,
      rule: 'constitution pinning',
      message: `terminal case is pinned to ${caseFile.constitutionVersion}, not active ${profile.version}`,
      fix: 'Pin the case to the active Constitution version and re-review its findings.',
    }))
  }

  const subject = caseFile.subject || {}
  const hasSubject = [subject.manufacturer, subject.model, subject.modelIdentifier]
    .some((value) => String(value || '').trim())

  if (caseFile.status === 'DECLARED') {
    if (!subject.manufacturer?.trim() || !subject.model?.trim() || !subject.modelIdentifier?.trim()) {
      errors.push(makeError({
        code: 'C-TERM-002',
        path: `${casePath}.subject`,
        id,
        rule: 'exact model identity',
        message: 'DECLARED requires one exact manufacturer, model, and model identifier',
        fix: 'Name one identifiable model or keep the case nonterminal.',
      }))
    }

    errors.push(...requiredRuleSet(
      caseFile.gates || [],
      profile.admissionGates.map((gate) => gate.id),
      `${casePath}.gates`,
      id,
      'five admission gates',
    ))

    for (const gate of caseFile.gates || []) {
      if (gate.status !== 'PASS') {
        errors.push(makeError({
          code: 'C-TERM-003',
          path: `${casePath}.gates.${gate.id}.status`,
          id,
          rule: 'five admission gates',
          message: `${gate.id} is ${gate.status}; every gate must be PASS`,
          fix: 'Resolve the gate with evidence or keep the case nonterminal.',
        }))
      }
    }

    errors.push(...requiredRuleSet(
      caseFile.hardDisqualifiers || [],
      profile.hardDisqualifiers.map((disqualifier) => disqualifier.id),
      `${casePath}.hardDisqualifiers`,
      id,
      'hard disqualifiers',
    ))

    for (const disqualifier of caseFile.hardDisqualifiers || []) {
      if (disqualifier.status !== 'ABSENT') {
        errors.push(makeError({
          code: 'C-TERM-004',
          path: `${casePath}.hardDisqualifiers.${disqualifier.id}.status`,
          id,
          rule: 'hard disqualifiers',
          message: `${disqualifier.id} is ${disqualifier.status}; terminal DECLARED requires ABSENT`,
          fix: 'Resolve the disqualifier or keep the case nonterminal.',
        }))
      }
    }
  } else if (hasSubject) {
    errors.push(makeError({
      code: 'C-TERM-005',
      path: `${casePath}.subject`,
      id,
      rule: 'EMPTY terminal shape',
      message: 'EMPTY must not name a winning product',
      fix: 'Remove the subject or use a nonterminal status while a candidate is being evaluated.',
    }))
  }

  if (!caseFile.evidenceIds?.length) {
    errors.push(makeError({
      code: 'C-TERM-006',
      path: `${casePath}.evidenceIds`,
      id,
      rule: 'evidence floor',
      message: 'terminal status requires an evidence packet',
      fix: 'Attach at least three verified evidence items from independent classes.',
    }))
  }

  const packet = (caseFile.evidenceIds || [])
    .map((evidenceId) => evidenceById.get(evidenceId))
    .filter(Boolean)
  const verified = packet.filter((item) => item.verificationStatus === 'VERIFIED')
  const classes = new Set(verified.map((item) => item.evidenceClass))
  const independenceGroups = new Set(verified.map((item) => item.independenceGroup))
  const hasPrimary = verified.some((item) => primarySourceRoles.has(item.sourceRole))
  const hasIndependent = verified.some((item) => item.independence === 'INDEPENDENT')
  const requirements = profile.evidenceRequirements

  if (verified.length < requirements.minimumItems || classes.size < requirements.minimumIndependentClasses || independenceGroups.size < requirements.minimumIndependentClasses) {
    errors.push(makeError({
      code: 'C-TERM-007',
      path: `${casePath}.evidenceIds`,
      id,
      rule: 'evidence floor',
      message: `terminal status requires >=${requirements.minimumItems} verified items from >=${requirements.minimumIndependentClasses} independent evidence classes/groups; found ${verified.length} items, ${classes.size} classes, ${independenceGroups.size} groups`,
      fix: 'Add verified evidence across independent classes and source groups.',
    }))
  }

  if (requirements.requiresPrimaryTechnicalOrService && !hasPrimary) {
    errors.push(makeError({
      code: 'C-TERM-008',
      path: `${casePath}.evidenceIds`,
      id,
      rule: 'primary technical or service evidence',
      message: 'terminal status requires primary technical or service evidence',
      fix: 'Attach a verified technical specification, service manual, or equivalent primary record.',
    }))
  }

  if (requirements.requiresIndependentSource && !hasIndependent) {
    errors.push(makeError({
      code: 'C-TERM-009',
      path: `${casePath}.evidenceIds`,
      id,
      rule: 'independent evidence',
      message: 'terminal status requires at least one verified independent source',
      fix: 'Attach a source independent of the manufacturer, seller, and financially interested parties.',
    }))
  }

  if (caseFile.evidenceGaps?.length) {
    errors.push(makeError({
      code: 'C-TERM-010',
      path: `${casePath}.evidenceGaps`,
      id,
      rule: 'material evidence gaps',
      message: 'terminal status cannot retain material evidence gaps',
      fix: 'Resolve every material gap or keep the case in a nonterminal state.',
    }))
  }

  if (!caseFile.failureModes?.length || !caseFile.maintenance?.trim() || !caseFile.repairEconomics?.trim()) {
    errors.push(makeError({
      code: 'C-TERM-011',
      path: casePath,
      id,
      rule: 'failure and permanence record',
      message: 'terminal status requires failure modes, maintenance, and repair economics',
      fix: 'Complete the permanence record before issuing the ruling.',
    }))
  }

  if (!caseFile.counterCase?.claim?.trim() || !caseFile.counterCase?.disposition?.trim()) {
    errors.push(makeError({
      code: 'C-TERM-012',
      path: `${casePath}.counterCase`,
      id,
      rule: 'strongest counter-case',
      message: 'terminal status requires a counter-case and disposition',
      fix: 'Record the strongest credible objection and why it does or does not overturn the ruling.',
    }))
  }

  if (caseFile.status === 'EMPTY') {
    if (!caseFile.categorySearch?.protocol?.trim() || !caseFile.categorySearch?.candidateSet?.length) {
      errors.push(makeError({
        code: 'C-EMPTY-001',
        path: `${casePath}.categorySearch`,
        id,
        rule: 'category coverage',
        message: 'EMPTY requires a search protocol and credible candidate set',
        fix: 'Record how the market was searched and which serious candidates were examined.',
      }))
    }

    const hasFailure = (caseFile.gates || []).some((gate) => gate.status === 'FAIL')
      || (caseFile.hardDisqualifiers || []).some((disqualifier) => disqualifier.status === 'PRESENT')
    if (!hasFailure) {
      errors.push(makeError({
        code: 'C-EMPTY-002',
        path: `${casePath}.gates`,
        id,
        rule: 'structural failure reasoning',
        message: 'EMPTY requires at least one documented material gate failure or hard disqualifier',
        fix: 'Record the shared failure pattern or keep the category nonterminal.',
      }))
    }

    if (!caseFile.futureRequirement?.trim()) {
      errors.push(makeError({
        code: 'C-EMPTY-003',
        path: `${casePath}.futureRequirement`,
        id,
        rule: 'future qualifying requirement',
        message: 'EMPTY requires a stated condition a future product would have to meet',
        fix: 'Describe the serviceability, durability, or other requirement that would reopen the category.',
      }))
    }
  }

  if (caseFile.confidence < profile.terminalConfidenceMinimum) {
    errors.push(makeError({
      code: 'C-TERM-013',
      path: `${casePath}.confidence`,
      id,
      rule: 'confidence floor',
      message: `terminal status requires confidence >=${profile.terminalConfidenceMinimum}/5`,
      fix: 'Increase evidence and verification or keep the case nonterminal.',
    }))
  }

  for (const requiredField of ['adjudicator', 'decisionDate', 'evidenceReceipt']) {
    if (!caseFile[requiredField]) {
      errors.push(makeError({
        code: 'C-TERM-014',
        path: `${casePath}.${requiredField}`,
        id,
        rule: 'terminal record',
        message: `terminal status requires ${requiredField}`,
        fix: 'Complete the adjudication record before issuing the ruling.',
      }))
    }
  }

  if (caseFile.evidenceReceipt && !setEqual(new Set(caseFile.evidenceReceipt.evidenceIds || []), new Set(caseFile.evidenceIds || []))) {
    errors.push(makeError({
      code: 'C-TERM-015',
      path: `${casePath}.evidenceReceipt.evidenceIds`,
      id,
      rule: 'evidence receipt completeness',
      message: 'public evidence receipt must match the case evidence packet',
      fix: 'Use the same evidence IDs in the case packet and public receipt.',
    }))
  }
}

function validateRulings({ rulings, casesById, evidenceById, profile, errors }) {
  const rulingIds = new Set()
  for (const event of rulings.events || []) {
    if (rulingIds.has(event.rulingId)) {
      errors.push(makeError({
        code: 'C-LEDGER-001',
        path: 'institution/rulings.json.events',
        id: event.id,
        rule: 'ruling ledger consistency',
        message: `ruling ${event.rulingId} has more than one current event in the founding ledger`,
        fix: 'Append historical events with an explicit event type and ensure only one current projection is used.',
      }))
    }
    rulingIds.add(event.rulingId)

    const caseFile = casesById.get(event.caseId)
    if (!caseFile) {
      errors.push(makeError({
        code: 'C-REF-002',
        path: `institution/rulings.json.events.${event.id}.caseId`,
        id: event.id,
        rule: 'ruling case reference',
        message: `references missing case ${event.caseId}`,
        fix: 'Add the case or remove the ruling event.',
      }))
    } else if (caseFile.status !== event.verdict) {
      errors.push(makeError({
        code: 'C-LEDGER-002',
        path: `institution/rulings.json.events.${event.id}.verdict`,
        id: event.id,
        rule: 'ruling/case consistency',
        message: `event verdict ${event.verdict} does not match case status ${caseFile.status}`,
        fix: 'Reference a terminal case with the same verdict or keep the event unpublished.',
      }))
    }

    if (event.constitutionVersion !== profile.version) {
      errors.push(makeError({
        code: 'C-LEDGER-003',
        path: `institution/rulings.json.events.${event.id}.constitutionVersion`,
        id: event.id,
        rule: 'ruling Constitution pinning',
        message: `event is pinned to ${event.constitutionVersion}, not active ${profile.version}`,
        fix: 'Use the active Constitution version for new events.',
      }))
    }

    for (const evidenceId of event.evidenceIds || []) {
      if (!evidenceById.has(evidenceId)) {
        errors.push(makeError({
          code: 'C-REF-003',
          path: `institution/rulings.json.events.${event.id}.evidenceIds`,
          id: event.id,
          rule: 'ruling evidence references',
          message: `references missing evidence item ${evidenceId}`,
          fix: 'Add the evidence item or remove the reference.',
        }))
      }
    }
  }
}

function validateChallenges({ challenges, rulingIds, casesById, evidenceById, errors }) {
  for (const challenge of challenges.challenges || []) {
    if (!rulingIds.has(challenge.rulingId)) {
      errors.push(makeError({
        code: 'C-REF-004',
        path: `institution/challenges.json.challenges.${challenge.id}.rulingId`,
        id: challenge.id,
        rule: 'challenge ruling reference',
        message: `references missing ruling ${challenge.rulingId}`,
        fix: 'Challenge an existing ruling or keep the challenge out of the docket.',
      }))
    }
    if (!casesById.has(challenge.caseId)) {
      errors.push(makeError({
        code: 'C-REF-005',
        path: `institution/challenges.json.challenges.${challenge.id}.caseId`,
        id: challenge.id,
        rule: 'challenge case reference',
        message: `references missing case ${challenge.caseId}`,
        fix: 'Reference the case attached to the challenged ruling.',
      }))
    }
    if (!challenge.evidenceIds?.length) {
      errors.push(makeError({
        code: 'C-CHALLENGE-001',
        path: `institution/challenges.json.challenges.${challenge.id}.evidenceIds`,
        id: challenge.id,
        rule: 'evidence-based challenges',
        message: 'challenge requires at least one evidence reference',
        fix: 'Attach verifiable evidence or do not submit the challenge.',
      }))
    }
    for (const evidenceId of challenge.evidenceIds || []) {
      if (!evidenceById.has(evidenceId)) {
        errors.push(makeError({
          code: 'C-REF-006',
          path: `institution/challenges.json.challenges.${challenge.id}.evidenceIds`,
          id: challenge.id,
          rule: 'challenge evidence references',
          message: `references missing evidence item ${evidenceId}`,
          fix: 'Add the evidence item or remove the reference.',
        }))
      }
    }
  }
}

export function validateInstitutionData({
  profile,
  constitutionText,
  evidenceStore,
  cases,
  rulings,
  challenges,
  schemasDir = path.join(repoRoot, 'schemas'),
}) {
  const errors = []
  const warnings = []
  const ajv = new Ajv({ allErrors: true, strict: false })
  const schemas = {}

  for (const [key, filename] of Object.entries(schemaFiles)) {
    const schemaPath = path.join(schemasDir, filename)
    const schema = JSON.parse(fs.readFileSync(schemaPath, 'utf8'))
    schemas[key] = ajv.compile(schema)
  }

  const profileValid = schemas.constitution(profile)
  if (!profileValid) errors.push(...schemaErrors(schemas.constitution, 'constitution/constitution.v1.json'))

  for (const [label, object, validator] of [
    ['institution/evidence.json', evidenceStore, schemas.evidence],
    ['institution/rulings.json', rulings, schemas.ruling],
    ['institution/challenges.json', challenges, schemas.challenge],
  ]) {
    if (!validator(object)) errors.push(...schemaErrors(validator, label))
  }

  const caseFiles = Array.isArray(cases) ? cases : []
  for (const caseFile of caseFiles) {
    if (!schemas.case(caseFile)) errors.push(...schemaErrors(schemas.case, `cases/${caseFile.id || 'unknown'}.json`, caseFile.id))
  }

  if (profileValid && constitutionText !== undefined) {
    const digest = createHash('sha256').update(constitutionText).digest('hex')
    if (digest !== profile.sourceSha256) {
      errors.push(makeError({
        code: 'C-PROFILE-002',
        path: 'constitution/constitution.v1.json.sourceSha256',
        rule: 'Constitution source digest',
        message: `profile digest ${profile.sourceSha256} does not match Constitution.md digest ${digest}`,
        fix: 'If the text change is intentional, update the semantic version and changelog before replacing the digest.',
      }))
    }
  }

  if (!profileValid) {
    return { ok: false, errors, warnings, summary: null }
  }

  if (evidenceStore.constitutionVersion !== profile.version) {
    errors.push(makeError({
      code: 'C-PROFILE-003',
      path: 'institution/evidence.json.constitutionVersion',
      rule: 'ledger Constitution pinning',
      message: `evidence ledger is pinned to ${evidenceStore.constitutionVersion}, not ${profile.version}`,
      fix: 'Pin the ledger to the active Constitution version.',
    }))
  }
  if (rulings.constitutionVersion !== profile.version || challenges.constitutionVersion !== profile.version) {
    errors.push(makeError({
      code: 'C-PROFILE-004',
      path: 'institution/*.json.constitutionVersion',
      rule: 'ledger Constitution pinning',
      message: 'all canonical ledgers must be pinned to the active Constitution version',
      fix: 'Update the ledger version before validation.',
    }))
  }

  errors.push(...uniqueIds(evidenceStore.items || [], 'institution/evidence.json.items'))
  errors.push(...uniqueIds(caseFiles, 'cases'))
  errors.push(...uniqueIds(rulings.events || [], 'institution/rulings.json.events'))
  errors.push(...uniqueIds(challenges.challenges || [], 'institution/challenges.json.challenges'))

  const evidenceById = new Map((evidenceStore.items || []).map((item) => [item.id, item]))
  const casesById = new Map(caseFiles.map((caseFile) => [caseFile.id, caseFile]))
  const rulingIds = new Set((rulings.events || []).map((event) => event.rulingId))

  for (const caseFile of caseFiles) {
    validateEvidenceReferences(caseFile, evidenceById, errors)
    if (terminalStatuses.has(caseFile.status)) validateTerminalCase(caseFile, profile, evidenceById, errors)
  }

  validateRulings({ rulings, casesById, evidenceById, profile, errors })
  validateChallenges({ challenges, rulingIds, casesById, evidenceById, errors })

  const terminalCount = caseFiles.filter((caseFile) => terminalStatuses.has(caseFile.status)).length
  const draftCount = caseFiles.filter((caseFile) => !terminalStatuses.has(caseFile.status)).length
  const summary = {
    constitutionVersion: profile.version,
    evidence: evidenceStore.items?.length || 0,
    cases: caseFiles.length,
    terminalCases: terminalCount,
    nonterminalCases: draftCount,
    rulings: rulings.events?.length || 0,
    challenges: challenges.challenges?.length || 0,
  }

  return { ok: errors.length === 0, errors, warnings, summary }
}

async function readJson(file) {
  return JSON.parse(await readFile(file, 'utf8'))
}

async function readCaseFiles(root) {
  const directory = path.join(root, 'cases')
  const entries = await readdir(directory, { withFileTypes: true })
  const files = entries
    .filter((entry) => entry.isFile() && entry.name.endsWith('.json'))
    .sort((a, b) => a.name.localeCompare(b.name))

  return Promise.all(files.map((entry) => readJson(path.join(directory, entry.name))))
}

export async function loadInstitution(root = repoRoot) {
  const [profile, constitutionText, evidenceStore, cases, rulings, challenges] = await Promise.all([
    readJson(path.join(root, 'constitution/constitution.v1.json')),
    readFile(path.join(root, 'constitution/CONSTITUTION.md'), 'utf8'),
    readJson(path.join(root, 'institution/evidence.json')),
    readCaseFiles(root),
    readJson(path.join(root, 'institution/rulings.json')),
    readJson(path.join(root, 'institution/challenges.json')),
  ])

  return { profile, constitutionText, evidenceStore, cases, rulings, challenges }
}

export async function validateInstitution({ root = repoRoot } = {}) {
  const data = await loadInstitution(root)
  return validateInstitutionData({ ...data, schemasDir: path.join(root, 'schemas') })
}
