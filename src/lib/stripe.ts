import { createHmac, timingSafeEqual } from 'node:crypto'
import Stripe from 'stripe'
import { dossier } from '@/data/dossier'

const checkoutSessionPattern = /^cs_(?:test_|live_)?[A-Za-z0-9]+$/
// Stripe restricted keys (rk_*) are valid server credentials too. The live
// production integration intentionally uses a restricted key with only the
// Checkout Sessions permission it needs.
const stripeSecretKeyPattern = /^(?:sk|rk)_(?:test_|live_)[A-Za-z0-9]+$/
const downloadTokenPattern = /^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$/
const downloadTokenLifetimeSeconds = 30 * 24 * 60 * 60
let cachedClient: Stripe | null | undefined

function env(name: string): string | undefined {
  const value = process.env[name]
  return typeof value === 'string' && value.trim() ? value.trim() : undefined
}

function getStripeSecretKey(): string | undefined {
  const secretKey = env('STRIPE_SECRET_KEY')
  return secretKey && stripeSecretKeyPattern.test(secretKey) ? secretKey : undefined
}

export function getStripeClient(): Stripe | null {
  if (cachedClient !== undefined) return cachedClient

  const secretKey = getStripeSecretKey()
  cachedClient = secretKey
    ? new Stripe(secretKey)
    : null
  return cachedClient
}

export function getStripeWebhookSecret(): string | undefined {
  return env('STRIPE_WEBHOOK_SECRET')
}

export interface PaidDossierSession {
  session: Stripe.Checkout.Session
  email: string | null
}

/**
 * Create a time-limited, signed download token. The raw Stripe session ID is
 * intentionally not placed in the email or download URL.
 */
export function createDossierDownloadToken(sessionId: string, now = Math.floor(Date.now() / 1000)): string | null {
  const secretKey = getStripeSecretKey()
  if (!secretKey || !checkoutSessionPattern.test(sessionId) || sessionId.length > 128) return null

  const payload = `${sessionId}.${now + downloadTokenLifetimeSeconds}`
  const encodedPayload = Buffer.from(payload, 'utf8').toString('base64url')
  const signature = createHmac('sha256', secretKey).update(encodedPayload).digest('base64url')
  return `${encodedPayload}.${signature}`
}

/**
 * Validate a download token without making a network request. Tokens are
 * bounded to the same lifetime that the application creates.
 */
export function getDossierSessionIdFromDownloadToken(token: string | null | undefined, now = Math.floor(Date.now() / 1000)): string | null {
  const secretKey = getStripeSecretKey()
  if (!secretKey || !token || token.length > 512 || !downloadTokenPattern.test(token)) return null

  try {
    const [encodedPayload, encodedSignature] = token.split('.')
    const expectedSignature = createHmac('sha256', secretKey).update(encodedPayload).digest('base64url')
    const receivedSignature = Buffer.from(encodedSignature, 'base64url')
    const expectedSignatureBytes = Buffer.from(expectedSignature, 'base64url')
    if (
      receivedSignature.length !== expectedSignatureBytes.length ||
      !timingSafeEqual(receivedSignature, expectedSignatureBytes)
    ) return null

    const payload = Buffer.from(encodedPayload, 'base64url').toString('utf8')
    const separator = payload.lastIndexOf('.')
    if (separator <= 0) return null

    const sessionId = payload.slice(0, separator)
    const expiresAt = Number(payload.slice(separator + 1))
    if (
      !checkoutSessionPattern.test(sessionId) ||
      sessionId.length > 128 ||
      !Number.isSafeInteger(expiresAt) ||
      expiresAt <= now ||
      expiresAt > now + downloadTokenLifetimeSeconds
    ) return null

    return sessionId
  } catch {
    return null
  }
}

/**
 * Retrieve and verify a paid Checkout Session for this exact edition.
 *
 * The configured price and product IDs are the authorization boundary. Do not
 * fall back to customer- or Payment-Link-controlled metadata: metadata alone
 * does not prove that the paid line item is the edition we deliver.
 */
export async function getPaidDossierSession(sessionId: string | null | undefined): Promise<PaidDossierSession | null> {
  if (!sessionId || sessionId.length > 128 || !checkoutSessionPattern.test(sessionId)) return null

  const stripe = getStripeClient()
  const secretKey = getStripeSecretKey()
  const expectedPriceId = env('STRIPE_PRICE_ID')
  const expectedProductId = env('STRIPE_PRODUCT_ID')
  if (!stripe || !secretKey || !expectedPriceId || !expectedProductId) return null

  try {
    const session = await stripe.checkout.sessions.retrieve(sessionId, {
      expand: ['line_items.data.price'],
    })

    const expectedLiveMode = /^(?:sk|rk)_live_/.test(secretKey)
    if (
      session.livemode !== expectedLiveMode ||
      session.status !== 'complete' ||
      session.mode !== 'payment' ||
      session.payment_status !== 'paid'
    ) return null

    const matchingLineItem = session.line_items?.data.some((item) => {
      if (item.quantity !== 1) return false
      const price = typeof item.price === 'string' ? null : item.price
      const productId = price && typeof price.product === 'string'
        ? price.product
        : price?.product && typeof price.product === 'object' && 'id' in price.product
          ? price.product.id
          : null
      return Boolean(
        price &&
        price.id === expectedPriceId &&
        productId === expectedProductId &&
        price.type === 'one_time' &&
        price.currency === 'usd' &&
        price.unit_amount === dossier.price * 100,
      )
    })

    if (!matchingLineItem) return null

    return {
      session,
      email: session.customer_details?.email || session.customer_email || null,
    }
  } catch {
    return null
  }
}

export function getPaymentLinkUrl(): string | undefined {
  return env('PUBLIC_STRIPE_PAYMENT_LINK_URL')
}

export function getDossierBlobPath(): string | undefined {
  return env('DOSSIER_BLOB_PATH')
}
