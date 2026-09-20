import { existsSync } from 'node:fs'
import { access, readdir, readFile } from 'node:fs/promises'
import path from 'node:path'
import Papa from 'papaparse'

const distRoot = path.resolve('dist')
const dist = existsSync(path.join(distRoot, 'client')) ? path.join(distRoot, 'client') : distRoot
const vercelConfigPath = path.resolve('vercel.json')
const productionOrigin = process.env.SITE_URL || 'https://www.platonicidealguide.com'
const registerPath = path.resolve('public/platonic_ideal.csv')
const forbiddenFragments = [
  'https://laurent1056.github.io',
  '/my-platonic-app/',
]
const requiredFiles = [
  'index.html',
  '404.html',
  'constitution/index.html',
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
const productionUrl = new URL(productionOrigin)
const register = Papa.parse(await readFile(registerPath, 'utf8'), { header: true, skipEmptyLines: true })
const expectedCategoryRoutes = register.data.length
if (register.errors.length) {
  errors.push(`Unable to parse canonical register: ${register.errors[0]?.message || 'unknown CSV error'}`)
}
const requiredRedirects = new Map([
  ['/my-platonic-app', '/'],
  ['/my-platonic-app/', '/'],
  ['/my-platonic-app/:path*', '/:path*'],
  ['/my-platonic-app/:path*/', '/:path*/'],
])

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
  if (pathname.startsWith('/api/') || pathname === '/purchase/success/') return null

  const localPath = pathname.replace(/^\//, '')
  if (pathname.endsWith('/')) return path.join(dist, localPath, 'index.html')
  return path.join(dist, localPath)
}

for (const required of requiredFiles) {
  if (!await exists(path.join(dist, required))) {
    errors.push(`Missing required build artifact: ${required}`)
  }
}

try {
  const vercelConfig = JSON.parse(await readFile(vercelConfigPath, 'utf8'))
  const redirects = Array.isArray(vercelConfig.redirects) ? vercelConfig.redirects : []

  for (const [source, destination] of requiredRedirects) {
    const redirect = redirects.find((entry) => entry.source === source)
    if (!redirect || redirect.destination !== destination || redirect.permanent !== true) {
      errors.push(`Missing permanent Vercel redirect: ${source} -> ${destination}`)
    }
  }
} catch (error) {
  errors.push(`Unable to validate vercel.json: ${error instanceof Error ? error.message : String(error)}`)
}

const categoryDirectory = path.join(dist, 'category')
if (await exists(categoryDirectory)) {
  const categoryEntries = (await readdir(categoryDirectory, { withFileTypes: true }))
    .filter((entry) => entry.isDirectory())
  if (categoryEntries.length !== expectedCategoryRoutes) {
    errors.push(`Expected ${expectedCategoryRoutes} category routes; found ${categoryEntries.length}`)
  }
}

if (await exists(path.join(dist, 'oracle', 'index.html'))) {
  errors.push('The private Oracle was emitted as a public route')
}

const files = await walk(dist)
const htmlFiles = files.filter((file) => file.endsWith('.html'))
const serverOutput = path.resolve('.vercel/output')
const serverFiles = await exists(serverOutput) ? await walk(serverOutput) : []
const credentialPatterns = [
  /sk_(?:test|live)_[A-Za-z0-9]+/,
  /whsec_[A-Za-z0-9]+/,
  /vercel_blob_rw_[A-Za-z0-9]+/,
  /re_[A-Za-z0-9]{20,}/,
]

for (const file of serverFiles.filter((candidate) => /\.(?:js|mjs|json|html|txt)$/.test(candidate))) {
  const content = await readFile(file, 'utf8')
  for (const pattern of credentialPatterns) {
    if (pattern.test(content)) {
      errors.push(`${path.relative(serverOutput, file)} contains a server credential-shaped value (${pattern})`)
    }
  }
}

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

  const title = content.match(/<title>([^<]+)<\/title>/i)?.[1]
  if (!title?.trim()) {
    errors.push(`${label} is missing a document title`)
  }

  const description = content.match(/<meta name="description" content="([^"]*)"/i)?.[1]
  if (!description?.trim()) {
    errors.push(`${label} is missing a meta description`)
  }

  const robots = content.match(/<meta name="robots" content="([^"]+)"/i)?.[1]
  if (!robots) {
    errors.push(`${label} is missing a robots directive`)
  }

  const isNoindex = /\bnoindex\b/i.test(robots || '')
  if (label === '404.html' && !isNoindex) {
    errors.push('404.html must be noindex')
  }

  if (!isNoindex) {
    const ogImage = content.match(/<meta property="og:image" content="([^"]+)"/i)?.[1]
    if (!ogImage) {
      errors.push(`${label} is missing an absolute og:image`)
    } else {
      try {
        const imageUrl = new URL(ogImage)
        if (imageUrl.origin !== productionUrl.origin) {
          errors.push(`${label} has an og:image outside the production origin: ${ogImage}`)
        }
      } catch {
        errors.push(`${label} has an invalid og:image URL: ${ogImage}`)
      }
    }

    const ogImageAlt = content.match(/<meta property="og:image:alt" content="([^"]+)"/i)?.[1]
    if (!ogImageAlt?.trim()) {
      errors.push(`${label} is missing og:image:alt`)
    }

    const twitterImage = content.match(/<meta name="twitter:image" content="([^"]+)"/i)?.[1]
    if (!twitterImage || twitterImage !== ogImage) {
      errors.push(`${label} has mismatched or missing Twitter image metadata`)
    }

    const structuredDataScripts = [...content.matchAll(/<script\b[^>]*type="application\/ld\+json"[^>]*>([\s\S]*?)<\/script>/gi)]
    const structuredDataTypes = new Set()
    if (!structuredDataScripts.length) {
      errors.push(`${label} is missing JSON-LD structured data`)
    }

    for (const [, rawJson] of structuredDataScripts) {
      try {
        const parsedJson = JSON.parse(rawJson)
        const nodes = Array.isArray(parsedJson?.['@graph']) ? parsedJson['@graph'] : [parsedJson]
        for (const node of nodes) {
          const types = Array.isArray(node?.['@type']) ? node['@type'] : [node?.['@type']]
          for (const type of types) if (type) structuredDataTypes.add(type)
        }
      } catch (error) {
        errors.push(`${label} contains invalid JSON-LD: ${error instanceof Error ? error.message : String(error)}`)
      }
    }

    for (const type of ['Organization', 'WebSite', 'WebPage']) {
      if (!structuredDataTypes.has(type)) errors.push(`${label} JSON-LD is missing ${type} data`)
    }
  }

  const references = content.matchAll(/(?:href|src)="([^"]+)"/gi)
  for (const [, value] of references) {
    if (!value.startsWith('/') || value.startsWith('//')) continue

    const candidate = candidateForUrl(value)
    if (candidate && !await exists(candidate)) {
      errors.push(`${label} references missing internal artifact: ${value}`)
    }
  }

  const imageReferences = content.matchAll(/<img\b[^>]*\bsrc="([^"]+)"/gi)
  for (const [, value] of imageReferences) {
    if (/^https?:\/\//i.test(value) || !value.startsWith('/images/')) {
      errors.push(`${label} contains a non-local public image source: ${value}`)
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

console.log(`Verified ${htmlFiles.length} HTML files, ${expectedCategoryRoutes} category routes, metadata, JSON-LD, root-relative assets, and Vercel canonical URLs.`)
