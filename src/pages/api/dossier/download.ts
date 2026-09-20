import type { APIRoute } from 'astro'
import { get } from '@vercel/blob'
import { dossier } from '@/data/dossier'
import { getDossierBlobPath, getDossierSessionIdFromDownloadToken, getPaidDossierSession } from '@/lib/stripe'

export const prerender = false

function env(name: string): string | undefined {
  const value = process.env[name]
  return typeof value === 'string' && value.trim() ? value.trim() : undefined
}

function safeFilename(value: string): string {
  const fallback = `platonic-ideal-${dossier.editionId}.pdf`
  const normalized = value
    .replace(/[\r\n"\\]/g, '')
    .replace(/[^A-Za-z0-9._ -]/g, '-')
    .trim()
  return normalized && normalized.toLowerCase().endsWith('.pdf') ? normalized : fallback
}

export const GET: APIRoute = async ({ url }) => {
  const sessionId = getDossierSessionIdFromDownloadToken(url.searchParams.get('token'))
  const paid = await getPaidDossierSession(sessionId)

  if (!paid) {
    return new Response('Not found.', { status: 404 })
  }

  const blobPath = getDossierBlobPath()
  if (!blobPath) {
    console.error('Dossier delivery is not configured.')
    return new Response('Dossier delivery is not configured.', { status: 503 })
  }

  try {
    const token = env('BLOB_READ_WRITE_TOKEN')
    const blob = await get(blobPath, {
      access: 'private',
      ...(token ? { token } : {}),
    })

    if (!blob || blob.statusCode !== 200) {
      return new Response('Dossier file not found.', { status: 404 })
    }

    const filename = safeFilename(env('DOSSIER_DOWNLOAD_FILENAME') || '')
    return new Response(blob.stream, {
      headers: {
        'Cache-Control': 'private, no-store, max-age=0',
        'Content-Disposition': `attachment; filename="${filename}"`,
        'Content-Length': String(blob.blob.size),
        'Content-Type': blob.blob.contentType || 'application/pdf',
        'Content-Security-Policy': "default-src 'none'; frame-ancestors 'none'",
        'Referrer-Policy': 'no-referrer',
        'X-Content-Type-Options': 'nosniff',
        'X-Robots-Tag': 'noindex, nofollow, noarchive',
      },
    })
  } catch {
    console.error('Private dossier download failed.')
    return new Response('Dossier delivery is temporarily unavailable.', { status: 503 })
  }
}
