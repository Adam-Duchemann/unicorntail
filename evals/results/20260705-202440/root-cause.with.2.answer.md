The bug occurs because `formatPrice(null)` produces `$NaN`. Fix it in the shared function:

```js
// pricing.js — shared
export function formatPrice(cents) {
  if (cents == null) return '–';
  return `$${(cents / 100).toFixed(2)}`;
}
```

This handles `null` prices by returning a dash, which will render consistently across the cart, checkout, and email receipt without modifying each call site.
