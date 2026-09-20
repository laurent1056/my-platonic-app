type AnalyticsScalar = string | number | boolean
type AnalyticsItem = Record<string, AnalyticsScalar>
type AnalyticsValue = AnalyticsScalar | null | AnalyticsItem[]
type AnalyticsProperties = Record<string, AnalyticsValue>

type AnalyticsEventName =
  | 'page_view'
  | 'category_view'
  | 'verdict_interaction'
  | 'dossier_cta_click'
  | 'view_item'
  | 'select_item'
  | 'add_to_cart'
  | 'checkout_start'
  | 'begin_checkout'
  | 'purchase'
  | 'fulfillment'
  | 'dossier_sample_open'
  | 'dossier_download'
  | 'file_download'
  | 'preview_add_to_cart'
  | 'preview_checkout_start'
  | 'preview_purchase'
  | 'preview_fulfillment'
  | 'email_signup'
  | 'email_unsubscribe'

interface AnalyticsEvent {
  event: AnalyticsEventName
  occurredAt: string
  path: string
  properties: AnalyticsProperties
}

declare global {
  interface Window {
    dataLayer?: unknown[]
    gtag?: (...args: unknown[]) => void
  }
}

const eventKey = 'PI_ANALYTICS_PREVIEW_V1'
const emailKey = 'PI_EMAIL_PREVIEW_V1'

const ga4EventNames: Partial<Record<AnalyticsEventName, string>> = {
  dossier_cta_click: 'select_item',
  checkout_start: 'begin_checkout',
  begin_checkout: 'begin_checkout',
  fulfillment: 'dossier_download',
  dossier_sample_open: 'dossier_download',
}

function getPreviewValue(key: string): string | null {
  try {
    return window.localStorage.getItem(key)
  } catch {
    return null
  }
}

function setPreviewValue(key: string, value: string): void {
  try {
    window.localStorage.setItem(key, value)
  } catch {
    // Local preview logging is best-effort.
  }
}

function removePreviewValue(key: string): void {
  try {
    window.localStorage.removeItem(key)
  } catch {
    // Local preview state is best-effort.
  }
}

function readEvents(): AnalyticsEvent[] {
  const raw = getPreviewValue(eventKey)
  if (!raw) return []
  try {
    const parsed = JSON.parse(raw)
    return Array.isArray(parsed) ? parsed.slice(-99) : []
  } catch {
    return []
  }
}

function numberValue(value: string | undefined): number | undefined {
  if (value === undefined || value.trim() === '') return undefined
  const parsed = Number(value)
  return Number.isFinite(parsed) ? parsed : undefined
}

function pageContext(): { pageType: string; funnelStage: string } {
  const path = window.location.pathname.replace(/\/+$/, '') || '/'

  if (path === '/') return { pageType: 'home', funnelStage: 'acquisition' }
  if (path === '/dossier') return { pageType: 'dossier', funnelStage: 'consideration' }
  if (path === '/cart') return { pageType: 'cart', funnelStage: 'checkout' }
  if (path === '/purchase/success') return { pageType: 'purchase_confirmation', funnelStage: 'conversion' }
  if (path === '/order-confirmation') return { pageType: 'preview_confirmation', funnelStage: 'preview' }
  if (path.startsWith('/category/')) return { pageType: 'category', funnelStage: 'research' }
  if (path.startsWith('/journal/')) return { pageType: 'journal', funnelStage: 'research' }
  return { pageType: 'content', funnelStage: 'research' }
}

function sendToGa4(event: AnalyticsEventName, properties: AnalyticsProperties): void {
  const eventName = ga4EventNames[event] || event
  const parameters: Record<string, unknown> = { ...properties }

  if (event === 'page_view') {
    parameters.page_title = document.title
    parameters.page_location = window.location.href
    parameters.page_path = window.location.pathname
  }

  if (event === 'dossier_sample_open') {
    parameters.download_type ??= 'sample'
    parameters.access_type ??= 'public'
    parameters.trial_download ??= 'true'
  }

  if (event === 'fulfillment') {
    parameters.download_type ??= 'paid_dossier'
    parameters.access_type ??= 'paid'
    parameters.trial_download ??= 'false'
  }

  try {
    window.gtag?.('event', eventName, parameters)
  } catch {
    // Analytics must never interrupt navigation or checkout.
  }
}

