The bug occurs because `formatPrice()` receives `null` or `NaN` when products lack a price. When dividing by 100, `null / 100` becomes `NaN`.

Fix `formatPrice()` in `pricing.js`:

```js
export function formatPrice(cents) {
  if (cents == null || isNaN(cents)) return '$0.00';
  return `$${(cents / 100).toFixed(2)}`;
}
```

This handles both individual items with `null` price and totals that sum to `NaN`, displaying `$0.00` instead of "NaN".
