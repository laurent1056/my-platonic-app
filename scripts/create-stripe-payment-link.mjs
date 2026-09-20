import Stripe from 'stripe'

const secretKey = process.env.STRIPE_SECRET_KEY?.trim()
if (!secretKey) {
  console.error('Set STRIPE_SECRET_KEY before creating the Payment Link.')
  process.exit(1)
}

const siteOrigin = (process.env.SITE_URL || 'https://www.platonicidealguide.com').replace(/\/$/, '')
const stripe = new Stripe(secretKey)
const editionId = 'platonic-ideal-declared-1940'
const productId = process.env.STRIPE_PRODUCT_ID?.trim()
const priceId = process.env.STRIPE_PRICE_ID?.trim()

let product
if (productId) {
  product = await stripe.products.retrieve(productId)
} else {
  product = await stripe.products.create({
    name: 'The Platonic Ideal Dossier — Declared Edition',
    description: 'A 157-page tagged PDF containing 48 declared product recommendations and the research behind them.',
    metadata: {
      edition_id: editionId,
      edition_version: '1940',
      recommendation_count: '48',
    },
  })
}

let price
if (priceId) {
  price = await stripe.prices.retrieve(priceId)
} else {
  price = await stripe.prices.create({
    currency: 'usd',
    unit_amount: 2400,
    product: product.id,
    metadata: {
      edition_id: editionId,
      edition_version: '1940',
    },
  })
}

const paymentLink = await stripe.paymentLinks.create({
  line_items: [{ price: price.id, quantity: 1 }],
  after_completion: {
    type: 'redirect',
    redirect: {
      url: `${siteOrigin}/purchase/success/?session_id={CHECKOUT_SESSION_ID}`,
    },
  },
  metadata: {
    product_id: 'the-dossier',
    edition_id: editionId,
    edition_version: '1940',
  },
})

console.log(JSON.stringify({
  paymentLinkId: paymentLink.id,
  paymentLinkUrl: paymentLink.url,
  productId: product.id,
  priceId: price.id,
  env: {
    PUBLIC_STRIPE_PAYMENT_LINK_URL: paymentLink.url,
    STRIPE_PRODUCT_ID: product.id,
    STRIPE_PRICE_ID: price.id,
  },
}, null, 2))
