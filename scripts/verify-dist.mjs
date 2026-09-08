import { access, readdir, readFile } from 'node:fs/promises'
import path from 'node:path'

const dist = path.resolve('dist')
const productionOrigin = 'https://my-platonic-app.vercel.app'
const forbiddenFragments = [
  'https://laurent1056.github.io',
  '/my-platonic-app/',
]
const requiredFiles = [
  'index.html',
  '404.html',
  'methodology/index.html',
  'category/frying-pan/index.html',
  'category/refrigerator/index.html',
  'category/task-chair/index.html',
  'favicon.svg',
  'images/plato-silanion-berlin.webp',
  'robots.txt',
  'sitemap-index.xml',
]

const errors = []

async function exists(file) {
  try {
    await access(file)
    return true
  } catch {
    return false
  }
}

async function walk(directory) {
  const entries = await readdir(directory, { withFileTypes: true })
  const files = []

  for (const entry of entries) {
    const absolute = path.join(directory, entry.name)
    if (entry.isDirectory()) files.push(...await walk(absolute))
    else files.push(absolute)
  }

  return files
}

function relative(file) {
  return path.relative(dist, file)
}

function candidateForUrl(value) {
  const url = new URL(value, productionOrigin)
  const pathname = decodeURIComponent(url.pathname)

  if (pathname === '/') return path.join(dist, 'index.html')
  if (pathname.startsWith('/api/')) return null

  const localPath = pathname.replace(/^\//, '')
  if (pathname.endsWith('/')) return path.join(dist, localPath, 'index.html')
  return path.join(dist, localPath)
}

for (const required of requiredFiles) {
  if (!await exists(path.join(dist, required))) {
    errors.push(`Missing required build artifact: ${required}`)
  }
}

const categoryDirectory = path.join(dist, 'category')
if (await exists(categoryDirectory)) {
  const categoryEntries = (await readdir(categoryDirectory, { withFileTypes: true }))
    .filter((entry) => entry.isDirectory())
  if (categoryEntries.length !== 68) {
    errors.push(`Expected 68 category routes; found ${categoryEntries.length}`)
  }
}

if (await exists(path.join(dist, 'oracle', 'index.html'))) {
  errors.push('The private Oracle was emitted as a public route')
}

const files = await walk(dist)
const htmlFiles = files.filter((file) => file.endsWith('.html'))

for (const file of htmlFiles) {
  const content = await readFile(file, 'utf8')
  const label = relative(file)

  for (const fragment of forbiddenFragments) {
    if (content.includes(fragment)) {
      errors.push(`${label} contains retired deployment fragment: ${fragment}`)
    }
  }

  const canonical = content.match(/<link rel="canonical" href="([^"]+)"/i)?.[1]
  if (!canonical?.startsWith(productionOrigin)) {
    errors.push(`${label} has an invalid canonical URL: ${canonical || 'missing'}`)
  }

  const references = content.matchAll(/(?:href|src)="([^"]+)"/gi)
  for (const [, value] of references) {
    if (!value.startsWith('/') || value.startsWith('//')) continue

    const candidate = candidateForUrl(value)
    if (candidate && !await exists(candidate)) {
      errors.push(`${label} references missing internal artifact: ${value}`)
    }
  }
}

for (const file of ['robots.txt', 'sitemap-index.xml']) {
  const absolute = path.join(dist, file)
  if (!await exists(absolute)) continue

  const content = await readFile(absolute, 'utf8')
  for (const fragment of forbiddenFragments) {
    if (content.includes(fragment)) {
      errors.push(`${file} contains retired deployment fragment: ${fragment}`)
    }
  }
  if (!content.includes(productionOrigin)) {
    errors.push(`${file} does not reference the production origin`)
  }
}

if (errors.length) {
  console.error('Vercel build verification failed:')
  for (const error of errors) console.error(`- ${error}`)
  process.exit(1)
}

console.log(`Verified ${htmlFiles.length} HTML files, 68 category routes, root-relative assets, and Vercel canonical URLs.`)
