```js
// pricing.js — shared
export function formatPrice(cents) {
  if (cents == null) return "$0.00";
  return `$${(cents / 100).toFixed(2)}`;
}
```

The issue is that `null / 100` produces `NaN`. The fix handles `null` and `undefined` values by treating them as zero before formatting.
