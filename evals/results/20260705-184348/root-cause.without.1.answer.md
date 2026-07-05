```js
// pricing.js — shared
export function formatPrice(cents) {
  if (cents == null) {
    return 'N/A';
  }
  return `$${(cents / 100).toFixed(2)}`;
}
```

The fix handles `null` values in `formatPrice` before the division operation. When `priceCents` is `null`, it now returns `'N/A'` instead of `'$NaN'`. This handles all three call sites (`cart.js`, `checkout.js`, and `email-receipt.js`) uniformly.
