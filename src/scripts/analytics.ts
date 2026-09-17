type AnalyticsEventName =
  | 'page_view'
  | 'category_view'
  | 'verdict_interaction'
  | 'dossier_cta_click'
  | 'add_to_cart'
  | 'checkout_start'
  | 'purchase'
  | 'fulfillment'
  | 'email_signup'
  | 'email_unsubscribe'

interface AnalyticsEvent {
  event: AnalyticsEventName
  occurredAt: string
  path: string
  properties: Record<string, string | number | boolean>
}

const eventKey = 'PI_ANALYTICS_PREVIEW_V1'
const emailKey = 'PI_EMAIL_PREVIEW_V1'

function getPreviewValue(key: string): string | null {
  try { return localStorage.getItem(key) } catch { return null }
}

function setPreviewValue(key: string, value: string) {
  try { localStorage.setItem(key, value) } catch {}
}

function removePreviewValue(key: string) {
  try { localStorage.removeItem(key) } catch {}
}

function readEvents(): AnalyticsEvent[] {
  try {
    const value = JSON.parse(getPreviewValue(eventKey) || '[]')
    return Array.isArray(value) ? value.slice(-99) : []
  } catch { return [] }
}

export function track(event: AnalyticsEventName, properties: Record<string, string | number | boolean> = {}) {
  const record: AnalyticsEvent = {
    event,
    occurredAt: new Date().toISOString(),
    path: window.location.pathname,
    properties,
  }

  setPreviewValue(eventKey, JSON.stringify([...readEvents(), record]))
  window.dispatchEvent(new CustomEvent('pi:analytics', { detail: record }))

  let endpoint: string | undefined
  let consent = false
  try {
    endpoint = import.meta.env.PUBLIC_ANALYTICS_ENDPOINT
    consent = localStorage.getItem('PI_ANALYTICS_CONSENT') === 'granted'
  } catch {}
  if (endpoint && consent) {
    void fetch(endpoint, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(record),
      keepalive: true,
    }).catch(() => {})
  }
}

function setFeedback(form: HTMLFormElement, message: string) {
  const feedback = form.querySelector<HTMLElement>('[data-email-feedback]')
  if (feedback) { feedback.textContent = message; feedback.hidden = false }
}

function wireEmailCapture() {
  document.querySelectorAll<HTMLFormElement>('[data-email-capture]').forEach((form) => {
    const unsubscribe = form.querySelector<HTMLElement>('[data-email-unsubscribe]')
    const sync = () => { if (unsubscribe) unsubscribe.hidden = getPreviewValue(emailKey) !== 'subscribed' }
    sync()
    form.addEventListener('submit', (event) => {
      event.preventDefault()
      const consent = form.querySelector<HTMLInputElement>('input[name="email-consent"]')
      if (!consent?.checked) { setFeedback(form, 'Please confirm that you want the preview signup to continue.'); return }
      const email = form.querySelector<HTMLInputElement>('input[type="email"]')
      if (!email?.checkValidity()) { email?.reportValidity(); return }
      // Preview mode deliberately discards the address. It is never sent or persisted.
      setPreviewValue(emailKey, 'subscribed')
      track('email_signup', { consent: true })
      setFeedback(form, 'Preview signup confirmed. No address was saved or sent.')
      form.reset()
      sync()
    })
    unsubscribe?.addEventListener('click', (event) => {
      event.preventDefault()
      removePreviewValue(emailKey)
      track('email_unsubscribe')
      setFeedback(form, 'Preview signup removed. No email record exists.')
      sync()
    })
  })
}

function wireAnalytics() {
  track('page_view')
  const category = document.querySelector<HTMLElement>('[data-category-page]')
  if (category) {
    const properties = {
      category: category.dataset.category || 'unknown',
      verdict: category.dataset.verdict || 'unknown',
    }
    track('category_view', properties)
    track('verdict_interaction', properties)
  }
  document.addEventListener('click', (event) => {
    const target = event.target instanceof Element ? event.target.closest<HTMLElement>('[data-analytics-event]') : null
    if (!target) return
    const name = target.dataset.analyticsEvent as AnalyticsEventName | undefined
    if (!name) return
    track(name, {
      ...(target.dataset.analyticsCategory ? { category: target.dataset.analyticsCategory } : {}),
      ...(target.dataset.analyticsOutcome ? { outcome: target.dataset.analyticsOutcome } : {}),
    })
  })
  wireEmailCapture()
}

if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', wireAnalytics, { once: true })
else wireAnalytics()
