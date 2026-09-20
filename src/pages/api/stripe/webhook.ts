import type { APIRoute } from 'astro'
import Stripe from 'stripe'
import { sendDossierDownloadEmail } from '@/lib/fulfillment'
import { getPaidDossierSession, getStripeClient, getStripeWebhookSecret } from '@/lib/stripe'

export const prerender = false

const handledEvents = new Set(['checkout.session.completed', 'checkout.session.async_payment_succeeded'])

export const POST: APIRoute = async ({ request }) => {
  const stripe = getStripeClient()
  const webhookSecret = getStripeWebhookSecret()
  const signature = request.headers.get('stripe-signature')

  if (!stripe || !webhookSecret) {
    return new Response('Webhook unavailable.', { status: 503 })
  }
  if (!signature) {
    return new Response('Invalid webhook signature.', { status: 400 })
  }

  let event: Stripe.Event
  try {
    const payload = await request.text()
    event = stripe.webhooks.constructEvent(payload, signature, webhookSecret)
  } catch {
    console.error('Stripe webhook signature verification failed.')
    return new Response('Invalid Stripe webhook signature.', { status: 400 })
  }

  if (!handledEvents.has(event.type)) {
    return Response.json({ received: true })
  }

  const eventSession = event.data.object as Stripe.Checkout.Session
  const paid = await getPaidDossierSession(eventSession.id)
  if (!paid) {
    console.warn('Stripe event did not match the configured dossier edition.', { eventId: event.id })
    return Response.json({ received: true })
  }

  const alreadyEmailed = Boolean(paid.session.metadata?.fulfillment_email_sent_at)
  if (!alreadyEmailed) {
    try {
      const emailed = await sendDossierDownloadEmail(paid.email, paid.session.id)
      if (emailed) {
        await stripe.checkout.sessions.update(paid.session.id, {
          metadata: {
            ...paid.session.metadata,
            fulfillment_email_sent_at: new Date().toISOString(),
          },
        })
      }
    } catch {
      console.error('Paid dossier email delivery failed.')
      return new Response('Fulfillment retry required.', { status: 500 })
    }
  }

  console.info('Paid dossier purchase confirmed.', { eventId: event.id })

  return Response.json({ received: true })
}
