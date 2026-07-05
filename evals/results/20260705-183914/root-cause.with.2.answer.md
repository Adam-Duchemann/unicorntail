The bug is in `formatPrice()` — when `cents` is `null`, the division `null / 100` produces `NaN`. Fix it to default to 0 for missing prices:

```js
// pricing.js — shared
export function formatPrice(cents) {
  return `$${((cents ?? 0) / 100).toFixed(2)}`;
}
```

The nullish coalescing operator `??` defaults to 0 when `cents` is `null` or `undefined`, so products with no price yet display as `$0.00` instead of `NaN`.
