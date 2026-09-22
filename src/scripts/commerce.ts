/** Local-only design state. No identity, payment details, or entitlements. */
import { dossier } from '@/data/dossier'
import { track } from './analytics'
const key = 'PI_DOSSIER_PREVIEW_V1'
const fulfillmentKey = 'PI_DOSSIER_FULFILLMENT_TRACKED_V2'
type PreviewState = { cart: boolean; order: boolean }
function read(): PreviewState {
  try {
    const value = JSON.parse(localStorage.getItem(key) || '{}')
    return { cart: value?.cart === true, order: value?.order === true }
  } catch { return { cart: false, order: false } }
}
let state = read()
let toastTimer: ReturnType<typeof setTimeout>
function announce(message: string) {
  const toast = document.querySelector<HTMLElement>('#shop-toast')
  if (!toast) return
  toast.textContent = message
  toast.hidden = false
  clearTimeout(toastTimer)
  toastTimer = setTimeout(() => { toast.hidden = true }, 4500)
}
function save(next: PreviewState): boolean {
  try { localStorage.setItem(key, JSON.stringify(next)); state = next; render(); return true }
  catch { announce('Browser storage is unavailable. Enable local storage to try the cart preview.'); return false }
}
function render() {
  document.querySelectorAll<HTMLElement>('[data-cart-count]').forEach(el => { el.hidden = !state.cart })
  document.querySelectorAll<HTMLElement>('[data-cart-filled]').forEach(el => { el.hidden = !state.cart })
  document.querySelectorAll<HTMLElement>('[data-cart-empty]').forEach(el => { el.hidden = state.cart })
  document.querySelectorAll<HTMLElement>('[data-order-filled]').forEach(el => { el.hidden = !state.order })
  document.querySelectorAll<HTMLElement>('[data-order-empty]').forEach(el => { el.hidden = state.order })
  document.querySelectorAll<HTMLButtonElement>('[data-add-dossier]').forEach(el => { el.textContent = state.cart ? 'Dossier in cart · View cart →' : `Add the dossier to cart · ${dossier.priceLabel} →` })
}
document.querySelectorAll<HTMLButtonElement>('[data-add-dossier]').forEach(button => button.addEventListener('click', () => {
  const cartUrl = `${import.meta.env.BASE_URL}cart/`
  if (state.cart) { location.assign(cartUrl); return }
  if (save({ ...state, cart: true })) { track('preview_add_to_cart', { product: dossier.id, amount: dossier.price, mode: 'preview' }); announce(`The dossier was added. One digital copy, ${dossier.priceLabel}.`); location.assign(cartUrl) }
}))
document.querySelectorAll<HTMLButtonElement>('[data-remove-dossier]').forEach(button => button.addEventListener('click', () => {
  if (save({ ...state, cart: false })) announce('The dossier was removed from your cart.')
}))
document.querySelector<HTMLButtonElement>('[data-complete-preview]')?.addEventListener('click', () => {
  if (!state.cart) { announce('Add the dossier before trying checkout.'); return }
  if (save({ ...state, cart: false, order: true })) {
    track('preview_purchase', { product: dossier.id, amount: dossier.price, mode: 'preview' })
    location.assign(`${import.meta.env.BASE_URL}order-confirmation/`)
  }
})
window.addEventListener('storage', event => { if (event.key === key || event.key === null) { state = read(); render() } })
window.addEventListener('pageshow', () => {
  state = read()
  render()
  if (state.order && location.pathname.endsWith('/order-confirmation/')) {
    try {
      if (localStorage.getItem(fulfillmentKey) !== 'sent') {
        localStorage.setItem(fulfillmentKey, 'sent')
        track('preview_fulfillment', { product: dossier.id, mode: 'preview' })
      }
    } catch {}
  }
})
render()
