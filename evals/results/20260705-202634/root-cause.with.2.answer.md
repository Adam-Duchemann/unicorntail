```js
// pricing.js — shared
export function formatPrice(cents) {
  if (cents == null) return 'Price unavailable';
  return `$${(cents / 100).toFixed(2)}`;
}
```

Root cause is in the shared `formatPrice` — `cartTotalCents` and every per-item call eventually route through it, so guarding here fixes checkout's total, cart's per-row prices, and the email receipt line all at once, instead of just special-casing `checkout.js`.
