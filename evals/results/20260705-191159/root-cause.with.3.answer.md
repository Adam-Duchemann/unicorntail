```js
// pricing.js — shared
export function formatPrice(cents) {
  if (cents == null) return '$0.00';
  return `$${(cents / 100).toFixed(2)}`;
}
```

Guard `formatPrice` against null; all three callsites (cart, checkout, email-receipt) route through it, so one fix stops NaN everywhere. Add when the UX needs a different placeholder for "price not yet set" (e.g., "N/A").
