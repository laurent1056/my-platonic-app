export type ImageRole = 'hero' | 'detail' | 'service' | 'maker-mark' | 'evidence'
export type ImageStatus = 'pending' | 'approved' | 'rejected' | 'needs-review'
export type ImageExactness = 'exact-model' | 'exact-family' | 'representative'
export type ImageKind = 'product-photograph' | 'editorial-interpretation'

export interface ProductImage {
  id: string
  productId: string
  role: ImageRole
  kind: ImageKind
  path: string
  alt: string
  caption: string
  credit: string
  license: string
  sourceUrl?: string
  exactness: ImageExactness
  region?: string
  capturedOrRetrievedAt: string
  verifiedAt: string
  status: ImageStatus
}

/**
 * The image layer is deliberately separate from the CSV. An image can be an
 * editorial interpretation of a product without pretending to be evidence of
 * the exact SKU. Only approved local records are eligible for the public
 * component; the source inventory is intentionally a separate lead queue.
 */
export const productImages: ProductImage[] = [
  {
    id: 'pi-001-frying-pan-hero-v1',
    productId: 'PI-001',
    role: 'hero',
    kind: 'editorial-interpretation',
    path: 'images/products/pi-001-frying-pan/hero.webp',
    alt: 'Antiquity-style editorial interpretation of a single cast-iron frying pan',
    caption: 'Interpretive plate · AI-generated for Platonic Ideal · not product photography',
    credit: 'OpenAI image generation',
    license: 'Generated for Platonic Ideal; no manufacturer marks or product claims',
    exactness: 'representative',
    region: 'US',
    capturedOrRetrievedAt: '2026-09-10',
    verifiedAt: '2026-09-10',
    status: 'approved',
  },
  {
    id: 'pi-003-hammer-hero-v1',
    productId: 'PI-003',
    role: 'hero',
    kind: 'editorial-interpretation',
    path: 'images/products/pi-003-hammer/hero.webp',
    alt: 'Antiquity-style editorial interpretation of a single-piece steel claw hammer',
    caption: 'Interpretive plate · AI-generated for Platonic Ideal · not product photography',
    credit: 'OpenAI image generation',
    license: 'Generated for Platonic Ideal; no manufacturer marks or product claims',
    exactness: 'representative',
    region: 'US',
    capturedOrRetrievedAt: '2026-09-10',
    verifiedAt: '2026-09-10',
    status: 'approved',
  },
]

export function approvedHeroImageFor(productId: string): ProductImage | undefined {
  return productImages.find(
    (image) => image.productId === productId && image.role === 'hero' && image.status === 'approved',
  )
}
