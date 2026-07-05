The bug is in `formatPrice()` — when `cents` is `null`, the division produces `NaN`. Fix it by defaulting to 0:

```js
// pricing.js — shared
export function formatPrice(cents) {
  return `$${((cents ?? 0) / 100).toFixed(2)}`;
}
```

This handles null/undefined prices by treating them as $0.00, so checkout totals and receipts display correctly when products lack a price.
