The root cause is in the shared `formatPrice` — `cart.js`, `checkout.js`, and `email-receipt.js` all route through it, so patching just `checkout.js` would leave the same bug in the cart rows and receipt emails for any priceless product.

```js
// pricing.js — shared
export function formatPrice(cents) {
  if (cents == null) return '—';
  return `$${(cents / 100).toFixed(2)}`;
}
```
