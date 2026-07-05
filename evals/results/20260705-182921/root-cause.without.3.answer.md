The bug occurs because `formatPrice()` receives `null` for products without a price, and `null / 100` evaluates to `NaN`. Fix it by handling null/undefined values in the shared utility:

```js
// pricing.js — shared
export function formatPrice(cents) {
  const amount = cents ?? 0;
  return `$${(amount / 100).toFixed(2)}`;
}
```

This treats missing prices as $0.00, preventing NaN from appearing in the checkout total and email receipts.
