import inventory from './image-source-inventory.json'

export type ImageSourceType =
  | 'manufacturer'
  | 'authorized-retailer'
  | 'retailer'
  | 'catalog-or-manual'
  | 'open-license'
  | 'owned'
  | 'ai-interpretation'
  | 'unlocated'

export type ImageAvailability = 'confirmed' | 'lead' | 'not-found'
export type ImageRightsStatus = 'unknown' | 'permission-pending' | 'licensed' | 'owned' | 'not-for-republish'
export type ImageIdentityStatus = 'exact' | 'family' | 'ambiguous' | 'generic'
export type ImageRecommendedUse = 'identity' | 'service' | 'evidence' | 'purchase-link-only'

export interface ImageSourceRecord {
  productId: string
  category: string
  declaredModel: string
  sourceType: ImageSourceType
  sourceUrl?: string
  sourcePageTitle: string
  sellerOrManufacturer: string
  exactModel: string
  variant: string
  region: string
  imageAvailability: ImageAvailability
  rightsStatus: ImageRightsStatus
  identityStatus: ImageIdentityStatus
  recommendedUse: ImageRecommendedUse
  notes: string
}

export const imageSourceInventoryCheckedAt = inventory.checkedAt
export const imageSourceInventory = inventory.records as ImageSourceRecord[]

export function imageSourceFor(productId: string): ImageSourceRecord | undefined {
  return imageSourceInventory.find((source) => source.productId === productId)
}

export const imageSourceStats = {
  total: imageSourceInventory.length,
  confirmed: imageSourceInventory.filter((source) => source.imageAvailability === 'confirmed').length,
  leads: imageSourceInventory.filter((source) => source.imageAvailability === 'lead').length,
  notFound: imageSourceInventory.filter((source) => source.imageAvailability === 'not-found').length,
  exact: imageSourceInventory.filter((source) => source.identityStatus === 'exact').length,
  rightsCleared: imageSourceInventory.filter((source) => source.rightsStatus === 'licensed' || source.rightsStatus === 'owned').length,
}
