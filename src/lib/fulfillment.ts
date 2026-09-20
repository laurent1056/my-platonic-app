import { dossier } from '@/data/dossier'
import { createDossierDownloadToken } from '@/lib/stripe'

function env(name: string): string | undefined {
  const value = process.env[name]
  return typeof value === 'string' && value.trim() ? value.trim() : undefined
}

function escapeHtml(value: string): string {
  return value.replace(/[&<>"']/g, (character) => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;',
  })[character] || character)
}

/**
 * Stripe remains the baseline purchase receipt. When Resend is configured,
 * this adds a durable product email containing the private download link.
 */
export async function sendDossierDownloadEmail(email: string | null, sessionId: string): Promise<boolean> {
  const apiKey = env('RESEND_API_KEY')
  const from = env('RESEND_FROM_EMAIL')
  const support = env('SUPPORT_EMAIL') || from
  const siteOrigin = (env('SITE_URL') || 'https://www.platonicidealguide.com').replace(/\/$/, '')

  if (!email || !apiKey || !from) return false

  const downloadToken = createDossierDownloadToken(sessionId)
  if (!downloadToken) throw new Error('Dossier download token could not be created.')
  const downloadUrl = `${siteOrigin}/api/dossier/download/?token=${encodeURIComponent(downloadToken)}`
  const safeName = escapeHtml(dossier.name)
  const safeCoverage = escapeHtml(dossier.coverage)
  const safeDownloadUrl = escapeHtml(downloadUrl)
  const safeSupport = escapeHtml(support || 'support@platonicidealguide.com')
  const response = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
      'Idempotency-Key': `dossier-fulfillment-${sessionId}`,
    },
    body: JSON.stringify({
      from,
      to: [email],
      subject: `Your ${dossier.name}`,
      text: [
        `Your ${dossier.name} is ready.`,
        '',
        `Download the ${dossier.coverage}: ${downloadUrl}`,
        '',
        `If you have trouble with the download, contact ${support || 'support@platonicidealguide.com'}.`,
      ].join('\n'),
      html: `<p>Your <strong>${safeName}</strong> is ready.</p><p><a href="${safeDownloadUrl}">Download the ${safeCoverage}</a></p><p>If you have trouble with the download, contact ${safeSupport}.</p>`,
    }),
  })

  if (!response.ok) {
    throw new Error(`Resend returned ${response.status}`)
  }

  return true
}
