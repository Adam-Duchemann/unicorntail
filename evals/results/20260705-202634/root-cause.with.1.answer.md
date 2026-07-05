```js
// pricing.js — shared
export function formatPrice(cents) {
  if (cents == null || Number.isNaN(cents)) return 'N/A';
  return `$${(cents / 100).toFixed(2)}`;
}
```

Root cause is in the shared `formatPrice`: it never guarded against a missing price, so `null / 100` → `NaN` → `"$NaN"` leaked out through every caller (cart, checkout, email receipt), not just the checkout page named in the report. The fix guards once in the shared function so all three call sites get a sane `"N/A"` display instead of `NaN`.
