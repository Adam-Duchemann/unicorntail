```js
// pricing.js — shared
export function formatPrice(cents) {
  if (cents == null || Number.isNaN(cents)) return '—';
  return `$${(cents / 100).toFixed(2)}`;
}
```

Fixed at the shared `formatPrice` function so `cart.js`, `checkout.js`, and `email-receipt.js` all get the fix — not just the checkout call site the report named.
