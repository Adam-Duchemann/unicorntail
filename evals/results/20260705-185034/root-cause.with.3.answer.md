```js
// pricing.js — shared
export function formatPrice(cents) {
  if (cents == null) return '—';
  return `$${(cents / 100).toFixed(2)}`;
}
```

The fix handles `null`/`undefined` values at the source. When a product has no price set, `formatPrice` now returns `'—'` instead of passing `null` to the division operator (which produces `NaN`). This single change fixes the bug across all call sites: cart.js, checkout.js, and email-receipt.js.
