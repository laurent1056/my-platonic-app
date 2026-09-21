import test from 'node:test'
import assert from 'node:assert/strict'
import { readFile, readdir } from 'node:fs/promises'
import { existsSync } from 'node:fs'
import path from 'node:path'

const distRoot = path.resolve('dist')
const root = existsSync(path.join(distRoot, 'client')) ? path.join(distRoot, 'client') : distRoot
async function html(route) { return readFile(path.join(root, route ? `${route}/index.html` : 'index.html'), 'utf8') }
async function htmlFiles(dir) {
  const entries = await readdir(dir, { withFileTypes: true })
  const files = await Promise.all(entries.map(entry => entry.isDirectory() ? htmlFiles(path.join(dir, entry.name)) : entry.name.endsWith('.html') ? [path.join(dir, entry.name)] : []))
  return files.flat()
}

test('every built page offers the same dossier, including existing editorial routes', async () => {
  for (const file of await htmlFiles(root)) {
    const content = await readFile(file, 'utf8')
    assert.match(content, /class="button nav-offer" href="\/dossier\/"/, path.relative(root, file))
  }
})

test('all requested page families have navigable destinations', async () => {
  const routes = ['register', 'collections/kitchen-cooking', 'dossier', 'search', 'cart', 'checkout', 'order-confirmation', 'account/login', 'account/register', 'account/password-reset', 'account', 'account/orders', 'account/orders/preview', 'account/addresses', 'account/payment-methods', 'account/wishlist', 'campaign', 'journal', 'journal/the-value-of-no', 'about', 'contact', 'help', 'shipping-returns', 'privacy', 'terms', 'store-locator', 'brands', 'gift-card', 'size-guide', 'compare', 'account/subscriptions', 'page-directory']
  for (const route of routes) assert.match(await html(route), /<main id="main">/, route)
  assert.match(await readFile(path.join(root, '404.html'), 'utf8'), /Page not found/)
})

test('checkout and account previews are noindex and do not offer editable credential or payment inputs', async () => {
  for (const route of ['cart', 'checkout', 'order-confirmation', 'account', 'account/login', 'account/register', 'account/password-reset', 'account/orders', 'account/payment-methods']) {
    const content = await html(route)
    assert.match(content, /name="robots" content="noindex,follow"/, route)
    for (const [input] of content.matchAll(/<input\b[^>]*>/g)) assert.match(input, /\bdisabled\b/, `${route}: ${input}`)
  }
  assert.match(await html('checkout'), /Complete preview · No charge/)
  assert.match(await html('order-confirmation'), /No payment was taken/)
})

test('Stripe confirmation, download, and webhook handlers are emitted as server routes', async () => {
  const entry = await readFile(path.resolve('.vercel/output/_functions/entry.mjs'), 'utf8')
  for (const route of ['src/pages/purchase/success.astro', 'src/pages/api/dossier/download.ts', 'src/pages/api/stripe/webhook.ts']) {
    assert.match(entry, new RegExp(route.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')), route)
  }
})

test('category verdicts do not become commercial cart items', async () => {
  const dir = path.join(root, 'category')
  for (const file of await htmlFiles(dir)) {
    const content = await readFile(file, 'utf8')
    assert.ok(!/<button\b[^>]*\bdata-add-dossier\b/.test(content), path.relative(root, file))
    assert.match(content, /class="dossier-offer offer-compact"/, path.relative(root, file))
  }
  assert.match(await html('dossier'), /48 declared recommendations/)
  assert.match(await html('dossier'), /Buy the declared edition|Stripe checkout is not configured/)
})

test('test-mode Stripe links never render as live purchase CTAs', async () => {
  // Regression: ISSUE-003 — a Stripe test-mode URL must not render as a live CTA.
  // Found by /qa on 2026-09-21
  // Report: .gstack/qa-reports/qa-report-platonicidealguide-com-2026-09-21.md
  const source = await readFile(path.resolve('src/lib/payment-link.ts'), 'utf8')
  assert.match(source, /!link\.includes\('buy\.stripe\.com\/test_'\)/)
  assert.doesNotMatch(await html('dossier'), /href="https:\/\/buy\.stripe\.com\/test_/)
})

test('catalog retains ownership and evidence controls, including empty verdicts', async () => {
  const content = await html('register')
  for (const id of ['catalog-query', 'catalog-domain', 'catalog-verdict', 'catalog-mechanism', 'catalog-sort', 'catalog-empty']) assert.ok(content.includes(`id="${id}"`), id)
  assert.match(content, /value="confidence"/)
  assert.match(content, /data-verdict="EMPTY"/)
  assert.doesNotMatch(content, /\b(?:CANDIDATE|SPLIT_REQUIRED|CONDITIONAL|CONSUMABLE)\b/)
})

test('preview and transaction routes are excluded from the sitemap', async () => {
  const sitemap = await readFile(path.join(root, 'sitemap-0.xml'), 'utf8')
  assert.doesNotMatch(sitemap, /<loc>[^<]*\/(?:account(?:\/[^<]*)?|cart\/|checkout\/|order-confirmation\/|purchase(?:\/[^<]*)?|privacy\/|terms\/|page-directory\/)<\/loc>/)
  assert.match(sitemap, /\/dossier\/<\/loc>/)
})

test('public promise, founder story, measurement hooks, and dossier edition details are present', async () => {
  const home = await html('')
  const about = await html('about')
  const dossier = await html('dossier')
  const confirmation = await html('order-confirmation')
  const analytics = await readFile(path.resolve('src/scripts/analytics.ts'), 'utf8')
  assert.match(home, /names one product worth choosing|no product qualifies/i)
  assert.match(home, /data-email-capture/)
  assert.match(about, /Laurent Courtines/)
  assert.match(about, /I am Catholic/)
  assert.match(about, /cultural conflict/)
  assert.match(about, /cognitive load/)
  assert.match(about, /refrigerator/i)
  assert.match(home, /data-analytics-event="dossier_cta_click"/)
  assert.match(home, /A founder’s letter/)
  assert.match(dossier, /157-page tagged PDF/)
  assert.match(dossier, /48 declared recommendations/)
  assert.match(dossier, /images\/platonic-ideal-dossier-cover\.jpg/)
  assert.match(dossier, /data-dossier-edition=/)
  assert.match(dossier, /data-analytics-event="dossier_sample_open"/)
  assert.match(dossier, /data-analytics-download-type="sample"/)
  assert.match(analytics, /begin_checkout/)
  assert.match(analytics, /view_item/)
  assert.match(analytics, /dossier_download/)
  assert.match(analytics, /trial_download/)
  assert.match(confirmation, /Download sandbox file/)
  assert.match(confirmation, /No payment was taken/)
})
