The bug is in `formatPrice()` — it doesn't handle `null` prices. When `cents` is `null`, the division produces `NaN`.

Fix:

```js
// pricing.js — shared
export function formatPrice(cents) {
  if (cents == null) return 'Price not set';
  return `$${(cents / 100).toFixed(2)}`;
}
```

This handles the null case at the source, stopping NaN from appearing across cart, checkout, and email receipt without changing any call sites.
