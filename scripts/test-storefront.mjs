import test from 'node:test'
import assert from 'node:assert/strict'
import { readFile, readdir } from 'node:fs/promises'
import path from 'node:path'

const root = path.resolve('dist')
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

test('category verdicts do not become commercial cart items', async () => {
  const dir = path.join(root, 'category')
  for (const file of await htmlFiles(dir)) {
    const content = await readFile(file, 'utf8')
    assert.ok(!/<button\b[^>]*\bdata-add-dossier\b/.test(content), path.relative(root, file))
    assert.match(content, /class="dossier-offer offer-compact"/, path.relative(root, file))
  }
  assert.match(await html('dossier'), /data-add-dossier/)
})

test('catalog retains ownership and evidence controls, including empty verdicts', async () => {
  const content = await html('register')
  for (const id of ['catalog-query', 'catalog-domain', 'catalog-verdict', 'catalog-mechanism', 'catalog-sort', 'catalog-empty']) assert.ok(content.includes(`id="${id}"`), id)
  assert.match(content, /value="confidence"/)
  assert.match(content, /data-verdict="EMPTY"/)
})

test('preview routes are excluded from the sitemap', async () => {
  const sitemap = await readFile(path.join(root, 'sitemap-0.xml'), 'utf8')
  assert.doesNotMatch(sitemap, /<loc>[^<]*\/(?:account(?:\/[^<]*)?|cart\/|checkout\/|order-confirmation\/|privacy\/|terms\/|page-directory\/)<\/loc>/)
  assert.match(sitemap, /\/dossier\/<\/loc>/)
})