export function track(event: AnalyticsEventName, properties: AnalyticsProperties = {}): void {
  const record: AnalyticsEvent = {
    event,
    occurredAt: new Date().toISOString(),
    path: window.location.pathname,
    properties,
  }

  setPreviewValue(eventKey, JSON.stringify([...readEvents(), record]))
  window.dispatchEvent(new CustomEvent('pi:analytics', { detail: record }))
  sendToGa4(event, properties)

  let endpoint: string | undefined
  let consent = false
  try {
    endpoint = import.meta.env.PUBLIC_ANALYTICS_ENDPOINT
    consent = window.localStorage.getItem('PI_ANALYTICS_CONSENT') === 'granted'
  } catch {
    // Optional server-side preview analytics are best-effort.
  }

  if (endpoint && consent) {
    void fetch(endpoint, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(record),
      keepalive: true,
    }).catch(() => {})
  }
}

function setFeedback(form: HTMLFormElement, message: string): void {
  const feedback = form.querySelector<HTMLElement>('[data-email-feedback]')
  if (feedback) feedback.textContent = message
}

function itemFromDataset(dataset: DOMStringMap): AnalyticsItem | null {
  const itemId = dataset.analyticsItemId
  if (!itemId) return null

  const price = numberValue(dataset.analyticsItemPrice)
  return {
    item_id: itemId,
    item_name: dataset.analyticsItemName || itemId,
    item_category: dataset.analyticsItemCategory || 'digital_dossier',
    quantity: numberValue(dataset.analyticsItemQuantity) || 1,
    ...(price === undefined ? {} : { price }),
  }
}

function itemFromProductDataset(element: HTMLElement): AnalyticsItem {
  const price = numberValue(element.dataset.dossierPrice)
  return {
    item_id: element.dataset.dossierId || element.dataset.dossierEdition || 'platonic-ideal-dossier',
    item_name: element.dataset.dossierName || 'The Platonic Ideal Dossier',
    item_category: 'digital_dossier',
    quantity: 1,
    ...(price === undefined ? {} : { price }),
  }
}

function propertiesFromTarget(target: HTMLElement): AnalyticsProperties {
  const properties: AnalyticsProperties = {}
  const item = itemFromDataset(target.dataset)
  const price = numberValue(target.dataset.analyticsValue || target.dataset.analyticsItemPrice)

  if (target.dataset.analyticsCategory) properties.category = target.dataset.analyticsCategory
  if (target.dataset.analyticsOutcome) properties.outcome = target.dataset.analyticsOutcome
  if (target.dataset.analyticsMode) properties.mode = target.dataset.analyticsMode
  if (target.dataset.analyticsEditionId) properties.edition_id = target.dataset.analyticsEditionId
  if (target.dataset.analyticsDownloadType) properties.download_type = target.dataset.analyticsDownloadType
  if (target.dataset.analyticsAccessType) properties.access_type = target.dataset.analyticsAccessType
  if (target.dataset.analyticsFileName) properties.file_name = target.dataset.analyticsFileName
  if (target.dataset.analyticsFileExtension) properties.file_extension = target.dataset.analyticsFileExtension
  if (target.dataset.analyticsTransactionId) properties.transaction_id = target.dataset.analyticsTransactionId
  if (target.dataset.analyticsTrial) properties.trial_download = target.dataset.analyticsTrial === 'true' ? 'true' : 'false'
  if (price !== undefined) properties.value = price
  if (target.dataset.analyticsCurrency) properties.currency = target.dataset.analyticsCurrency

  if (item) {
    properties.items = [item]
    if (target.dataset.analyticsItemListName) properties.item_list_name = target.dataset.analyticsItemListName
  }

  return properties
}

