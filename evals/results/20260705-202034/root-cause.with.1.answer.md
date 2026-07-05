Root cause: `formatPrice` is the shared function every caller routes through, but it does no guarding — it just divides whatever `cents` is by 100. When `priceCents` is `null`/`undefined` (or a total computed from one), the arithmetic yields `NaN`, and `cart.js` and `email-receipt.js` have the exact same latent bug, they just haven't been reported yet. Fixing only `checkout.js` would leave those two broken.

```js
// pricing.js — shared
export function formatPrice(cents) {
  if (cents == null || Number.isNaN(cents)) return '—';
  return `$${(cents / 100).toFixed(2)}`;
}
```

No changes needed in `cart.js`, `checkout.js`, or `email-receipt.js` — they all call the shared function, so this single fix covers the reported checkout total, the cart row display, and the email receipt line.
