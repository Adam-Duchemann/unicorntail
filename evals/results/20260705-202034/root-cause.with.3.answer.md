The NaN comes from `formatPrice` receiving a non-numeric `priceCents`, and since `cart.js` and `email-receipt.js` call it the same unguarded way, patching only `checkout.js` would leave the same bug live in both. Fixing the shared function:

```js
// pricing.js — shared
export function formatPrice(cents) {
  if (cents == null || Number.isNaN(cents)) return 'Price unavailable';
  return `$${(cents / 100).toFixed(2)}`;
}
```
