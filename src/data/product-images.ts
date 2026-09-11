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
  {
    id: 'pi-005-kitchen-knife-hero-v1',
    productId: 'PI-005',
    role: 'hero',
    kind: 'editorial-interpretation',
    path: 'images/products/pi-005-kitchen-knife/hero.jpg',
    alt: 'Antiquity-style editorial interpretation of a plain professional chef knife',
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
    id: 'pi-007-saucepan-hero-v1',
    productId: 'PI-007',
    role: 'hero',
    kind: 'editorial-interpretation',
    path: 'images/products/pi-007-saucepan/hero.jpg',
    alt: 'Antiquity-style editorial interpretation of a tri-ply stainless steel saucepan',
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
    id: 'pi-009-dutch-oven-hero-v1',
    productId: 'PI-009',
    role: 'hero',
    kind: 'editorial-interpretation',
    path: 'images/products/pi-009-dutch-oven/hero.jpg',
    alt: 'Antiquity-style editorial interpretation of an enameled cast-iron Dutch oven',
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
    id: 'pi-012-drill-hero-v1',
    productId: 'PI-012',
    role: 'hero',
    kind: 'editorial-interpretation',
    path: 'images/products/pi-012-drill/hero.jpg',
    alt: 'Antiquity-style editorial interpretation of a corded industrial hand drill',
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
    id: 'pi-013-kettle-hero-v1',
    productId: 'PI-013',
    role: 'hero',
    kind: 'editorial-interpretation',
    path: 'images/products/pi-013-kettle/hero.jpg',
    alt: 'Antiquity-style editorial interpretation of a simple stainless steel electric kettle',
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
    id: 'pi-016-backpack-hero-v1',
    productId: 'PI-016',
    role: 'hero',
    kind: 'editorial-interpretation',
    path: 'images/products/pi-016-backpack/hero.jpg',
    alt: 'Antiquity-style editorial interpretation of a durable 30-liter travel backpack',
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
    id: 'pi-018-hand-saw-hero-v1',
    productId: 'PI-018',
    role: 'hero',
    kind: 'editorial-interpretation',
    path: 'images/products/pi-018-hand-saw/hero.jpg',
    alt: 'Antiquity-style editorial interpretation of a Japanese pull saw with replaceable blade',
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
    id: 'pi-019-desk-hero-v1',
    productId: 'PI-019',
    role: 'hero',
    kind: 'editorial-interpretation',
    path: 'images/products/pi-019-desk/hero.jpg',
    alt: 'Antiquity-style editorial interpretation of a solid hardwood butcher-block desk',
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
    id: 'pi-020-boots-hero-v1',
    productId: 'PI-020',
    role: 'hero',
    kind: 'editorial-interpretation',
    path: 'images/products/pi-020-boots/hero.jpg',
    alt: 'Antiquity-style editorial interpretation of a pair of resoleable full-leather work boots',
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
    id: 'pi-022-belt-hero-v1',
    productId: 'PI-022',
    role: 'hero',
    kind: 'editorial-interpretation',
    path: 'images/products/pi-022-belt/hero.jpg',
    alt: 'Antiquity-style editorial interpretation of a thick full-grain leather belt',
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
