```js
// pricing.js — shared
export function formatPrice(cents) {
  if (cents == null) return 'N/A';
  return `$${(cents / 100).toFixed(2)}`;
}
```

The bug is in the root function; all callers already route through it. Handling `null` there prevents NaN everywhere at once.