function wireEmailCapture(): void {
  document.querySelectorAll<HTMLFormElement>('[data-email-capture]').forEach((form) => {
    form.addEventListener('submit', (event) => {
      event.preventDefault()
      const input = form.querySelector<HTMLInputElement>('input[type="email"]')
      const email = input?.value.trim().toLowerCase()
      if (!email || !email.includes('@')) {
        setFeedback(form, 'Enter a valid email address.')
        return
      }

      const existing = getPreviewValue(emailKey)
      const emails = existing ? existing.split(',').filter(Boolean) : []
      if (!emails.includes(email)) emails.push(email)
      setPreviewValue(emailKey, emails.join(','))
      track('email_signup', { consent: true })
      setFeedback(form, 'You are on the list.')
      form.reset()
    })

    form.querySelector<HTMLButtonElement>('[data-email-unsubscribe]')?.addEventListener('click', () => {
      removePreviewValue(emailKey)
      track('email_unsubscribe')
      setFeedback(form, 'You have been removed from the preview list.')
    })
  })
}

function wireDossierView(): void {
  const product = document.querySelector<HTMLElement>('[data-dossier-edition]')
  if (!product) return

  const price = numberValue(product.dataset.dossierPrice)
  track('view_item', {
    edition_id: product.dataset.dossierEdition || 'declared-edition',
    currency: product.dataset.dossierCurrency || 'USD',
    ...(price === undefined ? {} : { value: price }),
    items: [itemFromProductDataset(product)],
  })
}

function wirePurchaseConfirmation(): void {
  const confirmation = document.querySelector<HTMLElement>('[data-purchase-confirmed="true"]')
  const transactionId = confirmation?.dataset.purchaseTransactionId
  if (!confirmation || !transactionId) return

  const sentKey = `PI_GA4_PURCHASE_SENT_${transactionId}`
  let alreadySent = false
  try {
    alreadySent = window.sessionStorage.getItem(sentKey) === 'sent'
    if (!alreadySent) window.sessionStorage.setItem(sentKey, 'sent')
  } catch {
    // GA4 also deduplicates transaction IDs; continue if storage is unavailable.
  }
  if (alreadySent) return

  const price = numberValue(confirmation.dataset.purchaseValue)
  const item: AnalyticsItem = {
    item_id: confirmation.dataset.purchaseItemId || 'platonic-ideal-dossier',
    item_name: confirmation.dataset.purchaseItemName || 'The Platonic Ideal Dossier',
    item_category: 'digital_dossier',
    quantity: 1,
    ...(price === undefined ? {} : { price }),
  }

  track('purchase', {
    transaction_id: transactionId,
    purchase_mode: 'live',
    edition_id: confirmation.dataset.purchaseEdition || 'declared-edition',
    currency: confirmation.dataset.purchaseCurrency || 'USD',
    ...(price === undefined ? {} : { value: price }),
    items: [item],
  })
}

function wireAnalytics(): void {
  const context = pageContext()
  track('page_view', { page_type: context.pageType, funnel_stage: context.funnelStage })

  const category = document.querySelector<HTMLElement>('[data-category-page]')
  if (category) {
    const properties = {
      category: category.dataset.category || 'unknown',
      verdict: category.dataset.verdict || 'unknown',
    }
    track('category_view', properties)
    track('verdict_interaction', properties)
  }

  wireDossierView()
  wirePurchaseConfirmation()

  document.addEventListener('click', (event) => {
    const target = event.target instanceof Element
      ? event.target.closest<HTMLElement>('[data-analytics-event]')
      : null
    if (!target) return
    const name = target.dataset.analyticsEvent as AnalyticsEventName | undefined
    if (!name) return
    track(name, propertiesFromTarget(target))
  })

  wireEmailCapture()
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', wireAnalytics, { once: true })
} else {
  wireAnalytics()
}
