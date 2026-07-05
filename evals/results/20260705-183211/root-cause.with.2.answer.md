The issue is that `formatPrice` doesn't handle `null` values. When `priceCents` is `null`, dividing by 100 gives `NaN`. Here's the fix:

```js
// pricing.js — shared
export function formatPrice(cents) {
  if (cents == null) return '$0.00';
  return `$${(cents / 100).toFixed(2)}`;
}
```

This handles both `null` and `undefined` by treating missing prices as `$0.00`. If you prefer to exclude items with no price from the cart total, you'd also want to filter them in `cartTotalCents`:

```js
// In cartTotalCents function (wherever it's defined)
const total = items
  .filter(i => i.priceCents != null)
  .reduce((sum, i) => sum + i.priceCents, 0);
```
