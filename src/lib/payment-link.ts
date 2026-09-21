export function getLivePaymentLink(value?: string): string | undefined {
  const link = value?.trim()
  return link && !link.includes('buy.stripe.com/test_') ? link : undefined
}
