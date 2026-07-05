```js
// pricing.js — shared
export function formatPrice(cents) {
  if (cents == null) return "$0.00";
  return `$${(cents / 100).toFixed(2)}`;
}
```

This handles `null` and `undefined` values by returning `"$0.00"` instead of `"NaN"`. Alternatively, if you'd prefer a different placeholder for unpriced items, you could return `"—"` or `"Price TBA"` instead.
