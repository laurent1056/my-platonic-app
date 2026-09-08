import { validateInstitution } from './lib/institution-validator.mjs'

const result = await validateInstitution()

if (result.summary) {
  const { constitutionVersion, evidence, cases, terminalCases, nonterminalCases, rulings, challenges } = result.summary
  console.log(`Institution: Constitution ${constitutionVersion} · ${evidence} evidence · ${cases} cases (${terminalCases} terminal / ${nonterminalCases} nonterminal) · ${rulings} ruling events · ${challenges} challenges`)
}

if (result.errors.length) {
  console.error(`Institution validation failed with ${result.errors.length} blocker${result.errors.length === 1 ? '' : 's'}:`)
  for (const error of result.errors) {
    console.error(`ERROR ${error.code} ${error.path}${error.id ? ` [${error.id}]` : ''}: ${error.message}`)
    console.error(`      Fix: ${error.fix}`)
  }
  if (process.argv.includes('--json')) console.error(JSON.stringify(result.errors, null, 2))
  process.exit(1)
}

console.log('Institution validation passed. No terminal ruling is emitted by this command.')
